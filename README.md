## Command Types

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