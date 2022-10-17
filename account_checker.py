import discord, requests, os
from replit import db

api_key = os.getenv("STEAM_API")

async def check_account(ctx, steam_id):
    try:
        s= "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key="+api_key+"&steamids="+str(steam_id)
        summary = requests.get(s).json()        
        name = summary['response']['players']['player'][0]['personaname']
        profile_picture = summary['response']['players']['player'][0]['avatarfull']        
        s= "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="+api_key+"&steamids="+str(steam_id)
        ban_info = requests.get(s).json()        
        embed = discord.Embed(
            title = 'Account Found',     
            descriptoin = "",
            colour = discord.Colour.from_rgb(50,255,100)
            )
        embed.add_field(name = "Name:", value=name, inline = False)
        if ban_info['players'][0]['VACBanned'] == False and ban_info['players'][0]['NumberOfGameBans'] == 0:
            embed.add_field(name = "Status:", value = 'No bans detected!', inline = False)
        else:
            #embed.add_field(name = "Banned?", value = 'Person is banned!', inline = False)
            embed.color =  discord.Color.from_rgb(255, 50, 50) #discord.Color.red()
            if ban_info['players'][0]['VACBanned'] == True:
              embed.add_field(name = "Vacs:", value = 'Vac On record', inline = False)
            else:
              embed.add_field(name = "Vacs:", value = 'None', inline = False)
            embed.add_field(name = "Gamebans:", value = (str(ban_info['players'][0]['NumberOfGameBans']) + " on record"), inline = False)
        embed.set_thumbnail(url=profile_picture)
        return embed    
        #await ctx.send(embed=embed)
    except Exception as E:
        print(E)
        await ctx.send("Error occurred, is the account ID valid?")
        
async def check_database():
    accounts = db["accounts"]
    #try:
    #    with open('steam_accounts.txt','r') as f:
    #        for i in f:
    #            ids = i.split(',')
    #            accounts.append(ids[0])
    #except Exception as E:
    #    print(E)
    counter = 0
    #print(accounts)
    for i in accounts:
        try:
            s= "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="+api_key+"&steamids="+str(i)
            ban_info = requests.get(s).json()        
            if ban_info['players'][0]['VACBanned'] == False and ban_info['players'][0]['NumberOfGameBans'] == 0:
                #pass
                print(str(i) + " is not banned")
            else:
                s= "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key="+api_key+"&steamids="+str(i)
                summary = requests.get(s).json()        
                name = summary['response']['players']['player'][0]['personaname']
                profile_picture = summary['response']['players']['player'][0]['avatarfull']       
                embed = discord.Embed(
                    title = 'Account Found',     
                    descriptoin = "",
                    colour = discord.Color.from_rgb(255, 50, 50)
                    )
                embed.add_field(name = "Name:", value=name, inline = False)    
                if ban_info['players'][0]['VACBanned'] == True:
                  embed.add_field(name = "Vacs:", value = 'Vac On record', inline = False)
                else:
                  embed.add_field(name = "Vacs:", value = 'None', inline = False)
                embed.add_field(name = "Gamebans:", value = (str(ban_info['players'][0]['NumberOfGameBans']) + " on record"), inline = False)
                embed.set_thumbnail(url=profile_picture)                
                #await ctx.send(embed=embed)
                accounts.pop(counter)   
                db["accounts"] = accounts             
                #database = open('steam_accounts.txt','w')
                #for i in accounts:
                #    database.write(str(i))
                #    database.write(",\n")
                #database.close()
                return embed
                break
                #await ctx.send("Account removed from database!")
        except Exception as E:
            print(E)            
        counter += 1
    #print("database cheked")
    return int(len(accounts))
    
async def add_account(ctx, steam_id):
    accounts = db["accounts"]
    if steam_id in accounts:
        await ctx.send("Account already in database!")
        return
    #try:
    #    with open('steam_accounts.txt','r') as f:
    #        for i in f:
    #            ids = i.split(',')
    #            accounts.append(ids[0])
    #    if steam_id in accounts:
    #        await ctx.send("Account already in database!")
    #except Exception as E:
    #    print(E)
    
    try:
        s= "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key="+api_key+"&steamids="+str(steam_id)
        summary = requests.get(s).json()        
        name = summary['response']['players']['player'][0]['personaname']
        profile_picture = summary['response']['players']['player'][0]['avatarfull']        
        s= "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key="+api_key+"&steamids="+str(steam_id)
        ban_info = requests.get(s).json()        
        embed = discord.Embed(
            title = 'Account Found',     
            descriptoin = "",
            colour = discord.Colour.blue()
            )
        embed.add_field(name = "Name:", value=name, inline = False)
        embed.set_thumbnail(url=profile_picture)
        should_add_player = False
        if ban_info['players'][0]['VACBanned'] == False and ban_info['players'][0]['NumberOfGameBans'] == 0:
            embed.add_field(name = "Banned?", value = 'Not Banned!', inline = False)
            should_add_player = True
        else:
            embed.add_field(name = "Banned?", value = 'Acc is banned!', inline = False)
        await ctx.send(embed=embed)
        if should_add_player == True:
            accounts.append(steam_id)
            db["accounts"] = accounts
            #database = open('steam_accounts.txt','w')
            #for i in accounts:
            #    database.write(str(i))
            #    database.write(",\n")
            #database.close()
            await ctx.send("Account has been added!")
        else:
            await ctx.send("Account is banned and was not added!")            
    except Exception as E:
        print(E)
        await ctx.send("Error occurred, is the account ID valid?")
        
async def print_database(ctx):
    accounts = db["accounts"]
    #try:
    #    with open('steam_accounts.txt','r') as f:
    #        for i in f:
    #            ids = i.split(',')
    #            accounts.append(ids[0])
    #except Exception as E:
    #    print(E)
    #    await ctx.send("Error occurred while reading database...")
    try:
        s = "The current database includes these id's: \n"
        for i in accounts:
            s+= "> " + i + ", \n"
        await ctx.send(s)
    except:
        await ctx.send("Error occurred while making string...")
        
async def remove_account(ctx, id):
    accounts = db["accounts"]
    try:
      found_acc = False
      index = -1
      for i in range(len(accounts)):
          if accounts[i] == id and found_acc == False:
              index = i
              found_acc = True
      if found_acc:
          accounts.pop(index)
          db["accounts"] = accounts
          await ctx.send("Account ID removed!")
      else:
          await ctx.send("Unable to find account ID in database...")
    except:
        await ctx.send("Error occurred while removing id...")
      
