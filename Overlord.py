# imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Countries and teams in the game (names of servers)
# List of potential channels to sent messages to and from
#country_teams = ['usa', 'china', 'russia', 'united-kingdom', 'france', 'india', 'brazil', 
#				 'japan', 'iran', 'south-africa', 'australia', 'egypt']
country_teams = ['usa', 'china', 'russia', 'uk', 'france', 'india', 'brazil', 
				 'japan', 'iran', 'south-africa', 'australia', 'egypt']				 
#media_teams = ['global-news-network', 'badger-news-corp']
media_teams = ['gnn', 'bnc']
un_teams = ['un', 'wtp', 'unhcr']
void_channel = ['void']
human_team_list = country_teams + media_teams + un_teams
#print(human_team_list)
# the above lists might not be needed

team_comms_list = []
#team_list = ['usa', 'egypt', 'united-kingdom', 'global-news-network', 'bnc', 'south-africa']
team_comms_dict = dict()
#server_name = "ggtest" # change this to the name of the server you want this bot to work in
control_list = []
control_dict = dict()
category_list = []
category_dict = dict()
public_list = ['role-assignment', 'announcements', 'pre-game-chatter', 'press-releases',
			   'global-chat', 'general']
public_dict = dict()
other_list = []
other_dict = dict()
server_name = "Watch The Skies"

# Creating the bot client
command_prefix = '/' # this is the prefix used in front of each command
bot_description = "Sky Watcher Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

###################################################################################################

# This is what loads when the bot starts up
@client.event
async def on_ready():
	""" Loading up everything on start """
	print("##############################")
	print('Initializing...')
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
	
	update_teams()
	print("Team channel list and dictionary initialized.")
	#print(team_comms_dict)
	print("##############################")

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
	Use format: "/msg DESTINATION MESSAGE", with '-' in place of spaces in the DESTINATION
	(spaces are fine to use in the MESSAGE portion of this command)
	"""

	# Parse out the name of the destination country from the message
	to_i = input_message.find(' ')
	to_unfmt = input_message[0:to_i]
	to_original = to_unfmt # original message for error msgs
	if '-comms' in to_unfmt: # stripping off '-comms' if they included it in the command
		to_unfmt = to_unfmt[:to_unfmt.rfind('-comms')]
	to_key = to_unfmt # For accessing the team channel dictionary
	to = to_unfmt.title()
	message = input_message[to_i+1:].strip() # stripping off the remainder for the msg

	# Getting the country's name from which 
	fro_original = ctx.message.channel.name
	fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro = fro.title()

	# Specific country name checks:
	# USA
	if to.lower() in ['usa','united-states','united-states-of-america','america']:
		to = to.upper()
	if fro.lower() == 'usa':
		fro = fro.upper()
	# UK
	if to.lower() in ['uk', 'united-kingdom']:
		to = 'uk'.upper()
		to_key = to.lower()
	if fro.lower() in ['uk', 'united-kingdom']:
		fro = 'uk'.upper()
	# South Africa
	if to.lower() == 'sa':
		to = 'South-Africa'
		to_key = to.lower()
	# Global News Network
	if to.lower() in ['gnn', 'global-news-network', 'global-news', 'global-news-corp']:
		to_unfmt = 'gnn'
		to = 'Global-News-Network'
		to_key = 'gnn'
	# Badger News Corp
	if to.lower() in ['bnc', 'badger', 'badger-news-network', 'badger-news-corp', 'badger-news']:
		to_unfmt = 'bnc'
		to = 'Badger-News-Corp'
		to_key = 'bnc'
	# United Nations
	if to.lower() in ['un', 'united-nations']:
		to_unfmt = 'un'
		to = 'United-Nations'
		to_key = 'un'
	# More UN comms? <======================================================================
	# Add more of these as necessary

	# Diagnostic messages
	#print('Input message:', input_message)
	#print("To: " + to)
	#print("From: " + fro)
	#print("to_i: " + str(to_i))
	#print('Input message: ' + input_message)

	#Error Checking
	if (fro_i < 1) or (fro.lower() not in team_comms_list): # not in correct channel
		#print(fro_i)
		#print(fro.lower())
		#print(team_comms_list)
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		await client.say(invalid_channel_error_msg)
		return
	if to_i < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	if to_key.lower() not in team_comms_list: # trying to send to invalid team
		not_team_error_msg = '"' + to_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	if to_key == fro: # trying to send a message to oneself
		same_team_error_msg = 'Use "' + command_prefix + 'echo" instead to send a message to the'
		same_team_error_msg += ' same channel.'
		await client.say(same_team_error_msg)
		return

	# Send the message to its destination
	send_msg = 'Incoming message from ' + fro + ':\n"' + message + '".'
	await client.send_message(team_comms_dict[to_key.lower()], send_msg)

	# Logging message for game controllers
	print(fro + ' sending message: ' + '"' + message + '"' + ' to ' + to + '.')

	# Confirmation message for the team sending the message
	if to.lower() == 'void': # special case for the void'
		confirmation_message = 'Message "' + message + '" sent to the ' + to + '.'
	else:
		confirmation_message = 'Message "' + message + '" sent to ' + to + '.'
	await client.say(confirmation_message)


def update_teams(verbose=True):
	""" Helper function to update the team lists and dicts. Called during initialization and 
	potentially elsewhere.
	"""
	# We'll get a list of all servers, then we'll look for the desired server ('server_name', 
	# above), then we'll create a dictionary of channels (if the name matches any in the 
	# 'human_team_list' list above)
	servers = client.servers
	for server in servers:
		#print(server.name)
		if server.name == server_name:
			for channel in server.channels:
				channel_name = channel.name.lower()
				# find all channels with '-comms' in the name, and populate the team list,
				# along with populating the team_comms_dict
				team_name_i = channel_name.rfind('-comms') # find all channels with '-comms' in
				team_name = channel_name[:team_name_i]
				# Setting up control team lists
				control_i = channel_name.rfind('-control')
				control_name = channel_name[:control_i]

				if control_i > 1: # if this exists, we add it to the control list and dict
					control_list.append(control_name)
					control_dict[control_name] = channel
				elif channel_name == 'development': # special case for the dev channel
					control_list.append(channel_name)
					control_dict[channel_name] = channel
				elif team_name_i > 1: # if this exists, add it to the list and the channel to the dict
					team_comms_list.append(team_name)
					team_comms_dict[team_name] = channel
				elif channel_name == 'void': # special case for void channel
					team_comms_list.append(channel_name)
					team_comms_dict[channel_name] = channel
				elif channel.type == 4: # catching all the categories
					category_list.append(channel_name)
					category_dict[channel_name] = channel
				elif channel_name in public_list: # checking if it belongs in the public group
					public_dict[channel_name] = channel
				else:
					if verbose:
						print('Not in any other category so added to public:', channel_name)
					#print(channel.type)
					#print(type(channel.type))
					other_list.append(channel_name)
					other_dict[channel_name] = channel
					#print('Not a "-comms" channel:', channel_name)
				#if team_name in human_team_list:
				#	team_comms_dict[team_name] = channel

				
				
	#print("team_comms_list:", team_comms_list)
	#print("team_comms_dict:", team_comms_dict)
	#print("team_comms_list then _dict lens", len(team_comms_list), len(team_comms_dict))
	#print("control_list:", control_list)
	#print("control_dict:", control_dict)
	#print("control_list then _dict lens", len(control_list), len(control_dict))
	#print("public_list:", public_list)
	#print("public_dict:", public_dict)
	#print("public_list then _dict lens", len(public_list), len(public_dict))
	#print("category_list:", category_list)
	#print("category_dict:", category_dict)
	#print("category_list then _dict lens", len(category_list), len(category_dict))
	#print("other_list:", other_list)
	#print("other_dict:", other_dict)
	#print("other_list then _dict lens", len(other_list), len(other_dict))
	

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

DONE

2) Team to Controller Channel - Being able to get something posted from a private team channel to hidden controller channel

3) Press Release - Being able to publish information into a group Public Release Channel

4) Public Information Blast - Information that gets automated into all channels.

5) Time-keeping - Phase/turn information that get's automated to all channels.


Those were the main things we were aiming to do.
Basically 2 diffrent functions, but deployed in 5 ways.

"""

"""

To do:
1) change msg destination to the -comms channels
2) void messaging (same as regular msg?)
3) press release
4) all comms blast
5) time-keeping
6) dynamically adding new teams

"""