Minivmac Disk Helper
-
[Minivmac](https://github.com/minivmac/minivmac) is an excellent Macintosh emulator that suffers from one minor flaw: no support for physical, removable storage mediums (floppy drive, USB drives, etc). This tool aims to change that by creating a pipeline that reads the data off of a storage medium, packages it as a .dsk file, handles insert/eject activity, and writes the updated data back to the medium.

*-  How Does This Work? -*
Minivmac patches the system ROM to load a custom floppy driver further modifies this custom driver to create "flag" files for insert and eject events. The Python script is able to emulate a keyboard and use the built-in "insert disk" hotkeys to mount disks in-emulator. USB events are monitored for storage devices containing a blank file named "disk" and a .dsk file. 

This script targets an x64 Debian-based system. This is for a couple of reasons:
- Less system overhead.
- Fine control over OS functions.
- If you want to emulate a mac, you're probably familiar with Linux already.

*-   TODO -*
 - [ ] greaseweasle support
 - [ ] fdd@1306 IC support (dd)
 - [x]  Multi-drive support: track drives, mount points, file names, disk # in emulator
 - [ ] Disable keyboard hotkeys for disk insertion to prevent accidental double inserts 
- [x] Clean all flags on exit
- [ ] Mercy mode: on exit, copy disk files one last time

**Before You Install:**
- Check that you are running an x64 Debian-based system.
- Make sure you have root access.
- Determine if your desktop environment auto-mounts external drives. If it does, disable its ability to do so.	
- Disable pop up notifications and/or notification sounds in your system settings. Anything that takes focus away from the emulator will break support.

**Automatic Setup:**
1) Download installer.sh from the Releases page.
2) Move installer.sh the directory you want to install in.
3) Run installer.sh. You will require root privileges.
4) Transfer a Mac II ROM and an OS disk to the minivmac folder.
5) Launch start.sh from the terminal. You will need root.


**Manual Setup:** [Under construction]
1) Update your system:`sudo apt-get update  && sudo apt-get upgrade`.

2) Install dependencies:
a) `sudo apt-install libsdl2`
b) `sudo apt-install make`
c) `sudo apt-install gcc`
d) `sudo apt-install git`

3) Navigate to a directory of your choice and place the corresponding machine ROM and system disk file that you are building for. Name the system 

4) Clone minivmac from Github: `git clone https://github.com/minivmac/minivmac`.

5) Clone Minivmac-Disk-Helper to the same parent folder as the minivmac folder: `git clone https://github.com/ngsenecal/Minivmac-Disk-Helper`.

6) Copy "Minivmac-Disk-Helper/helper_files/SONYEMDV.c" into "minivmac/src" and overwrite the file.

7) Edit "build_linux.sh": `sudo nano minivmac/build_linux.sh
`. Configure the emulated mac to your specifications, but these settings must me included:
a)  `-drives 2 \` :  Locks the maximum number of mountable drives to 2 - internal (OS) and external.
b) `-iid 1 \`:  Enables "insert ith disk." When the control key (ctrl by default) and a number key is held, minivmac searches its folder for "disk{#}.dsk. So ctrl+5 would search and insert disk5.dsk.
c) `speed z \`:  (not required, highly recommended). Locks emulation speed to 1x, the original speed of the emulated machine.

8) Build minivmac: `./build_linux.sh`.

9) Run minivmac: `./minivmac`. It may complain about how you named your ROM file. Rename it and relaunch minivmac.

