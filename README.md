# Telegram Verification with-Discord Bot
Do you need to link your telegram account to your discord channel? We can use this mod. Here is an example of how a discord bot works, which gives a role to a verified user, but you can change this example to anything you like

# How to use
step by step
- clone this repo
```
git clone https://github.com/Faynot/Telegram-Verification-with-Discord-Bot.git
cd Telegram-Verification-with-Discord-Bot
```
- Run ![ngrok](https://ngrok.com/docs)
```
ngrok http 8080
```
- Copy url (for example https://123a-45-678-910-11.ngrok-free.app/) to tg.py
```
DISCORD_BOT_URL = 'https://123a-45-678-910-11.ngrok-free.app/verify'
DISCORD_REMOVE_USER_URL = 'https://123a-45-678-910-11.ngrok-free.app/remove_user'
```
- Create telegram bot in ![BotFather](https://t.me/BotFather)
- Copy telegram bot token
- Paste token to tg.py
```
API_TOKEN = 'PASTE_YOUR_TOKEN'
```
- Go to ![Discord Developer Portal](https://discord.com/developers/applications) and create new application
- Go to "bot"

![](https://cdn.discordapp.com/attachments/1100716068588245083/1259853929781661716/image.png?ex=668d31e7&is=668be067&hm=f0eb15d5279ef1f51be333c850684513a1e77cf266228884b73dab5ca73c6a1a&)
- Copy bot Token
- Paste this token to ds.py
```
    bot.run('PASTE_YOUR_TOKEN')
```
- Copy ID youre server to ds.py
```
GUILD_ID = 'PASTE_ID'
```
- Copy ID youre role to ds.py
```
ROLE_ID = 'PASTE_ID'
```
- If you want to check whether a user is in a particular chat or channel, copy your channel ID here (to find out the ID of a private channel, go to the web version of telegram and copy it from the page url). If you do not want this check, then simply remove the part of the code with this check
```
CHANNEL_ID = 'PASTE_ID'
```

Last steps:

Download all dependencies
```
pip install -r requirements.txt
```

Run discord bot
- For windows
```
python ds.py
```
- For linux
```
python3 ds.py
```

Run telegram bot
- For windows
```
python tg.py
```
- For linux
```
python3 tg.py
```

That's all!
