import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class ApplicationLogger:
    """
    Advanced logging configuration class
    """
    
    def __init__(self, name="MyApplication", log_dir="logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Setup different handlers
        self._setup_file_handlers()
        self._setup_console_handler()
        
        self.logger.info(f"Logger initialized for {name}")
    
    def _setup_file_handlers(self):
        """
        Setup file handlers for different log levels
        """
        # Debug log file (all messages)
        debug_handler = logging.FileHandler(
            self.log_dir / "debug.log",
            mode='a',
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        debug_handler.setFormatter(debug_formatter)
        self.logger.addHandler(debug_handler)
        
        # Error log file (errors and critical only)
        error_handler = logging.FileHandler(
            self.log_dir / "errors.log",
            mode='a',
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'Function: %(funcName)s, Line: %(lineno)d\n'
            'Module: %(module)s\n'
            '---'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
        
        # Rotating file handler (prevents log files from getting too large)
        rotating_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "app_rotating.log",
            maxBytes=1024*1024,  # 1MB
            backupCount=5
        )
        rotating_handler.setLevel(logging.INFO)
        rotating_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        rotating_handler.setFormatter(rotating_formatter)
        self.logger.addHandler(rotating_handler)
    
    def _setup_console_handler(self):
        """
        Setup console handler with colored output
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Custom formatter for console
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """
        Get the configured logger
        """
        return self.logger

class DataProcessor:
    """
    Example class that uses advanced logging
    """
    
    def __init__(self):
        # Initialize logger
        app_logger = ApplicationLogger("DataProcessor")
        self.logger = app_logger.get_logger()
        
        self.processed_count = 0
        self.error_count = 0
    
    def process_json_file(self, filename):
        """
        Process JSON file with detailed logging
        """
        self.logger.info(f"Starting JSON processing for: {filename}")
        
        try:
            # Validate file exists
            if not os.path.exists(filename):
                self.logger.error(f"File not found: {filename}")
                self.error_count += 1
                raise FileNotFoundError(f"File '{filename}' does not exist")
            
            self.logger.debug(f"File exists, checking size: {filename}")
            file_size = os.path.getsize(filename)
            self.logger.debug(f"File size: {file_size} bytes")
            
            # Read and parse JSON
            with open(filename, 'r', encoding='utf-8') as file:
                self.logger.debug(f"Reading file content: {filename}")
                content = file.read()
                
                if not content.strip():
                    self.logger.warning(f"File is empty: {filename}")
                    return None
                
                self.logger.debug(f"Parsing JSON content from: {filename}")
                data = json.loads(content)
                
                # Validate data structure
                self._validate_json_data(data, filename)
                
                self.processed_count += 1
                self.logger.info(f"Successfully processed JSON file: {filename}")
                return data
        
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            self.error_count += 1
            raise
        
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in {filename}: {e}")
            self.logger.error(f"Error at line {e.lineno}, column {e.colno}")
            self.error_count += 1
            raise
        
        except UnicodeDecodeError as e:
            self.logger.error(f"Unicode decode error in {filename}: {e}")
            self.error_count += 1
            raise
        
        except Exception as e:
            self.logger.critical(f"Unexpected error processing {filename}: {type(e).__name__}: {e}")
            self.error_count += 1
            raise
        
        finally:
            self.logger.debug(f"Finished processing attempt for: {filename}")
    
    def _validate_json_data(self, data, filename):
        """
        Validate JSON data structure
        """
        self.logger.debug(f"Validating JSON data structure for: {filename}")
        
        if isinstance(data, dict):
            self.logger.debug(f"JSON is dictionary with {len(data)} keys: {list(data.keys())}")
            
            # Check for common required fields
            if 'id' in data:
                self.logger.debug(f"Found ID field: {data['id']}")
            else:
                self.logger.warning(f"No ID field found in: {filename}")
        
        elif isinstance(data, list):
            self.logger.debug(f"JSON is list with {len(data)} items")
        
        else:
            self.logger.warning(f"JSON data is neither dict nor list in: {filename}")
    
    def batch_process(self, filenames):
        """
        Process multiple files with summary logging
        """
        self.logger.info(f"Starting batch processing of {len(filenames)} files")
        
        results = []
        for filename in filenames:
            try:
                result = self.process_json_file(filename)
                results.append({'filename': filename, 'status': 'success', 'data': result})
            except Exception as e:
                results.append({'filename': filename, 'status': 'error', 'error': str(e)})
        
        # Log summary
        successful = len([r for r in results if r['status'] == 'success'])
        failed = len(results) - successful
        
        self.logger.info(f"Batch processing completed: {successful} successful, {failed} failed")
        self.logger.info(f"Total processed files: {self.processed_count}")
        self.logger.info(f"Total errors encountered: {self.error_count}")
        
        return results
    
    def get_statistics(self):
        """
        Get processing statistics
        """
        return {
            "processed_count": self.processed_count,
            "error_count": self.error_count
        }

# Example usage:
if __name__ == "__main__":
    data_processor = DataProcessor()

    # Example file list
    filenames = ["file1.json", "file2.json", "file3.json"]
    results = data_processor.batch_process(filenames)

    # Output processing statistics
    print(data_processor.get_statistics())
