import os
import json
import discord
from discord.ext import commands
import logging
import python_aternos as aternos
import requests
import base64
# Clear shell
os.system('cls')

# Settings
ps1 = '\033[96m🛆\033[0m'
creds = json.load(open('creds.json'))
config = json.load(open('data.json'))
formater = logging.Formatter(ps1 + '\033[91m Error at %(asctime)s: %(message)s',
                             datefmt='%d/%m %H:%M')

# Setup clients
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=">")
api = aternos.Client.from_credentials(creds['usr'], creds['pwd'])

# Load server
if config['id']:
    cur = api.get_server(config['id'])
    print(ps1, f'Resumed last session server: {config["id"]}')


@bot.event
async def on_ready() -> None:
    print(ps1, 'Bot ready')


servers = api.list_servers(False)
cur = servers[0]
config['id'] = cur.servid


@bot.command(aliases=['Start', 'START'])
async def start(ctx):
    """
    Start the server
    """
    print(ps1, f"starting server {cur.domain}")
    try:
        cur.start(True, True)
        await ctx.reply("starting server")
    except:
        await ctx.reply("server is already on")


@bot.command(aliases=['Stop', 'STOP'])
async def stop(ctx):
    """
    Stop the server
    """
    print(ps1, f"stop server {cur.domain}")
    try:
        cur.stop()
        await ctx.reply("stopping the server")
    except:
        await ctx.reply("server is already off")


@bot.command(aliases=['Restart', 'RESTART'])
async def restart(ctx):
    """
    Restart the server
    """
    print(ps1, f"restart server {cur.domain}")
    try:
        cur.restart()
        await ctx.reply("restarting the server")
    except:
        await ctx.reply("oops idk wat happened contact nadeem")
@bot.command()
async def ping(ctx):
    """
    Ping!
    """
    await ctx.reply('Pong!   `{0} seconds`'.format(round(bot.latency, 1)))

@bot.command()
@commands.has_permissions(administrator=True)
async def info(ctx):
    """
    Nadeems special command dont use pls
    """
    cur.fetch()
    data = cur._info

    print(ps1, 'Sending data')
    try:
        await ctx.reply(f'Fetched data: ```json\n{json.dumps(data, indent=3)}```')
    except:
        await ctx.reply("somethings wrong call nadeem")

@bot.command(aliases=['status', 'Status'])
async def mcstatus(ctx):
        """
        MC Server Status, Updates every 10 minutes
        """
        cur.fetch()
        data = requests.get("https://eu.mc-api.net/v3/server/ping/Mincreft22.aternos.me:61553").json()
        motdto = requests.get("https://mcapi.us/server/status?ip=Mincreft22.aternos.me&port=61553").json()
        embed = discord.Embed(title="Server status", colour=discord.Colour.blurple())
        try:
            if cur.status == 'online':
                embed.add_field(name="Status", value=f"{cur.status} :green_circle:")
            else:
                embed.add_field(name="Status" , value=f"{cur.status} :red_circle:")
        except:
            embed.add_field(name="Status", value="Failed")
        try:
            embed.add_field(name="Players online", value=f"{data['players']['online']} / {data['players']['max']}")
        except:
            embed.add_field(name="Players online", value="Failed")
        try:
            embed.add_field(name="Latency", value=f"{data['took']} ms")
        except:
            embed.add_field(name="Latency", value="Failed")

        try:
            embed.add_field(name="Version", value=f"{cur.version}")
        except:
            embed.add_field(name="Version", value="Failed")

        try:
            embed.add_field(name="Motd", value=f"{cur.motd}")
        except:
            embed.add_field(name="Motd", value="Failed")

        try:
            embed.add_field(name="Player Names", value=f"{motdto['players']['list']}")
        except:
            embed.add_field(name="Player Names", value="Failed")

        try:
            embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/or7mN4DQa7IqfuCuN8XTP3OQLlwx1hMTn0Cdq_qwWaM/https/eu.mc-api.net/v3/server/favicon/mincreft22.aternos.me%3A61553?width=80&height=80")
        except:
            embed.set_thumbnail(url="https://media.minecraftforum.net/attachments/300/619/636977108000120237.png")
        await ctx.send(embed=embed)


bot.run(creds['tkn'], log_level=logging.ERROR, log_formatter=formater)
# EOF
