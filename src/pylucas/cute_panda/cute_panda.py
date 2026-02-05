# Standard
# Internal
from pylucas.basic.func import dependency_check
dependency_check("pandas", "Exception")
dependency_check("numpu", "Exception")
# External
from pandas import (
    DataFrame,
    read_excel as pd_read_excel
)
from numpy import nan

def read_excel(
    io: str,
    sheet_name: int = 0,
    key_tags: list = [],
    search_range: int = 15
):
    """_用于简化读取Excel文件并进行基础清洗的过程._

    Args:
        io (str): _Excel文件路径_
        sheet_name (int | str, optional): _数据表名称或是索引._ 默认为 0.
        KeyTags (list[list[str]], optional): _数据表列标签中必须包含的关键字, 若单个列标签存在多个可能的关键字则使用列表包裹, 允许缺省._ 默认为 [].
        SearchRange (int, optional): _检索标题行的范围._ 默认为 15, 为 -1 时无限制.

    Raises:
        Exception: _在预设的范围内[header < {TagLine}]无法找到标题行._

    Returns:
        DataFrame: _完成读取与基础清晰的 DataFrame 实例._
    """
    sheet: DataFrame = pd_read_excel(io=io,
                                  sheet_name=sheet_name,
                                  header=None,
                                  dtype=str).fillna('')
    sheet = sheet.replace(['', ' '], nan).dropna(how='all').fillna('')
    search_range = sheet.shape[0] if search_range == -1 else search_range
    key_tags = [key_tag if isinstance(key_tag, list) else [key_tag] for key_tag in key_tags]
    for row_idx, row in sheet.iterrows():
        col_tags = row.tolist()
        is_title: bool = all([any([col_tag in col_tags for col_tag in key_tag]) for key_tag in key_tags])
        if row_idx > search_range:
            raise Exception(f"在预设的范围内[header < {row_idx}]无法匹配到标题行.")
        elif is_title or not key_tags:
            sheet = sheet.iloc[row_idx+1:].reset_index(drop=True)
            sheet.columns = [col_tag.strip() if col_tag else f'Unnamed: {col_idx}' for col_idx, col_tag in enumerate(col_tags)]
            return sheet
    else:
        raise Exception(f"在数据表内无法匹配到标题行.")
