import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from logging_config import getLogger

logger = getLogger(__name__)


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
            logger.error("Configuration file not found; path='%s'", self.configPath)
            raise FileNotFoundError(f"Configuration file not found: {self.configPath}") from exc
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in configuration file; path='%s', error='%s'", self.configPath, exc)
            raise ValueError(f"Invalid JSON in configuration file: {exc}") from exc

        logger.info("Configuration loaded; path='%s', mapping_rules=%d, columns=%d",
                    self.configPath, len(self._config.get('mapping', {})),
                    len(self._config.get('columns', [])))

    def __validateConfiguration(self) -> None:
        requiredFields = ['creditAccount', 'mapping', 'columns']
        for field in requiredFields:
            if field not in self._config:
                logger.error("Missing required configuration field; field='%s'", field)
                raise ValueError(f"Missing required configuration field: {field}")

        if not isinstance(self._config['creditAccount'], str):
            logger.error("Invalid creditAccount type; type='%s'", type(self._config['creditAccount']).__name__)
            raise ValueError("creditAccount must be a string")

        if not isinstance(self._config['mapping'], dict):
            logger.error("Invalid mapping type; type='%s'", type(self._config['mapping']).__name__)
            raise ValueError("mapping must be an object")

        for category, ruleOrRules in self._config['mapping'].items():
            self.__validateMappingEntry(category, ruleOrRules)

        if not isinstance(self._config['columns'], list):
            logger.error("Invalid columns type; type='%s'", type(self._config['columns']).__name__)
            raise ValueError("columns must be an array")

        ignoreConfig = self._config.get('ignore', {})
        if 'transactions' in ignoreConfig:
            for pattern in ignoreConfig['transactions']:
                self.__validatePattern(pattern, "ignore transaction pattern")

    def __validateMappingEntry(self, category: str, ruleOrRules) -> None:
        ruleList: List[dict] = ruleOrRules if isinstance(ruleOrRules, list) else [ruleOrRules]
        if not ruleList:
            logger.error("Empty mapping rules list; category='%s'", category)
            raise ValueError(f"Mapping rules for '{category}' must not be empty")
        for rule in ruleList:
            if not isinstance(rule, dict):
                logger.error("Invalid mapping rule type; category='%s', type='%s'", category, type(rule).__name__)
                raise ValueError(f"Mapping rule for '{category}' must be an object")
            if 'description' not in rule or 'debitAccount' not in rule:
                logger.error("Missing required mapping rule fields; category='%s', has_description=%s, has_debitAccount=%s",
                            category, 'description' in rule, 'debitAccount' in rule)
                raise ValueError(f"Mapping rule for '{category}' must have description and debitAccount")
            if 'pattern' in rule:
                self.__validatePattern(rule['pattern'], f"mapping rule for '{category}'")

        if not isinstance(self._config['columns'], list):
            logger.error("Invalid columns type; type='%s'", type(self._config['columns']).__name__)
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
            logger.error("Invalid regex pattern; context='%s', pattern='%s', error='%s'", context, pattern, exc)
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
    def mappingRules(self) -> Dict[str, List[MappingRule]]:
        rules: Dict[str, List[MappingRule]] = {}
        for category, ruleOrRules in self._config['mapping'].items():
            ruleList: Union[List[dict], dict] = ruleOrRules if isinstance(ruleOrRules, list) else [ruleOrRules]
            rules[category] = [
                MappingRule(
                    description=r['description'],
                    debitAccount=r['debitAccount'],
                    pattern=r.get('pattern')
                )
                for r in ruleList
            ]
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
