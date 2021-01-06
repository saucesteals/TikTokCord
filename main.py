import os, re, io, json, asyncio
from colorer import cprint, colors

try:
    import discord
    from discord.ext import commands
    from dotenv import load_dotenv
    import aiohttp
except:
    print('You forgot to pip/3 install requirements.txt!')
    exit()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CUSTOM_PREFIX = os.getenv("CUSTOM_PREFIX")

if BOT_TOKEN is None:
    print("You forgot to put your BOT_TOKEN in .env!")
    exit()

client = commands.Bot(command_prefix=CUSTOM_PREFIX if CUSTOM_PREFIX else "!", intents=discord.Intents.all())
client.session = None

## Heplers ##

async def set_cookies():
    await client.session.get('https://tiktok.com')
    
def is_admin(ctx):
    return ctx.author.id == 630545390785265674 or  ctx.author.guild_permissions.administrator

def guild_status(guild:discord.Guild) -> bool:
    return guild and str(guild.id) in client.data["guilds"] and client.data["guilds"][str(guild.id)]["status"] is True

def change_guild_status(guild:discord.Guild, new_status:bool) -> bool:
    if str(guild.id) not in client.data["guilds"]:
        client.data["guilds"][str(guild.id)] = {"status":False}

    client.data["guilds"][str(guild.id)]["status"] = new_status

    return client.data["guilds"][str(guild.id)]["status"]

def load_data() -> dict:
    return json.loads(open('data/data.json').read())

def dump_data():
    json.dump(client.data, open('data/data.json','w'))

############

@client.event
async def on_ready():

    if not os.path.exists('data/data.json'):
        if not os.path.exists('data'):
            os.mkdir('data')
        open('data/data.json', 'w').write('{"guilds":{}}')

    client.data = load_data()

    client.get_tiktok_link = re.compile(r'http[s]?://.+?tiktok\.com\S+')
    client.get_addr = re.compile("playAddr\":\"(.*?)\"")

    client.color = discord.Color(15605074)

    client.headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
    client.session = await aiohttp.ClientSession(headers=client.headers).__aenter__()
    await set_cookies()

    cprint(f"Ready as {client.user}", colors.GREEN)
    cprint(f"Invite Link: ", colors.GREEN, "")
    cprint(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions=8", colors.YELLOW)


@client.event
async def on_message(message):
    if client.is_ready() and guild_status(message.guild):
        if "tiktok.com" in message.content:
            urls = client.get_tiktok_link.findall(message.content)
            
            async with message.channel.typing():
                for url in urls:
                    cprint(f"Processing video for {str(message.author)} [{url}]!", colors.YELLOW)
                    video = await client.session.get(url)
                    if video.status == 200:
                        text = await video.text()
                        video_url = client.get_addr.findall(text)
                        if video_url:
                            raw_video_url = video_url[0].encode().decode('unicode-escape')
                            raw_video = await client.session.get(raw_video_url, headers={'Referer': url})
                            
                            if raw_video.status == 200:
                                data = io.BytesIO(await raw_video.read())
                                
                                file=discord.File(data, message.author.name + '.mp4')

                                if discord.__version__[:3] != "1.5":
                                    await message.reply(file=file)
                                
                                else:   
                                    await message.channel.send(content=message.author.mention, file=file)


                                cprint(f"Successfully sent video for {str(message.author)} [{url}]!", colors.GREEN)

                            else:
                                cprint(f"Bad response on video DOWNLOAD request! ({raw_video.status})", colors.RED)
                    else:
                        cprint(f"Bad response on video request! ({video.status})", colors.RED)

                    continue

    await client.process_commands(message)

@client.command()
@commands.check(is_admin)
async def toggle(ctx):
    current = guild_status(ctx.guild)
    
    new = change_guild_status(ctx.guild, not current)

    dump_data()
    await ctx.send(embed=discord.Embed(color=client.color, description=f"Tiktoks are now {'' if new else 'no longer '}automaically posted!"))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    raise error


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(client.start(BOT_TOKEN))

except KeyboardInterrupt:
    if client.session:
        loop.run_until_complete(client.session.close())

    loop.run_until_complete(client.logout())
    
finally:
    loop.close()
