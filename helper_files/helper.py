import subprocess
import psutil
from pathlib import Path
from evdev import UInput, ecodes as e
import pyudev
import shutil
import time
import os
import sys

class Disk:
    def __init__(self, filename, mount, number):
        self.filename = filename
        self.mount = mount
        self.number = number

class DiskManager:
	def __init__(self, mnt, limit):
		self.board = UInput()
        self.disks = {1: "SYSTEM", 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
		self.mnt = mnt
        self.limit = limit
        self.pairs = {1: e.KEY_1, 2: e.KEY_2, 3: e.KEY_3, 4: e.KEY_4, 5: e.KEY_5, 6: e.KEY_6, 7: e.KEY_7, 8: e.KEY_8,
                         9: e.KEY_9}
		self.observer = None

		self.detection_init()
	
	def detection_init(self):
		context = pyudev.Context()
		monitor = pyudev.Monitor.from_netlink(context)
		monitor.filter_by(subsystem="block")
		
		def event(action, device):
			if action == "add" and device.device_type == "partition":
				node = device.device_node
				partition = device.device_node.split("/")[-1]
				self.mount(node, partition)
			#elif action == "remove" and device.device_type == "partition":
			#	pass
					# either save the file for sync later bc the eject was probably
					# unintentional OR have no mercy and wipe it so that it doesn't
					# cause issues later
					
		self.observer = pyudev.MonitorObserver(monitor, event)
		self.observer.start()


	def mount(self, node, partition):
        path = f"{self.mnt}/{partition}
		if not os.path.exists(path):
			os.makedirs(path)
		subprocess.run(["sudo", "mount", node, path], check=True, capture_output=True, text=True)
        #check for hfs system. otherwise:
		if os.path.isfile(f"{path}/disk"):
			for file in Path(path).glob("*.dsk"):
                for slot in range(1:self.limit+1):
                    if self.disks[slot] is None:
                        temp_disk = Disk(file.name, path, slot)
                        shutil.copy(f"{path}/{file.name}", f"disk{slot}.dsk")

                        self.board.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
                        self.board.write(e.EV_KEY, self.pairs[slot], 1)
                        self.board.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
                        self.board.write(e.EV_KEY,self.pairs[slot], 0)
                        self.board.syn()
                        break
                break
		else:
			subprocess.run(["sudo", "umount", path], check=True, capture_output=True, text=True)
			
		
	def unmount(self, num):
        loaded_drive = self.drives[num]
        shutil.copy(f"disk{num}.dsk", f"{loaded_drive.mount}/{loaded_drive.filename}")
        subprocess.run(["sudo", "umount", loaded_drive.mount], check=True, capture_output=True, text=True)
        self.drives[num] = None
        os.remove(f"eject{num}")
		
if __name__  == "__main__":
	time.sleep(1)
	manager = DiskManager("/mnt/usb", 2)
	log = []
	
	while True:
		for program in psutil.process_iter(['pid', 'name']):
			log.append(program.info['name'])

		if "minivmac" not in log:
			manager.observer.stop()
            subprocess.run(["deactivate"], check=True, capture_output=True, text=True)
            #clear parent of mount directories
			sys.exit()
		else:
			log = []
        for file in Path(".").glob("eject*"):
            manager.unmount(int(file.filename[-1]))
		time.sleep(0.5)
