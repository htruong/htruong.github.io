---
layout : "post"
title : "Notes on installing Rollo/Beeprt CUPS driver for Raspberry Pi OS (Arm64)"
---

TLDR: If you just want your darn Rollo Thermal Printer to work and don't mind running some binary blobs from me with sudo permissions, then here comes the tarred driver: [`Rollo_arm64.tar.gz`](/downloads/Rollo_arm64.tar.gz). Just untar it, run `sudo ./install.sh`, then go to the CUPS admin interface, add new printer, pick the PPD file that you just extracted from this package. I also patched the PPD file to solve some typos from Rollo PPD definitions, you're welcome. 

If you want to not trust me with binary blobs, then read on.

The long explanation: If you encounter errors complaining about "Filter errors" while trying to get the Rollo USB Thermal Printer to work with your Arm64 Raspberry Pi, it's because Rollo [released the driver for Arm32 only](https://www.rollo.com/driver-linux/), without being explicit about the driver being 32-bit only. I suppose they released this driver some time ago when Raspberry Pi OS was 32-bit.

```bash
$ ./install.sh
$ tar xvf /tmp/Printer_ThermalPrinter.tar.gz
$ file Printer_ThermalPrinter/Filter/rastertolabel
Printer_ThermalPrinter/Filter/rastertolabel: ELF 32-bit LSB pie executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, for GNU/Linux 3.2.0, BuildID[sha1]=067e1c402edb5e3c8155ad3eeab240544b89ff74, with debug_info, not stripped
```

Too bad, `rastertolabel` is some hacked-together closed-source binary crap. After being confused for a while, I realized that proski [added the support for CUPS](https://github.com/proski/cups/commit/9ade138db4387ed016f70feb11a3b7a05daf04ca), but the patch [never got merged to mainline CUPS](https://github.com/michaelrsweet/lprint/issues/54).

So if you're looking for using the Raspberry Pi as a thermal print server, you should check out the cups driver from proski's CUPS repository, compile it, and use Rollo's PPD file in the closed driver's suite. Configuring and making the CUPS suite is quite normal and boring so I won't bore you with the details here, this is left as an exercise for you -- the readers.

Hope that saved you some frustrations with their driver situation. 

PS: Rollo is a good thermal printer, I have no problems with it. It has been one of my favorite tech items as I ship stuff for Ebay/friends from time to time and having it is very convenient. With this driver, I could print from my iPhone, which is very convenient.
