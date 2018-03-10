import telethon
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
import config
from datetime import datetime, timedelta
import random
import names
from SMSreg import SMSreg
import socks
from telethon.tl.functions.account import UpdateStatusRequest

class Account:
#variables
        client = None
        phone = None

        proxyName = None
        proxyPort = None
        
#private funcs:
        def __log(self, string):
                log_stream = open(config.logfile, "a", encoding = 'utf8')
                mem = 'ACCN (' + self.phone + ') [' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + ']: ' + string + '\n'
                log_stream.write(mem)
                log_stream.close()
        
        
        def __init__(self, phone = None):
                '''
                Конструктор создает клиент и гарантирует соединение с сервером в случае успешного завершения.

                Параметр phone - номер, привязаный к этому аккаунту в последствии сменить НЕЛЬЗЯ

                Если phone не указан, то происходит регистрация нового аккаунта, phone берется из сервиса активаций.
                '''

                #self.proxyName = prox_name
                #self.proxyPort = prox_port
                
                if(phone):
                        self.phone = phone
                        self.__connect()
                else:
                        self.__reg()


        def __connect(self):
                try:
                        self.client = TelegramClient(self.phone, config.api_id, config.api_hash)#, proxy = (socks.SOCKS5, self.proxyName, self.proxyPort))
                        for i in range(50):
                                self.__log("Connecting...")
                                
                                if self.client.connect():
                                        self.__log("Successfully connected to the server")
                                        return
                        
                        self.__log("UNABLE TO CONNECT TO THE SERVER")
                        return False
                           
                except PermissionError:
                        self.__log("Unable to create account!!! An error appeared due to wrong api_id or api_hash")
                        return False

                except ValueError:
                        self.__log("Unable to create account!!! An error appeared due to wrong Session parameter")
                        return False

                
        
        def __reg(self):
                numResponse = SMSreg.getNum()

                self.phone = numResponse['num']

                self.__log("Phone got. Registration is starting, self.phone="+self.phone)
                try:
                        self.__connect()
                        self.__log("Sending code request for this account")
                        self.client.send_code_request(self.phone)

                except telethon.errors.rpc_error_list.PhoneNumberBannedError:
                        self.__log('This phone number is banned')

                        SMSreg.wrongNum(numResponse['tzid'])
                        self.__reg()
                
                '''
                except PhoneNumberInvalidError:
                        self.__log('phone number invalid')
                        self.__init__(proxyName, proxyPort)
                '''
                '''
                except PhoneNumberBannedError:
                        self.__log('phone number banned')
                        SMSreg.wrongNum(self.phone)


                '''

                fname = random.choice(names.firstnames)
                lname = random.choice(names.lastnames)
                self.__log('The chosen name for acc is ' + fname + ' ' + lname)
                Code=SMSreg.getCode(numResponse['tzid'])

                if Code == 0:
                        self.client.send_code_request(self.phone, True)
                        Code = SMSreg.getCode(numResponse['tzid'])
                
                try:
                        self.client.sign_up(Code, fname, lname)

                except telethon.errors.rpc_error_list.PhoneNumberOccupiedError:
                        self.__log('This phone number is already occupied')
                        try:
                                self.client.sign_in(phone=self.phone, code=Code)
                        except telethon.errors.rpc_error_list.SessionPasswordNeededError:
                                SMSreg.finish(numResponse['tzid'])
                                self.__reg()
                
                '''
                except Exception:
                        try:
                                self.client.sign_up(SMSreg.reviseCode(self.phone), fname, lname)
                        except Exception:
                                SMSreg.wrongCode(self.phone)
                '''
                SMSreg.finish(numResponse['tzid'])
                self.__log("Client is signed up")


#public funcs:

        def setOnline(self):
                self.client(UpdateStatusRequest(False))
                self.__log('gone online')

        def setOffline(self):
                self.client.client(updateStatusRequest(True))
                self.__log('gone offline')

        def subscribe(self, channel):
                self.client(JoinChannelRequest(self.client.get_entity(channel)))    
                self.__log('Joined ' + channel) 

        def unsubscribe(self, channel):
                self.client(LeaveChannelRequest(self.client.get_entity(channel)))
                self.__log('left '+channel)


#me = Account('+79851272285')
'''
messages = client.get_message_history(PeerChannel(…), limit=3000)
#retain views
'''
