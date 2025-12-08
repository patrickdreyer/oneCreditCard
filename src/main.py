#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

from accountMapper import AccountMapper
from configuration import Configuration
from logging_config import setupLogging, getLogger
from odsGenerator import OdsGenerator
from parsers.directoryParser import DirectoryParser
from transactionGrouper import TransactionGrouper

logger = getLogger(__name__)


def createArgumentParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='onecreditcard',
        description='Convert Viseca credit card text exports to accounting ODS files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Process credit card exports in current directory
  onecreditcard

  # Specify custom data folder and month
  onecreditcard --folder /path/to/exports --month 2025-07

  # Use custom config file
  onecreditcard --config custom-config.json

  # Enable debug logging
  onecreditcard --log-level DEBUG
        '''
    )
    parser.add_argument(
        '--folder', '-f',
        type=Path,
        default=Path.cwd(),
        help='Data folder path (default: current working directory)'
    )
    parser.add_argument(
        '--month', '-m',
        type=str,
        default=None,
        help='Processing month in YYYY-MM format (default: previous month)'
    )
    parser.add_argument(
        '--config', '-c',
        type=Path,
        default=None,
        help='Configuration file path (default: {folder}/onecreditcard.json)'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--log-file',
        type=Path,
        default=None,
        help='Log file path (default: onecreditcard.log in current directory)'
    )
    return parser

def validateFolder(folder: Path) -> None:
    if not folder.exists():
        logger.error("Folder not found; path='%s'", folder)
        raise FileNotFoundError(f"Folder not found: {folder}")
    if not folder.is_dir():
        logger.error("Path is not a directory; path='%s'", folder)
        raise NotADirectoryError(f"Path is not a directory: {folder}")

def evaluateTargetMonth(monthStr: str = None) -> datetime:
    if monthStr:
        try:
            return datetime.strptime(monthStr, '%Y-%m')
        except ValueError as exc:
            logger.error("Invalid month format; month='%s'", monthStr)
            raise ValueError(f"Invalid month format: {monthStr}. Use YYYY-MM") from exc

    # Default to previous month
    today = datetime.now()
    firstDayThisMonth = today.replace(day=1)
    lastDayPreviousMonth = firstDayThisMonth - timedelta(days=1)
    targetMonth = lastDayPreviousMonth.replace(day=1)
    logger.info("Target month: %s", targetMonth.strftime('%Y-%m'))
    return targetMonth

def loadConfig(args) -> Configuration:
    configPath = args.config or (args.folder / 'onecreditcard.json')
    if not configPath.exists():
        logger.error("Configuration file not found; path='%s'", configPath)
        raise FileNotFoundError(f"Configuration file not found: {configPath}")
    return Configuration(configPath)

def parseTransactions(folder: Path, targetMonth: datetime) -> list:
    directoryParser = DirectoryParser()
    allTransactions = directoryParser.parse(folder)
    lastMonthTransactions = [
        t for t in allTransactions
        if t.date.year == targetMonth.year and t.date.month == targetMonth.month
    ]
    return lastMonthTransactions

def groupTransactions(transactions: list, config: Configuration) -> tuple:
    grouper = TransactionGrouper(config)
    individualTransactions, groups = grouper.group(iter(transactions))
    return individualTransactions, groups

def mapToBookingEntries(individualTransactions: list, groups: list, config: Configuration) -> list:
    mapper = AccountMapper(config)
    entries = list(mapper.mapTransactions(individualTransactions))
    entries.extend(list(mapper.mapGroups(groups)))
    return entries

def generateOdsFile(config: Configuration, entries: list, outputPath: Path) -> None:
    outputFile = outputPath / 'bookings.ods'
    generator = OdsGenerator(config)
    generator.generate(entries, outputFile)
    logger.info("Processing completed successfully; output_file='%s', entries=%d", outputFile, len(entries))

def main():
    parser = createArgumentParser()
    args = parser.parse_args()

    setupLogging(args.log_level, args.log_file)

    try:
        validateFolder(args.folder)
        targetMonth = evaluateTargetMonth(args.month)
        config = loadConfig(args)

        logger.info("Starting processing; folder='%s'", args.folder)

        lastMonthTransactions = parseTransactions(args.folder, targetMonth)
        individualTransactions, groups = groupTransactions(lastMonthTransactions, config)
        entries = mapToBookingEntries(individualTransactions, groups, config)
        generateOdsFile(config, entries, args.folder)
        return 0

    except Exception as exc:
        logger.error("Processing failed; error='%s'", exc)
        return 1

if __name__ == "__main__":
    sys.exit(main())
