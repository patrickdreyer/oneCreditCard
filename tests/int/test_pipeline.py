from pathlib import Path

from configuration import Configuration
from parsers.directoryParser import DirectoryParser
from transactionGrouper import TransactionGrouper
from accountMapper import AccountMapper
from odsGenerator import OdsGenerator


class TestPipeline:
    def test_pipeline_onlyIgnoredTransactions_emptyEntries(self, setupInputDir, writeConfig):
        # arrange
        inputDir = setupInputDir(['2025-08_1.txt'])

        configData = {
            'creditAccount': '2000',
            'ignore': {
                'categories': ['Shopping', 'Fahrzeug', 'Essen & Trinken', 'TRX123245678', 'Einlagen']
            },
            'mapping': {},
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'}
            ]
        }
        configPath = writeConfig(configData, 'input')

        config = Configuration(configPath)
        parser = DirectoryParser()
        grouper = TransactionGrouper(config)
        mapper = AccountMapper(config)

        # act
        transactions = list(parser.parse(inputDir))
        individualTransactions, groups = grouper.group(iter(transactions))
        entries = list(mapper.mapTransactions(individualTransactions))
        entries.extend(list(mapper.mapGroups(groups)))

        # assert
        assert len(entries) == 0

    def test_pipeline_onlyGroupedTransactions_groupedEntries(self, setupInputDir, writeConfig):
        # arrange
        inputDir = setupInputDir(['2025-08_1.txt'])

        configData = {
            'creditAccount': '2000',
            'mapping': {
                'Shopping': {
                    'description': 'Groceries',
                    'debitAccount': '6000'
                },
                'Fahrzeug': {
                    'description': 'Vehicle',
                    'debitAccount': '6100'
                },
                'Essen & Trinken': {
                    'description': 'Food',
                    'debitAccount': '6000'
                },
                'TRX123245678': {
                    'description': 'Misc',
                    'debitAccount': '6200'
                },
                'Einlagen': {
                    'description': 'Deposits',
                    'debitAccount': '6300'
                }
            },
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Soll', 'type': 'debitAccount'},
                {'name': 'Haben', 'type': 'creditAccount'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        configPath = writeConfig(configData, 'input')

        config = Configuration(configPath)
        parser = DirectoryParser()
        grouper = TransactionGrouper(config)
        mapper = AccountMapper(config)

        # act
        transactions = list(parser.parse(inputDir))
        individualTransactions, groups = grouper.group(iter(transactions))
        entries = list(mapper.mapTransactions(individualTransactions))
        entries.extend(list(mapper.mapGroups(groups)))

        # assert
        assert len(individualTransactions) == 0
        assert len(groups) > 0
        assert len(entries) == len(groups)
        assert all(entry.group is not None for entry in entries)

    def test_pipeline_fullWorkflow_odsGenerated(self, setupInputDir, writeConfig, tmp_path: Path):  # pylint: disable=too-many-locals
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt', '2025-07_2.txt'])

        configData = {
            'creditAccount': '2000',
            'mapping': {
                'Lebensmittel': {
                    'description': 'Groceries',
                    'debitAccount': '6000'
                }
            },
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Soll', 'type': 'debitAccount'},
                {'name': 'Haben', 'type': 'creditAccount'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        configPath = writeConfig(configData, 'input')

        config = Configuration(configPath)
        parser = DirectoryParser()
        grouper = TransactionGrouper(config)
        mapper = AccountMapper(config)
        generator = OdsGenerator(config)
        outputFile = tmp_path / 'output.ods'

        # act
        transactions = list(parser.parse(inputDir))
        individualTransactions, groups = grouper.group(iter(transactions))
        entries = list(mapper.mapTransactions(individualTransactions))
        entries.extend(list(mapper.mapGroups(groups)))
        generator.generate(entries, outputFile)

        # assert
        assert outputFile.exists()
        assert len(entries) > 0

    def test_pipeline_crossCategoryPatternFallback_groupedCorrectly(self, setupInputDir, writeConfig):  # pylint: disable=too-many-locals
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt', '2025-07_2.txt'])

        configData = {
            'creditAccount': '2110',
            'mapping': {
                'Fahrzeug': [
                    {'pattern': 'Gasstation', 'description': 'Auto; Diesel', 'debitAccount': '6210'},
                    {'pattern': 'parking', 'description': 'Auto; Parkgebühren', 'debitAccount': '6232'}
                ],
                'Transport': {
                    'pattern': '^(SBB|CFF|FFS)',
                    'description': 'Öffentlicher Verkehr',
                    'debitAccount': '6282'
                }
            },
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Soll', 'type': 'debitAccount'},
                {'name': 'Haben', 'type': 'creditAccount'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        configPath = writeConfig(configData, 'input')

        config = Configuration(configPath)
        parser = DirectoryParser()
        grouper = TransactionGrouper(config)
        mapper = AccountMapper(config)

        # act
        transactions = list(parser.parse(inputDir))
        _, groups = grouper.group(iter(transactions))
        groupEntries = list(mapper.mapGroups(groups))

        # assert
        parkingEntries = [e for e in groupEntries if e.mappedDescription == 'Auto; Parkgebühren']
        assert len(parkingEntries) == 1
        assert parkingEntries[0].group.totalAmount == 73.00
        assert parkingEntries[0].group.transactionCount == 3

        sbbEntries = [e for e in groupEntries if e.mappedDescription == 'Öffentlicher Verkehr']
        assert len(sbbEntries) == 1
        assert sbbEntries[0].group.transactionCount == 1
        assert sbbEntries[0].group.totalAmount == 6.40
