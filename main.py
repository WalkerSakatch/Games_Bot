"""
This is the main file for the bot, this is the file that must be run for the bot to work. MOST of the methods in this file coorespond to different commands that the bot can handle
Docs for the Telegram Bot API: https://python-telegram-bot.readthedocs.io/en/stable/index.html
"""

import telegram
import logging, random, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import league as lg
import db as db
import strings
import fortnite as fnite
import apex as apx

#Telegram gives each bot a specific identifier or token that is required for it to work
TOKEN = os.getenv('GAMES_BOT_TOKEN')

#command /start sends a message
def start(update, context):
	context.bot.send_message(chat_id=update.message.chat_id, text="Beep Beep Boop! I am a bot!")

#command /help sends a funny reply that isn't that helpful
def help(update, context):
	context.bot.send_message(chat_id=update.message.chat_id, text="I am poorly programmed and cannot help :(")

#command /stats [name] sends back info on the most played champions in League of Legends for the name given
def stats(update, context):
	summoner_name = ""
	
	#msg_ID is the ID of the message that called the command, this is used so the bot can reply to the specific message
	msg_ID = update.message.message_id

	#args given after the command are given as a list, this basically forms the players name if there were spaces in it
	for i in context.args:
		summoner_name = summoner_name + i + " "
	
	reply = ""
	
	#getChampMastery(summoner_name) returns a tuple with info regarding a players most played champs (found in league.py)
	#The tuple looks like ([list of champions], [list of mastery points])
	champ_mastery_result = lg.getChampMastery(summoner_name)
	count = 0
	#For each champion (up to 5), add to a string their name and the points the player has on them.
	for champ in champ_mastery_result[0]:
		reply += champ + " - " + str(champ_mastery_result[1][count]) + "\n"
		count += 1
	if(len(reply) <= 0):
		reply = "Wow, something went wrong!"
	
	#Bot replies to the message with the command with the reply string
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

#command /match [name] sends back an image detailing the players and champions in the specified players League of Legends game. (This command takes a while to finish, but can be fixed)
def match(update, context):
	summoner_name = ""
	msg_ID = update.message.message_id
	for i in context.args:
		summoner_name = summoner_name + i + " "

	#Bot sends a message saying that it is working on the request
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me login and check the game! One second")
	
	#Calls a method that will modify an image that the bot will send. (method found in league.py)
	lg.getCurrentGame(summoner_name)

	#The image being modified is saved to disk, so once the method above is finished the bot can send the file, and telegram takes care of the rest
	context.bot.send_photo(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, photo=open("tesload.png", 'rb'))

#command /league makes the bot tag everyone in the chat that plays League of Legends by their telegram username
def league(update, context):
	msg_ID = update.message.message_id
	
	#-507793116 for joshs other chat
	if(update.message.chat_id == -507793116):
		question = "@hey brother league?"
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	else:
		if not context.args:
			question = "@SaveTheBeeees @anobdya @hotterthanahotdog @GangplankWinsIfHeDoesntAFK @Randomenzyme @Insolent_child @Atrawolf @bleachonmytshirt league?"
			context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
		
		else:
			summoner_name = ""
			for i in context.args:
				summoner_name = summoner_name + i + " "

			context.bot.send_message(parse_mode='MARKDOWN', chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="beep boop one sec")
			ranked_stats = lg.getAllStats(summoner_name)
			context.bot.send_chat_action(chat_id=update.message.chat_id, action="UPLOAD_PHOTO")
			context.bot.send_photo(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, photo=open("statstest.png", 'rb'))

def aram(update, context):
	msg_ID = update.message.message_id
	question = "@Bush69420 @PuddlesofDoom @jarker1 @stooolfan @kivorkdts @Uncle_Phil9 @SyyCam @GangplankWinsIfHeDoesntAFK ARAM?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def tft(update, context):
	msg_ID = update.message.message_id
	question = "@Bush69420 @PuddlesofDoom @kivorkdts @Uncle_Phil9 @stooolfan TFT?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /dota makes the bot tag everyone in the chat that plays Dota by their telegram username
#def dota(update, context):
#	msg_ID = update.message.message_id
#	question = "@Insolent_child @AtraWolf @prankpatrol dota?"
#	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def dota(update, context):
	msg_ID = update.message.message_id
	question = "@AtraWolf @prankpatrol @anobdya dota?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)


#command /ror makes the bot tag everyone in the chat that plays Risk of Rain by their telegram username
def ror(update, context):
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @AtraWolf @prankpatrol Risk of Rain 2?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def lor(update, context):
	msg_ID = update.message.message_id
	#-507793116 for joshs other chat
	if(update.message.chat_id == -507793116):
		question = "@stooolfan @GangplankWinsIfHeDoesntAFK Runeterra?"
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	else:
		msg_ID = update.message.message_id
		question = "@SaveTheBeeees @anobdya @GangplankWinsIfHeDoesntAFK @Atrawolf @bantzdealer @bleachonmytshirt Runeterra?"
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /ror makes the bot tag everyone in the chat that plays Risk of Rain by their telegram username
def r6(update, context):
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @Insolent_child @AtraWolf @prankpatrol @bleachonmytshirt R6 Siege?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	
#command /fortnite can take optional arguments
def fortnite(update, context):
	msg_ID = update.message.message_id

	#command /fortnite makes the bot tag everyone in the chat that plays Fortnite by their telegram username
	if not context.args:
		question = "@TheBoneDoctor @prankpatrol @Insolent_child @bleachonmytshirt @AtraWolf @hotterthanahotdog @SaveTheBeeees fortnite?"
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

	#command /fortnite shop makes the bot reply with an album of images detailing what is currently in the fortnite shop
	elif (len(context.args) == 1 and context.args[0] == "shop"):
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me open the shop up! One second please.")
		context.bot.send_chat_action(chat_id=update.message.chat_id, action="UPLOAD_PHOTO")

		#Sends an album with every weekly item in the shop
		resp = fnite.getWeeklyStore()
		context.bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)
		
		#Sends an album with every daily item in the shop
		resp = fnite.getDailyStore()
		context.bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)

	#command /fortnite challenges makes the bot reply with the current weekly challenges in Fortnite
	elif (len(context.args) == 1 and context.args[0] == "challenges"):
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me check the challenges")
		resp = fnite.getChallenges()
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)
	
	#command /fortnite [name] gets the bot to send [name]'s stats in the current Fortnite season
	else:
		name = ""
		for word in context.args:
			name = name + word + " "

		resp = fnite.getStats(name)
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

def apex(update, context):
	msg_ID = update.message.message_id

	#-507793116 for joshs other chat
	if not context.args:
		if(update.message.chat_id == -507793116):
			question = "@Bush69420 @stooolfan @Uncle_Phil9 @SyyCam @kivorkdts apex?"
			context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
		else:
			question = "@SaveTheBeeees @anobdya @hotterthanahotdog @AtraWolf @bleachonmytshirt @prankpatrol apex?"
			context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	else:
		platform = context.args[0]
		player_name = ""
		for i in context.args[1:]:
				player_name = player_name + i + " "


		if(platform.lower() == 'xbox'):
			platform = 1
		elif(platform.lower() == 'psn' or platform.lower() == 'ps4'):
			platform = 2
		elif(platform.lower() == 'pc'):
			platform = 5
		else:
			context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Type /apex [platform] [name]\nPlatforms are xbox, psn, pc")
	
	resp = apx.getStats(platform, player_name)
	context.bot.send_message(parse_mode='MARKDOWN', chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)
		
#command /overwatch makes the bot tag everyone in the chat that plays Overwatch by their telegram username
def overwatch(update, context):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf Overwatch?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /valorant makes the bot tag everyone in the chat that plays Valorant by their telegram username
def valorant(update, context):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf @GangplankWinsIfHeDoesntAFK @Randomenzyme Valorant?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /amongus makes the bot tag everyone in the chat that plays Valorant by their telegram username
def among_us(update, context):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf @GangplankWinsIfHeDoesntAFK @Insolent_child @Randomenzyme Among Us?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
		
#command /forest makes the bot tag everyone in the chat that plays The Forest by their telegram username
def forest(update, context):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @anobdya forest?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /dauntless makes the bot tag everyone in the chat that plays Dauntless by their telegram username
def dauntless(update, context):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @anobdya dauntless?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def rl(update, context):
	msg_ID = update.message.message_id
	if(update.message.chat_id == -507793116):
		question = "@Bush69420 @PuddlesofDoom @jarker1 @stooolfan @kivorkdts @Uncle_Phil9 @SyyCam Rocket League?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def gta(update, context):
	msg_ID = update.message.message_id
	if(update.message.chat_id == -507793116):
		question = "@Bush69420 @PuddlesofDoom @stooolfan @kivorkdts @Uncle_Phil9 @SyyCam GTA?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def nba(update, context):
	msg_ID = update.message.message_id
	if(update.message.chat_id == -507793116):
		question = "@Bush69420 @PuddlesofDoom @jarker1 @stooolfan @Uncle_Phil9 @SyyCam NBA?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def dice(update, context):
	msg_ID = update.message.message_id
	#emoji='\U0001F3B0'
	context.bot.send_dice(chat_id=update.message.chat_id, reply_to_message_id=msg_ID)

#command /mhw makes the bot tag everyone in the chat that plays Monster hunter world by their telegram name
def mhw(update, context):
	msg_ID = update.message.message_id
	question = "@prankpatrol @AtraWolf @SaveTheBeeees @anobdya @bleachonmytshirt Monster Hunter?"
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

######DATABASE FORTUNE / SUBMIT STUFF BELOW########

def submit(update, context):
	msg_ID = update.message.message_id
	word = update.message.reply_to_message.text
	resp = db.submit(word)
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

def fortune(update, context):
	msg_ID = update.message.message_id
	resp = db.fortune(update, context)
	#context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

def kill(update, context):
	msg_ID = update.message.message_id
	if not update.message.reply_to_message:
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="reply to a fortune with /kill to remove it")
		pass
	word = update.message.reply_to_message.text
	resp = db.kill(word)
	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

#Method that reads every message sent in chat, and if a user says certain words it will interrupt.
def interjection(update, context):
	#get some info for each message, like who sent it
	from_user = update.message.from_user.first_name
	from_user = from_user.lower()
	msg_ID = update.message.message_id
	msg_text = update.message.text.lower()
	msg_lst = msg_text.split()

	#If Kalada says the word yi, then trash talk him (replies are picked at random from a list in strings.py)
	#if(from_user == "kalada" and "yyeai" in msg_lst):
	#	i = random.randrange(len(strings.master_yi))
	#	reply = strings.master_yi[i]
	#	context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

	#If Josh says the word clash, then send KEKW sticker: CAACAgEAAxkBAAIGwV8FWRznc257kSPI5Nf84aGxy_nsAAKJAAMVihsHYu3bTjyQwT4aBA
	if(update.message.from_user.id == 1052764994):
		#bot.send_sticker(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, sticker="CAACAgEAAxkBAAIGwV8FWRznc257kSPI5Nf84aGxy_nsAAKJAAMVihsHYu3bTjyQwT4aBA")
		#anti_josh_txt = msg_text.strip(".,!@#$%*/?\"'][:;_-()")
		
		if ("clash" in msg_text):
			context.bot.send_sticker(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, sticker="CAACAgEAAxkBAAIGwV8FWRznc257kSPI5Nf84aGxy_nsAAKJAAMVihsHYu3bTjyQwT4aBA")

	if("brown" in msg_lst or "browns" in msg_lst):
		reply = "The shared iq phenomenon occurs when there is one or more person of South East Asian descent in an online video game lobby. There is 80 iq allocated for brown people to use upon entering a lobby, however the amount of iq does not increase depending on the amount of South East Asian players in the lobby. This means that if there is one in the lobby they receive all 80 IQ points (a relatively large amount to what they are used to), however if another South East Asian joins the lobby the first one is forced to give the new one a portion of his iq (usually half) which means on average each SEA player only has 40 iq. This is an extreme problem when there are 3 or more SEA players in one lobby as each one will have only 25 or less IQ to work with, much to the dismay of their intellectually superior teammates"
		context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

#If a user types in a command that doesn't exist then the bot will reply to them (doesn't work yet)
def unknown(update, context):
	context.bot.send_message(chat_id=update.message.chat_id, text="Sorry I didn't understand that command. :(")

#command /caps [string] makes the bot reply with the same string but in all upper case
def caps(update, context):
	text_caps = ' '.join(context.args).upper()
	context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

#Main method that is ran when the bot is started up
def main():
	#Basic stuff required by telegram to make the bot work. Basically lets Telegram know who the bot is / who it belongs to.
	bot = telegram.Bot(token=TOKEN)
	updater = Updater(token=TOKEN)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	#Each command that the bot can handle needs a "Handler". These basically map the command (/[command] to a method in main.py)
	#It is set up so the commands execute methods with the exact same name, but the command is the first argument, and the method that it executes is the second.
	#pass_args says whether the command can take additional arguments (bot uses these for summoner names, or fortnite names). Default is to False
	
	start_handler = CommandHandler('start', start)
	help_handler = CommandHandler('help', help)
	caps_handler = CommandHandler('caps', caps)
	stats_handler = CommandHandler('stats', stats)
	match_handler = CommandHandler('match', match)
	league_handler = CommandHandler('league', league)
	aram_handler = CommandHandler('aram', aram)
	tft_handler = CommandHandler('tft', tft)
	dota_handler = CommandHandler('dota', dota)
	fortnite_handler = CommandHandler('fortnite', fortnite)
	apex_handler = CommandHandler('apex', apex)
	overwatch_handler = CommandHandler('overwatch', overwatch)
	valorant_handler = CommandHandler('valorant', valorant)
	amongus_handler = CommandHandler('amongus', among_us)
	forest_handler = CommandHandler('forest', forest)
	dauntless_handler = CommandHandler('dauntless', dauntless)
	rl_handler = CommandHandler('rl', rl)
	gta_handler = CommandHandler('gta', gta)
	nba_handler = CommandHandler('nba', nba)
	ror_handler = CommandHandler('ror', ror)
	lor_handler = CommandHandler('lor', lor)
	r6s_handler = CommandHandler('r6', r6)
	mhw_handler = CommandHandler('mhw', mhw)
	submit_handler = CommandHandler('submit', submit)
	fortune_handler = CommandHandler('fortune', fortune)
	kill_handler = CommandHandler('kill', kill)
	dice_handler = CommandHandler('dice', dice)
	interjection_handler = MessageHandler(Filters.all, interjection)

	#Unkown doesn't quite work yet
	unknown_handler = MessageHandler(Filters.command, unknown)

	#This adds handlers to the bot's dispatcher more info at: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dispatcher.html
	#Basically every command needs to have a handler and then that handler needs to be added to the dispatcher to work. If you don't add a handler to the dispatcher then it won't work.
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(caps_handler)
	dispatcher.add_handler(stats_handler)
	dispatcher.add_handler(match_handler)
	dispatcher.add_handler(league_handler)
	dispatcher.add_handler(aram_handler)
	dispatcher.add_handler(tft_handler)
	dispatcher.add_handler(dota_handler)
	dispatcher.add_handler(fortnite_handler)
	dispatcher.add_handler(apex_handler)
	dispatcher.add_handler(overwatch_handler)
	dispatcher.add_handler(valorant_handler)
	dispatcher.add_handler(amongus_handler)
	dispatcher.add_handler(forest_handler)
	dispatcher.add_handler(dauntless_handler)
	dispatcher.add_handler(rl_handler)
	dispatcher.add_handler(gta_handler)
	dispatcher.add_handler(nba_handler)
	dispatcher.add_handler(ror_handler)
	dispatcher.add_handler(lor_handler)
	dispatcher.add_handler(r6s_handler)
	dispatcher.add_handler(mhw_handler)
	dispatcher.add_handler(submit_handler)
	dispatcher.add_handler(fortune_handler)
	dispatcher.add_handler(kill_handler)
	dispatcher.add_handler(dice_handler)

	dispatcher.add_handler(interjection_handler)	
	dispatcher.add_handler(unknown_handler)

	#After setting up the handlers and the dispatcher, the bot starts polling, which means that the bot will now read updates from Telegram, and any update will be handled by a handler
	#Because of this, the program runs until forcefully quit (^C)
	updater.start_polling()

main()
