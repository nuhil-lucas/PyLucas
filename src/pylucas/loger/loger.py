# Standard
from os import (
    makedirs as os_makedirs,
    listdir as os_listdir,
    getcwd as os_getcwd,
    remove as os_remove
)
from os.path import (
    exists as path_exists
)
from sys import (
    _getframe as sys_getframe,
    stderr
)
from atexit import register as atexit_register
from io import TextIOWrapper
from typing import Literal
from types import FrameType
# Internal
from pylucas.basic.func import (
    time_stamp as get_time_stamp,
)
from pylucas.better_print import APrint
# External

LEVELS = Literal["info", "warn", "error"]

class LogManager():
    def __init__(
        self,
        title: str = None,
        dir_log: str = "./log",
        limit_log_files: int = 10,
        logto_console: bool = True,
        logto_file: bool = True,
    ) -> None:
        """_summary_

        Args:
            
        """
        self.log_title: str = "" if title is None else title

        self.limit_log_level: str | LEVELS = "info" # if log level lower than this, will not log to file
        self.limit_log_files: int = limit_log_files # max log files to keep

        self.path_cwd: str = os_getcwd() + "\\" # use to replace in get_stack
        self.path_cwd_len: int = len(self.path_cwd)
        self.dir_log: str = dir_log
        self.path_log: str = f"{self.dir_log}/{get_time_stamp()}.log"
        self.file_log: TextIOWrapper = None

        self.logto_console: bool = logto_console
        self.logto_file: bool = logto_file

        self._log_file_()

        self._log_file_limit_()

        atexit_register(self._log_file_close_)

    def __call__(
        self,
        *msg: str,
        level: LEVELS = "info",
        time_stamp: bool = True,
        module: bool | str = True,
        to_console: bool = True,
        to_file: bool = True,
    ):
        """_summary_

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            LogConsole (bool, optional): _Whether the Log is output in the console._ Defaults is -1 mean fallow to self.LogConsole.
        """
        self.log(
            *msg,
            level=level,
            time_stamp=time_stamp,
            module=self.get_stack(2) if module is True else module,
            to_console=to_console,
            to_file=to_file,
        )

    def _log_file_(self):
        if not self.limit_log_files: return
        os_makedirs(name=self.dir_log, exist_ok=True)

        self.file_log = open(file=self.path_log, mode="w", encoding="utf-8")

        if self.log_title:
            ascii_art: str = APrint.ascii_art(text=self.log_title, split_line='=')
            self.file_log.write(f"{ascii_art}\n\n")
        self.file_log.write(f"Log File Created At {get_time_stamp()}\n\n")

    def _log_file_close_(self):
        if self.file_log and not self.file_log.closed:
            self.file_log.flush()
            self.file_log.close()
            self.file_log = None

    def _log_file_limit_(self):
        if self.limit_log_files <= 0: return
        if not path_exists(self.dir_log): return

        log_files: list[str] = [file for file in os_listdir(self.dir_log) if file.lower().endswith('.log')]
        if not log_files: return

        while len(log_files) > self.limit_log_files:
            oldest_file = min(log_files)
            try:
                os_remove(f"{self.dir_log}/{oldest_file}")
            except Exception as E:
                self.log(
                    LogMessage = f"Failed to Delete Oldest LogFile -> {oldest_file}. Error: {E}",
                    Module="LogManager.CheckFileLimit",
                    level="error"
                )
            else:
                self.log(
                    f"Deleted Oldest LogFile -> {oldest_file}.",
                    module="LogManager.CheckFileLimit",
                    level="info"
                )
            finally:
                log_files.remove(oldest_file)

    def log(
        self,
        *msg: str,
        level: LEVELS = "info",
        time_stamp: bool = True,
        module: bool | str = True,
        to_console: bool = True,
        to_file: bool = True,
    ):
        """_summary_

        Args:
            Module (str, optional): _Log Source._ Defaults By Auto Get.
            Level (Literal[Error, Warn, Normal], optional): _Log Level._ Defaults to 'Normal'.
            LogMessage (str, optional): _Log Output Message._ Defaults to 'Invalid Information'.
            LogConsole (bool, optional): _Whether the Log is output in the console._ Defaults is -1 mean fallow to self.LogConsole.
        """

        module: str = self.get_stack(2) if module is True else module
            # if From__Call__: Module = self.GetStack(3)

        prefix: str = "".join([
            f"[{get_time_stamp()}]" if time_stamp is True else "",
            f"[{level}]",
            f"[{module}]" if module else ""
        ])

        msg: str = "    " + " ".join([str(_) for _ in msg])

        if to_console:
            print(prefix + "\n" + msg, file=stderr)

        if to_file:
            self.file_log.write(f"{prefix}\n{msg}\n")

    def get_stack(self, depth: int = 1) -> str:
        """_summary_
        Args:
            depth (int, optional): _Call Stack Depth._ 1 if call directly; 2 if call from another LogManager method.
        Returns:
            str: _Description_
        """
        frame: FrameType = sys_getframe(depth)
        current_file: str = "./" + frame.f_code.co_filename[self.path_cwd_len:].replace("\\", "/")

        call_chain: list[str] = []
        while frame:
            co_name: str = frame.f_code.co_name # 获取代码对象名称
            if co_name == "<module>": break # 如果碰到模块层级就停止

            _self = frame.f_locals.get('self') # 获取实例对象
            _class = frame.f_locals.get('cls') # 获取类对象

            if _self or _class:
                class_name = (_self.__class__.__name__ if _self else _class.__name__)
                co_name = f"{class_name}.{co_name}"

            call_chain.append(co_name)
            frame = frame.f_back
        return current_file + "|" + ".".join(reversed(call_chain))

if __name__ == "__main__":
    logger: LogManager = LogManager(title="Nuhil Lucas", limit_log_files=10)
    logger.log("This is an info message.", level="info", module="TestModule")
    logger("a test", "This is a warning message.", level="warn")
    logger.log("This is an info message.", level="info", module="TestModule")
