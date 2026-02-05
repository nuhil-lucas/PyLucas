# Standard
from random import (
    uniform as randflo
)
from math import (
    hypot,
    cos,
    sin,
    atan2,
    comb,
    pi as PI
)
from time import (
    sleep as time_sleep
)
from typing import (
    Iterator,
    Literal,
    TypeAlias,
    get_args
)
# Internal
from pylucas.basic.func import dependency_check
dependency_check("pyautogui", "Exception") 
# External
import pyautogui; pyautogui.FAILSAFE = False
from pyautogui._pyautogui_win import (
    _position,
    _mouseDown,
    _mouseUp
)
from pyautogui import (
    mouseInfo,
    moveTo
)

USEABLE_MK: TypeAlias = Literal[
    "left",
    "middle",
    "right"
]
MOUSE_KEYS: tuple[str] = get_args(USEABLE_MK)

def bezier_point(*points, t: float):
    n = len(points) - 1  # 核心修复：阶数 = 点数-1
    if n < 0:
        return (0.0, 0.0)
    if n == 0:  # 单点退化情况
        return points[0]
    
    x_bezier = y_bezier = 0.0
    for i, (x, y) in enumerate(points):
        coeff = comb(n, i) * ((1 - t) ** (n - i)) * (t ** i)
        x_bezier += coeff * x
        y_bezier += coeff * y
    return x_bezier, y_bezier

class Mouse():
    @classmethod
    def _get_ctrl_points_(
        cls,
        x_start: int,
        y_start: int,
        x_end: int,
        y_end: int,
        qty: int,
        curvature: tuple[float, float]
    ) -> Iterator[tuple[int, int]]:
        dx = (x_end - x_start) / (qty - 1) if qty > 1 else 0
        dy = (y_end - y_start) / (qty - 1) if qty > 1 else 0
        
        offset: float = hypot(x_end-x_start, y_end-y_start) * randflo(*curvature) * randflo(0.8, 1.2)
        angle: float = atan2(dy, dx) + PI / 2

        for i in range(qty):
            x = x_start + i * dx + cos(angle) * offset
            y = y_start + i * dy + sin(angle) * offset

            yield i, x, y

    @classmethod
    def debuger(cls):
        mouseInfo()

    @classmethod
    def pos(cls) -> tuple[int, int]:
        return _position()

    @classmethod
    def press(
        cls,
        key: USEABLE_MK
    ):
        _mouseDown(*cls.pos(), button=key)

    @classmethod
    def release(
        cls,
        key: USEABLE_MK
    ):
        _mouseUp(*cls.pos(), button=key)

    @classmethod
    def click(
        cls,
        key: USEABLE_MK,
        interval: tuple[float, float] = (0.05, 0.12)
    ):
        _mouseDown(*cls.pos(), button=key)
        time_sleep(randflo(*interval))
        _mouseUp(*cls.pos(), button=key)

    @classmethod
    def dbclick(
        cls,
        key: USEABLE_MK,
        interval: tuple[float, float] = (0.05, 0.12)
    ):
        pos: tuple[int, int] = cls.pos()
        _mouseDown(*pos, button=key)
        time_sleep(randflo(*interval))
        _mouseUp(*pos, button=key)
        time_sleep(randflo(*interval))
        _mouseDown(*pos, button=key)
        time_sleep(randflo(*interval))
        _mouseUp(*pos, button=key)

    @classmethod
    def tp_to(cls, x: int, y: int):
        moveTo(x=x, y=y)

    @classmethod
    def move_to(
        cls,
        x: int, y: int,
        timeuse: float = 2,
        curvature: tuple[float, float] = (-0.1, 0.1),
        jitter: float = 5.0,
        smooth: float = 4.0,
        cp_qty: int = 6
    ):
        """
        模拟人类的鼠标移动
        
        参数:
            x, y: 目标坐标
            timeuse: 总移动时间（秒）
            curvature: 轨迹弯曲程度区间
            jitter: 轨迹抖动幅度
            smooth: 平滑系数
            cp_qty: 控制点数量
        """
        x_start, y_start = cls.pos()
        x_end, y_end = x, y

        coef_smooth: float = 4.0 if smooth == 0 else abs(smooth)

        jitter: float = abs(jitter)
        smooth_move = lambda t: 1 - (1 - t) ** coef_smooth
        ctrl_points: list[tuple[int, int]] = [(x, y) for i, x, y in cls._get_ctrl_points_(x_start, y_start, x_end, y_end, cp_qty, curvature)]
        steps: int = max(15, min(100, int(timeuse * 40))) if timeuse > 0 else 1
        interval: float = timeuse / steps
        
        for i in range(steps + 1):
            t = i / steps

            coef_jitter = (1-t)**coef_smooth
            
            bx, by = bezier_point((x_start, y_start), *ctrl_points, (x_end, y_end), t=smooth_move(t))

            if i < steps:
                bx += randflo(-jitter, jitter) * coef_jitter
                by += randflo(-jitter, jitter) * coef_jitter
            else:
                bx, by = x_end, y_end
            
            if abs(x_end-bx) < 0.07 and abs(y_end-by) < 0.07:
                moveTo(x_end, y_end, _pause=False)
                break
            moveTo(bx, by, _pause=False)
            
            if i < steps:
                time_sleep(interval * randflo(0.5, 1.1))

    @classmethod
    def drag_to(
        cls,
        key: USEABLE_MK,
        x: int, y: int,
        timeuse: float = 2,
        curvature: tuple[float, float] = (-0.1, 0.1),
        jitter: float = 5.0,
        smooth: float = 4.0,
        cp_qty: int = 6
    ):
        pos: tuple[int, int] = cls.pos()
        _mouseDown(*pos, button=key)
        cls.move_to(
            x=x, y=y,
            timeuse=timeuse,
            curvature=curvature,
            jitter=jitter,
            smooth=smooth,
            cp_qty=cp_qty
        )
        _mouseUp(*pos, button=key)

if __name__ == "__main__":
    if 0:
        Mouse.move_to(x=10, y=10)
    
    if 1:
        # Mouse.click(key="left")
        Mouse.dbclick(key="left")
    
    if 0:
        Mouse.press(key="left")
        time_sleep(1)
        Mouse.release(key="left")

    if 0:
        Mouse.drag_to("left", 10, 300)