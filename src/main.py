#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from src.logging_config import setupLogging, getLogger
from src.configuration import Configuration
from src.parser.directoryParser import DirectoryParser
from src.transactionGrouper import TransactionGrouper
from src.accountMapper import AccountMapper
from src.odsGenerator import OdsGenerator

logger = getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog='onecreditcard',
        description='Convert Viseca credit card text exports to accounting ODS files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Process all .txt files in current directory
  onecreditcard .
  
  # Process files with custom output path
  onecreditcard input/ output/2025-12-bookings.ods
  
  # Use custom config file
  onecreditcard input/ -c custom-config.json
  
  # Enable debug logging
  onecreditcard input/ --log-level DEBUG
        '''
    )
    
    parser.add_argument(
        'input_directory',
        type=Path,
        help='Directory containing .txt credit card export files'
    )
    
    parser.add_argument(
        'output_file',
        type=Path,
        nargs='?',
        default=None,
        help='Output ODS file path (default: bookings.ods in input directory)'
    )
    
    parser.add_argument(
        '-c', '--config',
        type=Path,
        default=None,
        help='Configuration file path (default: onecreditcard.json in input directory)'
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
        # Validate input directory
        if not args.input_directory.exists():
            logger.error("Input directory not found; path='%s'", args.input_directory)
            print(f"Error: Input directory not found: {args.input_directory}", file=sys.stderr)
            return 1
        
        if not args.input_directory.is_dir():
            logger.error("Input path is not a directory; path='%s'", args.input_directory)
            print(f"Error: Input path is not a directory: {args.input_directory}", file=sys.stderr)
            return 1
        
        # Determine output file path
        outputFile = args.output_file or (args.input_directory / 'bookings.ods')
        
        # Load configuration
        configPath = args.config or (args.input_directory / 'onecreditcard.json')
        if not configPath.exists():
            logger.error("Configuration file not found; path='%s'", configPath)
            print(f"Error: Configuration file not found: {configPath}", file=sys.stderr)
            return 1
        
        logger.info("Starting processing; input_dir='%s', output_file='%s', config='%s'",
                   args.input_directory, outputFile, configPath)
        
        config = Configuration(configPath)
        
        # Parse transactions from directory
        parser = DirectoryParser()
        transactions = list(parser.parse(args.input_directory))
        
        if not transactions:
            logger.warning("No transactions found in directory; path='%s'", args.input_directory)
            print(f"Warning: No transactions found in {args.input_directory}", file=sys.stderr)
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
