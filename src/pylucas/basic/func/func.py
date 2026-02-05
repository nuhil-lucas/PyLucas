# Standard
from typing import Literal
from time import localtime, strftime
# Internal
from pylucas.basic.result import Result
# External

def time_stamp(
    rule: str = "%Y{split}%m{split}%d %H{split}%M{split}%S", 
    split: str = "-"
) -> str:
    """
    Use To Get TimeStamp

    Args:
        Split (str, '-'): _description_. Used to separate units of time.

    Returns:
        str: _description_. Return a timestamp accurate to the second.
    """
    time: str = localtime()
    time_formated: str = strftime(rule.format(split=split), time)

    return time_formated

def current_frame_info() -> tuple[str]:  # 获取当前帧信息
    """
    Gets the current code execution location

    Returns:
        tuple[str]: _description_. (Path_File, Name_Func, FuncLine_Def, FuncLine_Current)
    """
    from inspect import currentframe
    # 获取当前栈帧
    CurrentFrame = currentframe()
    # 文件名
    Path_File: str = CurrentFrame.f_code.co_filename
    # 函数名
    Name_Func: str = CurrentFrame.f_code.co_name
    # 函数定义的起始行号
    FuncLine_Def: int = CurrentFrame.f_code.co_firstlineno
    # 当前执行的行号 - 即调用currentframe()的行
    FuncLine_Current: int = CurrentFrame.f_lineno
    return (Path_File, Name_Func, FuncLine_Def, FuncLine_Current)

def lindex(List: list, Value: any) -> int:
    """_用于从左侧查找值索引, 类似 str.find, 如未找到则返回 -1._

    Args:
        List (list): _待查找的列表._
        Value (any): _待查找的值._

    Returns:
        int: _从列表左侧开始找到的第一个索引值._
    """
    if not Value in List: return -1
    Index = List.index(Value)
    return Index

def rindex(List: list, Value: any) -> int:
    """_用于从右侧查找值索引, 类似 str.rfind, 如未找到则返回 -1._

    Args:
        List (list): _待查找的列表._
        Value (any): _待查找的值._

    Returns:
        int: _从列表右侧开始找到的第一个索引值._
    """
    if not Value in List: return -1
    Index = len(List) - 1 - list(reversed(List)).index(Value)
    return Index

def dependency_check(
        module: str,
        mode: Literal["bool", "str", "dict", "Result", "Exception"] = "str"
    ) -> bool | str | Result:
    """
    dependency_check 的 Docstring
    
    :param module: Not Support The Format Like \"Module Name (Module Version)\"; Use Module Name Or Pkg Name Only Pls.
    :type module: str
    :param mode: Use To Control The Result Type.
    :type mode: Literal["bool", "str", "dict", "Result", "Exception"]
    :return: ...
    :rtype: bool | str | Result
    """
    from importlib.metadata import metadata, PackageNotFoundError

    module_found: bool = False # Distribution Package
    meta_data: dict = dict()
    msg: str = ""

    try:
        meta_data: dict = dict(metadata(module))
    except PackageNotFoundError:
        msg = f"Package '{module}' Not Found"
    except Exception as E:
        msg = f"Package '{module}' Not Found;" + f" {str(E)}"
    else:
        msg = f"Package '{module}' Found"
        module_found = True

    meta_data = meta_data | {"Msg": msg} if module_found else {"Name": module, "Msg": msg}

    match mode:
        case "bool":
            return module_found
        case "str":
            return msg
        case "dict":
            return meta_data
        case "Result":
            return Result(state=module_found, data=meta_data)
        case "Exception":
            if not module_found: raise ModuleNotFoundError(msg)

def terminal_clear():
    from os import system as os_system
    from platform import system as platform_system
    os_system('cls' if platform_system() == 'Windows' else 'clear')

if __name__ == "__main__":
    terminal_clear()
    print(dependency_check("tomli_w"))
    print(dependency_check("tomli-w"))
    print(dependency_check("time"))
