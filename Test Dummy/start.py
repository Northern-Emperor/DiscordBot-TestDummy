#This is where the code imports the modules it needs
import discord
import asyncio
#This makes the bot be able to connect to discord
client = discord.Client()
#This is where the channel lists will be stored
textChannels = []
voiceChannels = []
#This is where the bot token will be stored
token = ""

#This function pulls data from the text files
def get(file, type):
    #This opens the file in read only
    f = open(file, 'r')
    #This checks if it is pulling a bot token or channel names
    #It reads and records whichever type properly
    if(type is 'token'):
        global token
        token = f.readline()
    elif(type is 'voice'):
        global voiceChannels
        voiceChannels = f.readline().split(";")
    elif(type is 'text'):
        global textChannels
        textChannels = f.readline().split(";")
        print(voiceChannels)
        
    #This closes the file *ALWAYS NEEDS TO BE DONE*
    f.close()

#This is called on first connection to Discord, but sometimes after
@client.event
async def on_ready():
    #Prints Bot info to the console.
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    if(textChannels):
        print('The bound text channels are:')
        for channel in textChannels:
            print(channel)
    if(voiceChannels):
        print('The bound voice channels are:')
        for channel in voiceChannels:
            print(channel)
    print('------')

#These are the commands directly to the bot
@client.event
async def on_message(message):
    if(message.channel.id in textChannels):
        #This has the bot count the number of messages between it and the user
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        #This makes the bot pretend to sleep
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')
        #This closes out the bot properly making it appear offline in the discord client
        elif message.content.startswith('!shutdown'):
            print('Shutting down')
            await client.close()
def main():
    #Get the token from Token.txt
    get('Token.txt', 'token')
    #Get the list of text channels from TextChannelList.txt
    get('TextChannelList.txt', 'text')
    #Get the list of voice channels from VoiceChannelList.txt
    get('VoiceChannelList.txt', 'voice')
    #Checks if token seems viable
    if(len(token) is 59):
        client.run(token)
    else:
        print("Unable to find bot credentials please put the bot's token into Token.txt")

#This tells the program to start at the function main()
if(__name__ == "__main__"):
    main()