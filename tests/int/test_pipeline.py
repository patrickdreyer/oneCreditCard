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
