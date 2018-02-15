---
layout: post
title: EzPi4ME - Getting rid of the Intel ME, for mere mortals
---

_The easiest, and most straightforward method to get rid of the Intel ME._

This project helps you create a Raspberry Pi image that can clean the 
Intel ME blob from your machine. In other words, "me-cleaner for dummies."

[Github project where you can download it](https://github.com/htruong/ezpi4me/).


What is the Intel Management Engine/Intel ME?
--

It's a binary blob on your firmware in the flash chip. It's a software that runs
independently of the main CPU on a co-processor/microcontroller on the PCH.
Intel ME runs even when the machine is off, 
and before anything on your machine with the highest ring permission. It can access
anything on your computer. It does a lot of (good?) things, but no one knows exactly 
what the Intel ME is capable of.

[It is a modified version of MINIX](http://www.cs.vu.nl/~ast/intel/).
[One good overview is here](https://hackaday.com/2017/12/11/what-you-need-to-know-about-the-intel-management-engine/).


What exactly does this process do to eliminate the Intel ME?
--

The ME firmware is very big, so the code doesn't reside on the coprocessor hardware. The firmware has to be fed to the coprocessor from somewhere. That somewhere is, in practice, a region of the flash chip of the computer. The ME firmware takes something like 512K-3MB in that 8MB chip. There is a hardware watchdog on the coprocessor that checks if the operation of the ME firmware after the computer is "on" for half an hour. If it realizes that the ME is not operational at all, it will reset the CPU. When the firmware runs, it sets certain (hidden/privileged) registers or memory values to the correct values signaling to the watchdog that it's operational, and thus makes the hardware watchdog happy.

The problem is you can't just feed the coprocessor a totally bogus ME code. Before the coprocessor runs the code, it will check certain signatures and if the signature doesn't match, the coprocessor won't run it. The me-cleaner software changes the firmware in a clever way: the botched code still passes some minimum security requirements, the coprocessor still executes it, and it still flags the ME as somewhat operational, and thus the watchdog is still happy.

Now the layout of the firmware has also one more tidbit. On the firmware, you can mark a certain critical regions of the chip to be read-only, to prevent that region from ever be written on. In the factory firmware, the ME region is often marked as read only, that's why you can't just change the ME firmware from the machine itself (even when you can update and flash a new firmware from the machine itself).

In short, an analogy of that that is like you can't install and run the anti-virus from an infected computer - if the virus itself is smart enough, it could prevent any anti-virus being run. You'd have to start with a clean computer, and plug the infected HDD in, and clean it from there. The Raspberry Pi is acting as the "clean" computer to clean the virus here.


Why did I do this? 
--

I want to make me_cleaner more widely accessible. 
Freedom from binary blobs shouldn't be hard or expensive.

This is after a person told me, "you need to make it easy for us mere mortals."

One doesn't need to be an electrical engineer to do be able to clean 
the ME on your computer. Now you just need to run some simple commands and connect 
6 wires to a Raspberry Pi. Bam, 10 minutes, done.

I've been thinking about this project for over a year, but prototyping was easy 
because I can just carry a customized Pi image with me. Now, to release
to the public the source and customization process, there is a lot of scripting
needed (because what's the point of advocating removing the 8MB Intel ME blob 
by releasing a 2GB blob and tell everyone to run it). I finally got up my butt 
and did it. Every script is extremely simple and can be audited quickly.


Beware
--

**Remember, that ultimately you're responsible for trying this with your machine.**
I can't guarrantee that it will work. I can't guarrantee that what I told you to do 
won't fry your $4000 laptop. I wrote it the whole thing in ten hours. 

That being said, I have put every safeguard I could think of and made this process
as simple and clear as possible. As long as you don't fry your chip by connecting
a 1.8V chip to the 3.3V Raspberry Pi, the process is entirely undoable.


Instructions
--

[Please view the detailed Instructions on Github](https://github.com/htruong/ezpi4me#instructions).

All you need are the following components:

![Raspberry Pi 0 WH](https://i.imgur.com/OcKklYys.jpg)
![Female2Female](https://i.imgur.com/SOQtFips.jpg)
![SOIC clip](https://i.imgur.com/ovZ6Ao0s.jpg)
![MicroSD](https://i.imgur.com/qwgiGlJs.jpg)

You'll need to **MAKE VERY SURE** the chip in your machine is 3.3V.

![Connect](https://i.imgur.com/a9rcEy6.jpg)

EzPi4ME provides the following tools:

    $ sudo ezpi4me-check-chip  <-- checks if you see the chip
    $ sudo ezpi4me-rom-backup  <-- backs up the current ROM from the chip
    $ sudo ezpi4me-rom-clean   <-- cleans the ME from the ROM
    $ sudo ezpi4me-rom-reflash <-- flashes it back to the chip

After you ran those commands, the "target" computer will be free of Intel ME.

![Command line](https://i.imgur.com/fATqixY.png)


Chromebooks specifics
--

[Please view the Chromebook directions on Github](https://github.com/htruong/ezpi4me#chromebooks-specifics).


FAQs
--

[Please view the FAQs on Github](https://github.com/htruong/ezpi4me#faqs).

