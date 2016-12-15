---
layout : "post"
title : "Making the Adafruits thermal printer print anything from anywhere"
---



The [Adafruits thermal printer](http://www.adafruit.com/products/597) is the [_most cutest printer in the universe_](http://www.youtube.com/watch?v=32FB-gYr49Y).

![BT printer](/assets/posts-images/bt-printer.jpg)

I would like to use it to print everyday trivial stuff easily, like a memo or a shopping list. However, I was unable to. There were several big problems with it:

1. There was no "driver" for it on my computer, thus making printing impossible.
2. Even there was one, I hate connecting the cable to my laptop just to print one.
3. I would like to eventually be able to print to the printer from my Android phone/iPhone.
4. Technically you can write a program based on adafruits' sample code, but it's a pain to write a program for each specific script I want to have output with formattings and graphics.

So the idea that popped up to my mind was to make the printer wireless and write a driver or it so that it accepts pseudo-HTML formatting, so I can pipe stuff from the command line and scripting languages to it from _anywhere_ without connecting the wires. 

This post will guide you to making this little printer wireless and print trivial stuff with formatting.

If you just want to talk to the printer via serial and you don't care about making it wireless (i.e. you would it to a USB-to-TTL adapter), you can skip the next section.


Making the printer wireless
---

The obvious choice to me was to use bluetooth as my computer, the Android phone and the iPhone all have bluetooth. Wifi seems overkill and expensive.

So having a spare HC-06 bluetooth module (which goes for $6) laying around, I tried to connect the bluetooth adapter to the printer.

In case you need a pinouts and reference for the HC-06, [this is all you would need to know](http://www.micro4you.com/files/ElecFreaks/Bluetooth%20HC-06.pdf).

Before we do that, as the printer work at 19200baud instead of 9600baud we would need need to configure the bluetooth adapter to work at 19200b. I connected the bluetooth adapter to a [USB-to-TTL adapter](https://www.tindie.com/products/jimparis/microftx-usb-serial-breakout-1/). Only the RX-TX-GND-+3V wires need connected to get the bluetooth adapter up and running. Then `sudo screen /dev/ttyUSB0 9600` will connect to the adapter AT interface and we're ready to configure it.

All we have to do is to paste (not type!) `AT+BAUD5` to the screen. It should reply back `OK19200`.

Now it's all easy. The HC-06 connection to the printer is really trivial, I just connected the +3V to some power source, and the two TX-RX pairs of the printer to the respective RX-TX pair of the bluetooth module.

Connecting the printer to the computer wirelessly
---

On Linux there is an utility called `rfcomm` that helps you create a virtual node in the `/dev/` tree. All you would have to do is to figure out the address of the bluetooth adapter:

	$ hcitool scan
	Scanning ...
        XX:XX:XX:XX:XX:XX       WasabiBluePrint

Note down the address, then edit `/etc/bluetooth/rfcomm.conf` so it looks like so:

	rfcomm0 {
        bind no;
        device XX:XX:XX:XX:XX:XX;
        channel 1;
        comment "WasabiBluePrint Serial Bluetooth";
    }

Then every time you need to connect to the printer, invoke:

	$ sudo rfcomm connect 0

Writing a HTML compiler
---

So the rest of the work is to write a compiler to communicate with the printer -- specifically, compile pseudo-HTML to the printer commands, and then take care of the timings and stuff. I have written such an utility and you can [download it here - v1.0.0 linux/Intel 32 and 64 bit/ARM](/downloads/serialprinter_1.0.0.tar.gz). It's currently closed source (sorry!), but I have a plan that will eventually free you up from having this annoying binary blob.

The ultility is supposed to take minimal resource and can be chained with another program (UNIX philosophy anyone?).

The simplest use case is to print something to it directly:

	$ echo "Hello world!" | sudo ./serialprinter64 -s /dev/rfcomm0

The sudo part isn't necessary if you have already set the permission of `/dev/rfcomm0` correctly, which I haven't done in my case. The `-s` switch tells the program to work in the "simple" mode, where it will automatically adds the HTML headers (the pseudo-compiler uses the header to initialize the printer, so you will need it).

You can print more exciting stuff too (the `out.print` sample file is included in the download package above):

	$ cat out.print | sudo ./serialprinter64 /dev/rfcomm0

Here comes the video for your viewing pleasure:

<amp-youtube
        layout="responsive"
        data-videoid="P8KgEC--LBE"
        width="480" height="270"></amp-youtube>


Having a controller or not having a controller
---

My long term plan is to write a compiler that is embedded into a microcontroller so that all you will have to do is sending the HTML to the bluetooth serial interface. This isn't hard given what I have done, but I have a bunch of work to do in school and stuff.

This will allow easier integration to other devices such as mobile devices too. Stay tuned.



Printing Google two-factor authentication backup code to put into your wallet has never been so easy (don't hack me bro):

![My Backup code](/assets/posts-images/backup-codes.jpg)
