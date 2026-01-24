class CPrint():
    BLUE: str = "\033[38;2;0;0;255m"
    ORANGE: str = "\033[38;2;255;165;0m"
    GREEN: str = "\033[38;2;0;128;0m"
    RED: str = "\033[38;2;255;0;0m"
    CRIMSON: str = "\033[38;2;220;20;60m"

    RESET: str = "\033[0m"

    def __new__(
        cls,
        *args,
        color: str = "\033[0m",
        reset: bool = False,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print((f"\033[38;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:], 16)}m" if color.startswith("#") else color) + (sep.join(arg.__str__() for arg in args)) + (cls.RESET if reset else ""), end=end, file=file)

    @classmethod
    def info(
        cls,
        *args,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print(cls.BLUE + sep.join(arg.__str__() for arg in args) + cls.RESET, end=end, file=file)

    @classmethod
    def warn(
        cls,
        *args,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print(cls.ORANGE + sep.join(arg.__str__() for arg in args) + cls.RESET, end=end, file=file)

    @classmethod
    def error(
        cls,
        *args,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print(cls.RED + sep.join(arg.__str__() for arg in args) + cls.RESET, end=end, file=file)

    @classmethod
    def success(
        cls,
        *args,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print(cls.GREEN + sep.join(arg.__str__() for arg in args) + cls.RESET, end=end, file=file)

    @classmethod
    def failure(
        cls,
        *args,
        sep: str = " ",
        end: str = "\n",
        file = None
    ):
        print(cls.CRIMSON + sep.join(arg.__str__() for arg in args) + cls.RESET, end=end, file=file)

    @classmethod
    def reset(cls):
        print(cls.RESET, end="")


if __name__ == "__main__":
    from sys import stderr
    CPrint.info("name:", "NuhilLucas")
    CPrint.warn("name:", "NuhilLucas")
    CPrint.error("name:", "NuhilLucas")
    CPrint.success("name:", "NuhilLucas")
    CPrint.failure("name:", "NuhilLucas")
    CPrint("name:", "NuhilLucas", color = "#D9FF00", reset=True)
    CPrint("name:", "NuhilLucas", color = "#D9FF00", file=stderr)
    CPrint("name:", "NuhilLucas")
    CPrint.reset()
    print("name:", "NuhilLucas")