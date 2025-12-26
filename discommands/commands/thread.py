from collections.abc import Coroutine
from discord import Thread
from inspect import iscoroutinefunction
from typing import Self


class ThreadCommand:
  async def __call__(self: Self, thread: Thread) -> None:
    if not isinstance(thread, Thread): raise TypeError(f"thread: Must be an instance of {Thread.__name__}; not {thread.__class__.__name__}")
    await self.callback(thread)
  
  
  def __init__(self: Self, *, name: str, callback: Coroutine) -> None:
    if not isinstance(name, str): raise TypeError(f"name: Must be an instance of {str.__name__}; not {name.__class__.__name__}")
    if not name.strip(): raise ValueError(f"name: Must not be an empty string")
    if not iscoroutinefunction(callback): raise TypeError(f"callback: Must be a coroutine")
    self.__name: str = name.strip()
    self.callback: Coroutine = callback


  @property
  def name(self: Self) -> str:
    return self.__name