# Standard
from random import (
    uniform as randflo
)
from time import (
    sleep as time_sleep
)
# Internal
from pylucas.basic.func import dependency_check
dependency_check("pyautogui", "Exception")
# External
from pyautogui._pyautogui_win import (
    _keyDown,
    _keyUp
)

class KeyBoard():
    @classmethod
    def press():
        pass

    @classmethod
    def release():
        pass

    @classmethod
    def click():
        pass

    @classmethod
    def hotkey():
        pass

    @classmethod
    def write(
        cls,
        text: str,
        interval: int = 5,
        mistake: int = 4,
        random_seed: tuple[float, float] = (3.0, 8.0)
    ):
        for char in text:
            seed: float = randflo(*random_seed)

            _keyDown(char)
            time_sleep(5/(seed*40*interval/1.5))
            _keyUp(char)
            time_sleep(1/(seed**(interval*3)))

            if mistake == 0: continue
            

            # if seed


if __name__ == "__main__":
    pass