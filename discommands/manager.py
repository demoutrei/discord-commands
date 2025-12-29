from .commands import AutocompleteCommand, ReplyCommand, ThreadCommand
from collections.abc import Coroutine
from discord import Interaction, InteractionType, Message, MessageType, Thread
from discord.app_commands import autocomplete, Choice, Command, command as slash, describe
from discord.ext.commands import Bot
from typing import Optional, Self


async def command_name_autocomplete(interaction: Interaction, current: str) -> list[Choice[str]]:
  commands: list[AutocompleteCommand] = interaction.client.discommands.autocomplete_commands
  return [Choice(name = f"{interaction.client.command_prefix}{command.name}", value = command.name) for command in commands if current.strip().lower() in command.name.lower()]


async def command_parameters_autocomplete(interaction: Interaction, current: str) -> list[Choice[str]]:
  return list()


class CommandManager:
  def __init__(self: Self, bot: Bot) -> None:
    if not isinstance(bot, Bot): raise TypeError(f"bot: Must be an instance of {Bot.__name__}; not {bot.__class__.__name__}")
    bot.discommands: Self = self
    self.__bot: Bot = bot
    self.__bot.add_listener(self.__autocomplete_command_listener, "on_interaction")
    self.__bot.add_listener(self.__reply_command_listener, "on_message")
    self.__bot.add_listener(self.__thread_command_listener, "on_thread_create")
    self.__autocomplete_commands_map: dict[str, AutocompleteCommand] = dict()
    self.__reply_commands_map: dict[str, ReplyCommand] = dict()
    self.__slash_autocomplete_command: Command = Command(name = "autocomplete", description = "Autocomplete command", callback = self.__autocomplete_command)
    self.__thread_commands_map: dict[str, ThreadCommand] = dict()


  @autocomplete(
    name = command_name_autocomplete,
    parameters = command_parameters_autocomplete
  )
  @describe(
    name = "Command name",
    parameters = "Command parameters, if any"
  )
  async def __autocomplete_command(self: Self, interaction: Interaction, name: str, parameters: Optional[str]) -> None:
    command: Optional[AutocompleteCommand] = self.__autocomplete_commands_map.get(name)
    if not command:
      await interaction.response.send_message(
        f"No autocomplete command with name: ` {name} `",
        ephemeral = True
      )
      return
    await command(interaction)


  async def __autocomplete_command_listener(self: Self, interaction: Interaction) -> None:
    if interaction.type is not InteractionType.application_command: return
    if interaction.command.name != "autocomplete": return
    await self.__autocomplete_command(interaction, interaction.namespace.name, interaction.namespace.parameters)


  async def __reply_command_listener(self: Self, message: Message) -> None:
    if message.type is not MessageType.reply: return
    if message.author.bot: return
    if not message.content: return
    if not message.content.startswith(self.__bot.command_prefix): return
    command_name: str = message.content[1:]
    command: Optional[ReplyCommand] = self.__reply_commands_map.get(command_name)
    if not command: return
    await command(message)


  async def __thread_command_listener(self: Self, thread: Thread) -> None:
    if not thread.name.startswith(self.__bot.command_prefix): return
    command_name: str = thread.name[1:]
    command: Optional[ThreadCommand] = self.__thread_commands_map.get(command_name)
    if not command: return
    await command(thread)


  def add_autocomplete_command(self: Self, command: AutocompleteCommand) -> AutocompleteCommand:
    if not isinstance(command, AutocompleteCommand): raise TypeError(f"command: Must be an instance of {AutocompleteCommand.__name__}; not {command.__class__.__name__}")
    if command.name in self.__autocomplete_commands_map: raise ValueError(f"command: AutocompleteCommand {command.name!r} is already added to the command manager")
    if not self.__autocomplete_commands_map:
      print("Adding autocomplete command slash command...")
      self.__bot.tree.add_command(self.__slash_autocomplete_command)
    print("Adding autocomplete command to map...")
    self.__autocomplete_commands_map[command.name]: AutocompleteCommand = command
    print(f"{self.__autocomplete_commands_map = }")
    return command


  def add_reply_command(self: Self, command: ReplyCommand) -> ReplyCommand:
    if not isinstance(command, ReplyCommand): raise TypeError(f"command: Must be an instance of {ReplyCommand.__name__}; not {command.__class__.__name__}")
    if command.name in self.__reply_commands_map: raise ValueError(f"command: ReplyCommand {command.name!r} is already added to the command manager")
    self.__reply_commands_map[command.name]: ReplyCommand = command
    return command


  def add_thread_command(self: Self, command: ThreadCommand) -> ThreadCommand:
    if not isinstance(command, ThreadCommand): raise TypeError(f"command: Must be an instance of {ThreadCommand.__name__}; not {command.__class__.__name__}")
    if command.name in self.__thread_commands_map: raise ValueError(f"command: ThreadCommand {command.name!r} is already added to the command manager")
    self.__thread_commands_map[command.name]: ThreadCommand = command
    return command


  def autocomplete(self: Self, *, name: Optional[str] = None) -> AutocompleteCommand:
    def wrapper(function: Coroutine) -> AutocompleteCommand:
      command_name: str = (name or function.__name__).strip()
      command: AutocompleteCommand = AutocompleteCommand(name = command_name, callback = function)
      return self.add_autocomplete_command(command)
    return wrapper


  @property
  def autocomplete_commands(self: Self) -> list[AutocompleteCommand]:
    return list(self.__autocomplete_commands_map.values())


  @property
  def bot(self: Self) -> Bot:
    return self.bot


  def reply(self: Self, *, name: Optional[str] = None) -> ReplyCommand:
    def wrapper(function: Coroutine) -> ReplyCommand:
      command_name: str = (name or function.__name__).strip()
      command: ReplyCommand = ReplyCommand(name = command_name, callback = function)
      return self.add_reply_command(command)
    return wrapper


  @property
  def reply_commands(self: Self) -> list[ReplyCommand]:
    return list(self.__reply_commands_map.values())


  def thread(self: Self, *, name: Optional[str] = None) -> ThreadCommand:
    def wrapper(function: Coroutine) -> ThreadCommand:
      command_name: str = (name or function.__name__).strip()
      command: ThreadCommand = ThreadCommand(name = command_name, callback = function)
      return self.add_thread_command(command)
    return wrapper


  @property
  def thread_commands(self: Self) -> list[ThreadCommand]:
    return list(self.__thread_commands_map.values())