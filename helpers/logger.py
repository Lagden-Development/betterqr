# Import the required modules
import logging
import re

# Constants
# Output file name
OUTPUT_FILE_NAME = "logs/betterqr.log"


# Helper functions
def remove_ansi_escape_sequences(s: str) -> str:
    # ANSI escape sequences regex pattern
    ansi_escape_pattern = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return ansi_escape_pattern.sub("", s)


# Custom formatter class with colors
class CustomFormatter(logging.Formatter):
    # ANSI escape sequences for colors
    COLORS = {
        "DEBUG": "\033[1;97m",  # Bold White
        "INFO": "\033[1;94m",  # Bold Blue
        "WARNING": "\033[1;93m",  # Bold Yellow
        "ERROR": "\033[1;91m",  # Bold Red
        "CRITICAL": "\033[1;97;101m",  # Bold Red on White background
        "DATE": "\033[1;30m",  # Bold Grey
        "NAME": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = f'{self.COLORS.get("DATE")}%(asctime)s{self.RESET} {self.COLORS.get(record.levelname, "")}%(levelname)s{self.RESET}     {self.COLORS.get("NAME")}%(name)s{self.RESET} %(message)s'
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# Custom formatter that removes ANSI colors
class CustomFileFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        original_format = formatter.format(record)
        return remove_ansi_escape_sequences(original_format)


# Define the betterqr sub-loggers
QRLOG_MAIN = logging.getLogger("betterqr.main")
QRLOG_REQUESTS = logging.getLogger("betterqr.requests")
QRLOG_DB = logging.getLogger("betterqr.db")


# Custom response formatter for betterqr.requests with colors
class CustomRequestFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[1;97m",  # Bold White
        "INFO": "\033[1;94m",  # Bold Blue
        "WARNING": "\033[1;93m",  # Bold Yellow
        "ERROR": "\033[1;91m",  # Bold Red
        "CRITICAL": "\033[1;97;101m",  # Bold Red on White background
        "DATE": "\033[1;30m",  # Bold Grey
        "NAME": "\033[35m",  # Magenta
        "METHOD": "\033[1;96m",  # Bold Cyan
        "PATH": "\033[1;92m",  # Bold Green
        "ADDR": "\033[35m",  # Magenta
        "REAL_ADDR": "\033[1;95m",  # Bold Magenta
        "STATUS": "\033[1;93m",  # Bold Yellow
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = (
            f'{self.COLORS.get("DATE")}%(asctime)s{self.RESET} '
            f'{self.COLORS.get(record.levelname, "")}%(levelname)s{self.RESET} '
            f'{self.COLORS.get("NAME")}%(name)s{self.RESET} '
        )
        if hasattr(record, "method"):
            log_fmt += f'{self.COLORS.get("METHOD")}%(method)s{self.RESET} '
        if hasattr(record, "path"):
            log_fmt += f'{self.COLORS.get("PATH")}%(path)s{self.RESET} '
        if hasattr(record, "addr"):
            log_fmt += f'{self.COLORS.get("ADDR")}%(addr)s{self.RESET} '
        if hasattr(record, "real_addr"):
            log_fmt += f'({self.COLORS.get("REAL_ADDR")}%(real_addr)s{self.RESET}) '
        if hasattr(record, "status"):
            log_fmt += f'{self.COLORS.get("STATUS")}%(status)s{self.RESET}'

        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# Custom file formatter for betterqr.requests without ANSI colors
class CustomRequestFileFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = "%(asctime)s %(levelname)s %(name)s "
        if hasattr(record, "method"):
            log_fmt += "%(method)s "
        if hasattr(record, "path"):
            log_fmt += "%(path)s "
        if hasattr(record, "addr"):
            log_fmt += "%(addr)s "
        if hasattr(record, "real_addr"):
            log_fmt += "(%(real_addr)s) "
        if hasattr(record, "status"):
            log_fmt += "%(status)s"

        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        original_format = formatter.format(record)
        return remove_ansi_escape_sequences(original_format)


# Create file and console handlers for QRLOG_REQUESTS
file_handler_requests = logging.FileHandler(
    filename=OUTPUT_FILE_NAME, mode="a"
)  # Append mode
file_handler_requests.setFormatter(CustomRequestFileFormatter())
console_handler_requests = logging.StreamHandler()
console_handler_requests.setFormatter(CustomRequestFormatter())

# Add handlers to QRLOG_REQUESTS
QRLOG_REQUESTS.addHandler(file_handler_requests)
QRLOG_REQUESTS.addHandler(console_handler_requests)

# Create file and console handlers for other loggers
file_handler_main = logging.FileHandler(
    filename=OUTPUT_FILE_NAME, mode="a"
)  # Append mode
file_handler_main.setFormatter(CustomFileFormatter())
console_handler_main = logging.StreamHandler()
console_handler_main.setFormatter(CustomFormatter())

# Add handlers to the other loggers
QRLOG_MAIN.addHandler(file_handler_main)
QRLOG_MAIN.addHandler(console_handler_main)
QRLOG_DB.addHandler(file_handler_main)
QRLOG_DB.addHandler(console_handler_main)


# Setup function
def setup_betterqr_logging(level=logging.INFO) -> None:
    """
    Sets the levels for all betterqr related loggers.

    Args:
        level (int): The logging level to set.

    Returns:
        None
    """
    if level not in {
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    }:
        raise ValueError("The level must be a valid logging level.")

    # Define betterqr logging levels
    logging.getLogger("betterqr.main").setLevel(level)
    logging.getLogger("betterqr.requests").setLevel(level)
    logging.getLogger("betterqr.db").setLevel(level)


# Example usage
if __name__ == "__main__":
    setup_betterqr_logging()
    QRLOG_MAIN.info("BetterQR main logging setup complete.")
    QRLOG_MAIN.debug("This is a debug message from the main sub-logger.")
    QRLOG_REQUESTS.info(
        "This is an info message from the requests sub-logger.",
        extra={
            "method": "GET",
            "path": "/api/data",
            "addr": "127.0.0.1",
            "real_addr": "192.168.1.1",
            "status": 200,
        },
    )
    QRLOG_DB.warning("This is a warning message from the db sub-logger.")
