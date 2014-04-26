import os
import json
import urllib
import socket
import subprocess as sub
import string
import sys

MPCONF = "/etc/magicpool.conf"
MPURL  = "https://magicpool.org/main/download_config/${U}/${W}/${G}"
SGCONF = "/home/crypto/.sgminer/sgminer.conf"

def niceprint(data):
	return json.dumps(data,sort_keys=True,indent=4, separators=(',', ': ')).__str__()
	

def getURL(url):
	try:
		u = urllib.urlopen(url)
		data = u.read()
	except:
		print("ERROR: cannot fetch url %s" %url)
		sys.exit(1)
	return data

def saveConf(conf):
	os.system("cp %s %s" %(SGCONF,SGCONF+".old"))
	c = open(SGCONF,"w")
	c.write(niceprint(conf))
	c.close()

def restart():
	os.system("md5sum %s | awk '{print $1}' > /tmp/get-pool.md5.1" % SGCONF)
	os.system("md5sum %s | awk '{print $1}' > /tmp/get-pool.md5.2" % (SGCONF+".old"))
	md51 = open("/tmp/get-pool.md5.1","r")
	md52 = open("/tmp/get-pool.md5.2","r")
	if md51.read() == md52.read():
		print "No changes in configuration"
	else:
		print "Found changes in configuration, restarting sgminer"
		#os.system('echo "quit|1" | nc 127.0.0.1 4028')
		os.system('killall -USR1 sgminer')
	md51.close()
	md52.close()

def getMPconf():
	try:
		mpconf = open(MPCONF,"r")
		mp = json.loads(mpconf.read())
		user = mp['username']
		worker = mp['workeralias']
	except:
		user = "generic"
		worker = "generic"
	return {"user":user,"worker":worker}

def getMPremote():
	url = MPURL
	mpconf = getMPconf()
	gpu = getGPU()
	s = string.Template(MPURL)
	mpurl = s.substitute(U=mpconf["user"],W=mpconf["worker"],G=gpu)
	print("Requesting URL %s" %mpurl)
	print(getURL(mpurl))
	try:
		data = json.loads(getURL(mpurl))
	except:
		print("ERROR: Cannot decode the magicpool json response")
		sys.exit(1)
	if 'ERROR' in data:
		print("ERROR: Some error in magicpool web server")
		sys.exit(1)
	if 'REBOOT' in data:
		os.execute("sudo reboot")
		sys.exit(2)
	return data
	
def getSGconf():
	try:
		fd_conf = open(SGCONF,"r")
		data = json.loads(fd_conf.read())
		fd_conf.close()
	except:
		print("WARNING: cannot read current sgminer config file")
		data = {}
	return data

def getGPU():
	vcards = []
	p = sub.Popen('lspci',stdout=sub.PIPE,stderr=sub.PIPE)
	output, errors = p.communicate()
	for pci in string.split(output,'\n'):
		if string.find(pci,'VGA') > 0:
			try:
				vcards.append(string.split(pci,':')[2])
			except:
				print("Card not recognized")
	cards = ""
	for v in vcards:
		cards = v.replace(',','').replace('\'','').replace(' ','%20').replace('[','%5B').replace(']','%5D')

	return cards

remoteconf = getMPremote()
saveConf(remoteconf)
restart()

#return json.loads(getURL(MPURL))
#print(niceprint(getSGconf()))

#conf["pools"] = remote["pools"]
#i=0
##while i < len(conf["pools"]):
#	new_u = conf["pools"][i]["user"].replace("USER",USER)
#	new_p = conf["pools"][i]["pass"].replace("PASS",PASS)
#	conf["pools"][i]["user"] = new_u
#	conf["pools"][i]["pass"] = new_p
#	i=i+1
#
#print niceprint(conf)
#fd_conf.close()
#saveConf()
#restart()
