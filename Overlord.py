# imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# main server, and list of channles
#discord_server = discord.Client()

# Countries and teams in the game (names of servers)
team_list = ['usa','egypt'] # list of potential channels to send messages to
team_dict = dict()
server_name = "ggtest" # change this to the name of the server you want this bot to work in

# Creating the bot client
command_prefix = '-'
bot_description = "Overlord Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

###################################################################################################

# This is what happens everytime the bot launches. In this case, it prints information like server
# count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone
# trusted.
@client.event
async def on_ready():
	print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' +
		  str(len(client.servers)) + ' servers | Connected to ' +
		  str(len(set(client.get_all_members()))) + ' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
		  platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.
		  format(client.user.id))
	print('--------')
	#server_list = discord_server.server_list
	servers = client.servers
	for server in servers:
		print("##########")
		print(server)
		if server.name == server_name:
			#print(server.members)
			for member in server.members:
				print(member.name)
			#print(server.channels)
			for channel in server.channels:
				channel_name = channel.name.lower()
				print(channel_name)
				if channel_name in team_list:
					pass
					team_dict[channel_name] = channel
	print("Team dict:")
	print(team_dict)
	print("##########")

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):
	""" Just a ping command for the Overlord """
	pinguser = "User"
	print("User " + pinguser + " is pinging the Overlord.")
	await client.say(":ping_pong: Pong!")
	#await asyncio.sleep(3)

@client.command()
async def echo(*, message: str):
	""" Has the Overlord echo a string """
	#await print(message)
	print('Echoing: "', message + '"')
	await client.say(message)

#async def msg(*, input_message: str):
#async def msg(ctx, *, input_message: str):
#async def msg(ctx, team_to: str, input_message: str):
#async def msg(team_to: str, input_message: discord.message):
#async def msg(ctx, team_to: str, input_message: str):
@client.command(pass_context=True)
async def msg(ctx, *, input_message: str):
	""" Sends a message to another team's private channel """

	to_i = input_message.find(' ')
	to = input_message[0:to_i].title()

	#to_msg = input_message[to_i+1:].strip()

	#print(to_msg)

	#team_to = "Egypt"

	#print(type(input_message))
	print('Input message:', input_message)

	#to = team_to
	#fro = "PLACEHOLDER"
	fro = ctx.message.channel.name
	fro = fro.title()

	if to.lower() == 'usa':
		to = to.upper()
	if fro.lower() == 'usa':
		fro = fro.upper()

	print("To: " + to)
	print("From: " + fro)
	print("to_i: " + str(to_i))
	print('Input message: ' + input_message)

	#print(type(ctx))
	#print("Message sent from channel:", fro)

	#Error Checking
	if to_i < 1:
		not_valid_msg_format = 'Not a valid message. The correct format is "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	if to.lower() not in team_list:
		not_team_error_msg = '"' + to + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	if to == fro:
		#print("ERROR")
		#print("To:", to)
		#print("From:", fro)
		same_team_error_msg = "You don't need me to send a message to yourself."
		await client.say(same_team_error_msg)
		return

	message = input_message[to_i+1:].strip()
	#message = input_message
	##message = ' '.join(message.split())

	#print(input_message)
	#print(to)
	#print(message)
	#print("Team", fro, 'sending message:', '\n"' + message + '"', '\nto team', to + '.')
	print("Team", fro, 'sending message:', '"' + message + '"', 'to team', to + '.')

	#await client.send_message(discord.Object(id='12324234183172'), 'message')

	send_msg = 'Incoming message from team ' + fro + ':\n"' + message + '".'
	#print("Sent message:", send_msg)

	await client.send_message(team_dict[to.lower()], send_msg)

	#await client.say(message)

	confirmation_message = 'Message "' + message + '" sent to team ' + to + '.'
	await client.say(confirmation_message)

# Get key info
login_path = "local/botkey"
login_file = open(login_path, 'r')
login_lines = login_file.readlines()
login_lines = [line.replace('\n','') for line in login_lines]
botkey = login_lines[0]
client.run(botkey)

"""

@client.command(pass_context=True)
async def hey(ctx, value):
	if value == "you":
		await client.say("What's cooking?") 
	else:
		pass
Something like that
If it's with multiple spaces, you could use .join or ctx.message.content etc
Just a tip- the ctx.message.content returns the content of the message including the command and prefix
So strip that or index that off

"""