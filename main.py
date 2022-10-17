

import discord, os
import misc as m, account_checker as s, keep_alive as kp  #extra files
from discord.ext import commands  # commands
from discord.ext.tasks import loop  # loop

client = commands.Bot(command_prefix='!')
token = os.getenv("BOT_TOKEN")

# Steam Commands
#--------------------------------------------------------------------------------------------------------------------------------------------

@client.command()
async def printDB(ctx):
  await s.print_database(ctx)

@client.command()
async def checkAcc(ctx, accid=""):
    embed_returned = await s.check_account(ctx, str(accid))
    woodys_server = client.get_channel(818107158213558302)
    try:
        await ctx.send(embed=embed_returned)
        await woodys_server.send(embed=embed_returned)
    except Exception as e:
        print(e)
        error_channel = client.get_channel(818923566480752653)
        await error_channel.send("failed Acc check, id: " + str(accid))


@client.command()
async def addAcc(ctx, accid=""):
    await s.add_account(ctx, str(accid))

@client.command()
async def removeAcc(ctx, accid=""):
    await s.remove_account(ctx, str(accid))


@loop(seconds=3600)
async def account_data_loop():
    embed_returned = await s.check_database()
    woodys_server = client.get_channel(818107158213558302)
    try:
        await woodys_server.send(embed=embed_returned)
        await woodys_server.send("Account removed from database.")
    except Exception as e:
        #print(e)
        print("database tested, no accounts found")
        pass


'''
@client.command()
async def accLoopStart(ctx):
    try:
        account_data_loop.start(ctx)
        await ctx.send("Loop has started, database will be checked every hour!")
    except:
        await ctx.send("Already checking database every hour.")
@client.command()
async def accLoopStop(ctx):
    try:
        account_data_loop.cancel()
        await ctx.send("Loop has stopped.")
    except:
        await ctx.send("Database loop is not running.")
'''


@client.command()
async def printDatabase(ctx):
    await s.print_database(ctx)

# Misc Commands
#--------------------------------------------------------------------------------------------------------------------------------------------


@client.command()
async def ping(ctx):
    await m.bot_ping(ctx, client)


@client.command()
async def clear(ctx, amount=1):
    await m.clear_msg(ctx, amount)


@client.command()
async def ball(ctx):
    await m.ball_answer(ctx)


client.remove_command('help')


@client.command()
async def help(ctx, com=""):
    await m.help_info(ctx, com)

# Run Bot
#--------------------------------------------------------------------------------------------------------------------------------------------


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("in the corner..."))
    print('Bot is ready')
    #woodys_server = client.get_channel(818107158213558302)
    #await woodys_server.send("Bot has started!")
    account_data_loop.start()


kp.keep_alive()
try:
  client.run(token)
except Exception as E:
  print(E)
  