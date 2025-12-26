from .commands import ReplyCommand
from collections.abc import Coroutine
from discord import Message, MessageType
from discord.ext.commands import Bot
from typing import Optional, Self


class CommandManager:
  def __init__(self: Self, bot: Bot) -> None:
    if not isinstance(bot, Bot): raise TypeError(f"bot: Must be an instance of {Bot.__name__}; not {bot.__class__.__name__}")
    bot.discommands: Self = self
    self.__bot: Bot = bot
    self.__bot.add_listener(self.__reply_command_listener, "on_message")
    self.__reply_commands_map: dict[str, ReplyCommand] = dict()


  async def __reply_command_listener(self: Self, message: Message) -> None:
    if message.type is not MessageType.reply: return
    if message.author.bot: return
    if not message.content: return
    if not message.content.startswith(self.__bot.command_prefix): return
    command_name: str = message.content[1:]
    command: Optional[ReplyCommand] = self.__reply_commands_map.get(command_name)
    if not command: return
    await command(message)


  def add_reply_command(self: Self, command: ReplyCommand) -> ReplyCommand:
    if not isinstance(command, ReplyCommand): raise TypeError(f"command: Must be an instance of {ReplyCommand.__name__}; not {command.__class__.__name__}")
    if command.name in self.__reply_commands_map: raise ValueError(f"command: ReplyCommand {command.name!r} is already added to the command manager")
    self.__reply_commands_map[command.name]: ReplyCommand = command
    return command


  @property
  def bot(self: Self) -> Bot:
    return self.bot


  def reply(self: Self, *, name: Optional[str] = None) -> ReplyCommand:
    def wrapper(function: Coroutine) -> ReplyCommand:
      command_name: str = (name or function.__name__).strip()
      command: ReplyCommand = ReplyCommand(name = command_name, callback = function)
      return self.add_reply_command(command)
    return wrapper