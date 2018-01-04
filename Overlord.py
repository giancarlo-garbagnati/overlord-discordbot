# imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random

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

#team_list = ['usa', 'egypt', 'united-kingdom', 'global-news-network', 'bnc', 'south-africa']
# There's probably a better way to do this...
team_comms_list = []
team_comms_dict = dict()
team_aar_list = []
team_aar_dict = dict()
team_disc_list = []
team_disc_dict = dict()
control_list = []
control_dict = dict()
category_list = []
category_dict = dict()
dev_list = []
dev_dict = dict()
all_list = []
all_dict = dict()
public_list = ['role-assignment', 'announcements', 'pre-game-chatter', 'press-releases',
			   'global-chat', 'general']
public_dict = dict()
other_list = []
other_dict = dict()
#server_name = "ggtest" # change this to the name of the server you want this bot to work in
server_name = "Watch The Skies"

# Creating the bot client
command_prefix = '/' # this is the prefix used in front of each command
bot_description = "Sky Watcher Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

# Greeting message for when a new user joins the server
greeting_msg = """Hi {0.mention}! Welcome to the game server for Watch the Skies - Sacramento! """
greeting_msg += """Please tell us what team are you on, and what role will you be playing so we """ 
greeting_msg += """can give you access to your play area."""

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


	#await client.send_message(team_comms_dict[to_key.lower()], send_msg)


# Greeting message upon user joining
@client.event
async def on_member_join(member):
	""" On member join function
	"""
	server = member.server
	#member_role = __getRole(server.roles, role)
	await client.send_message(public_dict['role-assignment'], greeting_msg.format(member))
	print("Member {} joined the server.".format(member))
	#await client.send_message(member, welcome_msg.format(member, server))
	#await client.send_message(client.get_channel(log_channel_id), "{0.name} has joined".format(member))


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


# Roll dice command (shamelessly adapted from Rapptz's basic_bot:
# https://github.com/Rapptz/discord.py/blob/async/examples/basic_bot.py)
@client.command()
async def roll(dice : str, mod : int = 0):
	"""Rolls a dice in NdN format."""
	try:
		rolls, limit = map(int, dice.split('d'))
	except Exception:
		await client.say('Format has to be in NdN!')
		return

	# Roll the dice, and sum them up
	roll_result = [random.randint(1, limit) for r in range(rolls)]
	result = ', '.join(str(roll_result))
	roll_sum = sum(roll_result)

	result_message = str(roll_result) + ' (sum = ' + str(roll_sum) + ')'

	if mod != 0:
		result_message += '\nWith modifer, sum = ' + str(roll_sum + mod)

	#result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
	await client.say(result_message)


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
	to, to_key = name_disambig(to_unfmt) # For accessing the team channel dictionary
	#to = to_unfmt.title()
	message = input_message[to_i+1:].strip() # stripping off the remainder for the msg

	# Getting the sending team's name 
	fro_original = ctx.message.channel.name
	fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro, fro_key = name_disambig(fro)
	
	# Diagnostic messages
	"""
	print('Input message:', input_message)
	print("To: " + to)
	print("From: " + fro)
	print("to_i: " + str(to_i))
	print('Input message: ' + input_message)
	"""

	#Error Checking
	if (fro_i < 1) or (fro_key.lower() not in team_comms_list): # not in correct channel
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
	if to_key == fro_key: # trying to send a message to oneself
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


# Command for a team to publish a press release
@client.command(pass_context=True)
async def press_release(ctx, *, input_message: str):
	""" Publishes a press release to the press-releases channel under the team's name.
	Can only be published by someone with a @Head of State role tag
	"""

	# Get sender's name
	fro_original = ctx.message.channel.name
	fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro, fro_key = name_disambig(fro)

	# Get the user info for the person who wrote this command
	user = ctx.message.author
	# https://stackoverflow.com/questions/44893044/how-to-get-users-roles-discord-python
	#user.roles
	#print(user)
	"""
	if 'head of state' in [role.name.lower() for role in user.roles]:
		await client.say("Hail to the Chief")
	else:
		await client.say("I don't have to listen to you")
	#print(user.roles)
	"""

	#input_message

	#Error Checking
	if (fro_i < 1) or (fro_key.lower() not in team_comms_list): # not in correct channel
		#print(fro_i)
		#print(fro.lower())
		#print(team_comms_list)
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		await client.say(invalid_channel_error_msg)
		return
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'press_release MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is a head-of-state. This command can only be used by heads-of-state
	if 'head of state' not in [role.name.lower() for role in user.roles]:
		not_headofstate_error = 'Only Heads-of-State can use this command in their respective '
		not_headofstate_error += '-comms channel. Non-Heads-of-State must go through news or '
		not_headofstate_error += 'with a Press conference.'
		await client.say(not_headofstate_error)
		return

	# Send the message to its destination
	send_msg = 'Official press release from ' + fro.upper() + ':\n"' + input_message + '".'
	await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'Head-of-State (' + user.name + ') from ' + fro + ' is publishing the following press release: "'
	log_message += input_message + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'Press release published successfully.'
	await client.say(confirmation_message)


# Command for control to be able to blast a message to all channels
@client.command(pass_context=True)
async def blast(ctx, *, input_message: str):
	""" Publishes a message to all channels (sends the message as is)
	Can only be published by someone with an @announcer role tag
	"""
	
	# The role tag that's allowed to use this command
	blast_role = 'announcer'

	# Get sender's name
	fro_original = ctx.message.channel.name
	fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro, fro_key = name_disambig(fro)

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	#Error Checking
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is has a @announcer role tag
	if blast_role not in [role.name.lower() for role in user.roles]:
		if user.name.lower() != 'pandiculate':
			not_announcer_error = 'Only an @Announcer can use this command.'
			await client.say(not_announcer_error)
			return
	
	# Send the message to its destination
	send_msg = input_message
	''' send to all channels here '''
	testing = True # if this is True, we'll restrict this command to just message dev channels
	if testing:
		for key, value in dev_dict.items():
			await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The following message is being blasted to all channels by user ' + user.name + ': "'
	log_message += input_message + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'Blast announcement sent successfully.'
	await client.say(confirmation_message)

# Command for control to send a PSA to all channels (differs from the blast command as it'll prepend 
# the message with a 'PSA'-like string)
@client.command(pass_context=True)
async def psa(ctx, *, input_message: str):
	""" Publishes a PSA to all channels (sends the message prepended with a 'PSA'-like announcement)
	Can only be published by someone with an @announcer role tag
	"""
	
	# PSA announcement
	PSA_str = 'PUBLIC SERVICE ANNOUNCEMENT:\n'
	PSA_str += input_message

	# We'll call blast to do the work
	blast(ctx, PSA_str)

	return

	# The role tag that's allowed to use this command
	blast_role = 'announcer'

	# Get sender's name
	fro_original = ctx.message.channel.name
	fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro, fro_key = name_disambig(fro)

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	#Error Checking
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is has a @announcer role tag
	if blast_role not in [role.name.lower() for role in user.roles]:
		if user.name.lower() != 'pandiculate':
			not_announcer_error = 'Only an @Announcer can use this command.'
			await client.say(not_announcer_error)
			return
	
	# Send the message to its destination
	send_msg = input_message
	''' send to all channels here '''
	testing = True # if this is True, we'll restrict this command to just message dev channels
	if testing:
		for key, value in dev_dict.items():
			await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The following message is being blasted to all channels by user ' + user.name + ': "'
	log_message += input_message + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'Blast announcement sent successfully.'
	await client.say(confirmation_message)

# Function for helping sort out different possible team names
def name_disambig(team_name):
	""" Helper function for helping sort through ambiguous team names.
	Returns tuple of 2 str: a 'proper' team name, and a key to access channels in the various dictionaries
	"""
	
	# If nothing else, it'll return itself twice (assuming the name and key are the same and correct)
	name = team_name.replace('_','-')
	key = team_name

	# Specific country name checks:
	# USA
	if name.lower() in ['usa', 'united-states', 'united-states-of-america', 'america', "'murica", 'murica']:
		name = 'USA'
		key = 'usa'
	# UK
	elif name.lower() in ['uk', 'united-kingdom', 'england']:
		name = 'UK'
		key = 'uk'
	# South Africa
	elif name.lower() == 'sa':
		name = 'South-Africa'
		key = name.lower()
	# Global News Network
	elif name.lower() in ['gnn', 'global-news-network', 'global-news', 'global-news-corp']:
		name = 'Global-News-Network'
		key = 'gnn'
	# Badger News Corp
	elif name.lower() in ['bnc', 'badger', 'badger-news-network', 'badger-news-corp', 'badger-news']:
		name = 'Badger-News-Corp'
		key = 'bnc'
	# United Nations
	elif name.lower() in ['un', 'united-nations']:
		name = 'United-Nations'
		key = 'un'
	# More UN comms? <======================================================================
	# Add more of these as necessary
	
	return name, key


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
				# Setting up team after action report (aar) list and dict
				team_aar_i = channel_name.rfind('-aar')
				team_aar = channel_name[:team_aar_i]
				# Setting up team discussion list and dict
				team_disc_i = channel_name.rfind('-discussion')
				team_disc = channel_name[:team_disc_i]
				
				# special case for the dev channels
				if channel_name in ['development', 'dev-comms', 'dev2-comms', 'dev-commandtesting']:
					dev_list.append(channel_name)
					dev_dict[channel_name] = channel
				if channel.type == 4: # catching all the categories
					category_list.append(channel_name)
					category_dict[channel_name] = channel
				else: # all other channels will be added to the all list and dict
					all_list.append(channel_name)
					all_dict[channel_name] = channel
					if control_i > 1: # if this exists, we add it to the control list and dict
						control_list.append(control_name)
						control_dict[control_name] = channel
					elif team_name_i > 1: # if this exists, add it to the list and the channel to the dict
						team_comms_list.append(team_name)
						team_comms_dict[team_name] = channel
					elif channel_name == 'void': # special case for void channel
						team_comms_list.append(channel_name)
						team_comms_dict[channel_name] = channel
					elif team_aar_i > 1: # if this exists, add it to the aar list and dict
						team_aar_list.append(team_aar)
						team_aar_dict[team_aar] = channel
					elif team_disc_i > 1: # if this exists, add it to the disc list and dict
						team_disc_list.append(team_disc)
						team_disc_dict[team_disc] = channel
					elif channel_name in public_list: # checking if it belongs in the public group
						public_dict[channel_name] = channel
					else:
						if verbose:
							print('Not in any other category so added to public:', channel_name)
						other_list.append(channel_name)
						other_dict[channel_name] = channel


				
	#Diagnostic Messages
	"""
	print("team_comms_list:", team_comms_list)
	print("team_comms_dict:", team_comms_dict)
	print("team_comms_list then _dict lens", len(team_comms_list), len(team_comms_dict))
	print("control_list:", control_list)
	print("control_dict:", control_dict)
	print("control_list then _dict lens", len(control_list), len(control_dict))
	print("public_list:", public_list)
	print("public_dict:", public_dict)
	print("public_list then _dict lens", len(public_list), len(public_dict))
	print("category_list:", category_list)
	print("category_dict:", category_dict)
	print("category_list then _dict lens", len(category_list), len(category_dict))
	print("other_list:", other_list)
	print("other_dict:", other_dict)
	print("other_list then _dict lens", len(other_list), len(other_dict))
	"""
	

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

3) Press Release - Being able to publish information into a group Public Release Channel

6) Greeting message

DONE

2) Team to Controller Channel - Being able to get something posted from a private team channel to hidden controller channel

4) Public Information Blast - Information that gets automated into all channels.

5) Time-keeping - Phase/turn information that get's automated to all channels.


Those were the main things we were aiming to do.
Basically 2 diffrent functions, but deployed in 5 ways.

"""

"""

To do:
1) all comms blast
1.1) blast
1.2) psa
1.3) ...?
1.5) Fix UN -comms msg
2) team to controller channel
2.5) controller to team channel
3) time-keeping
4) dynamically adding new teams
5) look into using @ tags

"""