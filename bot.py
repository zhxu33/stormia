import discord
from sql import *
token = "PLACEHOLDER"
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
                        await message.channel.send(f"Successfully added {memberId} to the list!")
                        return
                    else:  
                        await message.channel.send(f"{memberId} is already on the list!")  
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
                        await message.channel.send(f"Successfully removed {memberId} from the list!")
                        return
                    else:  
                        await message.channel.send(f"{memberId} is not on the list!")
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
                s = status(memberId)
                await message.channel.send(s)
        elif (messageList[1] == "status" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s = status(memberId)
            await message.channel.send(s)
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
                s = add(memberId, int(messageList[3]))
                await message.channel.send(s)
        elif (messageList[1] == "add" and len(messageList) == 3):
            memberId = "<@"+str(message.author.id)+">"
            s = add(memberId, int(messageList[2]))
            await message.channel.send(s)
        elif (messageList[1] == "list" and len(messageList) == 2):
            s = list()
            await message.channel.send(s) 
        elif (messageList[1] == "resume" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s = resume(memberId)
            await message.channel.send(s)
        elif (messageList[1] == "pause" and len(messageList) == 2):
            memberId = "<@"+str(message.author.id)+">"
            s = pause(memberId)
            await message.channel.send(s)
        elif (messageList[1] == "reset" and len(messageList) == 2):
            s = reset()
            await message.channel.send(s)

client.run(token)

