import json
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from src.main import main


class TestMain:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path, monkeypatch):
        # arrange
        monkeypatch.chdir(tmp_path)

    @pytest.fixture
    def fixturesDir(self):
        return Path(__file__).parent.parent / 'fixtures' / 'inputs'

    @pytest.fixture
    def setupInputDir(self, tmp_path, fixturesDir):
        def _setupInputDir(files):
            inputDir = tmp_path / 'input'
            inputDir.mkdir(parents=True, exist_ok=True)
            for filename in files:
                srcFile = fixturesDir / filename
                dstFile = inputDir / filename
                shutil.copy(srcFile, dstFile)
            return inputDir
        return _setupInputDir

    @pytest.fixture
    def writeConfig(self, tmp_path):
        def _writeConfig(directory, configData):
            inputDir = tmp_path / directory
            inputDir.mkdir(parents=True, exist_ok=True)
            configPath = inputDir / 'onecreditcard.json'
            with open(configPath, 'w', encoding='utf-8') as f:
                json.dump(configData, f)
            return configPath
        return _writeConfig

    def test_main_singleFile_successfulProcessing(self, setupInputDir, writeConfig, tmp_path):
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
        writeConfig('input', configData)
        
        outputFile = tmp_path / 'output.ods'
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(inputDir), str(outputFile)]):
            result = main()
        
        # assert
        assert result == 0
        assert outputFile.exists()

    def test_main_multipleFiles_successfulProcessing(self, setupInputDir, writeConfig, tmp_path):
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
        writeConfig('input', configData)
        
        outputFile = tmp_path / 'output.ods'
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(inputDir), str(outputFile)]):
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
        writeConfig('input', configData)
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(inputDir)]):
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
        
        outputFile = tmp_path / 'output.ods'
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(inputDir), str(outputFile), '-c', str(configPath)]):
            result = main()
        
        # assert
        assert result == 0
        assert outputFile.exists()

    def test_main_inputDirectoryNotFound_error(self, tmp_path):
        # arrange
        nonExistentDir = tmp_path / 'nonexistent'
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(nonExistentDir)]):
            result = main()
        
        # assert
        assert result == 1

    def test_main_inputPathNotDirectory_error(self, tmp_path):
        # arrange
        filePath = tmp_path / 'file.txt'
        filePath.write_text('test')
        
        # act
        with patch.object(sys, 'argv', ['onecreditcard', str(filePath)]):
            result = main()
        
        # assert
        assert result == 1

    def test_main_configFileNotFound_error(self, setupInputDir):
        # arrange
        inputDir = setupInputDir(['2025-07_1.txt'])
        
        # act (no config file created)
        with patch.object(sys, 'argv', ['onecreditcard', str(inputDir)]):
            result = main()
        
        # assert
        assert result == 1

