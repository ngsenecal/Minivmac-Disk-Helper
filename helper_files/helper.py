from pathlib import Path
import subprocess
import psutil
import shutil
import pyudev
import time
import os
import sys

# Create helper function that checks for a file. If the file does not exist after x iterations
# return False and let the parent function determine what to do

class Disk:
	def __init__(self, filename, node, mount, number, filesystem, v_drive=None):
		self.filename = filename
		self.node = node
		self.mount = mount
		self.number = number
		self.v_drive = v_drive
		self.fs = filesystem

class DiskManager:
	def __init__(self, mnt, limit):
		#self.board = UInput()
		self.disks = {1: "SYSTEM", 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}
		self.mnt = mnt
		self.limit = limit
		# self.pairs = {1: e.KEY_1, 2: e.KEY_2, 3: e.KEY_3, 4: e.KEY_4, 5: e.KEY_5,
		# 			6: e.KEY_6, 7: e.KEY_7, 8: e.KEY_8, 9: e.KEY_9}
		self.observer = None
		self.detection_init()
	
	def detection_init(self):
		context = pyudev.Context()
		monitor = pyudev.Monitor.from_netlink(context)
		monitor.filter_by(subsystem="block")
		
		def event(action, device):
			if action == "add" and device.device_type == "partition":
				node = device.device_node
				filesystem = device.get("ID_FS_TYPE")
				self.mount(node, filesystem) # for rootless, only node is required
			elif action == "remove" and device.device_type == "partition":
				pass
				# loop through the dictionary and try to match mount points
				# either save the file for sync later bc the eject was probably
				# unintentional OR have no mercy and wipe it so that it doesn't
				# cause issues later
		self.observer = pyudev.MonitorObserver(monitor, event)
		self.observer.start()


	def mount(self, node, filesystem):
		if filesystem == "hfs":
			subprocess.run(["dd", f"if={node}", "of=./disk3.dsk", "bs=512" ], check=True, capture_output=True, text=True)
		else:
			cap = subprocess.run(["udisksctl", "mount", "-b", node], capture_output=True, text=True)
			path = cap.stdout.split()[-1]
			if os.path.isfile(f"{path}/disk"):
				file, slot, num = None, None, None
				for temp in Path(path).glob("*.dsk"):
					file = temp
					break
				for val in range(1, self.limit+1):
					if self.disks[val] is None:
						slot = val
						break
				shutil.copy(f"{path}/{file.name}", f"./minivmac/disk{slot}.dsk")
				#os.chmod(f"./minivmac/disk{slot}.dsk", 0o666)

				# self.board.write(e.EV_KEY, e.KEY_F5, 1)
				# self.board.write(e.EV_KEY, self.pairs[slot], 1)
				# self.board.write(e.EV_KEY, e.KEY_F5, 0)
				# self.board.write(e.EV_KEY, self.pairs[slot], 0)
				# self.board.syn()
				subprocess.run(["ydotool", "key","-d", "1", "63:1", "3:1", "63:0", "3:0"])

				i = 0
				while i < 10:
					temp = []
					for insert in Path(".").glob("insert*"):
						temp.append(insert)
					if len(temp)> 0:
						num = temp[0].name[-1]
						break
					else:
						i += 1
						time.sleep(0.1)
				if num is not None:
					os.remove(f"./insert{num}")
					self.disks[slot] = Disk(file.name, node, path, slot, filesystem, num)
				else:
					subprocess.run(["udisksctl", "unmount", "-b",  node])
			else:
				subprocess.run(["udisksctl", "unmount", "-b",  node])
			
		
	def unmount(self, num):
		for key in self.disks:
			if self.disks[key] is not None and key != 1:
				if self.disks[key].v_drive == num:
					drive = self.disks[key]
					if drive.fs != "hfs":
						if os.path.isfile(f"{drive.mount}/{drive.filename}"):
							shutil.copy(f"./minivmac/disk{key}.dsk", f"{drive.mount}/{drive.filename}")
							#os.chmod(f"{drive.mount}/{drive.filename}", 0o666)
							subprocess.run(["udisksctl", "unmount", "-b", drive.node])
						self.disks[key] = None
						os.remove(f"./minivmac/disk{key}.dsk")
						os.remove(f"./eject{num}")
					else:
						pass
						##Floppy specific code
		
if __name__ == "__main__":
	for file in Path(".").glob("eject*"):
		os.remove(f"./{file.name}")
	for file in Path(".").glob("insert*"):
		os.remove(f"./{file.name}")
	for file in Path("./minivmac").glob("disk*"):
		if file.name != "disk1.dsk":
			os.remove(f"./minivmac/{file.name}")

	time.sleep(1)
	manager = DiskManager("/mnt/usb", 2)
	log = []
	
	while True:
		for file in Path(".").glob("eject*"):
			manager.unmount(file.name[-1])
				
		for program in psutil.process_iter(['pid', 'name']):
			log.append(program.info['name'])

		if "minivmac" not in log:
			manager.observer.stop()
			#clear parent of mount directories?
			sys.exit(0)
		else:
			log = []
		time.sleep(0.5)
