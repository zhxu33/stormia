import discord
from data import *
from info import *
token = "MTA0MjI1NTgxNzY4NjEzNDgzNQ.GBwIvu.23ETc_CvpthGsw_NJ_fTztvZ4VMmN_dTmOVkcw"
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event 
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == client.user:
        return

    messageList = user_message.split()

    if (messageList[0] == "!dl" and len(messageList) > 1):

        if (messageList[1] == "insert" and len(messageList) == 3):

            if (message.mentions):
                s = str(message.mentions)
                i = s.index("name='")
                name = s[i+6:s.index("'", i+6)]
                i = s.index("discriminator='")
                discriminator = s[i+15:s.index("'", i+15)]
                userTag = name+'#'+discriminator
                i = s.index("id=")
                memberId = "<@"+s[i+3:s.index(" ", i+3)]+">"
                if (messageList[2] == memberId and len(messageList) == 3):
                    if (insert(memberId) == True):
                        s=discord.Embed(title="Insert", description=f"Successfully added {memberId} to the list!", color = 0x2ecc71)
                        s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                        await message.channel.send(embed=s)
                        return
                    else: 
                        s=discord.Embed(title="Insert", description=f"{memberId} is already on the list!", color = 0x2ecc71)
                        s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                        await message.channel.send(embed=s) 

        elif (messageList[1] == "drop" and len(messageList) == 3):
            if (message.mentions):
                s = str(message.mentions)
                i = s.index("name='")
                name = s[i+6:s.index("'", i+6)]
                i = s.index("discriminator='")
                discriminator = s[i+15:s.index("'", i+15)]
                userTag = name+'#'+discriminator
                i = s.index("id=")
                memberId = "<@"+s[i+3:s.index(" ", i+3)]+">"
                if (messageList[2] == memberId and len(messageList) == 3):
                    if (drop(memberId) == True):
                        s=discord.Embed(title="Drop", description=f"Successfully removed {memberId} from the list!", color = 0xe74c3c)
                        s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                        await message.channel.send(embed=s)
                        return
                    else:  
                        s=discord.Embed(title="Drop", description=f"{memberId} is not on the list!", color = 0xe74c3c)
                        s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                        await message.channel.send(embed=s)

        elif (messageList[1] == "status" and len(messageList) == 3):
            if (message.mentions):
                s = str(message.mentions)
                i = s.index("name='")
                name = s[i+6:s.index("'", i+6)]
                i = s.index("discriminator='")
                discriminator = s[i+15:s.index("'", i+15)]
                userTag = name+'#'+discriminator
                i = s.index("id=")
                memberId = "<@"+s[i+3:s.index(" ", i+3)]+">"
                s=discord.Embed(title="Status", description=status(memberId), color = 0x3498db)
                s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                await message.channel.send(embed = s)

        elif (messageList[1] == "status" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s=discord.Embed(title="Status", description=status(memberId), color = 0x3498db)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed = s)

        elif (messageList[1] == "add" and len(messageList) == 4):
            if (message.mentions):
                s = str(message.mentions)
                i = s.index("name='")
                name = s[i+6:s.index("'", i+6)]
                i = s.index("discriminator='")
                discriminator = s[i+15:s.index("'", i+15)]
                userTag = name+'#'+discriminator
                i = s.index("id=")
                memberId = "<@"+s[i+3:s.index(" ", i+3)]+">"
                s=discord.Embed(title="Add", description=add(memberId, int(messageList[3])), color = 0x2ecc71)
                s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
                await message.channel.send(embed = s)

        elif (messageList[1] == "add" and len(messageList) == 3):
            memberId = "<@"+str(message.author.id)+">"
            s=discord.Embed(title="Add", description=add(memberId, int(messageList[2])), color = 0x2ecc71)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed = s)

        elif (messageList[1] == "list" and len(messageList) == 2):
            s=discord.Embed(title="Report", description=list(), color = 0x3498db)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed=s) 

        elif (messageList[1] == "resume" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s=discord.Embed(title="Resume", description=resume(memberId), color = 0x2ecc71)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed = s)

        elif (messageList[1] == "pause" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s=discord.Embed(title="Pause", description=pause(memberId), color = 0xf1c40f)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed = s)

        elif (messageList[1] == "reset" and len(messageList) == 2):
            s=discord.Embed(title="Reset", description=reset(), color = 0x3498db)
            s.set_footer(text=str(message.author)+" | "+str(message.author.id), icon_url=message.author.avatar.url)
            await message.channel.send(embed = s)

client.run(token)

