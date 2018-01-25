---
layout : "page"
title : "The Big, Growing List of Notable Hackable Devices"
hidetitle : true
comments: true
---

*Last revised: January 2018*

Here I try to maintain a list of consumer devices that are ubiquitous, cheap and have significant hacking values, many accidentally and unintended by the manufacturers. I tried to list all the devices that are still somewhat relevant to 2018 (i.e. still somewhat fun and useful), instead of just being historically interesting.

The advent of custom firmwares have pushed the capabilities and use cases of those devices to far beyond their intended original use, extending their life way beyond their official support lifetime.



## Laptops

### Acer Chromebook C720 (2013)

This laptop is cheap, runs cool, the battery lasts forever, and it runs every operating system ever. You can flash [coreboot](https://mrchromebox.tech/), an open-source UEFI BIOS for it and it will run Linux, Windows flawlessly, and even macOS. It is also extremely easy to open up. Virtually unbrickable.

### Thinkpad X200 (2009)

For the fans of truly-free BIOS. It runs [libreboot](https://libreboot.org/docs/hcl/x200.html) which has no binary blobs and it seems like the Management Engine can be partially disabled.

### The rest and resources

- [Other Thinkpads](https://libreboot.org/docs/hcl/)
- [Other Chromebooks](https://www.reddit.com/r/chrultrabook/). 
- **Where to learn more**: Search for Coreboot, GalliumOS, chrultrabook


## Routers

Routers are the exception to the norm. Most of the routers available on the market since 2002 seem to be capable of running custom firmwares and they usually don't have any protection against doing so. They make fantastic embedded Linux devices before Single Board Computers (SBC) such as the Raspberry Pi become mainstream.

### Linksys WRT54G (2002)

The router that started it all. It was sued for violating the GPLv2 license. Linksys had to publish the source code for the router, and the rest was history. It is still now being used and trusted by many many people, 15 years after its first release. It can run mesh network, has a huge ham fanbase, and has interchangable antennas. What's not to like?

### The rest and resources

- Everything that is supported by LEDE/OpenWRT. ASUS, Linksys, Netgear routers are notorously good about this.
- **Where to learn more**: Search for LEDE, OpenWRT, wikidevi, hackaday, ASUS merlin, tomato and derrivatives, Gargoyle-router.

## Game Consoles & Handhelds

### Sony PS3 (2006)

The PS3 was advertised as a console that can run Linux, and [could do some serious computing](PlayStation 3 cluster). Then Sony removed the functionality. Then people got mad and added it back again. Then some guy by the name Geohot got sued and [made a video for it](https://www.youtube.com/watch?v=9iUvuaChDEg). 

### Microsoft Original Xbox (2001)

The Original XBox is a x86 PC in disguise and has [a book dedicated to hacking it](http://hackingthexbox.com/). Even being a 16 year old system, it is probably still one of the best cheap readymade systems that you could buy for retro emulation. The Raspberry Pi is also a good emulation system, except for the cumbersome controller set-up.

### Other notable devices

- Sony PSP: Really good contender if you want a retro portable device.
- Nintendo Wii: Hackable and has cool games, but hardware was meh.
- Nintendo DS/2DS/3DS: Hackable.
- Microsoft XBox 360, Microsoft Kinect: Good support from Microsoft but limited applications.
- Nintendo NES/SNES minis: You can add more games and if you just need a console to play some NES/SNES games that you like, then you should have a look at them.
- **Where to learn more**: Ben Heck show. There isn't a central location for game console hacks afaik, just search *how to jailbreak yourgameconsolemodel*

## Development boards

### Expressif ESP8266 (201?)

It is less-than-$5 cheap, it has wifi and it is an Arduino. Now we're talking real values. My memory about this module is murky, but I think it was intended to be a dumb WiFi module initially, but people hacked Nodejs and Arduino later on to make it a microcontroller with WiFi built-in.

### Raspberry Pi 3 (2016)

Tried-and-true device for millions of makers worldwide, the Raspberry Pi 3 is the definite device to have if you want to start hacking. It does everything and runs everything.

### Arduino Uno (2010)

If you want to start with microcontrollers, just start with this one. It has a huge fanbase and developer community, and you could always find a project worth working on with the Arduino.

### The rest and resources

- Other Arduinos, esp. the Arduino Micro: They are just as good.
- Teensy: Good and small.
- Expressif ESP32: Designed to be good, but not as crazy of a hack as ESP8266 was.
- Raspberry Pi Zero W: Good choice if you want a cheap Raspberry Pi.
- [HC-05 and HC-06 Bluetooth modules](https://www.youtube.com/watch?v=BBqsVKMYz1I).
- **Where to learn more**: Hackaday, eevblog, [reddit](http://reddit.com/r/raspberry_pi), search for single board computers

## Smartphones and Tablets

I am quite reluctant to write about smartphones because there is a new phone released every day. So of course this is outdated the moment you read it.

### Google Nexus 5 (2013) and Google Nexus 7 (2013)

Supported by many third-party, obscure, crazy mobile OS projects, including Ubuntu Touch, Maru OS, Mobile Plasma. Of course, it is still powerful enough to run the latest version of Android as well.

### HTC HD2 (2009)

It was designed to run Windows Mobile 6 but it runs _everything_. So, if you want a phone that runs _everything_, then get the HD2. It is pre-historic in terms of age in the ever-evolving mobile world, but seems like this phone is just too good to not be mentioned. 

### The rest and resources

- Nokia N900: No longer available, and hardware is outdated.
- OnePlus One: Good but not crazily good. Has/had an active development community.
- Fairphone: Seems like the only phone that is designed to be opened up. So that's only fair to include them in here.
- HP Touchpad: No longer available, and hardware is outdated. But it was phenomenal years ago.
- iPhones: Can jailbreak but you can't generally update them.
- Motorola Droid: No longer available, and hardware is outdated.
- **Where to learn more**: XDA-developers 


## Miscleneaous devices

### Eye-Fi SD cards (?)

The small SD-card that runs Linux. It even has [a wiki](http://magiclantern.wikia.com/wiki/Eye-Fi) dedicated to hacking it.

### Canon cameras

They have an [open source firmware](http://www.magiclantern.fm) that adds tons of features to the cameras, such as interval shots and finer manual controls. If you have a point-and-shoot, [there is a firmware for it](http://chdk.wikia.com/), too.

### SanDisk Sansa Clip (2007)

It would have been otherwise a "no wireless, less space than a Nomad" device otherwise, but Rockbox transformed all that. Rockbox is an open-source firmware that allows your player to play every audio format imaginable. Also, who knows that [your MP3 player can run Doom now](https://www.rockbox.org/)?

### The rest and resources

- Other than Canon, [Nikon cameras](https://nikonhacker.com/), and [Sony cameras](https://github.com/ma1co/OpenMemories-Tweak) all have models that are hackable. 
- TI Calculators: They are expensive brand new but seems a pretty fun target if you find one at Goodwill or a garage sale for a cheap price. They aren't fancy by today's standards in terms of hardware, but apparently there are active communities to hack them.   
- Chumby/Insignia Infocast 3: Good but outdated hardware, and it is no longer available. I have a lot of fond memories and good things to say about the Chumby. bunnie is a great person.
- Everything supported by Rockbox: Could be dicey.
- **Where to learn more**: Hackaday, rockbox wiki, other wikis.

## My personal gear

As I get older, I tend to choose a more popular/widely supported device over a more performant but less widely supported device when it comes to firmware hacking. The amount of time I have to spend figure stuff out like toolchains and such can be much better spent optimizing the software, given the hardware can meet it.

- I have a lot of **Raspberry Pi Zero W**s: It is slow, it might be unreliable, its one USB port is picky, the built-in audio is bad, it has some proprietary blobs, but who cares? The Pi Zero W is good enough, easy enough, cheap enough, versatile enough for many applications. It enables me to do a lot of things that I would otherwise not bothered to do. It is probably my favorite device of all times to hack on.
- **Arduino Uno** for certain applications, especially considering robotics. It is well supported, predictable, easy to transfer, easy to debug. I personally have the *Electron Asset tracker* and I haven't seen a board that is so well designed, documented and polished.
- **Dell Chromebook 13** for personal laptop. It runs coreboot without the main ME modules.
- **Netgear R6100** for my home WiFi router. It's fast, cheap and has plenty of RAM and NAND storage.
