---
layout : "post"
title : "Notes on running Ubuntu Linux the Thinkpad X1 Nano"
---

I received the Thinkpad X1 Nano last night and wiped Windows to install Ubuntu. I was too lazy to install Ubuntu from scratch so I used [CloneZilla](https://clonezilla.org/) to transfer the current Linux I have on the Dell XPS laptop I have to the new laptop.

For the new cloned laptop to boot, you will need the Secure Boot in the UEFI setup interface to not be in the "customer" mode. The Thinkpad X1 Nano is using the 11th Generation Intel chipset so you'd need a new Linux kernel for it to boot. As the Dell XPS laptop I have is already running 5.10 so I did not have to do anything extra. The laptop just booted. It looks like we don't have yet 5.10 as of Jan 2021 in Ubuntu 20.04, so I just installed `5.10.0-1008-oem`.

Audio works out of the box, but the volume control doesn't. So to fix that, edit `/usr/share/alsa/ucm2/sof-hda-dsp/HiFi.conf` [as if you're working on the X1 Carbon 7th gen](https://www.sysorchestra.com/linux-mint-20-upgrade-on-lenovo-thinkpad-x1-carbon-7th-sound-and-fingerprints/), except don't change `Speaker` to `Master`, change it to `PGA1.0 1 Master`. You're all set!

For the fingerprint reader to work, you can refer to the same post on sysorchestra above. That's one item that I didn't expect it to work but it did!

Please let me know if it works for you.

![Thinkpad X1 Nano Gen1](/assets/posts-images/thinkpadx1nano.png)
