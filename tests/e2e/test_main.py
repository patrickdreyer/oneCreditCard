import json
import sys
from unittest.mock import patch

import pytest

from main import main


class TestMain:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path, monkeypatch):
        # arrange
        monkeypatch.chdir(tmp_path)

    def test_main_singleFile_successfulProcessing(self, setupInputDir, writeConfig):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])

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
        writeConfig(configData, 'input')

        outputFile = inputDir / 'bookings.ods'

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 0
        assert outputFile.exists()

    def test_main_multipleFiles_successfulProcessing(self, setupInputDir, writeConfig):
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
        writeConfig(configData, 'input')

        outputFile = inputDir / 'bookings.ods'

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 0
        assert outputFile.exists()

    def test_main_defaultOutputPath_successfulProcessing(self, setupInputDir, writeConfig):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])

        configData = {
            'creditAccount': '2000',
            'mapping': {},
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        writeConfig(configData, 'input')

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 0
        assert (inputDir / 'bookings.ods').exists()

    def test_main_customConfigPath_successfulProcessing(self, setupInputDir, tmp_path):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])

        configPath = tmp_path / 'custom-config.json'
        configData = {
            'creditAccount': '2000',
            'mapping': {},
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        with open(configPath, 'w', encoding='utf-8') as f:
            json.dump(configData, f)

        outputFile = inputDir / 'bookings.ods'

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07', '--config', str(configPath)]):
            result = main()

        # assert
        assert result == 0
        assert outputFile.exists()

    def test_main_inputDirectoryNotFound_error(self, tmp_path):
        # arrange
        nonExistentDir = tmp_path / 'nonexistent'

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(nonExistentDir)]):
            result = main()

        # assert
        assert result == 1

    def test_main_inputPathNotDirectory_error(self, tmp_path):
        # arrange
        filePath = tmp_path / 'file.txt'
        filePath.write_text('test')

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(filePath)]):
            result = main()

        # assert
        assert result == 1

    def test_main_configFileNotFound_error(self, setupInputDir):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])

        # act (no config file created)
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 1

    def test_main_emptyDirectory_warning(self, tmp_path, writeConfig):
        # arrange
        inputDir = tmp_path / 'input'
        inputDir.mkdir()

        configData = {
            'creditAccount': '2000',
            'mapping': {},
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'}
            ]
        }
        writeConfig(configData, 'input')

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 0

    def test_main_invalidJsonConfig_error(self, setupInputDir, tmp_path):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])

        configPath = inputDir / 'onecreditcard.json'
        configPath.write_text('{ invalid json }')

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-07']):
            result = main()

        # assert
        assert result == 1

    def test_main_monthFilter_onlyTargetMonthProcessed(self, setupInputDir, writeConfig):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt', '2025-08_1.txt', '2025-09_1.txt'])

        configData = {
            'creditAccount': '2000',
            'mapping': {},
            'columns': [
                {'name': 'Datum', 'type': 'date', 'format': 'DD.MM.YY'},
                {'name': 'Text', 'type': 'description'},
                {'name': 'Betrag CHF', 'type': 'amountChf'}
            ]
        }
        writeConfig(configData, 'input')

        outputFile = inputDir / 'bookings.ods'

        # act
        with patch.object(sys, 'argv', ['onecreditcard', '--folder', str(inputDir), '--month', '2025-08']):
            result = main()

        # assert
        assert result == 0
        assert outputFile.exists()

