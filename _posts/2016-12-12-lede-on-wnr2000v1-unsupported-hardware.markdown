---
layout: post
title: Notes on getting LEDE/OpenWRT to work on WNR2000V1
published: true
---

State of the Union regarding custom firmwares for home routers
---

Custom firmwares are no strangers to home networking enthuasts. They offer several advantages compared to stock firmwares in many cases: Security, customizability, performance, and features -- all long after manufacturers abandon the routers.

Among the most popular are [DD-WRT](http://www.dd-wrt.com/), [Tomato/USB](http://www.polarcloud.com/tomato) and variants, [Gargoyle](https://www.gargoyle-router.com/) and [OpenWRT](https://openwrt.org/) (they have a new fork called [LEDE](https://lede-project.org), but more to that later). DD-WRT might be the most popular choice among those, and for the most part it works acceptably, but DD-WRT comes with limitations. I have been more than once frustrated by the inconsistency of DD-WRT: sometimes only a specific build works, sometimes you have to hunt for a specific version. Additionally, DD-WRT has no good, clear changelog, you have to dig through pages of discussion in the forums to get something working, and the list of problems go on. What it entails is you flash once and forget about it and never update your router. This is, for the most part, acceptable for a router, but is certainly annoying. Tomato has good user-interface, but is severly limited by the amount of hardware and features it supports.

Why OpenWRT/LEDE?
---

 OpenWRT, unlike everyone else, didn't strive to be simple initially. It was a fully-featured distro on a router, so it has everything imaginable, and it runs on practically everything. It might have been a good thing, I don't know -- but when I tried out years ago, it was clunky and unintuitive. As time goes by, I have to say that initial impression of mine is no longer valid. 

 OpenWRT is now an excellent choice lately when it comes to the software I really, really like and the intuitiveness has been solved for the most part. Some developers have switched to a new branch called LEDE, with the hope of better control on the code. Either way, *I have nothing but good things to say about the OpenWRT/LEDE project*. Among my favorite features about the project is stability. You can check out the latest trunk build of any router model at any time and be relatively confident that it works. I also like new advancements and algorithms being investigated and added every day by project contributors, such as anti-buffer bloat. What is buffer bloat? I have here is an excellent explanation for layman people, like me: [Bufferbloat - A plumber's view](https://www.youtube.com/watch?v=lQNSab8eCQ4}). In my case, those clever algorithms helped me a lot on my slow 5Mbps connection that is shared between roommates.

<amp-youtube
        layout="responsive"
        data-videoid="lQNSab8eCQ4"
        width="480" height="270"></amp-youtube>


WRN2000v1
---

Last weekend, my friend Andrew asked me to look at his router, an old WRN2000v1 he scrapped from another friend he intended to be a range extender. He [couldn't find a DD-WRT build](http://www.dd-wrt.com/wiki/index.php/Netgear_WNR2000V2) and was wondering if I could take a look. I, naturally, immediately suggest him to check out LEDE/OpenWRT. However, it is apparent that is is a [hard case](https://wiki.openwrt.org/toh/netgear/wnr2000). It is a relatively obscure router that no one cared about, especially now when it is 6 year old. I doubt even then it was that well supported. So I decided to take on the challenge of getting something decent on it.

First, I thought it was possible to load the firmware on it with a regular firmware upgrade and it turned out that I was wrong. Even the `telnetenable` script [mentioned in the wiki](https://wiki.openwrt.org/toh/netgear/wnr2000#flashing_modified_u-boot_and_pre-built_openwrt_on_wnr2000v1) doesn't work, for one reason or another, on our machine. So naturally I had to go home and get my good ole USB-to-TTL adapter -- one of the indispensable tools in my firmware tinkering toolbox. 

![The WNR2000v1 board with TTL cables hooked up](/assets/posts-images/2000v1board.jpg)

So after a couple of seconds looking around I was able to hook the TTL wires to the serial console of the router and was greeted with the root shell. Everything seemed well and couldn't be easier - I was able to get Backfire on the router shortly after following the directions on the wiki. I thought it was going to be smooth, but it turned out that it was just the beginning.

So with a normal OpenWRT device, it is often the case that once the user could get the initial firmware going for it, upgrade to newer versions is done easily by the upgrade firmware interface in the control panel. It turns out that it is not the case here, as the upgrader script doesn't know how to exactly deal with the upgrade files so it rejected everything, even on the command line. Moreover, there isn't a build for the device. So I tried to figure out how to upgrade the firmware manually.

MTD explained
---

It seemed like that the small flash memory (called the `mtd` - Memory Technology Device) is divided into several smaller partitions named `mtd*`, and there are two things that I flashed at the beginning to get Backfire to work: `mtd2` which contains the `rootfs` (root file system, literally where you mount `/`) and `mtd4` which contains the `uImage` (sort of the kernel and init scripts). So, my first reaction was to just write new images directly to the partitions by issuing the `mtd write` command of sorts. Writing new `uImages` always returned an error, and when I gave up and restarted the router, nothing could bring it to boot. 

I also figured out that writing over the boundaries of a partition will result in corrupting the next partition in the flash and will require a reinstallation of the whole firmware. After some more tinkering with `uboot`, basically the bootloader, I figure as long as I don't corrupt uboot, it is always possible to revert to the stock firmware by repartitioning and then, re-uploading the original firmware via TFTP, and then flashing Backfire by running the `install-repart.sh` script as pointed out by the wiki.

But then, it was apparent that the small 4MB flash chip was part of the problem. It realy, really doesn't help that the partitions for everything was really really small. Here is [what the partition map looks like on stock firmware](https://github.com/lede-project/source/blob/87f7ac6b4e6c3bd22c361ba24fd0de018edc1c61/target/linux/ar71xx/files/arch/mips/ath79/mach-wnr2000.c):

```C
{
	.name		= "u-boot",
	.offset		= 0,
	.size		= 0x040000,
	.mask_flags	= MTD_WRITEABLE,
}, {
	.name		= "u-boot-env",
	.offset		= 0x040000,
	.size		= 0x010000,
}, {
	.name		= "rootfs",
	.offset		= 0x050000,
	.size		= 0x240000,
}, {
	.name		= "user-config",
	.offset		= 0x290000,
	.size		= 0x010000,
}, {
	.name		= "uImage",
	.offset		= 0x2a0000,
	.size		= 0x120000,
}, {
	.name		= "language_table",
	.offset		= 0x3c0000,
	.size		= 0x020000,
}, {
	.name		= "rootfs_checksum",
	.offset		= 0x3e0000,
	.size		= 0x010000,
}, {
	.name		= "art",
	.offset		= 0x3f0000,
	.size		= 0x010000,
	.mask_flags	= MTD_WRITEABLE,
}
```

So... size is the problem ;-). We only have `1179648` bytes for the `uImage` and `2359296` bytes for `rootfs`. Given the latest trunk of LEDE (before 12/12/2016) has a `1354098` `uImage` and `1966080` bytes `rootfs`, this is not a good news. So we can either:

1. Find an old build that has a small uImage and rootfs
2. Find a way to shrink the images
3. Repartition the mtd so that the images fit?

1 is really not a wise choice -- no, I tried, and wasted a couple of more hours to it. 2 is almost impossible, unless we really, really want to apply a whole bunch of patches and such to LEDE. So choice number 3... how does it work?

The boot process of WNR2000v1
---

We can indeed repartition the `mtd` device. I learned as I worked with the WNR2000v1 is that, unlike PCs, embedded devices don't really have exactly the idea of dynamic partitions in the MBR like PCs -- *ain't nobody has space for that*. So *you have to tell the kernel where every partition begins and ends*. So how you tell it? Either it is hard-coded to the kernel like in the stock firmware, or in the LEDE case, via the bootloader. In this case, the bootloader is u-boot, an open-source bootloader. It has code running literally at the very beginning of the `mtd` devie (`u-boot` partition starts at `0x0`), and every of its settings is written flat on another partition (for example, what parameters it gives to the kernel) (`u-boot-env` starts at offset `0x040000`, so that is hard-coded into u-boot code at compile time). Das u-boot also oversees flashing the `mtd` device, and can load code over TFTP.

![You can interrupt u-boot by pressing any key at start-up](/assets/posts-images/uboot1.png)

On embedded devices, such as the WNR2000 here, flash devices have memory-mapped addresses. The first byte of the `mtd` (offset `0x000000`) is mapped to `0xbf000000` on the CPU. Thus, we can write whatever we want to the flash device, but we don't want to write anything before offset `0x050000` (`0xbf500000` memory-wise) because `0x00000` to `0x050000` is where our lifeline, u-boot, is. I learned, we want to preserve ART partition too (ART stores our device-specific information such as serial numbers, MAC addresses). So as long as our code and data fits in the offset `0x050000`-`0x3f0000`, everything should be okay.

Some other tidbits, so u-boot has a hardcoded "magic" value it would look to check to make sure that the code it is about to excute is indeed the kernel image, and that varies between one device and another (in the case of our board, it is `0x32303031` -- *Edit: later I learned that this version of the router does not check for the magic constant*). The compressed uImage has a kernel that starts at pre-arranged entry point `0x80060000`. The kernel will then figure out where all the partitions are by what is told by u-boot, then proceeds to mount them. It would also mount a squashfs that has some reserved space for an "overlay" which is a partition on top of the real partition to retain settings.

Building LEDE
---

I want to preserve space so I went ahead and built LEDE from source, it took about 3 hours or less on my laptop. The build script would go fetch, compile the cross compile toolkit and then proceeds to cmpile the kernel, ipgk packages and then put everything together. I would say given how complex the project is, the build system works perfectly the first time I tried it by following instructions, which is super impressive.

If you need a pre-built image for this router that has the web interface LuCi built-in, [head here](https://drive.google.com/drive/folders/0B8bRJIYStpVlZG13NEoyNGQ3a3M?usp=sharing). *Edit on 12/14/2016: As WRN2000v1 support is mainlined, you can download stock uImage and rootfs images on LEDE daily build website, but it won't have LuCi built-in*. You'll need two files: ar71xx-generic-wnr2000-rootfs-squashfs.bin (rename it sqfs.bin), and ar71xx-generic-uImage-lzma.bin (rename it uImage.bin).

So as we can see, the uImage won't fit into the old partitions, so we will need to expand it a bit. Luckily, as explained, the kernel won't have a problem adjusting to it. Given we have already flashed the modified u-boot as explained in the OpenWRT wiki, we can go ahead and flash the `uImage` and `rootfs` image by setting up a TFTP server and do the following while in the u-boot bootloader:

```
# Tell u-boot that we have a tftp server on 192.168.1.10
setenv serverip 192.168.1.10

# Tell u-boot that the router should take the address 192.168.1.1
setenv ipaddr 192.168.1.1

# Erase the region from 0x050000-0x3f0000
erase 0xbf050000 +0x3A0000

# Load sqfs.bin on TFTP server, and put it to memory address 0x81000000
tftpboot 0x81000000 sqfs.bin
# U-boot will tell you the length of sqfs.bin in hex, let's say ZZZZZZ
# Copy bit by bit 0xZZZZZZ bytes from offset 0x050000
cp.b 0x81000000 0xbf050000 0xZZZZZZ

# Same to the uImage.bin, write it right next to sqfs.bin
# Again, 0xYYYYYY is the length that tftpboot reports
tftpboot 0x81000000 uImage.bin
cp.b 0x81000000 0xbf2b0000 0xYYYYYY

# We need to tell the kernel what board it is booting into, and where to find the partitions
setenv bootargs "board=WNR2000 console=ttyS0,115200 mtdparts=spi0.0:256k(u-boot)ro,64k(u-boot-env)ro,3712k(firmware),64k(art)ro rootfstype=squashfs,jffs2 noinitrd"

# Tell u-boot where to find the uImage
setenv bootcmd "bootm 0xbf2b0000"

# Tell u-boot to save parameters to the u-boot-env partitions
saveenv

# Reset the board
reset
```

One nifty thing about the newer LEDE/OpenWRT releases is that we only have to tell it where to generally find rootfs and uImage (called the `firmware` region). We don't have to tell it where exactly to find any of those partitions.

![U-boot should look like this once you have set up everything correctly](/assets/posts-images/uboot2.png)

That's it... After about 24 hours, I was able to get LEDE to work wonderfully on my router. Looking back, there wasn't anything super-tricky, but there were a lot of things that got in the way. I hope my [pull request to LEDE](https://github.com/lede-project/source/pull/609) will be accepted and we will all see official support of LEDE for the WNR2000v1 board soon. **Edit 12/14/2016: [Now the board support is mainlined](https://github.com/lede-project/source/pull/611).**  If you need really detailed installation instructions, head to [The wiki](wiki.openwrt.org/toh/netgear/wnr2000) for more how-to information.

![LEDE up and running on my board](/assets/posts-images/2000v1bootup.png)

So that was not too hard! I hope this will inspire some of you to go ahead and port it to a new router and contribute to the LEDE project :) They have a [relatively strict standard for code submission](https://github.com/lede-project/source/pull/592), which is good for me to create good habits, though.


**Notes**:

- Don't try to upgrade from stock firmware with the factory image, this will make the router unable to boot. The factory image will flash over the stock control panel and will also flash over the emergency TFTP interface, but *it won't boot.* I know why, but I don't know how to fix it. There is an integrity check, but I sort of gave up after a day now -- it took me too much time and it is sort of a diminishing return.
- I figured out the reason that u-boot said that it see `bad magic` is that it expects the raw squashfs image instead of the squashfs filesystem with a magic number, unlike every other model in the WNR2000 series.
- The reason why we want to load the uImage at `0xbf2b0000` instead of `0xbf2a0000` (default for many devices) is that only then we have enough erase blocks for the `rootfs_data` partition (firmware settings). If we burn uImage at 0xbf2a0000, we won't be able to save any setting.
- It is still now impossible to upgrade via sysupgrade image.
