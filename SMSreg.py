from datetime import datetime
import requests
import json
import time
import config
import math

#TODO: add exceptions

#TODO: log every answer
class SMSreg:
	currentRate = 3.0
	
	#tzid=None
	'''
	def __init__(SMSreg):
		r = requests.get('http://api.sms-reg.com/getNum.php?country=all&service=telegram&appid='+APIkey)
		if (not r.json()['responce']=='1'):
			raise r.json()['responce']
		SMSreg.tzid=r.json()['tzid']
		__log('number received')
	'''

	def __setRate(value):
		SMSreg.__log('Setting rate (__setRate func), value = ' + str(value))
		
		r = requests.get('http://api.sms-reg.com/setRate.php?rate=' + str(float(value)) + '&apikey=' + config.APIkey).json()
		
		if r['response'] != '1' or not math.isclose(float(r['rate']), float(value)):
			SMSreg.__log("Some error occured, r['response'] = " + r['response'])
			try:
				SMSreg.__log("r['rate'] = " + str(r['rate']))
			except KeyError:
				pass
		else:
			SMSreg.__log('Successfully set rate')
			
			#SMSreg.__setRate(value)

		SMSreg.__log('finish setting rate')#('Successfully set rate')

	def raiseRate(value):
		SMSreg.currentRate += value
		SMSreg.currentRate = min(SMSreg.currentRate, config.maxRate)
		
		SMSreg.__setRate(SMSreg.currentRate)
	
	def getNum():#returns number
		SMSreg.__setRate(SMSreg.currentRate)
	
		r = requests.get('http://api.sms-reg.com/getNum.php?country=all&service=telegram&appid='+config.APP_APIKEY+'&apikey='+config.APIkey)
		if (r.json()['response']=='ERROR'):
			if (r.json()['error_msg']=='ERROR_WRONG_KEY'):
				pass

		SMSreg.__log('Operation begun, tzid is '+r.json()['tzid'])
		#return r.json()['tzid']

		for i in range (0,60):
			time.sleep(2)
			SMSreg.__log('getting state')
			Num=requests.get('http://api.sms-reg.com/getState.php?tzid='+r.json()['tzid']+'&apikey='+config.APIkey)
			if (Num.json()['response']=='TZ_NUM_PREPARE'):
				SMSreg.__log('JSON response is "TZ_NUM_PREPARE"')
				SMSreg.__log('phone is '+Num.json()['number'])

				SMSreg.currentRate -= config.lowerRateOnSuccess
				if SMSreg.currentRate < 2.0:
					SMSreg.currentRate = 2.0

				SMSreg.__log('Set VARIABLE SMSreg.currentRate to be ' + str(SMSreg.currentRate))
				
				return {'num' : Num.json()['number'], 'tzid' : r.json()['tzid']}
			elif (Num.json()['response']=='TZ_INPOOL'):
				SMSreg.__log('waiting for number')
			else:
				SMSreg.__log('Operation status is not valid. Trying again (status == ' + Num.json()['response'] + ')')
				
				if (Num.json()['response'] == 'WARNING_NO_NUMS'):
					SMSreg.raiseRate(config.raiseRateOnFail)
				
				return SMSreg.getNum()

	def wrongNum(tzid):
		time.sleep(15)#this method should be used after 15sec min since getNum
		'''
		while((requests.get('http://api.sms-reg.com/setOperationUsed.php?tzid='+tzid+'&apikey='+config.APIkey)).json()['response'] != '1'):
			SMSreg.__log('setOperationUsed did not work properly')
			time.sleep(5)

		while((requests.get('http://api.sms-reg.com/setOperationOk.php?tzid='+tzid+'&apikey='+config.APIkey)).json()['response'] != '1'):
			SMSreg.__log('setOperationOk did not work properly')
			time.sleep(5)
		'''
		if((requests.get('http://api.sms-reg.com/setOperationUsed.php?tzid='+tzid+'&apikey='+config.APIkey)).json()['response'] != '1'):
			SMSreg.__log('setOperationUsed did not work properly')
			time.sleep(5)

	def getCode(tzid):#returns code from sms
		r = requests.get('http://api.sms-reg.com/setReady.php?tzid='+tzid+'&apikey='+config.APIkey)
		if (not r.json()['response']=='1'):
			SMSreg.__log(r.json()['response'])
			raise Exception(r.json()['response'])

		
		for i in range (0, 50):
			r = requests.get('http://api.sms-reg.com/getState.php?tzid='+tzid+'&apikey='+config.APIkey)
			SMSreg.__log('Waiting for code to come')
			time.sleep(3)
			if ((r.json()['response']=='TZ_NUM_ANSWER') or (r.json()['response'])=='TZ_NUM_ANSWER2'):
				return r.json()['msg']
			if (not ((r.json()['response']=='TZ_NUM_WAIT') or (r.json()['response'])=='TZ_NUM_WAIT2')):
				SMSreg.__log(r.json()['response'])
				raise Exception(r.json()['response'])

		return 0

	def reviseCode(tzid):#returns new code
		r = requests.get('http://api.sms-reg.com/setOperationRevise.php?tzid='+tzid+'&apikey='+config.APIkey)
		if (not r.json()['responce']=='1'):
			SMSreg.__log(r.json()['response'])
			raise Exception(r.json()['responce'])
		for i in range (0,20):
			time.sleep(3)
			r = requests.get('http://api.sms-reg.com/getState.php?tzid='+tzid+'&apikey='+config.APIkey)
			if ((r.json()['responce']=='TZ_NUM_ANSWER') or (r.json()['responce'])=='TZ_NUM_ANSWER2'):
				return r.json()['msg']
			if (not ((r.json()['response']=='TZ_NUM_WAIT') or (r.json()['responce'])=='TZ_NUM_WAIT2')):
				SMSreg.__log(r.json()['response'])
				raise Exception(r.json()['response'])

	def wrongCode(tzid):
		r = requests.get('http://api.sms-reg.com/setOperationOver.php?tzid='+tzid+'&apikey='+config.APIkey)
		if (not r.json()['response']=='1'):
			SMSreg.__log(r.json()['response'])
			raise Exception(r.json()['response'])

	def getBalance():
		r = requests.get('http://api.sms-reg.com/getBalance.php?apikey='+config.APIkey)
		if (not r.json()['response']=='1'):
			SMSreg.__log(r.json()['response'])
			raise Exception(r.json()['response'])
		return r.json()['balance']

	def finish(tzid):
		r = requests.get('http://api.sms-reg.com/setOperationOk.php?tzid='+tzid + '&apikey=' + config.APIkey)
		if (not r.json()['response']=='1'):
			SMSreg.__log('On finish response = ' + r.json()['response'])

	def __log(line):
		log_stream = open(config.logfile, "a", encoding = 'utf8')
		mem = 'SREG (' + ') [' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + ']: ' + line + '\n'
		log_stream.write(mem)
		log_stream.close()
