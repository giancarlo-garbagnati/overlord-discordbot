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
voice_dict = dict()
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

# Phase stuff
current_phase_i = 0
game_phases = [	'Pre-Pre-Game',
				'Pre-Game Briefing',
				'Spring 2020 - Initial Preparation',
				'Spring 2020 - Operations Phase (15 minutes)',
				'Spring 2020 - Check-in Phase (10 minutes)',
				'Spring 2020 - Free Phase (15 minutes)',
				'Summer 2020 - Operations Phase (15 minutes)',
				'Summer 2020 - Check-in Phase (10 minutes)',
				'Summer 2020 - Free Phase (15 minutes)',
				'Fall 2020 - Operations Phase (15 minutes)',
				'Fall 2020 - Check-in Phase (10 minutes)',
				'Fall 2020 - Free Phase (15 minutes)',
				'Winter 2020 - Operations Phase (15 minutes)',
				'Winter 2020 - Check-in Phase (10 minutes)',
				'Winter 2020 - Free Phase (15 minutes)',
				'Spring 2021 - Operations Phase (15 minutes)',
				'Spring 2021 - Check-in Phase (10 minutes)',
				'Spring 2021 - Free Phase (15 minutes)',
				'Summer 2021 - Operations Phase (15 minutes)',
				'Summer 2021 - Check-in Phase (10 minutes)',
				'Summer 2021 - Free Phase (15 minutes)',
				'Fall 2021 - Operations Phase (15 minutes)',
				'Fall 2021 - Check-in Phase (10 minutes)',
				'Fall 2021 - Free Phase (15 minutes)',
				'Winter 2021 - Operations Phase (15 minutes)',
				'Winter 2021 - Check-in Phase (10 minutes)',
				'Winter 2021 - Free Phase (15 minutes)',
				'Spring 2022 - Operations Phase (15 minutes)',
				'Spring 2022 - Check-in Phase (10 minutes)',
				'Spring 2022 - Free Phase (15 minutes)',
				'Summer 2022 - Operations Phase (15 minutes)',
				'Summer 2022 - Check-in Phase (10 minutes)',
				'Summer 2022 - Free Phase (15 minutes)',
				'Fall 2022 - Operations Phase (15 minutes)',
				'Fall 2022 - Check-in Phase (10 minutes)',
				'Fall 2022 - Free Phase (15 minutes)',
				'Winter 2022 - Operations Phase (15 minutes)',
				'Winter 2022 - Check-in Phase (10 minutes)',
				'Winter 2022 - Free Phase (15 minutes)',
				'Spring 2023 - Operations Phase (15 minutes)',
				'Spring 2023 - Check-in Phase (10 minutes)',
				'Spring 2023 - Free Phase (15 minutes)',
				'Summer 2023 - Operations Phase (15 minutes)',
				'Summer 2023 - Check-in Phase (10 minutes)',
				'Summer 2023 - Free Phase (15 minutes)',
				'Fall 2023 - Operations Phase (15 minutes)',
				'Fall 2023 - Check-in Phase (10 minutes)',
				'Fall 2023 - Free Phase (15 minutes)',
				'Winter 2023 - Operations Phase (15 minutes)',
				'Winter 2023 - Check-in Phase (10 minutes)',
				'Winter 2023 - Free Phase (15 minutes)',
				'Game End and Debrief']
# Game phase change prepend str
game_phase_change = "-----GAME PHASE CHANGE-----\n"
game_start_str = "--------GAME START--------\n"

# Nations and flag emoji
teamkeys = [	'usa',
				'un',
				'uk',
				'russia',
				'india',
				'france',
				'egypt',
				'china',
				'brazil',
				'australia',
				'south-africa',
				'iran',
				'japan',
				'gnn',
				'bnc'
				'wfp'
				'unhcr']
teamemoji = [	':flag_us:',
				'<:FlagUN:398385909705211906>',
				':flag_gb:',
				':flag_ru:',
				':flag_in:',
				':flag_fr:',
				':flag_eg:',
				':flag_cn:',
				':flag_br:',
				':flag_au:',
				':flag_za:',
				':flag_ir:',
				':flag_jp:',
				'<:LogoGNN:398385987719397377>',
				'<:LogoBadgerNews:398385891434954753>',
				'<:FlagUN:398385909705211906>',
				'<:FlagUN:398385909705211906>']
teamemoji_cu = [	':FlagUS:',
					':FlagUN:',
					':FlagUK:',
					':FlagRussia:',
					':FlagIndia:',
					':FlagFrance:',
					':FlagEgypt:',
					':FlagChina:',
					':FlagBrazil:',
					':FlagAustralia:',
					':flag_za:',
					':flag_ir:',
					':flag_jp:',
					':LogoGNN:',
					':LogoBadgerNews:',
					'<:FlagUN:398385909705211906>',
					'<:FlagUN:398385909705211906>']
# Create the flag_emoji_dict
flag_emoji_dict = dict()
for i in range(len(teamkeys)):
	flag_emoji_dict[teamkeys[i]] = teamemoji[i]

# Creating the bot client
command_prefix = '/' # this is the prefix used in front of each command
bot_description = "Sky Watcher Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

# Dev stuff
testing = True
disable_msg = True
disable_pr = False

timekeeper_role = 'game control'

# Greeting message for when a new user joins the server
greeting_msg = """Hi {0.mention}! Welcome to the game server for Watch the Skies - Sacramento! """
greeting_msg += """Please tell us what team are you on, and what role will you be playing so we """ 
greeting_msg += """can give you access to your play area."""

###################################################################################################
# Events
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
	
	update_teams(verbose=False)
	print("Team channel list and dictionary initialized.")
	#print(team_comms_dict)
	print('--------')
	
	print("Checking emoji...")
	emojis, notset = check_flag_emoji()
	print(notset)
	# To see all the emoji in Discord
	#await client.send_message(dev_dict['dev-announcements'], emojis)

	# This will show all custom emoji with it's respective code in the terminal
	#for emoji in client.get_all_emojis():
	#	print(emoji)

	print("##############################")

	"""
	for key, channel in all_dict.items():
		print('key:', key)
		print('channel:', channel.name)
		if "Voice Chat".lower() in channel.name.lower():
			print('VOICE CHANNEL --- channel type:', channel.type)
			print('VOICE CHANNEL --- channel type typeof:', type(channel.type))
			print('VOICE CHANNEL --- channel type = "voice"', channel.type == 'voice')
			print('VOICE CHANNEL --- discord.ChannelType.voice', channel.type == discord.ChannelType.voice)
	"""

	#await client.send_message(dev_dict['dev-announcements'], dev_dict['dev-announcements'].mention)
	#await client.send_message('')


# Greeting message upon user joining
@client.event
async def on_member_join(member):
	""" On member join function
	"""
	server = member.server
	await client.send_message(public_dict['role-assignment'], greeting_msg.format(member))
	print("Member {} joined the server.".format(member))




###################################################################################################
# Basic commands (not WtS specific)
###################################################################################################

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

###################################################################################################
# Player Commands
###################################################################################################

# Messaging function to send a message from one team (channel) to another
@client.command(pass_context=True)
async def msg(ctx, *, input_message: str):
	""" Sends a message to another (valid) team's private channel.
	Use format: "/msg [DESTINATION] [MESSAGE]", with '-' in place of spaces in the [DESTINATION]
	(spaces are fine to use in the [MESSAGE] portion of this command)
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

	if testing:
		if disable_msg:
			if (fro_key.lower() not in ['dev','dev2']) or (to_key.lower() not in ['dev','dev2']):
				return
	
	# Diagnostic messages
	"""
	print('Input message:', input_message)
	print("To: " + to)
	print("From: " + fro)
	print("to_i: " + str(to_i))
	print('Input message: ' + input_message)
	"""

	# Error Checking
	if (fro_i < 1) or (fro_key.lower() not in team_comms_list): # not in correct channel
		#print(fro_i)
		#print(fro.lower())
		#print(team_comms_list)
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		await client.say(invalid_channel_error_msg)
		return
	if to_i < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg [DESTINATION] [MESSAGE]".'
		await client.say(not_valid_msg_format)
		return
	if to_key.lower() not in team_comms_list: # trying to send to invalid team
		not_team_error_msg = '"' + to_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	if to_key.lower() == fro_key.lower(): # trying to send a message to oneself
		same_team_error_msg = 'Use "' + command_prefix + 'echo" instead to send a message to the'
		same_team_error_msg += ' same channel.'
		await client.say(same_team_error_msg)
		return

	# Send the message to its destination
	fro_emoji = get_emoji(fro_key)
	send_msg = 'Incoming message from {}{}:\n"{}".'.format(fro_emoji,fro,message)
	#send_msg = 'Incoming message from ' + fro + ':\n"' + message + '".'
	await client.send_message(team_comms_dict[to_key.lower()], send_msg)

	# Logging message for game controllers
	print(fro + ' sending message: ' + '"' + message + '"' + ' to ' + to + '.')

	# Confirmation message for the team sending the message
	if to.lower() == 'void': # special case for the void'
		confirmation_message = 'Message successfully sent to the ' + to + '.'
	else:
		confirmation_message = 'Message successfully sent to ' + to + '.'
	await client.say(confirmation_message)


# Command for a team to publish a press release
@client.command(pass_context=True)
async def press_release(ctx, *, input_message: str):
	""" Publishes a press release to the press-releases channel under the team's name.
	Can only be published by someone with a @Head of State role tag or
	@Secretary-General of the United Nations tag. Command format:
	/press_release
	"""

	# Get sender's channel/team name
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

	if testing:
		if disable_pr:
			if (fro_key.lower() not in ['dev','dev2']) or (to_key.lower() not in ['dev','dev2']):
				return

	# Error Checking
	if (fro_i < 1) or (fro_key.lower() not in team_comms_list): # not in correct channel
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		await client.say(invalid_channel_error_msg)
		return
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'press_release [MESSAGE]".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is a head-of-state. This command can only be used by heads-of-state
	not_headofstate = False
	if 'head of state'.lower() not in [role.name.lower() for role in user.roles]:
		sec_gen_role = 'secretary-general of the united nations'
		if sec_gen_role.lower() not in [role.name.lower() for role in user.roles]:
			not_headofstate = True
		else:
			not_headofstate = False
	if not_headofstate:
		not_headofstate_error = 'Only Heads-of-State or UN Secretary Generals can use this '
		not_headofstate_error += 'command in their respective -comms channel. All others '
		not_headofstate_error += 'must go through news or with a Press conference.'
		await client.say(not_headofstate_error)
		return

	# Send the message to its destination
	fro_emoji = get_emoji(fro_key)
	send_msg = 'Official press release from {}{}'.format(fro_emoji,fro.upper())
	send_msg += ':\n"{}".'.format(input_message)
	pr_channel = public_dict['press-releases'].mention
	pr_announcement = 'New press release from {}{}! ({})'.format(fro_emoji,fro.upper(),pr_channel)
	if testing:
		await client.send_message(dev_dict['dev-press-releases'], send_msg)
		for key, channel in dev_dict.items():
			if channel.name != 'dev-press-releases':
				await client.send_message(channel, pr_announcement)
	else:
		await client.send_message(public_dict['press-releases'], send_msg)
		for key, channel in team_comms_dict.items():
			await client.send_message(channel, pr_announcement)

	# Logging message for game controllers
	log_message = 'Head-of-State (' + user.name + ') from ' + fro + ' is publishing the '
	log_message += 'following press release: "{}".'.format(input_message)
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'Press release published successfully.'
	await client.say(confirmation_message)


###################################################################################################
# Game Controller Commands
###################################################################################################

# Command for control to be able to blast a message to all channels
@client.command(pass_context=True)
async def blast(ctx, *, input_message: str):
	""" Publishes a message to all channels (sends the message as is)
	Can only be published by someone with an @announcer role tag.
	Format: /blast [MESSAGE]
	"""
	
	# The role tag that's allowed to use this command
	blast_role = 'announcer'

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'blast [MESSAGE]".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is has a @announcer role tag
	if blast_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_announcer_error = 'Only an @Announcer can use this command.'
				await client.say(not_announcer_error)
				return
		else:
			not_announcer_error = 'Only an @Announcer can use this command.'
			await client.say(not_announcer_error)
			return
	
	# Send the message to its destination
	send_msg = input_message
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
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
	confirmation_message = 'Blast message sent successfully.'
	await client.say(confirmation_message)


# Command for control to send a PSA to all channels (differs from the blast command as it'll prepend 
# the message with a 'PSA'-like string)
@client.command(pass_context=True)
async def psa(ctx, *, input_message: str):
	""" Publishes a PSA to all channels (sends the message prepended with a 'PSA'-like announcement)
	Can only be published by someone with an @announcer role tag. Command format: /psa [MESSAGE]
	"""
	
	# PSA announcement
	PSA_str = 'PUBLIC SERVICE ANNOUNCEMENT:\n'

	# The role tag that's allowed to use this command
	blast_role = 'announcer'

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg COUNTRY MESSAGE".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is has a @announcer role tag
	if blast_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_announcer_error = 'Only an @announcer can use this command.'
				await client.say(not_announcer_error)
				return
		else:
			if user.name.lower() != 'pandiculate':
				not_announcer_error = 'Only an @announcer can use this command.'
				await client.say(not_announcer_error)
				return
			'''
			not_announcer_error = 'Only an @announcer can use this command.'
			await client.say(not_announcer_error)
			return
			'''

	
	# Send the message to its destination
	send_msg = PSA_str + input_message
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		#print(len(all_dict.keys()))
		#i = 0
		for key, value in all_dict.items():
			#print(key, value)
			#await client.send_message(dev_dict['dev-spam'], str(i))
			#i += 1
			await client.send_message(value, send_msg)
		#return
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The following PSA is being sent to all channels by user ' + user.name + ': "'
	log_message += input_message + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'PSA sent successfully.'
	await client.say(confirmation_message)


"""
Command: "/an" | User:: @Game Control
Function: Post in the announcment channel
Secondary Function: Post in all Comm's channals message: `New global announcement! (#announcements)
(edited)
...and then the same secondary function on the press release option that posts to comms channals New Press Release from [Country Flag]
"""
# Command for control to be able to post a message to the Announcements channel, and send a message
# to all other -comms channels to check announcements
@client.command(pass_context=True)
async def an(ctx, *, input_message: str):
	""" Publishes a message to the announcements channel, and send a message to all other -comms
	channels to check the announcements channel
	Can only be published by someone with an @announcer role tag
	"""
	
	# The role tag that's allowed to use this command
	an_role = 'announcer'
	an_key = 'announcements'
	an_channel = public_dict[an_key]
	#announcement_announcement = "New global announcement! (#announcements)"
	announcement_announcement = "New global announcement! ({})".format(an_channel.mention)

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	if len(input_message.strip()) < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'an [MESSAGE]".'
		await client.say(not_valid_msg_format)
		return
	# Check if the user is has a @announcer role tag
	if an_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_announcer_error = 'Only an @Announcer can use this command.'
				await client.say(not_announcer_error)
				return
		else:
			not_announcer_error = 'Only an @Announcer can use this command.'
			await client.say(not_announcer_error)
			return
	
	# Send the message to its destination
	send_msg = input_message
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		await client.send_message(dev_dict['dev-announcements'], send_msg)
		for key, value in dev_dict.items():
			if '-comms' in key:
				await client.send_message(value, announcement_announcement)
	else: # otherwise everyone gets the message
		await client.send_message(an_channel, send_msg)
		for key, value in team_comms_dict.items():
			await client.send_message(value, announcement_announcement)

	# Logging message for game controllers
	log_message = 'The following announcement has been sent to the announcements channel by user '
	log_message += '{}: "{}".'.format(user.name, input_message)
	print(log_message)

	# Confirmation message for the team sending the message
	confirmation_message = 'Announcement sent successfully.'
	await client.say(confirmation_message)


# Messaging command for control to send a message fake messages to one team while faking the
# source team
@client.command(pass_context=True)
async def fakemsg(ctx, *, input_message: str):
	""" Sends a message to another (valid) team's private channel, faking the source as a
	different team. Can only be sent by anyone with a @Game Control or @Covert Control tag
	Use format: "/msg [SENDER] [DESTINATION] [MESSAGE]", with '-' in place of spaces in the 
	[SENDER] or [DESTINATION] (spaces are fine to use in the MESSAGE portion of this command)
	"""

	# Roles that have permission to use this command
	role_permissions = ['game control', 'covert control']

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Let's parse out all the parts of the command
	#try:
	sender_i = input_message.find(' ')
	sender_original = input_message[:sender_i].strip()
	message = input_message[sender_i+1:].strip()

	destination_i = message.find(' ')
	destination_original = message[:destination_i].strip()
	message = message[destination_i+1:].strip()

	# dev stuff
	"""
	print(input_message)
	print('sender_original:', sender_original)
	print('sender_i:', sender_i)
	print('destination_original:', destination_original)
	print('destintion_i:', destination_i)
	print('message:', message)
	#message_list = input_message.split()
	"""
	#except:

	# Let's clean up sender and destination
	sender = sender_original
	destination = destination_original
	# First we strip off '-comms' if it's included
	if '-comms' in sender:
		sender = sender[:sender.rfind('-comms')]
	if '-comms' in destination:
		destination = destination[:destination.rfind('-comms')]
	# Now let's disambig the team names
	sender, sender_key = name_disambig(sender)
	destination, destination_key = name_disambig(destination)

	"""
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
	"""
	
	# Diagnostic messages
	"""
	print('Input message:', input_message)
	print("To: " + to)
	print("From: " + fro)
	print("to_i: " + str(to_i))
	print('Input message: ' + input_message)
	"""

	# Error Checking
	# Check if the user of this commands has one of the correct roles
	correct_role = False
	for permission in role_permissions:
		if permission in [role.name.lower() for role in user.roles]:
			correct_role = True
	if not correct_role:
		if testing:
			if user.name.lower() != 'pandiculate':
				incorrect_role_error = 'You do not have permission to use this command.'
				await client.say(incorrect_role_error)
				return
		else:
			incorrect_role_error = 'You do not have permission to use this command.'
			await client.say(incorrect_role_error)
			return
	if (sender_i < 0) or (destination_i < 0): # incorrect command format
		not_valid_fakemsg_format = "Not a valid `{}fakemsg` format. ".format(command_prefix)
		not_valid_fakemsg_format += 'The correct format for this command is:'
		not_valid_fakemsg_format += '```{}fakemsg '.format(command_prefix)
		not_valid_fakemsg_format += '[SENDER] [DESTINATION] [MESSAGE]```'
		await client.say(not_valid_fakemsg_format)
		return
	# trying to send to or from invalid team
	if sender_key.lower() not in team_comms_list:
		not_team_error_msg = '"' + sender_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	if destination_key.lower() not in team_comms_list:
		not_team_error_msg = '"' + destination_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return

	# Send the message to its destination
	sender_emoji = get_emoji(sender_key)
	send_msg = 'Incoming message from {}{}:\n"{}".'.format(sender_emoji,sender,message)
	await client.send_message(team_comms_dict[destination_key.lower()], send_msg)

	# Logging message for game controllers
	log_msg = 'Fake message sent from {} to {}: "{}".'.format(sender, destination, message)
	print(log_msg)

	# Confirmation message for the team sending the message
	confirmation_message = 'Fake message sent from {} '.format(sender)
	if destination.lower() == 'void': # special case for the void'
		confirmation_message += 'to the {}: "{}"'.format(destination, message)
	else:
		confirmation_message += 'to {}: "{}"'.format(destination, message)
	await client.say(confirmation_message)


# Command for control to publish press_releases under other teams name
@client.command(pass_context=True)
async def fakepress_release(ctx, *, input_message: str):
	""" Publishes a fake press release to the press-releases channel under a specific team's name.
	This is scoped only to certain control members (@Game Control and @Covert Control). Command
	format is: /fakepress_release [SENDER] [MESSAGE]
	"""

	# Roles that have permission to use this command
	role_permissions = ['game control', 'covert control']

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Let's parse out all the parts of the command
	#try:
	sender_i = input_message.find(' ')
	sender_original = input_message[:sender_i].strip()
	message = input_message[sender_i+1:].strip()

	# Let's clean up sender and destination
	sender = sender_original
	# First we strip off '-comms' if it's included
	if '-comms' in sender:
		sender = sender[:sender.rfind('-comms')]
	# Now let's disambig the team name
	sender, sender_key = name_disambig(sender)

	# Error Checking
	# Check if the user of this commands has one of the correct roles
	correct_role = False
	for permission in role_permissions:
		if permission in [role.name.lower() for role in user.roles]:
			correct_role = True
	if not correct_role:
		if testing:
			if user.name.lower() != 'pandiculate':
				incorrect_role_error = 'You do not have permission to use this command.'
				await client.say(incorrect_role_error)
				return
		else:
			incorrect_role_error = 'You do not have permission to use this command.'
			await client.say(incorrect_role_error)
			return
	if sender_i < 0: # incorrect command format
		not_valid_fakemsg_format = 'Not a valid `{}fakepress_release`'.format(command_prefix)
		not_valid_fakemsg_format += ' format. The correct format for this command is:'
		not_valid_fakemsg_format += '```{}fakepress_release '.format(command_prefix)
		not_valid_fakemsg_format += '[SENDER] [MESSAGE]```'
		await client.say(not_valid_fakemsg_format)
		return
	# trying to send to or from invalid team
	if sender_key.lower() not in team_comms_list:
		not_team_error_msg = '"' + sender_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return

	# Post the press-release to the #press-releases channel
	sender_emoji = get_emoji(sender_key)
	send_msg = 'Official press release from {}{}'.format(sender_emoji,sender.upper())
	send_msg += ':\n"{}".'.format(message)
	pr_channel = public_dict['press-releases'].mention
	pr_announcement = 'New press release from '
	pr_announcement += '{}{}! ({})'.format(sender_emoji,sender.upper(),pr_channel)
	if testing:
		await client.send_message(dev_dict['dev-press-releases'], send_msg)
		for key, channel in dev_dict.items():
			if (channel.name != 'dev-press-releases') and ('-comms' in channel.name):
				await client.send_message(channel, pr_announcement)
	else:
		await client.send_message(public_dict['press-releases'], send_msg)
		for key, channel in team_comms_dict.items():
			await client.send_message(channel, pr_announcement)

	# Logging message for game controllers
	log_msg = 'Fake press release sent from {}: "{}".'.format(sender, message)
	print(log_msg)

	# Confirmation message for the team sending the message
	confirmation_message = 'Fake press release sent from {}: '.format(sender)
	confirmation_message += '"{}"'.format(message)
	await client.say(confirmation_message)


# Command to manually refresh the team comms list/dict
@client.command()
async def update_team_comms(*args):
	""" Command that refreshed the team comms list/dev
	Usable by anyone
	"""

	update_teams()
	print('Team comms updated.')



###################################################################################################
# Phase Commmands (also only game control commands)
###################################################################################################

# Command for the @Game Control to be able to make the game's phase clock move to the next phase
@client.command(pass_context=True)
async def next_phase(ctx):
	""" Command to let the @Game Control move the game's phase clock forward one phase
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Dev stuff
	"""
	print('current_phase_i:', current_phase_i)
	print('new phase:', current_phase_i+1)
	print('max game phases:', len(game_phases)-1)
	"""

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return
	if current_phase_i+1 >= len(game_phases):
		last_phase_error = 'No more phases to cycle through. Use `{}'.format(command_prefix)
		last_phase_error += 'reset_phase` to set the game back to the first phase.\n'
		last_phase_error += 'Alternatively, you can use `{}set_phase '.format(command_prefix)
		last_phase_error += 'PHASENUMBER` to set the phase to a specific phase, `'
		last_phase_error += '{}last_phase` or `{}'.format(command_prefix, command_prefix)
		last_phase_error += 'prev_phase` to get to the previous phase, or `'
		last_phase_error += '{}list_phase` to get a list of all the'.format(command_prefix)
		last_phase_error += ' phases.'
		await client.say(last_phase_error)
		return

	# Move the phase 1 up ahead
	change_current_phase(1)

	# Get the current phase
	current_phase = game_phases[current_phase_i]
	if current_phase_i == 1:
		send_msg = game_start_str + current_phase
	else:
		send_msg = game_phase_change + current_phase

	# Send the message to its destination
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			if key == 'dev-commandtesting':
				await client.send_message(value, send_msg)
			#await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The game has been moved to the next phase by user ' + user.name + '. Phase: "'
	log_message += current_phase + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	#confirmation_message = 'Game moved to phase: "{}".'.format(current_phase)
	#await client.say(confirmation_message)


# Command for the @Game Control to be able to set the game's phase clock to a certain phase number
@client.command(pass_context=True)
async def set_phase(ctx, x: int):
	""" Command to let the @Game Control set the game phase
	Uses the indices of the game_phrases list
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return
	if (x >= len(game_phases)) or (x < 0): # if the phase # chosen is out of range
		outofrange_error = 'The phase number chosen is out of range. Must be greater or equal '
		outofrange_error += 'to 0 and less than {}. You can use the '.format(len(game_phases))
		outofrange_error += '/list_phase command to see all the phases.'
		await client.say(outofrange_error)
		return


	# Set the phase
	set_current_phase(x)

	# Get the new phase
	current_phase = game_phases[current_phase_i]
	if current_phase_i == 0:
		send_msg = game_start_str + current_phase
	else:
		send_msg = game_phase_change + current_phase

	# Send the message to its destination
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			if key == 'dev-commandtesting':
				await client.send_message(value, send_msg)
			#await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The game has been set by user ' + user.name + ' to phase: "'
	log_message += current_phase + '".'
	print(log_message)


# Command for the @Game Control to be able to make the game's phase clock back to the previous
# phase
@client.command(pass_context=True)
async def prev_phase(ctx):
	""" Command to let the @Game Control move the game's phase clock back one phase
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return
	if current_phase_i <= 0:
		first_phase_error = 'No more phases to reverse through. Use `{}'.format(command_prefix)
		first_phase_error += 'next_phase` to go forward one phase.\nAlternatively, you can use '
		first_phase_error += '`{}set_phase PHASENUMBER` to set the phase'.format(command_prefix)
		first_phase_error += ' to a specific phase or `{}list_phase` to '.format(command_prefix)
		first_phase_error += 'get a list of all the phases.'
		await client.say(first_phase_error)
		return

	# Move the phase 1 back
	change_current_phase(-1)

	# Get the new phase
	current_phase = game_phases[current_phase_i]
	if current_phase_i == 0:
		send_msg = game_start_str + current_phase
	else:
		send_msg = game_phase_change + current_phase

	# Send the message to its destination
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			if key == 'dev-commandtesting':
				await client.send_message(value, send_msg)
			#await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The game has been moved to the previous phase by user ' + user.name
	log_message += '. Phase: "' + current_phase + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	#confirmation_message = 'Game moved to phase: "{}".'.format(current_phase)
	#await client.say(confirmation_message)


# Command for the @Game Control to be able to make the game's phase clock back to the previous 
# phase
@client.command(pass_context=True)
async def last_phase(ctx):
	""" Command to let the @Game Control move the game's phase clock back one phase
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return
	if current_phase_i <= 0:
		first_phase_error = 'No more phases to reverse through. Use `{}'.format(command_prefix)
		first_phase_error += 'next_phase` to go forward one phase.\nAlternatively, you can use '
		first_phase_error += '`{}set_phase PHASENUMBER` to set the phase '.format(command_prefix)
		first_phase_error += 'to a specific phase or `{}list_phase` to '.format(command_prefix)
		first_phase_error += 'get a list of all the phases.'
		await client.say(first_phase_error)
		return

	# Move the phase 1 back
	change_current_phase(-1)

	# Get the new phase
	current_phase = game_phases[current_phase_i]
	if current_phase_i == 0:
		send_msg = game_start_str + current_phase
	else:
		send_msg = game_phase_change + current_phase

	# Send the message to its destination
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			if key == 'dev-commandtesting':
				await client.send_message(value, send_msg)
			#await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The game has been moved to the previous phase by user ' + user.name
	log_message += '. Phase: "' + current_phase + '".'
	print(log_message)

	# Confirmation message for the team sending the message
	#confirmation_message = 'Game moved to phase: "{}".'.format(current_phase)
	#await client.say(confirmation_message)

# Command for the @Game Control to be able to reset the game's phase clock to the beginning
@client.command(pass_context=True)
async def reset_phase(ctx):
	""" Command to let the @Game Control reset the game phase to the first phase
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return

	# Set the phase
	set_current_phase(0)

	# Get the current phase
	send_msg = 'Game phase have been reset'

	# Send the message to the channel the command was called from
	await client.say(send_msg)

	# Logging message for game controllers
	log_message = 'The game has been reset to the first phase by user ' + user.name + '."'
	print(log_message)


# Command for the @Game Control to be able to set the game's phase clock to the end phase
@client.command(pass_context=True)
async def end_phase(ctx):
	""" Command to let the @Game Control set the game phase clock to the end phase
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return

	# Set the phase
	set_current_phase(len(game_phases)-1)

	# Get the current phase
	current_phase = game_phases[current_phase_i]
	if current_phase_i == 0:
		send_msg = game_start_str + current_phase
	else:
		send_msg = game_phase_change + current_phase

	# Send the message to its destination
	
	if testing: # if this is True, we'll restrict this command to just message dev channels
		for key, value in dev_dict.items():
			if key == 'dev-commandtesting':
				await client.send_message(value, send_msg)
			#await client.send_message(value, send_msg)
	else: # otherwise everyone gets the message
		for key, value in all_dict.items():
			await client.send_message(value, send_msg)
	#await client.send_message(public_dict['press-releases'], send_msg)

	# Logging message for game controllers
	log_message = 'The game has been set to the last phase by user ' + user.name + '."'
	print(log_message)

# Command for the @Game Control to display the current phase in the channel the command was used in
@client.command(pass_context=True)
async def what_phase(ctx):
	""" Command to let the @Game Control get a reminder what phase the game is in.
	This will get seen only in the channel the @Game Controller used it in
	"""

	# Calling global variables
	#global current_phase_i

	# The role tag that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return

	# Get the current phase
	current_phase = game_phases[current_phase_i]

	# Send the message to the channel it was used in
	send_msg = 'We are in phase: "{}".'.format(current_phase)
	await client.say(send_msg)

# Command for @Game Control to display a list of all the phase in the game, with the index used to
# access it.
@client.command(pass_context=True)
async def list_phase(ctx):
	""" Command for the @Game Controller to be able to get displayed a list of all the game phases
	with the index needed to access it
	"""

	# The role that's allowed to use this command
	control_role = timekeeper_role

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Error Checking
	# Check if the user is has a @Game Control role tag
	if control_role not in [role.name.lower() for role in user.roles]:
		if testing:
			if user.name.lower() != 'pandiculate':
				not_gamecontrol_error = 'Only a @Game Control can use this command.'
				await client.say(not_gamecontrol_error)
				return
		else:
			not_gamecontrol_error = 'Only a @Game Control can use this command.'
			await client.say(not_gamecontrol_error)
			return
	
	# Get the current phase
	current_phase = game_phases[current_phase_i]

	# Build the phase list output
	send_msg = "```"
	for i, phase in enumerate(game_phases):
		if current_phase_i == i:
			phase_str = '{} - {} <---- we are here\n'.format(i, phase)
		else:
			phase_str = '{} - {}\n'.format(i, phase)
		send_msg += phase_str
	send_msg += "```"

	# Send the message to the channel the command was used in
	await client.say(send_msg)


# Helper functions for changing the current_phase_i iterator
def change_current_phase(x):
	""" Function for incrementing or decrementing the current_phase_i by x
	"""
	global current_phase_i
	current_phase_i += x
def set_current_phase(x):
	""" Function for setting the current_phase_i to x
	"""
	global current_phase_i
	current_phase_i = x




###################################################################################################
# Helper Functions
###################################################################################################


# Function for helping sort out different possible team names
def name_disambig(team_name):
	""" Helper function for helping sort through ambiguous team names.
	Returns tuple of 2 str: a 'proper' team name, and a key to access channels in the various 
	dictionaries
	"""
	
	# If nothing else, it'll return itself twice (assuming the name and key are the same and 
	# correct)
	name = team_name.replace('_','-').title()
	key = team_name.replace('_','-').lower()

	# Specific country name checks:
	# USA
	if name.lower() in ['usa', 'united-states', 'united-states-of-america', 'america', "'murica", 
						'murica']:
		name = 'USA'
		key = name.lower()
	# UK
	elif name.lower() in ['uk', 'united-kingdom', 'england', 'gb', 'great-britain']:
		name = 'UK'
		key = name.lower()
	# South Africa
	elif name.lower() == 'sa':
		name = 'South-Africa'
		key = name.lower()
	# Global News Network
	elif name.lower() in ['gnn', 'global-news-network', 'global-news', 'global-news-corp']:
		name = 'Global-News-Network'
		key = 'gnn'
	# Badger News Corp
	elif name.lower() in ['bnc', 'badger', 'badger-news-network', 'badger-news-corp', 
						  'badger-news']:
		name = 'Badger-News-Corp'
		key = 'bnc'
	# United Nations
	elif name.lower() in ['un', 'united-nations']:
		name = 'United-Nations'
		key = 'un'
	elif name.lower() in ['unhcr', 'un-high-commission-on-refugees',
						  'un-high-commission-of-refugees']:
		name = 'UNHCR'
		key = name.lower()
	elif name.lower() in ['wfp', 'world-food-program']:
		name = 'WFP'
		key = name.lower()
	# Add more of these as necessary
	
	return name, key


def update_teams(verbose=False):
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
				if channel_name in ['development', 'dev-comms', 'dev2-comms', 
									'dev-commandtesting', 'dev-announcements',
									'dev-press-releases', 'dev-spam']:
					dev_list.append(channel_name)
					dev_dict[channel_name] = channel
				if channel.type == 4: # catching all the categories
					category_list.append(channel_name)
					category_dict[channel_name] = channel
				elif channel.type == discord.ChannelType.voice: # catching all voice channels
					voice_dict[channel_name] = channel
				elif channel_name == 'pre-game-planning':
					pass
				else: # all other channels will be added to the all list and dict
					all_list.append(channel_name)
					all_dict[channel_name] = channel
					if control_i > 1: # if this exists, we add it to the control list and dict
						control_list.append(control_name)
						control_dict[control_name] = channel
					 # if this exists, add it to the list and the channel to the dict
					elif team_name_i > 1:
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

# A helper function that goes through all flags and emoji, puts them in one string returns it, 
# and compares it to all in the -comms list/dict and sends a string of all items in the
# -comms list/dict that aren't in the flag dict
def check_flag_emoji():
	""" Helper function to check all flag emoji in the flag emoji dict.
	Returns a string of all the flag emoji with it's key, and also returns a string
	of all the elements in the -comms list/dict that aren't in the flag dict
	"""

	# Create a string of all the flag emoji with its key
	emoji_str = ''
	for key, value in flag_emoji_dict.items():
		emoji_str += '{} {}\n'.format(value, key)

	# Create a string of all items in the -comms list/dict that aren't in the flag dict
	not_in_set = "These -comms channels don't have a respective emoji:\n"
	for comm_key in team_comms_dict.keys():
		if comm_key not in flag_emoji_dict.keys():
			not_in_set += '{}, '.format(comm_key)
	not_in_set = not_in_set[:-2]

	return emoji_str, not_in_set
			
	
# A helper function to retrieve the emoji string given a key string
def get_emoji(key):
	""" A helper function to retrieve the emoji string given a key string, if it doesn't exist
	in the dict, returns a blank string
	"""
	#print(key)
	#print(flag_emoji_dict.keys())
	if key in flag_emoji_dict.keys():
		return flag_emoji_dict[key]
	else:
		return ''

	
###################################################################################################
# Other
###################################################################################################


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

4) Public Information Blast - Information that gets automated into all channels.

6) Greeting message

DONE

2) Team to Controller Channel - Being able to get something posted from a private team channel to hidden controller channel

5) Time-keeping - Phase/turn information that get's automated to all channels.


Those were the main things we were aiming to do.
Basically 2 diffrent functions, but deployed in 5 ways.

"""

"""

To do:
1.5) Fix UN -comms msg
1.55) Write-up google docs documentation
1.7) fakemsg
2) team to controller channel
2.5) controller to team channel
3) time-keeping
4) dynamically adding new teams
5)
5.5) change things to use the flag emoji
6) look into using @ tags

Done (but testing):
1) all comms blast
1.1) blast
1.2) psa
1.3) test with @announcer tag
2) Phases Commands



"""