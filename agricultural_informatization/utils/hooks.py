from typing import Callable, Any
import signal

from .log import logger


EXIT_HOOK_FUNCS: list[Callable[[], Any]] = []
"""退出程序钩子函数"""

def quit_hook(signal, frame):
    logger.info("收到程序终止信号，开始运行结束钩子函数...")
    for func in EXIT_HOOK_FUNCS:
        logger.debug(f"开始运行结束钩子函数 {func.__name__}")
        func()

signal.signal(signal.SIGINT, quit_hook)


__all__ = [
    "EXIT_HOOK_FUNCS"
]