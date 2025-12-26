from collections.abc import Coroutine
from discord import Message
from inspect import iscoroutinefunction
from typing import Self


class ReplyCommand:
  async def __call__(self: Self, message: Message) -> None:
    if not isinstance(message, Message): raise TypeError(f"message: Must be an instance of {Message.__name__}; not {message.__class__.__name__}")
    await self.callback(message.reference.cached_message or message.reference.resolved)
  
  
  def __init__(self: Self, *, name: str, callback: Coroutine) -> None:
    if not isinstance(name, str): raise TypeError(f"name: Must be an instance of {str.__name__}; not {name.__class__.__name__}")
    if not name.strip(): raise ValueError("name: Must not be an empty string")
    if not iscoroutinefunction(callback): raise TypeError("callback: Must be a coroutine")
    self.__name: str = name.strip()
    self.callback: Coroutine = callback


  @property
  def name(self: Self) -> str:
    return self.__name