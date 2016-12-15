---
layout : "post"
title : "Chumby, revisited with Bittorrent Sync"
---


Remember the good-looking, ill-fated Chumby? The company went under on December 2011 and shut down their "cloud" services on February 2013, rendering all devices a dumb calendar widget making everyone sad.

If the Chumby were a closed device, this would have been so much entertainment you could get out of your $100. However, the story is quite different with the Chumby thanks to its openess. It's possible to swap the near-useless firmware of the Chumbies and flash new ones that amazing things: [offline firmware? check!](http://forum.chumby.com/viewtopic.php?id=7831) or [running webkit? check!](http://www.engadget.com/2012/05/31/developer-runs-webkit-on-chumby/) (my previous attempt),... 

After doing those amazing things, I still have several Chumbies laying around!

So here is my recent itch: I need an easy way to synchronize/automatically back up my data on my laptop and Android phone. However, I'm not yet buying the idea of backing up data to the "cloud" like Dropbox, especially with the PRISM scandal that just happened. But, my NAS is pretty NASty as it doesn't provide a braindead way to achieve the same functionality as Dropbox (Samba? I don't want to fight with configuring the automounter AND backup programs on every device I have! FTP? Who the hell uses FTP! Moreover, I don't want to VPN to my home network to sync files whenever I'm away). 

So recently Bittorrent labs came up with the Bittorrent Sync, which proved to be working really well for me -- it's the NO PRISM (supposedly?) version of Dropbox. So I wanted to get BT Sync to work on my NAS device. And it is proven to be impossible with my NAS to run due to the weak and incompatible CPU support. So what do I do? (drum roll...)

Introducing...

Chumby with Bittorrent Sync
---

So what is Bittorrent Sync? Basically it's a Dropbox clone that works (most of the time!) with your local storage. It syncs every file you have on every defined folder on every desired device. You would have to define what folders you want to get synched on every device and BT Sync will do the work.

I have hacked the interface so that I could monitor the traffic and stuff easily with the handy screen of the Chumby.

Read more [here](http://labs.bittorrent.com/experiments/sync.html)

![Sync](https://i.imgur.com/yEEKklZ.jpg)

So how do you get started? 

First, you will have to [clone my repository](https://github.com/htruong/chumbybt) with `git`. Then customize your WPA key and secret and if you want, define a NFS mountpoint as laid out in the `README` file. 

To the to get the Chumby to connect to your wireless network password just put in the password for your network on `network_config`. 

I exported my NAS to a NFS share and let the Chumby mount the NFS share. If you just have a USB flash drive or external drive, just plug it in the back of the Chumby, it will be automounted, so don't bother to modify the `nfsmount` file.

You need to change the web interface password by modifying `htpasswd` (google `htpasswd generator`).

Then, excute `./repack-update` to create the cusomized update package (oh if you want to do all this, better be on Mac OS or Linux!). Copy the update.tgz to a FAT32-formatted drive and press on the Chumby screen while turning it on, and upgrade the firmware as directed on the screen.

I created a webkit based interface (thanks to the previous hack I did) to monitor the status of bittorrent sync on the handy screen of the Chumby. Then, adding synchronized folders is as easy as going to `http://address-of-your-chumby/gui/` on your computer and define them (create them first on your HDD, as you can't create the synchronized folder on the fly yet), and then paste/scan the sync code with your other computers. For more information, refer to the BT Sync documentation.

![Yahoo!](https://i.imgur.com/mAJHQMi.jpg)

Voila! We now have a very pretty backup device. Very pretty, indeed.

So my Chumby could live a couple of years more.

PS: The Chumby has only wireless connection so it will be slow, but who cares, it's a back up device and it's done whenever it's done, right.

PS2: I didn't password-protect ssh on the chumby, so beware of that fact.

PS3: I really wished the BT Sync team opening up the application, or at least publish the protocol. It has been proven time and time again being open is so much better than being closed. If it hadn't been for being open, my Chumby would have been useless. And BtSync will also be useless if at some point the dev team stopped giving out new updates and new platforms emerge, which is really sad...

`Edited on 8:45PM CST 07/25/2013 for new updates I pushed on github.`
`Edited on 6:45AM CST 08/03/2013 for USB 1.1 misinformation.`
