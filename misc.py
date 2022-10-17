import random

async def bot_ping(ctx, client):
    print('pinged bot')
    s = str("bot latency is "+str(round(client.latency *1000))+ "ms")
    await ctx.send(s)
    #print('sent ping')
    
    
async def clear_msg(ctx, amount):
    s = str('Tying to delete '+str(amount) + ' messages...')
    await ctx.send(s)
    try:
        await ctx.channel.purge(limit = amount+2)
    except:
        await ctx.send("Could not delete messages...")

async def ball_answer(ctx):
    answers = ["Yes!", "I don't think so.", "Absolutely not!", "Without a doubt!", "Probably...?", "I have no idea...", "No!" ]
    await ctx.send(random.choice(answers))

async def help_info(ctx, com):    
    if com == "help":
        await ctx.send("This command shows the list of commands")
    elif com == "skip":
        await ctx.send("This command stops the music playing")
    elif com == "ping":
        await ctx.send("This command shows the bot's latency")
    elif com == "clear":        
        await ctx.send("This command deletes that amount of messages")
    elif com == "checkAcc":        
        await ctx.send("This command will use the steam api to check for any bans on the specified account.")
    elif com == "addAcc":        
        await ctx.send("This command will add the id to the database to be checked every hour (if the loop is running)")
    
    #elif com == "accLoopStart":        
    #    await ctx.send("This command will start the loop to check for any banned accounts  in the databse.\nIf an account is banned the bot will post a notification in the channel the loop was started in.")
    #elif com == "accLoopStop":        
    #    await ctx.send("This command will stop the bot from checking the databse.")
    
    else:
        await ctx.send('Bot Prefix: !\nSteam Commands: ```checkAcc (ID), addAcc (ID), accLoopStart, accLoopStop```\nMisc Commands: ```help (text), ping, clear (number)```')
        await ctx.send("``You can type !help 'command here' for more info on a specific command``")
        
