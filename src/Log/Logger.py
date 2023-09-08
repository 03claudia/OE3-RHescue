from enum import Enum
from contextlib import contextmanager
import threading
import traceback

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
    argv_keywords = ["-v", "-vi", "-iv", "--verbose", "-d", "--debug"]
    custom_descriptor = ""
    lock: threading.Lock = threading.Lock()

    def __init__(self, custom_descriptor: str) -> None:
        self.custom_descriptor = custom_descriptor

    @staticmethod
    def set_log_type(args: list[str]):
        args = [arg for arg in args if arg in Logger.argv_keywords]
        if not args:
            return
        logger_arg = args[0]

        match logger_arg:
            case "-v":
                Logger.log_type = LogType.VERBOSE
            case "-vi":
                Logger.log_type = LogType.VERBOSE
            case "-iv":
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

    def get_debug_info(self) -> str: 
        dbg = ""
        if Logger.log_type == LogType.DEBUG or Logger.log_type == LogType.VERBOSE:
            dbg = "\n" + traceback.extract_stack()[-3].filename\
                    + "\nLine: " + str(traceback.extract_stack()[-3].lineno) + "\n"
        return dbg    

    def set_lock(self, lock: threading.Lock):
        self.lock_changed = True
        self.lock = lock

    @contextmanager
    def lock_timeout(self, timeout: int):
        result = self.lock.acquire(timeout=timeout)
        try:
            yield result
        finally:
            if result:
                self.lock.release()

    def execute_locked_process(self, callback) -> None:
        with self.lock_timeout(1):
            callback()


    def print_critical_error(self, log: str):
        self.execute_locked_process(
                lambda: print(f"{Colors.FAIL}[CRITICAL ERROR] ({self.custom_descriptor})-> {log}{Colors.ENDC} {self.get_debug_info()}")
        )

    def print_success(self, log: str):
        self.execute_locked_process(
                lambda: print(f"{Colors.OKGREEN}[SUCCESS] ({self.custom_descriptor})-> {log}{Colors.ENDC}")
        )

    def print_error(self,log: str):
        if(Logger.log_type != LogType.DEBUG and Logger.log_type != LogType.VERBOSE):
            return
        
        self.execute_locked_process(
                lambda: print(f"[{Colors.WARNING}ERROR] ({self.custom_descriptor})-> {log}{Colors.ENDC} {self.get_debug_info()}")
        )

    def print_info(self, log: str):
        if(Logger.log_type != LogType.DEBUG and Logger.log_type != LogType.VERBOSE):
            return
        self.execute_locked_process(
                lambda: print(f"{Colors.OKBLUE}[INFO] ({self.custom_descriptor})-> {log}{Colors.ENDC}") 
        )
