#INSERT __LOG() EVERYWHERE
'''
cd desktop\grisha\progproj\tgb\tgservice
C:\programming\python\python.exe
from cluster import Cluster
Cluster.addAccounts(1)

'''
import config
from account import Account
import time
import random

lTasks = []

class Cluster:
#variables:
	lAccounts = []

#private funcs:
	def __log(line):
		log_stream = open(config.logfile, "a", encoding = 'utf8')
		
		mem = 'CLST:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line
		log_stream.write(mem)

		log_stream.close()

	def __save():
		saveFile = open(config.dataSavePath + 'clust.cluster', 'w', encoding = 'utf8')
		
		for acc in Cluster.lAccounts:
			saveFile.write(str(acc.phone) + '\n')

		saveFile.close()

	def save_acc(acc):
		#if(acc.client.is_user)
		saveFile = open(config.dataSavePath + 'clust.cluster', 'a', encoding = 'utf8')
		saveFile.write(str(acc.phone) + '\n')
		saveFile.close()

#public funcs:
	def addAccounts(numToCreate = 0, lPhoneNumbers = None):
		if not lPhoneNumbers:
			for i in range(numToCreate):
				Cluster.lAccounts.append(Account())
				Cluster.onlineThisAcc(len(Cluster.lAccounts) - 1)

		else:
			for i in range(len(lPhoneNumbers)):
				Cluster.lAccounts.append(Account(phone = lPhoneNumbers[i]))
				Cluster.onlineThisAcc(len(Cluster.lAccounts) - 1)
				Cluster.save_acc(lAccounts[(len(Cluster.lAccounts) - 1)])

		Cluster.__save()
	
	def subscribe(channel, ammount):
		global lTasks
		
		for i in range(ammount):
			timeToSub = time.time() + (i * random.randint(1200, 3600))

			lTasks.append({'acc' : i, 'time' : timeToSub, 'event' : 'sub', 'arg1' : channel})


	def unsubscribe(channel, ammount):
		global lTasks
		
		for i in range(ammount):
			timeToSub = time.time() + (i * random.randint(1200, 2400))

			lTasks.append({'acc' : i, 'time' : timeToSub, 'event' : 'unsub', 'arg1' : channel})

	def subThisAcc(i, channel):
		Cluster.lAccounts[i].subscribe(channel)
			
	def unsubThisAcc(i, channel):
		Cluster.lAccounts[i].unsubscribe(channel)

	def onlineThisAcc(i):
		global lTasks

		timeToGo = time.time() + random.randint(60, 500)
		(Cluster.lAccounts[i]).log('This account set online. Will go offline in ' + str(timeToGo - time.time()) + ' sec')

		Cluster.lAccounts[i].setOnline()
		lTasks.append({'acc' : i, 'time' : timeToGo, 'event' : 'offline'})

	def offlineThisAcc(i):
		global lTasks

		timeToGo = time.time() + random.randint(900, 7200)
		(Cluster.lAccounts[i]).log('This account set offline. Will go online in ' + str(timeToGo - time.time()) + ' sec')

		Cluster.lAccounts[i].setOffline()
		lTasks.append({'acc' : i, 'time' : timeToGo, 'event' : 'online'})

#end of class

def mainLoop():
        while True:
                global lTasks
                
                for task in lTasks:
                        if time.time() >= task['time']:

                                #switch (pochti)
                                if task['event'] == 'sub':
                                        Cluster.subThisAcc(task['acc'], task['arg1'])

                                elif task['event'] == 'unsub':
                                        Cluster.unsubThisAcc(task['acc'], task['arg1'])

                                elif task['event'] == 'online':
                                        Cluster.onlineThisAcc(task['acc'])

                                elif task['event'] == 'offline':
                                        Cluster.offlineThisAcc(task['acc'])

                                else:
                                        raise Exception('Wrong statement in tasks list')
                                #end of switch

                                lTasks.remove(task)



def load():
	file = open(config.dataSavePath + 'clust.cluster', 'r', encoding = 'utf8')
	
	telList = [line.strip() for line in file]
	Cluster.addAccounts(lPhoneNumbers = telList)

	file.close()
		
		




	
				





	
				
						
		

		
	
