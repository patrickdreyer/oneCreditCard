import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ColumnConfig:
    name: str
    type: Optional[str] = None
    format: Optional[str] = None


@dataclass
class MappingRule:
    description: str
    debitAccount: str
    pattern: Optional[str] = None


@dataclass
class IgnoreRules:
    categories: List[str]
    transactions: List[str]


class Configuration:
    def __init__(self, configPath: Path):
        # Args: configPath - Path to JSON configuration file
        # Raises: FileNotFoundError, json.JSONDecodeError, ValueError
        self.configPath = configPath
        self.__loadConfiguration()
        self.__validateConfiguration()

    def __loadConfiguration(self) -> None:
        # Load configuration from JSON file
        try:
            with open(self.configPath, 'r', encoding='utf-8') as file:
                self._config = json.load(file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Configuration file not found: {self.configPath}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in configuration file: {exc}") from exc

    def __validateConfiguration(self) -> None:
        requiredFields = ['creditAccount', 'mapping', 'columns']
        for field in requiredFields:
            if field not in self._config:
                raise ValueError(f"Missing required configuration field: {field}")

        if not isinstance(self._config['creditAccount'], str):
            raise ValueError("creditAccount must be a string")

        if not isinstance(self._config['mapping'], dict):
            raise ValueError("mapping must be an object")

        for category, rule in self._config['mapping'].items():
            if not isinstance(rule, dict):
                raise ValueError(f"Mapping rule for '{category}' must be an object")
            if 'description' not in rule or 'debitAccount' not in rule:
                raise ValueError(f"Mapping rule for '{category}' must have description and debitAccount")
            if 'pattern' in rule:
                self.__validatePattern(rule['pattern'], f"mapping rule for '{category}'")

        if not isinstance(self._config['columns'], list):
            raise ValueError("columns must be an array")

        ignoreConfig = self._config.get('ignore', {})
        if 'transactions' in ignoreConfig:
            for pattern in ignoreConfig['transactions']:
                self.__validatePattern(pattern, "ignore transaction pattern")

    @staticmethod
    def __validatePattern(pattern: str, context: str) -> None:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"Invalid regex pattern in {context}: {pattern}") from exc

    @property
    def creditAccount(self) -> str:
        return self._config['creditAccount']

    @property
    def ignoreRules(self) -> IgnoreRules:
        ignoreConfig = self._config.get('ignore', {})
        return IgnoreRules(
            categories=ignoreConfig.get('categories', []),
            transactions=ignoreConfig.get('transactions', [])
        )

    @property
    def mappingRules(self) -> Dict[str, MappingRule]:
        rules = {}
        for category, ruleConfig in self._config['mapping'].items():
            rules[category] = MappingRule(
                description=ruleConfig['description'],
                debitAccount=ruleConfig['debitAccount'],
                pattern=ruleConfig.get('pattern')
            )
        return rules

    @property
    def columns(self) -> List[ColumnConfig]:
        columns = []
        for columnConfig in self._config['columns']:
            columns.append(ColumnConfig(
                name=columnConfig['name'],
                type=columnConfig.get('type'),
                format=columnConfig.get('format')
            ))
        return columns

    def getCoreColumns(self) -> List[ColumnConfig]:
        # Columns with type field (containing actual data)
        return [col for col in self.columns if col.type is not None]

    def getOptionalColumns(self) -> List[ColumnConfig]:
        # Columns without type field (used for formatting/compatibility)
        return [col for col in self.columns if col.type is None]

    @classmethod
    def fromDirectory(cls, directory: Path) -> 'Configuration':
        configPath = directory / 'onecreditcard.json'
        return cls(configPath)

    def __repr__(self) -> str:
        return f"Configuration(path={self.configPath}, rules={len(self.mappingRules)})"
