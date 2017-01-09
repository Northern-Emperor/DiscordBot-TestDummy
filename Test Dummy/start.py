#This is where the code imports the modules it needs
import discord
import asyncio
from sys import modules
#This makes the bot be able to connect to discord
client = discord.Client()
#This is where the channel lists will be stored
textChannels = []
voiceChannels = []
#This is where the bot token will be stored
token = ""
#This is where the Message object is stored
currentMsg = ''
#This is the character is the command prefix
prefix = '!'


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

@client.event
async def on_message(message):
    #This makes sure the message is in on of the bound channels
    if(message.channel.id in textChannels):
        #This cleans up the message and makes sure that it is a command
        command = message.content.strip().lower()
        if(command.startswith(prefix)):
            command = command.lstrip(prefix)
            global currentMsg
            currentMsg = message
            #This executes command if it exist or tells user the command doesn't exist
            await getattr(modules[__name__], 'cmd_%s' %command, commandNotFound())()
#This is called when a command doesn't exist
async def commandNotFound():
    print('Invalid command received')
    await client.send_message(currentChannel, 'Command was unable to be processed. Please check command and try again.')

#These are the all the commands that can be used

#This closes out the bot properly making it appear offline in the discord client
async def cmd_shutdown():
    print('Shutting Down')
    await client.send_message(currentMsg.channel, 'Shutting Down')
    await client.close()

#This has the bot count the number of messages between it and the user
async def cmd_test():
    print('Running Test...')
    counter = 0
    tmp = await client.send_message(currentMsg.channel, 'Calculating messages...')
    async for log in client.logs_from(currentMsg.channel, limit=100):
        if log.author == currentMsg.author:
            counter += 1
    await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    print('Test Complete')

#This makes the bot inactive for 5 seconds
async def cmd_sleep():
    print('Sleeping...')
    await client.send_message(currentMsg.channel, 'Sleeping')
    await asyncio.sleep(5)
    await client.send_message(currentMsg.channel, 'Done sleeping')
    print('Awake!')

async def cmd_speak

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