# -*- coding: utf-8 -*-

import json
import schedule
import socket
import time
import urllib2

localAddress = ""

def notifyToSlack():
	global localAddress
	data = json.dumps({"text": "IP가 바뀌었어요! config.xml을 다음 주소로 수정해주세요.\n"+localAddress})
	req = urllib2.Request("slack-webhook url", data, {'Content-Type': 'application/json'})
	print urllib2.urlopen(req).read()

def checkLocalAddress():
	global localAddress
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	currentLocalAddress = str(s.getsockname()[0])
	if localAddress != currentLocalAddress:
		localAddress = currentLocalAddress
		notifyToSlack()


schedule.every(1).minutes.do(checkLocalAddress)

checkLocalAddress()
while True:
	schedule.run_pending()
	time.sleep(1)