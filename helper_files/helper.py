import subprocess
import psutil
from pathlib import Path
from evdev import UInput, ecodes as e
import pyudev
import shutil
import time
import os
import sys

class DiskManager:
	def __init__(self):
		self.board = UInput()
		self.mnt_dir = "/mnt/usb"
		self.node = None
		self.name = None
		self.loc = None
		self.diskname = None
		self.observer = None
		self.detection()
	
	def detection(self):
		context = pyudev.Context()
		monitor = pyudev.Monitor.from_netlink(context)
		
		monitor.filter_by(subsystem="block")
		
		def event(action, device):
			if action == "add" and device.device_type == "partition":
				self.node = device.device_node
				self.name = device.device_node.split("/")[-1]
				self.mount()
			#elif action == "remove" and device.device_type == "partition":
			#	pass
					# either save the file for sync later bc the eject was probably
					# unintentional OR have no mercy and wipe it so that it doesn't
					# cause issues later
					
		self.observer = pyudev.MonitorObserver(monitor, event)
		self.observer.start()
	
	def mount(self):
		self.loc = self.mnt_dir + "/" + self.name
		if not os.path.exists(self.loc):
			os.makedirs(self.loc)
		subprocess.run(["sudo", "mount", self.node, self.loc], check=True, capture_output=True, text=True)
		if os.path.isfile(self.loc + "/disk"):
			for file in Path(self.loc).glob("*.dsk"):
				self.diskname = file.name
				shutil.copy(self.loc + "/" + self.diskname,"disk9.dsk")
				self.board.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
				self.board.write(e.EV_KEY, e.KEY_9, 1)
				self.board.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
				self.board.write(e.EV_KEY, e.KEY_9, 0)
				self.board.syn()
				break
		else:
			self.node = None
			subprocess.run(["sudo", "umount", self.loc], check=True, capture_output=True, text=True)
			
		
	def unmount(self):
		os.remove("eject")
		if self.node != None:
			shutil.copy("disk9.dsk", self.loc + "/" + self.diskname)
			os.remove("disk9.dsk")
			self.node = None
			subprocess.run(["sudo", "umount", self.loc], check=True, capture_output=True, text=True)
		
if __name__  == "__main__":
if __name__  == "__main__":
	time.sleep(1)
	manager = DiskManager()
	log = []
	
	while True:
		for program in psutil.process_iter(['pid', 'name']):
			log.append(program.info['name'])
		if "minivmac" not in log:
			manager.observer.stop()
            try:
                os.remove("eject")
            except:
                pass
			sys.exit()
		else:
			log = []
		
		if os.path.isfile("eject"):
			manager.unmount()
		time.sleep(0.5)
