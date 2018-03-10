from datetime import datetime
from account import account
import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.bot_token)
acc=account()
whitelist=[116690394, 325581035, 153155480]#list of chat ids that are allowed to control registration function

def log(line):
	log_stream = open(config.logfile, "a", encoding = 'utf8')
	mem = 'BREG:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line+'\n'
	log_stream.write(mem)
	log_stream.close()

def save(account_phone):
	log("saving account " + account_phone)
	f=open(config.accountfile,'a')
	f.write(account_phone+'\n')
	f.close()

@bot.message_handler(commands=['start'])
def start(message):
	if message.chat.id in whitelist:
		markup = types.ReplyKeyboardMarkup()
		markup.row('reg')
		bot.send_message(message.chat.id, "BREG ONLINE", reply_markup=markup)
	log("Bot is online by "+str(message.chat.id))

@bot.message_handler(regexp="reg")
def reg(message):
	if message.chat.id in whitelist:
		acc=account()
		bot.send_message(message.chat.id, "Enter phone:")
		
@bot.message_handler(regexp="\d\d\d\d\d\d\d\d\d\d\d")
def reg_query(message):
	if message.chat.id in whitelist:
                try:
                        acc.reg_code_request(message.text)
                        #bot.send_message(message.chat.id, type(acc))#temp
                        bot.send_message(message.chat.id, "Enter code:")
                        save(message.text)
                except PhoneNumberBannedError:
                        bot.send_message(message.chat.id, "This phone number is in ban")
                except PhoneNumberOccupiedError:
                        bot.send_message(message.chat.id, "This phone number is already occupied")


@bot.message_handler(regexp="\d\d\d\d\d")
def code_proceed(message):
	if message.chat.id in whitelist:
                try:
                        temp_str = acc.reg_auto(message.text)
                        log('registration complete '+temp_str)
                        acc.subscribe("NeonVision")
                        acc.subscribe("GregorioChernyshov")
                        #bot.send_message(message.chat.id, type(acc))#temp
                        bot.send_message(message.chat.id, "Registered successfuly "+temp_str)
                except PhoneCodeInvalidError:
                        bot.send_message(message.chat.id, "Entered code is wrong")

@bot.message_handler(commands=['getlog'])
def getlog(message):
	log("log request from "+str(message.chat.id))
	logfile=open(config.logfile, "r")
	bot.send_message(message.chat.id, logfile.read())

@bot.message_handler(commands=['getstate'])
def getstate(message):
	log("state request from "+str(message.chat.id))
	bot.send_message(message.chat.id, "ONLINE NOW")


if __name__ == '__main__':
	bot.polling(none_stop=True)
