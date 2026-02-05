# Standard
from typing import Any, Literal, TypeAlias
# Internal
from pylucas.basic.func import dependency_check
from pylucas.basic import Result
# External

MODULE_ART: bool = dependency_check("art", "bool")
FONT_TYPES: TypeAlias = Literal["univers", "tarty8", "tarty7", "tarty1", "block", "starwars"]
FONT_NAMES: list[str] = []

def text2art(
    text: Any,
    font: str = "DEFAULT_FONT",
    chr_ignore: bool = True,
    decoration: Any | None = None,
    sep: str = "\n",
    space: int = 0,
    __detailed_return: bool = False
) -> (tuple[str, Any | str, Any | None] | str):
    print("If need to use ascii_art related features, you need to install the 'art' package first. 'pip install art'")
    return text

class APrint():
    FONT: str = "tarty8"

    def __new__(
        cls,
        *args,
        font: FONT_TYPES = None,
        split_line: bool | str = False,
        sep: str = " ",
        end: str = ""
    ):
        print(cls.ascii_art(
            text=sep.join([str(arg) for arg in args]) + end,
            font=cls.FONT if font is None else font,
            split_line=split_line
        ), end=end)

    @staticmethod
    def ascii_art(
        text: str,
        font: str = None,
        split_line: bool | str = False
    ) -> str:
        """
        Generate Ascii Art Characters

        Args:
            text (str): _description_. Source String.
            font (str, 'univers'): _description_. Set the font for generating Ascii Art.
            split_line (bool | str, False): _description_. Add a context split line

        Returns:
            str: _description_. Ascii Art Characters
        """
        text: str = text2art(text=text, font=APrint.FONT if font is None else font).strip()

        if split_line:
            split_line: str = ("=" if not isinstance(split_line, str) else split_line)*(text.find("\n") if "\n" in text else len(text))
            text: str = split_line + "\n" + text + "\n" + split_line

        return text

    @classmethod
    def set_font(cls, font: str):
        if not MODULE_ART:
            print("If need to use ascii_art related features, you need to install the 'art' package first. 'pip install art'")
        else:
            if not font in FONT_NAMES:
                raise ValueError(f"Unsupported Font '{font}'")
            else:
                cls.FONT = font

    @classmethod
    def tittle(
        cls,
        *args,
        font: FONT_TYPES = None,
        split_line: str = "#"
    ):
        cls(*args, font=cls.FONT if font is None else font, split_line=split_line)

if MODULE_ART:
    from art import (
        text2art as art_text2art,
        FONT_NAMES as art_FONT_NAMES
    )

    text2art = art_text2art
    FONT_NAMES = art_FONT_NAMES

if __name__ == "__main__":
    # print(APrint.ascii_art("TEST TEST", "tarty8"))
    # APrint("TEST TEST")
    # APrint.set_font("tarty8")
    # APrint("TEST TEST")
    # APrint.set_font("Unsupported Font")
    # APrint(123, font="block")
    APrint.tittle(123, split_line="+")