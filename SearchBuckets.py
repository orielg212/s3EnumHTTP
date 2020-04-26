import mechanize
import json
import urllib
import sys
import ssl
import threading
from threading import Thread  
import time
import string
import requests
import os

#threads = 5
def send(url):
	url = url.replace('\n', '').replace('\r', '')
	#print ("[*] Checking "+url)#print url

	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
		}
		# For Burp
		# proxies = {
		  # "http": "http://127.0.0.1:8080",
		  # "https": "https://127.0.0.1:8080",
		# }
		#requests.get(url, proxies=proxies, verify=False, headers=headers)
		response = requests.get(url, verify=False, headers=headers).text
		if "<Code>SlowDown</Code>" in response:
			print ("[*] Blocked by Amazon - SlowDown baby!!!")
			os._exit(1)
		if "The specified bucket does not exist" in response:
			#print("bucket doesn't exist: " + url)
			pass
		else:
			if ("<Code>AccessDenied</Code>" in response) or ("<Code>AllAccessDisabled</Code>" in response):
				print("[+] bucket exist but no access: "+ url)
				log = open('existing_backets.txt', 'a')
				log.write(str("[+] bucket exist but no access: "+ url+"\n"))
				log.close()

			else:
				print("[+] bucket exist and maybe you have access!!!: "+ url)
				log = open('existing_backets.txt', 'a')
				log.write(str("[+] bucket exist and maybe you have access!!!: "+ url+"\n"))
				log.close()


	except:
		pass



if not len(sys.argv) > 2:
	print ("[-] Usage: python SearchBuckets.py <company name> <threads>")
	exit()

company_name = sys.argv[1]
try:
	threads = int(sys.argv[2])
except:
	print ("[-] Threads should be a number...exit")
	exit()
	
print ("[*] Look at existing_backets.txt file for existing bucket list")
print ("[*] Using fuzzlist.txt as fuzz list")
try:
	os.remove("existing_backets.txt")
except:
	pass
separetors = ["-","_","."]
f = open("fuzzlist.txt", "r")

url = "http://"+company_name+".s3.amazonaws.com"
t = Thread(target = send, args=(url,))
t.start()



for bucket in f:
	for char in separetors:
		url = "http://"+bucket.replace('\n', '').replace('\r', '')+char+company_name+".s3.amazonaws.com"
		x_run = False
		while not x_run:
			if threading.active_count()< threads:
				t = Thread(target = send, args=(url,))
				t.start()
				x_run = True
			else:
				time.sleep(2)
	for char in separetors:
		url = "http://"+company_name+char+bucket.replace('\n', '').replace('\r', '')+".s3.amazonaws.com"
		x_run = False
		while not x_run:
			if threading.active_count()< threads:
				t = Thread(target = send, args=(url,))
				t.start()
				x_run = True
			else:
				time.sleep(2)
			
	

			










