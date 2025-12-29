from collections.abc import Coroutine
from discord import Interaction
from inspect import iscoroutinefunction
from typing import Self


class AutocompleteCommand:
  async def __call__(self: Self, interaction: Interaction) -> None:
    if not isinstance(interaction, Interaction): raise TypeError(f"interaction: Must be an instance of {Interaction.__name__}; not {interaction.__class__.__name__}")
    await self.callback(interaction)
  
  
  def __init__(self: Self, *, name: str, callback: Coroutine) -> None:
    if not isinstance(name, str): raise TypeError(f"name: Must be an instance of {str.__name__}; not {name.__class__.__name__}")
    if not name.strip(): raise ValueError("name: Must not be an emptry string")
    if not iscoroutinefunction(callback): raise TypeError("callback: Must be a coroutine")
    self.__name: str = name.strip()
    self.callback: Coroutine = callback


  @property
  def name(self: Self) -> str:
    return self.__name