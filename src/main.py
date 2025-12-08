#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from accountMapper import AccountMapper
from configuration import Configuration
from logging_config import setupLogging, getLogger
from odsGenerator import OdsGenerator
from parsers.directoryParser import DirectoryParser
from transactionGrouper import TransactionGrouper

logger = getLogger(__name__)


def main():
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

    args = parser.parse_args()

    # Setup logging
    logFile = args.log_file or Path('onecreditcard.log')
    setupLogging(args.log_level, logFile)

    try:
        # Validate folder
        folder = args.folder
        if not folder.exists():
            logger.error("Folder not found; path='%s'", folder)
            print(f"Error: Folder not found: {folder}", file=sys.stderr)
            return 1

        if not folder.is_dir():
            logger.error("Path is not a directory; path='%s'", folder)
            print(f"Error: Path is not a directory: {folder}", file=sys.stderr)
            return 1

        # Determine output file path
        # TODO: implement month filtering with args.month
        outputFile = folder / 'bookings.ods'

        # Load configuration
        configPath = args.config or (folder / 'onecreditcard.json')
        if not configPath.exists():
            logger.error("Configuration file not found; path='%s'", configPath)
            print(f"Error: Configuration file not found: {configPath}", file=sys.stderr)
            return 1

        logger.info("Starting processing; folder='%s', output_file='%s', config='%s'",
                   folder, outputFile, configPath)

        config = Configuration(configPath)

        # Parse transactions from directory
        directoryParser = DirectoryParser()
        transactions = list(directoryParser.parse(folder))

        if not transactions:
            logger.warning("No transactions found in folder; path='%s'", folder)
            print(f"Warning: No transactions found in {folder}", file=sys.stderr)
            return 0

        # Group transactions
        grouper = TransactionGrouper(config)
        individualTransactions, groups = grouper.group(iter(transactions))

        # Map to booking entries
        mapper = AccountMapper(config)
        entries = list(mapper.mapTransactions(individualTransactions))
        entries.extend(list(mapper.mapGroups(groups)))

        # Generate ODS file
        generator = OdsGenerator(config)
        generator.generate(entries, outputFile)

        logger.info("Processing completed successfully; output_file='%s', entries=%d",
                   outputFile, len(entries))
        print(f"Success: Generated {outputFile} with {len(entries)} entries")
        return 0

    except Exception as exc:
        logger.error("Processing failed; error='%s'", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
