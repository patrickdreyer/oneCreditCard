import pytest
from configuration import Configuration, ColumnConfig, MappingRule, IgnoreRules


class TestConfiguration:
    def test_ctor_validConfig_loaded(self, writeConfig):
        # arrange
        configPath = writeConfig({
            "creditAccount": "2110",
            "mapping": {"Food": {"description": "Meals", "debitAccount": "5821"}},
            "columns": [{"name": "Date", "type": "date"}]
        })

        # act
        testee = Configuration(configPath)

        # assert
        assert testee.creditAccount == "2110"
        assert len(testee.mappingRules) == 1
        assert "Food" in testee.mappingRules

    def test_ctor_nonExistentFile_error(self, tmp_path):
        # arrange
        nonExistentPath = tmp_path / "missing.json"

        # act & assert
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            Configuration(nonExistentPath)

    def test_ctor_invalidJson_error(self, tmp_path):
        # arrange
        configPath = tmp_path / "invalid.json"
        with open(configPath, 'w', encoding='utf-8') as f:
            f.write("{ invalid json")

        # act & assert
        with pytest.raises(ValueError, match="Invalid JSON"):
            Configuration(configPath)

    def test_ctor_missingRequiredFields_error(self, writeConfig):
        # arrange
        filePath = writeConfig({"mapping": {}, "columns": []})

        # act & assert
        with pytest.raises(ValueError, match="Missing required configuration field: creditAccount"):
            Configuration(filePath)

    def test_ctor_invalidCreditAccount_error(self, writeConfig):
        # arrange
        filePath = writeConfig({
            "creditAccount": 123,  # Should be string
            "mapping": {},
            "columns": []
        })

        # act & assert
        with pytest.raises(ValueError, match="creditAccount must be a string"):
            Configuration(filePath)

    def test_ctor_invalidMappingStructure_error(self, writeConfig):
        # arrange
        filePath = writeConfig({
            "creditAccount": "2110",
            "mapping": "not an object",  # Should be dict
            "columns": []
        })

        # act & assert
        with pytest.raises(ValueError, match="mapping must be an object"):
            Configuration(filePath)

    def test_ctor_incompleteMappingRule_error(self, writeConfig):
        # arrange
        filePath = writeConfig({
            "creditAccount": "2110",
            "mapping": {
                "Food": {"description": "Meals"}  # Missing debitAccount
            },
            "columns": []
        })

        # act & assert
        with pytest.raises(ValueError, match="must have description and debitAccount"):
            Configuration(filePath)

    def test_ctor_invalidMappingPattern_error(self, writeConfig):
        # arrange
        filePath = writeConfig({
            "creditAccount": "2110",
            "mapping": {
                "Food": {
                    "description": "Meals",
                    "debitAccount": "5821",
                    "pattern": "[unclosed"  # Invalid regex
                }
            },
            "columns": []
        })

        # act & assert
        with pytest.raises(ValueError, match="Invalid regex pattern in mapping rule"):
            Configuration(filePath)

    def test_ctor_invalidIgnorePattern_error(self, writeConfig):
        # arrange
        filePath = writeConfig({
            "creditAccount": "2110",
            "mapping": {},
            "columns": [],
            "ignore": {
                "transactions": ["(invalid"]  # Invalid regex
            }
        })

        # act & assert
        with pytest.raises(ValueError, match="Invalid regex pattern in ignore transaction pattern"):
            Configuration(filePath)


class TestConfigurationProperties:
    @pytest.fixture
    def validConfig(self, writeConfig):
        configData = {
            "creditAccount": "2110",
            "ignore": {
                "categories": ["Einlagen"],
                "transactions": ["Payment"]
            },
            "mapping": {
                "Food": {
                    "description": "Meals",
                    "debitAccount": "5821"
                },
                "Transport": {
                    "description": "Public Transport",
                    "debitAccount": "6282",
                    "pattern": "^SBB.*"
                }
            },
            "columns": [
                {"name": "Date", "type": "date", "format": "DD.MM.YY"},
                {"name": "Description", "type": "description"},
                {"name": "Empty"},
                {"name": "Amount", "type": "amount", "format": "decimal"}
            ]
        }
        configPath = writeConfig(configData)
        return Configuration(configPath)

    def testCreditAccount(self, validConfig):
        # act
        result = validConfig.creditAccount

        # assert
        assert result == "2110"

    def test_ignoreRules_validConfig_ignoreRulesObject(self, validConfig):
        # act
        ignoreRules = validConfig.ignoreRules

        # assert
        assert isinstance(ignoreRules, IgnoreRules)
        assert ignoreRules.categories == ["Einlagen"]
        assert ignoreRules.transactions == ["Payment"]

    def test_ignoreRules_emptyIgnoreSection_emptyLists(self, writeConfig):
        # arrange
        configPath = writeConfig({
            "creditAccount": "2110",
            "mapping": {},
            "columns": []
        })

        # act
        testee = Configuration(configPath)
        ignoreRules = testee.ignoreRules

        # assert
        assert ignoreRules.categories == []
        assert ignoreRules.transactions == []

    def test_mappingRules_validConfig_mappingRuleObjects(self, validConfig):
        # act
        rules = validConfig.mappingRules

        # assert
        assert len(rules) == 2

        foodRule = rules["Food"]
        assert isinstance(foodRule, MappingRule)
        assert foodRule.description == "Meals"
        assert foodRule.debitAccount == "5821"
        assert foodRule.pattern is None

        transportRule = rules["Transport"]
        assert transportRule.pattern == "^SBB.*"

    def test_columns_validConfig_columnConfigObjects(self, validConfig):
        # act
        columns = validConfig.columns

        # assert
        assert len(columns) == 4

        dateColumn = columns[0]
        assert isinstance(dateColumn, ColumnConfig)
        assert dateColumn.name == "Date"
        assert dateColumn.type == "date"
        assert dateColumn.format == "DD.MM.YY"

        emptyColumn = columns[2]
        assert emptyColumn.name == "Empty"
        assert emptyColumn.type is None
        assert emptyColumn.format is None

    def test_getCoreColumns_validConfig_coreColumnsOnly(self, validConfig):
        # act
        coreColumns = validConfig.getCoreColumns()

        # assert
        assert len(coreColumns) == 3  # Date, Description, Amount
        assert all(col.type is not None for col in coreColumns)

    def test_getOptionalColumns_validConfig_optionalColumnsOnly(self, validConfig):
        # act
        optionalColumns = validConfig.getOptionalColumns()

        # assert
        assert len(optionalColumns) == 1  # Empty
        assert all(col.type is None for col in optionalColumns)


class TestConfigurationClassMethods:
    def test_fromDirectory_validDirectory_configurationObject(self, writeConfig):
        # arrange
        configPath = writeConfig({
            "creditAccount": "2110",
            "mapping": {},
            "columns": []
        })

        # act
        testee = Configuration.fromDirectory(configPath.parent)

        # assert
        assert testee.creditAccount == "2110"

    def test_fromDirectory_missingFile_error(self, tmp_path):
        # act & assert
        with pytest.raises(FileNotFoundError):
            Configuration.fromDirectory(tmp_path)

    def test_repr_validConfig_stringRepresentation(self, writeConfig):
        # arrange
        configPath = writeConfig({
            "creditAccount": "2110",
            "mapping": {"Food": {"description": "Meals", "debitAccount": "5821"}},
            "columns": []
        })
        testee = Configuration(configPath)

        # act
        reprStr = repr(testee)

        # assert
        assert "Configuration" in reprStr
        assert str(configPath) in reprStr
        assert "rules=1" in reprStr
