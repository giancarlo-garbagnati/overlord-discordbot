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
game_phases = [	'Transition Phase',
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
				'bnc',
				'wfp',
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

# Agent choices list (len 28)
agent_choices = [
	' successful survival secret ',
	' successful secret survival ',
	' survival successful secret ',
	' survival secret successful ',
	' secret survival successful ',
	' secret successful survival '
]

# Creating the bot client
command_prefix = '/' # this is the prefix used in front of each command
bot_description = "Sky Watcher Bot for Watch The Skies"
client = Bot(description=bot_description, command_prefix=command_prefix, pm_help = True)

# Dev stuff
testing = True
testing = False
disable_msg = True
disable_pr = False
#dev_discord_name = 'Giancarlo-China-Chief of Staff'.lower()
dev_discord_name = 'pandiculate'.lower()

# Roles
timekeeper_role = 'game control'

# Open aliens comms group
open_alien = []

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
	
	update_teams(verbose=False, reset=False)
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

	#print(public_dict)
	#print(team_disc_dict)

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
	#await client.send_message(dev_dict['dev2-comms'], flag_emoji_dict['unhcr'])
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


# When a channel is created, we'll update team-comms if necessary
@client.event
async def on_channel_create(channel):
	""" When a channel is created, we want to check if it has '-comms'/'-aar'/'-discussion' 
	in it's name. If so, we update the team_comms_dict 
	"""
	#event.channel.send_message('Woah, check out this new channel!')
	#await client.send_message(channel, 'Woah, check out this new channel!')

	channels_to_update = [
		'-comms',
		'-discussion',
		'-aar'
	]

	for s in channels_to_update:
		if s in channel.name.lower():
			update_teams(reset=True)
			print('New channel created and added to dicts')
			break


# When a channel's name is changed, we'll check if team-comms needs to be reset
@client.event
async def on_channel_update(before, after):
	""" When a channel gets updates, we check to see if the name has been changed to (or from)
	something with a '-comms'/'-aar'/'-discussion' in it. If so, we update lists
	"""
	#await client.send_message(after, 'I sense a disturbance in the force...')

	channels_to_update = [
		'-comms',
		'-discussion',
		'-aar'
	]

	#print('Topic', after.topic)
	#print('type', type(after.topic))

	for s in channels_to_update:
		if (s in before.name.lower()) or (s in after.name.lower()):
			update_teams(reset=True)
			print('Teams channels have been updated.')
			
	
	




###################################################################################################
# Basic commands (not WtS specific)
###################################################################################################

# Basic ping command
@client.command()
async def ping(*args):
	""" A ping command for the Sky Watcher """
	pinguser = "User"
	print("User is pinging the Sky Watcher.")
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

	# Get the user info
	user = ctx.message.author

	# Player roles that a player must have to use this command
	permissions = [
		'diplomat',
		'head of state',
		'lead editor',
		'secretary-general of the united nations',
		'extraterrestrial organism'
	]

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
	from_control = False
	if '-control' in fro_original.lower():
		fro_i = fro_original.rfind('-control')
		from_control = True
	else:
		fro_i = fro_original.rfind('-comms')
	fro = fro_original[:fro_i]
	fro, fro_key = name_disambig(fro)

	# Check if it's coming from ETs
	et_role = 'Extraterrestrial Organism'.lower()
	alien_permissions = False
	alien_sender = False
	if et_role in [role.name.lower() for role in user.roles]:
		alien_sender = True
		if fro_key in open_alien:
			alien_permissions = True

	# Check if it's going to an ET team without permissions
	alien_destination_allowed = False
	alien_destination = False
	if to_key.lower() in team_comms_dict.keys():
		#print(":", team_comms_dict[to_key.lower()].topic, ":")
		#if type(team_comms_dict[to_key.lower()].topic) is not NoneType:
		if team_comms_dict[to_key.lower()].topic != None:
			#print('not NoneType')
			if 'alien' in team_comms_dict[to_key.lower()].topic.lower(): # destination is alien -comm
				alien_destination = True
				if to_key in open_alien:
					alien_destination_allowed = True

	if testing:
		if disable_msg:
			if (fro_key.lower() not in ['dev','dev2']) or (to_key.lower() not in ['dev','dev2']):
				#print("we're here")
				return
	
	# Diagnostic messages
	"""
	print('Input message:', input_message)
	print("To: " + to)
	print("From: " + fro)
	print("to_i: " + str(to_i))
	print('Input message: ' + input_message)
	"""

	#print(to_key)

	# Error Checking
	# Not in correct channel (or not from control)
	if (fro_i < 1) or (fro_key.lower() not in team_comms_list):
		if (not from_control) and ():
			#print(fro_i)
			#print(fro.lower())
			#print(team_comms_list)
			invalid_channel_error_msg = 'You cannot use this command in this channel.'
			invalid_channel_error_msg += ' Use this in your "-comms" channel.'
			await client.say(invalid_channel_error_msg)
			return
	# if the sender is an alien and trying to send from a team without /msg permissions
	if alien_sender and not alien_permissions:
		no_permissions_yet_msg = 'You are not able to use this command.'
		await client.say(no_permissions_yet_msg)
		return
	# Trying to send to an alien team that doesn't have -comms enabled
	if alien_destination and not alien_destination_allowed:
		alien_destination_not_allowed_msg = '"{}" not a valid team. Try again.'.format(to_original)
		await client.say(alien_destination_not_allowed_msg)
		return
	if to_i < 1: # missing a message
		not_valid_msg_format = 'Not a valid message. The correct format for this command is: "'
		not_valid_msg_format += command_prefix + 'msg [DESTINATION] [MESSAGE]".'
		await client.say(not_valid_msg_format)
		return
	# trying to send to invalid team
	if to_key.lower() not in team_comms_list:
		not_team_error_msg = '"' + to_original + '"' + ' not a valid team. Try again.'
		await client.say(not_team_error_msg)
		return
	# Not correct permissions
	correct_permission = False
	for permission in permissions:
		if permission in [role.name.lower() for role in user.roles]:
			correct_permission = True
			break
	if not correct_permission:
		incorrect_permission_msg = 'Only team leaders (@Head of State, @Lead Editor, '
		incorrect_permission_msg += '@Secretary-General of the United Nations) or those with a '
		incorrect_permission_msg += '@Diplomat tag can use this command.'
		await client.say(incorrect_permission_msg)
		return
	if to_key.lower() == fro_key.lower(): # trying to send a message to oneself
		same_team_error_msg = 'Use "' + command_prefix + 'echo" instead to send a message to the'
		same_team_error_msg += ' same channel.'
		await client.say(same_team_error_msg)
		return

	# Send the message to its destination
	if from_control:
		fro_emoji = '<:WTSblack:398402231432511500>'
		control_fro = fro.title() + '-control'
		send_msg = 'Incoming message from {}{}:\n"{}".'.format(fro_emoji,control_fro,message)
		await client.send_message(team_comms_dict[to_key.lower()], send_msg)
	else:
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
	@Secretary-General of the United Nations or @Lead Editor tag. Command format:
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
		invalid_channel_error_msg += ' Use this in your "-comms" channel.'
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
			lead_editor_role = 'lead editor'
			if lead_editor_role.lower() not in [role.name.lower() for role in user.roles]:
				not_headofstate = True
			else:
				not_headofstate = False
	if not_headofstate:
		not_headofstate_error = 'Only Heads-of-State, UN Secretary General, or Lead Editors can '
		not_headofstate_error += 'use this command in their respective -comms channel. All others '
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


# Command for players to request an agent action. They rank the agent success choices 
# (survival/success/secret) and a mission, and covert-control determines what actually happens
@client.command(pass_context=True)
async def agent(ctx, *, input_message: str):
	""" Command for players to request an agent action. They rank the agent success choices 
	(survival/success/secret) and a mission. The game does a roll, and sends the whole thing as
	a structured message to #covert-control, who then determines what happens. Command format:
	/agent [LOCATION/TARGET] [1ST SUCCESS CHOICE] [2ND SUCCESS CHOICE] [3RD SUCCESS CHOICE] [MISSION]
	"""

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	permissions = [
		'agent commander'
	]

	# Get the channel this was sent by
	sender_original = ctx.message.channel.name
	sender_i = sender_original.rfind('-comms')
	sender = sender_original[:sender_i]
	sender, sender_key = name_disambig(sender)

	# Let's parse out all the parts of the command
	choice_found = False
	multiple_choices_found = False
	choices_offset = len(agent_choices[0])
	message_lower_case = ' ' + input_message.lower()
	choices_start_i = len(message_lower_case)
	for choice in agent_choices: # look for the first instance of 
		if choice in message_lower_case:
			if choice_found: # if we've already found one <--- problem
				multiple_choices_found = True
			found_i = message_lower_case.find(choice)
			#print(found_i)
			if message_lower_case.find(choice) < choices_start_i:
				choices_start_i = message_lower_case.find(choice) - 1
			choice_found = True
	choices_end_i = choices_start_i + choices_offset # get the ending index

	# Get a string of all the choices, ranked, and parse each out
	choice_rank = input_message[choices_start_i:choices_end_i]
	choice_rank_list = choice_rank.split()
	choices_error = False
	if len(choice_rank_list) == 3:
		choice1 = choice_rank_list[0].title()
		choice2 = choice_rank_list[1].title()
		choice3 = choice_rank_list[2].title()
	else:
		#print(choice_rank_list)
		#print(choices_start_i)
		#print(input_message)
		choices_error = True

	# Parse the [LOCATION/TARGET] and [MISSION]
	target = input_message[:choices_start_i].strip()
	mission = input_message[choices_end_i:].strip()

	# Tries to see if the target is one that exists in the emoji list
	if ' ' not in target:
		target, target_key = name_disambig(target)
	else:
		target_key = ''

	# Error Checking
	correct_fmt_str = 'Correct format is: ```/agent [LOCATION/TARGET] ' 
	correct_fmt_str += '[1ST SUCCESS CHOICE] [2ND SUCCESS CHOICE] '
	correct_fmt_str += '[3RD SUCCESS CHOICE] [MISSION]```'
	# check permissions
	for permission in permissions:
		if permission not in [role.name.lower() for role in user.roles]:
			invalid_permissions = 'Only players with the @Agent Commander tag can use this '
			invalid_permissions += 'command. Confer with your team and team leader/s, then '
			invalid_permissions += 'ask @Game Control or @Covert Control for the tag.'
			await client.say(invalid_permissions)
			return
	if (sender_i < 1) or (sender_key.lower() not in team_comms_list): # not in correct channel
		invalid_channel_error_msg = 'You cannot use this command in this channel.'
		invalid_channel_error_msg += ' Use this in your "-comms" channel.'
		await client.say(invalid_channel_error_msg)
		return
	if multiple_choices_found: # the command's inputted parameters (for choice rank) was ambiguous
		ambiguous_choices_error_msg = 'Choice ranks were too ambiguous. Please '
		ambiguous_choices_error_msg += 'only include one set of [successful/survival/secret] '
		ambiguous_choices_error_msg += '(seperated by spaces) after the [LOCATION/TARGET] and '
		ambiguous_choices_error_msg += 'before the [MISSION].'
		await client.say(ambiguous_choices_error_msg)
		return
	if choices_error: # incorrect format (we're missing three choices)
		incorrect_command_fmt_error = 'Incorrect message format. '
		incorrect_command_fmt_error += correct_fmt_str
		await client.say(incorrect_command_fmt_error)
		return
	if len(target) < 1: # [LOCATION/DESTINATION] is missing
		target_missing_error_msg = 'Missing a [LOCATION/DESTINATION] in this command. '
		target_missing_error_msg += correct_fmt_str
		await client.say(target_missing_error_msg)
		return
	if len(mission) < 1: # [MISSION] is missing
		mission_missing_error_msg = 'Missing a [MISSION] in this command. '
		mission_missing_error_msg += correct_fmt_str
		await client.say(mission_missing_error_msg)
		return

	# Diagnostic messages
	"""
	print('target:', target)
	print('mission:', mission)
	print('choice1', choice1)
	print('choice2', choice2)
	print('choice3', choice3)
	"""

	# Let's get some of the variables for the final message
	sender_emoji = get_emoji(sender_key)
	target_emoji = get_emoji(target_key)

	# Let's do the rolls
	roll1 = random.randint(1, 6)
	roll2 = random.randint(1, 6)
	rollsum = roll1 + roll2

	# Let's build the output text sent to #covert-control
	agent_request_msg = '{}{} has requested an agent action\n'.format(sender_emoji, sender)
	agent_request_msg += '--------------------------------------------------\n'
	agent_request_msg += 'Target/Location: {}{}\n'.format(target_emoji, target)
	agent_request_msg += '--------------------------------------------------\n'
	agent_request_msg += 'Mission Details: {}\n'.format(mission)
	agent_request_msg += '--------------------------------------------------\n'
	agent_request_msg += 'Priority:        {} | {} | {}\n'.format(choice1, choice2, choice3)
	agent_request_msg += '--------------------------------------------------\n'
	agent_request_msg += 'Mission Roll:    {}, {} [{}]'.format(roll1, roll2, rollsum)

	# Send the message to its destination
	covert_channel = control_dict['covert']
	if testing:
		await client.send_message(dev_dict['dev-comms'], agent_request_msg)
		#await client.send_message(covert_channel, agent_request_msg)
	else:
		await client.send_message(covert_channel, agent_request_msg)

	# Logging message for game controllers
	print(agent_request_msg)

	# Confirmation message
	confirmation_msg = 'Agent action request has been sent to @Covert Control. Please '
	confirmation_msg += 'wait to hear back from them regarding the outcome.'
	await client.say(confirmation_msg)


###################################################################################################
# Team-To-Control Commmands (commands for teams to communicate with control)
###################################################################################################

# These commands are for players to communicate with the various control teams. They use
# /[CONTROL TEAM NAME] [MESSAGE] to contact the team and the message gets conveyed over to that
# team. Only team leaders (Heads of State, UN Secretary General, Lead Editor), @diplomats, and 
# aliens

@client.command(pass_context=True)
async def game(ctx, *, input_message: str):
	""" A command for communicating with the game control team (#game-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Game'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def npc(ctx, *, input_message: str):
	""" A command for communicating with the npc control team (#npc-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'NPC'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def covert(ctx, *, input_message: str):
	""" A command for communicating with the covert control team (#covert-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Covert'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def national(ctx, *, input_message: str):
	""" A command for communicating with the national control team (#national-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'National'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def globe(ctx, *, input_message: str):
	""" A command for communicating with the globe control team (#globe-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Globe'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def un(ctx, *, input_message: str):
	""" A command for communicating with the un control team (#un-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'UN'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def science(ctx, *, input_message: str):
	""" A command for communicating with the science control team (#science-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Science'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def media(ctx, *, input_message: str):
	""" A command for communicating with the media control team (#media-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Media'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)

@client.command(pass_context=True)
async def alien(ctx, *, input_message: str):
	""" A command for communicating with the alien control team (#alien-control)
	"""

	# Call ttc_get_sender_info() to get all the info
	user, sender_i, sender, sender_key, sender_emoji = ttc_get_sender_info(ctx)

	# Get the destination channel
	control_team = 'Alien'
	destination = control_dict[control_team.lower()]

	# Error Checking
	all_good, error_msg = ttc_error_check(user, sender_i, sender_key)
	if not all_good:
		await client.say(error_msg)
		return

	# Let's get the output
	ttc_msg = ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message)

	# Send the message to its destination
	if testing:
		await client.send_message(dev_dict['dev-spam'], ttc_msg)
	else:
		await client.send_message(destination, ttc_msg)

	# Logging message for game controllers
	print(ttc_msg)

	# Confirmation message
	confirmation_msg = 'Your message has been sent to {} Control.'.format(control_team)
	await client.say(confirmation_msg)


########## Helper functions for the ttc commands

# Helper function for the team-to-control commands to get all sender into
def ttc_get_sender_info(ctx):
	""" Helper function for the team-to-control commands to get all the sender info stuff.
	Returns user object, sender_i index, sender, sender_key, and a sender emoji (if exists)
	"""

	# Get the user info for the person who wrote this command
	user = ctx.message.author

	# Get the channel this was sent by
	sender_original = ctx.message.channel.name
	sender_i = sender_original.rfind('-comms')
	sender = sender_original[:sender_i]
	sender, sender_key = name_disambig(sender)

	# Get sender emoji
	sender_emoji = get_emoji(sender_key)

	return user, sender_i, sender, sender_key, sender_emoji

# Helper fxn for ttc commands to error check and return the message string
def ttc_error_check(user, sender_i, sender_key):
	""" Helper function for the ttc commands to error check.
	Returns True if everything is good (and a blank error message), otherwise returns False
	and returns an error message
	"""
	
	# List of roles with permission to use these commands
	permissions = [
		'head of state',
		'secretary-general of the united nations',
		'lead editor',
		'diplomat',
		'extraterrestrial organism'
	]

	# Error Checking
	if (sender_i < 1) or (sender_key.lower() not in team_comms_list): # not in correct channel
		# aliens can use this command in any channel
		if 'extraterrestrial organism' not in [role.name.lower() for role in user.roles]:
			invalid_channel_error_msg = 'You cannot use this command in this channel.'
			invalid_channel_error_msg += ' Use this in your "-comms" channel.'
			#await client.say(invalid_channel_error_msg)
			return False, invalid_channel_error_msg
	# Check if the user has the correct permission
	correct_permission = False
	for permission in permissions:
		if permission.lower() in [role.name.lower() for role in user.roles]:
			correct_permission = True
			break
	if not correct_permission:
		if (not testing) and (user.name.lower() != dev_discord_name):
			print(user.name.lower())
			not_headofstate_error = 'You do not have permissions to use this command. This '
			not_headofstate_error += 'command must be used by one with a team leader tag (ie '
			not_headofstate_error += '@Head of State, @Secretary General of the United Nations, '
			not_headofstate_error += 'or @Lead Editor) or someone with a @Diplomat tag.'
			return False, not_headofstate_error

	return True, ''

# Helper function for ttc commands for returning a string of the message to send to the respective
# control team
def ttc_return_msg(user, sender, sender_key, sender_emoji, control_team, input_message):
	""" Helper function for building the message that will be received by the control team
	"""

	# Get sender channel
	sender_channel = team_comms_dict[sender_key]

	# Let's build the output text sent to the control channel
	ttc_msg = '{} from {}{} '.format(user.mention, sender_emoji, sender)
	ttc_msg += '({}) has a message for {} Control:\n'.format(sender_channel.mention, control_team)
	ttc_msg += '--------------------------------------------------\n'
	ttc_msg += '{}\n'.format(input_message)
	ttc_msg += '--------------------------------------------------\n'

	return ttc_msg


"""
TO-DO

DONE
game
npc
covert
national
globe
un
science
media
alien



{'game': <discord.channel.Channel object at 0x10df2ef48>, 
'npc': <discord.channel.Channel object at 0x10df334c8>, 
'globe': <discord.channel.Channel object at 0x10df337c8>, 
'national': <discord.channel.Channel object at 0x10df38b48>, 
'un': <discord.channel.Channel object at 0x10df3c9c8>, 
'alien': <discord.channel.Channel object at 0x10df41248>, 
'media': <discord.channel.Channel object at 0x10df41648>, 
'covert': <discord.channel.Channel object at 0x10df41a48>, 
'science': <discord.channel.Channel object at 0x10df45448>}

"""





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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
				not_announcer_error = 'Only an @announcer can use this command.'
				await client.say(not_announcer_error)
				return
		else:
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
		#print(len(all_dict.keys()))
		#i = 0
		#for key, value in all_dict.items():
			#print(key, value)
			#await client.send_message(dev_dict['dev-spam'], str(i))
			#i += 1
			#await client.send_message(value, send_msg)
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
			if user.name.lower() != dev_discord_name:
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
			if user.name.lower() != dev_discord_name:
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
			if user.name.lower() != dev_discord_name:
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


# Command to open up an alien's -comms channel for open use of /msg
@client.command(pass_context=True)
async def alien_comms(ctx, *, input_message: str):
	""" Function for control (@Game Control or @Alien Control) to open up the -comms channel
	for a group to use /msg openly like other earth groups. Using this while a group is already
	in the list removes them from it
	"""

	# Get the user info
	user = ctx.message.author

	# Take out '-comms' from input_message if it exists
	message = input_message
	if '-comms' in message:
		message = message[:-6]

	# Permissions for roles that can use this command
	permissions = [
		'game control',
		'alien control'
	]

	# Error checking
	# Check to see if the person using this command has the correct permissions
	correct_permission = False
	for permission in permissions:
		if permission in [role.name.lower() for role in user.roles]:
			correct_permission = True
			break
	if not correct_permission:
		if testing:
			if user.name.lower() != dev_discord_name:
				not_correct_permission_msg = "Only a person with a @Game Control or "
				not_correct_permission_msg += "@Alien Control tag can use this command."
				await client.say(not_correct_permission_msg)
				return
		else:
			not_correct_permission_msg = "Only a person with a @Game Control or "
			not_correct_permission_msg += "@Alien Control tag can use this command."
			await client.say(not_correct_permission_msg)
			return

	# Add or remove the team from the list
	change = update_open_alien(message)

	# Log for the controllers
	print('The aliens with /msg permissions have changed: {}'.format(open_alien))

	# Let the user know what happened
	if change > 0:
		send_msg = 'The {} alien group have been GIVEN `/msg` permissions. '.format(message)
		send_msg += 'All alien groups with these permissions: {}'.format(open_alien)
	elif change < 0:
		send_msg = 'The {} alien group have been REMOVED of `/msg` permissions. '.format(message)
		send_msg += 'All alien groups with these permissions: {}'.format(open_alien)
	else:
		send_msg = 'No change to the aliens with `/msg` permissions. '.format(message)
		send_msg += 'All alien groups with these permissions: {}'.format(open_alien)
	await client.say(send_msg)


# Command to manually refresh the team comms list/dict
@client.command()
async def update_team_comms(*args):
	""" Command that refreshed the team comms list/dev
	Usable by anyone
	"""

	update_teams(reset=True)
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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
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
			if user.name.lower() != dev_discord_name:
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
		for key, value in team_disc_dict.items():
			await client.send_message(value, send_msg)
		await client.send_message(public_dict['global-chat'], send_msg)
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
			if user.name.lower() != dev_discord_name:
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
			if user.name.lower() != dev_discord_name:
				print(user.name)
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
		phase_s = phase
		if ' minutes)' in phase_s:
			phase_s = phase_s[:-13]
		if current_phase_i == i:
			phase_str = '{} - {} <---- we are here\n'.format(i, phase_s)
		else:
			phase_str = '{} - {}\n'.format(i, phase_s)
		send_msg += phase_str
	send_msg += "```"
	#print(len(send_msg))

	# Send the message to the channel the command was used in
	#await client.say('test')
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


def update_teams(verbose=False, reset=True):
	""" Helper function to update the team lists and dicts. Called during initialization and 
	potentially elsewhere.
	"""
	# We'll get a list of all servers, then we'll look for the desired server ('server_name', 
	# above), then we'll create a dictionary of channels (if the name matches any in the 
	# 'human_team_list' list above)

	# Let's reset all the team dicts (if requested)
	if reset:
		reset_dicts()

	# Now let's sort
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
	not_in_set = "These -comms channels don't have an emoji:  \n"
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


# Helper function to reset all team dicts. Only called by update_teams()
def reset_dicts():
	"""
	"""
	global team_comms_dict
	team_comms_dict = dict()
	global team_aar_dict
	team_aar_dict = dict()
	global team_disc_dict
	team_disc_dict = dict()
	global control_dict
	control_dict = dict()
	global category_dict
	category_dict = dict()
	global voice_dict
	voice_dict = dict()
	global dev_dict
	dev_dict = dict()
	global all_dict
	all_dict = dict()
	global public_dict
	public_dict = dict()
	global other_dict
	other_dict = dict()


# Helper function for adding or removing from the open_alien
def update_open_alien(new_open_alien):
	""" Helper function for either adding to or removing from the open_alien list.
	Any alien team  
	"""
	global open_alien

	start_size = len(open_alien)

	if new_open_alien.lower() in open_alien:
		open_alien = [s for s in open_alien if s != new_open_alien.lower()]
	else:
		open_alien.append(new_open_alien.lower())
	
	end_size = len(open_alien)

	# should return -1 if an alien group was removed, and 1 if the alien group was added
	return end_size - start_size
	
	
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