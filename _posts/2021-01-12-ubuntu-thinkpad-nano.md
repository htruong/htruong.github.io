---
layout : "post"
title : "Notes on running Ubuntu Linux on the Thinkpad X1 Nano"
---

I received the Thinkpad X1 Nano last night and wiped Windows to install Ubuntu. I was too lazy to install Ubuntu from scratch, so I used [CloneZilla](https://clonezilla.org/) to transfer the current Linux installation the Dell XPS laptop that I was using to have to it.

For the new cloned laptop to boot, I had to set the Secure Boot in the UEFI setup interface to not be in the "customer" mode. The Thinkpad X1 Nano is using the 11th Generation Intel chipset so it needs a new Linux kernel. As the Dell XPS laptop was already running 5.10 so I did not have to do anything extra. The laptop just booted. For reference, I installed `5.10.0-1008-oem` kernel.

Audio worked out of the box, but the volume control didn't. So to fix that, I edited `/usr/share/alsa/ucm2/sof-hda-dsp/HiFi.conf` [as if you're working on the X1 Carbon 7th gen](https://www.sysorchestra.com/linux-mint-20-upgrade-on-lenovo-thinkpad-x1-carbon-7th-sound-and-fingerprints/). The only difference to make it work with the X1 Nano is that instead of changing `Speaker` to `Master`, I changed it to `PGA1.0 1 Master`.

For the fingerprint reader to work, I also followed the same post in the link above. That was one item that I didn't expect it to work, but it did!

Please let me know if it works for you.

![Thinkpad X1 Nano Gen1](/assets/posts-images/thinkpadx1nano.png)
