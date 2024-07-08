import disnake
from disnake.ext import commands
from aiohttp import web

intents = disnake.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

verification_requests = {}

GUILD_ID = 'PASTE_ID'
ROLE_ID = 'PASTE_ID'


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id in verification_requests:
        code = verification_requests.pop(user_id)
        if message.content.strip() == code:
            guild = bot.get_guild(int(GUILD_ID))
            if guild:
                member = guild.get_member(user_id)
                if member:
                    role = disnake.utils.get(guild.roles, id=int(ROLE_ID))
                    await member.add_roles(role)
                    await message.channel.send("The role has been given!")
                else:
                    await message.channel.send("User is not found.")
            else:
                await message.channel.send("Server not found.")
        else:
            await message.channel.send(
                "Invalid code, please try again or contact support: \n write support links.")
    await bot.process_commands(message)


async def handle_verification(request):
    data = await request.json()
    telegram_id = data['telegram_id']
    discord_username = data['discord_username']
    code = data['code']

    guild = bot.get_guild(int(GUILD_ID))
    member = disnake.utils.get(guild.members,
                               name=discord_username)

    if member:
        verification_requests[member.id] = code
        await member.send("Hello! I am a Telegram and Discord verification bot,if you have not received any code, please contact support:\n 
write support links here\n Enter code:")
        return web.Response(text="Verification request received.")
    else:
        return web.Response(text="User not found.")



async def handle_user_removal(request):
    data = await request.json()
    telegram_id = data['telegram_id']
    discord_username = data['discord_username']

    guild = bot.get_guild(int(GUILD_ID))
    member = disnake.utils.get(guild.members, name=discord_username)

    if member:
        role = disnake.utils.get(guild.roles, id=int(ROLE_ID))
        await member.remove_roles(role)
        print(f"The user {telegram_id} no longer exists, the role has been removed from {discord_username}")

    return web.Response(text="User removal notification received.")


app = web.Application()
app.router.add_post('/verify', handle_verification)
app.router.add_post('/remove_user', handle_user_removal)

if __name__ == "__main__":
    bot.loop.create_task(web._run_app(app, port=8080))
    bot.run('PASTE_TOKEN')
