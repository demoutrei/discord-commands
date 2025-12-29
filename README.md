## Command Types

### AutocompleteCommand
```py
# Triggers when the /autocomplete slash command's "name"
#   slash option matches the AutocompleteCommand's name

@bot.discommands.autocomplete()
async def ping(interaction: Interaction) -> None:
  await interaction.response.send_message("Pong!")
```

### ReplyCommand
```py
# Triggers when a reply message matches a ReplyCommand
#   name

@bot.discommands.reply()
async def sample(message: Message) -> None:
  await message.reply("Sample")
```

### ThreadCommand
```py
# Triggers when a created thread's name matches a
#   ThreadCommand name

@bot.discommands.thread()
async def sample(thread: Thread) -> None:
  await thread.send("Sample")
```


Credits for the command [ideas](<https://gist.github.com/Soheab/a6229dbbe3acf3ce9a4625bf9e7177da>):
- [Soheab](<https://github.com/Soheab>)
- [maukkis](<https://github.com/maukkis>)