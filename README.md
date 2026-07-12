Minivmac Disk Helper

[Minivmac](https://github.com/minivmac/minivmac) is an excellent Macintosh emulator that suffers from one minor flaw: no support for physical, removable storage mediums. This helper script aims to change that.

Method:
Minivmac uses disk (.dsk) images formatted in hfs to load external software and files. This script create a pipeline that reads the data off of a storage medium, packaging it as a .dsk file, handles insert/eject activity, and writes the updated data to the medium.

Minivmac patches the system ROM to allow for a custom floppy driver to load. This helper script patches the this custom driver to create "flag" files to trigger ejects. It also uses the built-in "insert disk" hotkeys to mount disks in-emulator.

This script targets an x64 Linux system. This is for a couple of reasons:
 -less system overhead.
 -fine control over OS functions.
 -let's face it, if you want to emulate a mac, you're probably familiar with Linux already.
 
For dependency compatibility, install a Debian-based system.
- Determine if your desktop environment auto-mounts external drives. If it does, disable its ability to do so.	
- Alternatively, consider disabling the desktop environment entirely.

*todo*
 -Support 2+ drives: track drives, mount points, file names, disk # in emulator
 -Check for physical floppy on device mount: "drive" file or partition formatted as hfs
 -on exit, delete eject flag one last time
 -realistic vs mercy mode: on exit, copy disk files one last time?
 -floppy read mode: pick between dd or hcopy (recursive)

**Automatic Setup:**
[TBD]

**Manual Setup:**
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

