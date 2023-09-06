from enum import Enum

class LogType(Enum):
    VERBOSE = "VERBOSE",
    DEBUG = "DEBUG",
    NORMAL = "NORMAL"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    log_type: LogType = LogType.NORMAL
    argv_keywords = ["-v", "--verbose", "-d", "--debug"]
    custom_descriptor = ""

    def __init__(self, custom_descriptor: str) -> None:
        self.custom_descriptor = custom_descriptor

    @staticmethod
    def set_log_type(args: list[str]):
        args = [arg for arg in args if arg in Logger.argv_keywords]
        print(args)
        if not args:
            return
        logger_arg = args[0]

        match logger_arg:
            case "-v":
                Logger.log_type = LogType.VERBOSE
            case "--verbose":
                Logger.log_type = LogType.VERBOSE
            case "-d":
                Logger.log_type = LogType.DEBUG
            case "--debug":
                Logger.log_type = LogType.DEBUG

    @staticmethod
    def get_log_type() -> LogType:
        return Logger.log_type

    def print_critical_error(self, log: str):
        print(f"{Colors.FAIL}[CRITICAL ERROR] ({self.custom_descriptor}) -> {log}{Colors.ENDC}")

    def print_success(self, log: str):
        print(f"{Colors.OKGREEN}[SUCCESS] ({self.custom_descriptor}) -> {log}{Colors.ENDC}")

    def print_error(self,log: str):
        if(Logger.log_type != LogType.DEBUG and Logger.log_type != LogType.VERBOSE):
            return
        print(f"[{Colors.WARNING}ERROR] ({self.custom_descriptor})-> {log}{Colors.ENDC}")

    def print_info(self, log: str):
        if(Logger.log_type != LogType.DEBUG and Logger.log_type != LogType.VERBOSE):
            return
        print(f"{Colors.OKBLUE}[INFO] ({self.custom_descriptor}) -> {log}{Colors.ENDC}")
