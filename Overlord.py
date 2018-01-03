# imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Countries and teams in the game (names of servers)
# List of potential channels to sent messages to and from
country_teams = ['usa', 'china', 'russia', 'united-kingdom', 'france', 'india', 'brazil', 
				 'japan', 'iran', 'south-africa', 'australia', 'egypt']
media_teams = ['global-news-network', 'badger-news-corp']
other_human_teams = ['united-nations']
void_channel = ['void']
team_list = country_teams + media_teams + other_human_teams
print(team_list)
#team_list = ['usa', 'egypt', 'united-kingdom', 'global-news-network', 'bnc', 'south-africa']
team_dict = dict()
#server_name = "ggtest" # change this to the name of the server you want this bot to work in
server_name = "Watch The Skies"

# Creating the bot client
command_prefix = '-' # this is the prefix used in front of each command
bot_description = "Sky Watcher Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

###################################################################################################

# This is what loads when the bot starts up
@client.event
async def on_ready():
	""" Loading up everything on start """
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
	
	# We'll get a list of all servers, then we'll look for the desired server ('server_name', 
	# above), then we'll create a dictionary of channels (if the name matches any in the 
	# 'team_list' list above)
	servers = client.servers
	for server in servers:
		#print(server.name)
		if server.name == server_name:
			for channel in server.channels:
				channel_name = channel.name.lower()
				if channel_name in team_list:
					team_dict[channel_name] = channel
	print("Team channel dictionary initialized.")
	#print(team_dict)
	print("##########")

# Basic ping command
@client.command()
async def ping(*args):
	""" A ping command for the Sky Watcher """
	pinguser = "User"
	print("User " + pinguser + " is pinging the Sky Watcher.")
	await client.say(":ping_pong: Pong!")
	#await asyncio.sleep(3)

# To have the Sky Watcher echo something into the same channel it was commanded in
@client.command()
async def echo(*, message: str):
	""" Has the Sky Watcher echo a string 
	Use format: "-echo MESSAGE"
	"""
	#await print(message)
	print('Echoing: "', message + '"')
	await client.say(message)

# Messaging function to send a message from one team (channel) to another
@client.command(pass_context=True)
async def msg(ctx, *, input_message: str):
	""" Sends a message to another (valid) team's private channel.
	Use format: "-msg TEAM-NAME MESSAGE", with '-' in place of spaces in the TEAM-NAME
	(spaces are fine to use in the MESSAGE portion of this command)
	"""

	# Parse out the name of the destination country from the message
	to_i = input_message.find(' ')
	to_unfmt = input_message[0:to_i]
	original_to = to_unfmt
	to = to_unfmt.title()
	to_key = to # For accessing the team channel dictionary
	message = input_message[to_i+1:].strip()

	original_to = to

	# Getting the country's name from which 
	fro = ctx.message.channel.name
	fro = fro.title()

	# Specific country name checks:
	# USA
	if to.lower() == 'usa':
		to = to.upper()
	if fro.lower() == 'usa':
		fro = fro.upper()
	# UK
	if to.lower() == 'uk':
		to = 'United-Kingdom'
		to_key = to.lower()
	if fro.lower() == 'uk':
		fro = 'United-Kingdom'
	# South Africa
	if to.lower() == 'sa':
		to = 'South-Africa'
		to_key = to.lower()
	# Global News Network
	if to.lower() in ['gnn', 'global-news-network']:
		to_unfmt = 'global-news-network'
		to = 'Global-News-Network'
		to_key = 'global-news-network'
	# Badger News Corp
	if to.lower() in ['bnc','badger', 'badger-news-network', 'badger-news-corp']:
		to_unfmt = 'badger-news-corp'
		to = 'Badger-News-Corp'
		to_key = 'badger-news-corp'
	# United Nations
	if to.lower() in ['un', 'united-nations']:
		to_unfmt = 'united-nations'
		to = 'United-Nations'
		to_key = 'united-nations'
	# Add more of these as necessary

	# Diagnostic messages
	#print('Input message:', input_message)
	#print("To: " + to)
	#print("From: " + fro)
	#print("to_i: " + str(to_i))
	#print('Input message: ' + input_message)

	#Error Checking
	if fro.lower() not in team_list:
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		await client.say(invalid_channel_error_msg)
		return
	if to_i < 1:
		not_valid_msg_format = 'Not a valid message. The correct format is: "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	if to_key.lower() not in team_list:
		not_team_error_msg = '"' + original_to + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	if to_key == fro:
		same_team_error_msg = 'Use "' + command_prefix + 'echo" instead to send a message to the'
		same_team_error_msg += ' same channel.'
		await client.say(same_team_error_msg)
		return

	# Send the message to its destination
	send_msg = 'Incoming message from team ' + fro + ':\n"' + message + '".'
	await client.send_message(team_dict[to_key.lower()], send_msg)

	# Logging message for game controllers
	print("Team", fro, 'sending message:', '"' + message + '"', 'to ', to + '.')

	# Confirmation message for the team sending the message
	confirmation_message = 'Message "' + message + '" sent to ' + to + '.'
	await client.say(confirmation_message)

# Get key info
login_path = "local/botkey"
login_file = open(login_path, 'r')
login_lines = login_file.readlines()
login_lines = [line.replace('\n', '') for line in login_lines]
botkey = login_lines[0]
client.run(botkey)

"""

1) Team to Team comms - Being able to get something posted from a private team channel to another private team channel

1.5) Void msging

2) Team to Controller Channel - Being able to get something posted from a private team channel to hidden controller channel

3) Press Release - Being able to publish information into a group Public Release Channel

4) Public Information Blast - Information that gets automated into all channels.

5) Time-keeping - Phase/turn information that get's automated to all channels.


Those were the main things we were aiming to do.
Basically 2 diffrent functions, but deployed in 5 ways.

"""