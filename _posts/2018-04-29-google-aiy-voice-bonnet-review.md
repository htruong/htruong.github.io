---
layout: post
title: "Google AIY Voice kit and the Voice Bonnet Review"
---


I needed to investigate a good DAC solution for Crankshaft. So I couldn't be happier to see Google offering their AIY Voice kit that I can buy directly (and recommend people to buy) from Target. 

After two weeks working with it, here are my impressions:

- First, you can get it directly by going to Target. I can't be more pleased to have a piece of hardware that is virtually available in any town in the US.

- The kit is generally well put together. The board looks very high-quality. It's called the Voice Bonnet.

- The documentation is severely lacking. So extreme to the point that there isn't a single document detailing what each pin does on the HAT. This probably 
will be improved over time, but given what I saw for the v1: it was not great 
- not beyond the bare-bones. There were no schematic, even on an overview level.
There was no datasheet.

- The tutorials were easy to follow and worked just as expected. 

- There is nothing that is special about the hardware, it's just a DAC tacked on a RPi 0 HW. You can as well just get a DAC HAT/USB sound card and follow the same tutorials. You can do it by downloading their image on your RPi 0.

- Now for being a DAC, the kit price is reasonable for what you get in the box: A RPi 0 HW and a voice bonnet, and several other unimportant stuff.

- This is not open hardware.

- They have a stereo mic on the board, but you can't relocate them. They are not the electret type. You can't desoler to move them.

- The driver is open source and can be built as DKMS, but until I asked on Github, there was no indication whatsoever where the source is. For anyone who wonders the same, it's not published online, it's local on the Pi 0 image, `/usr/local/src` or something like that. Since it's GPLv2, I re-hosted it 
[here](https://github.com/htruong/aiy-voicebonnet-soundcard-dkms-driver).

- As with every Google product, there is no support other than the project on Github. I emailed the developer of the driver that has an 
@google.com address more than a week ago and received no replies. 
You can create issues and hope they will reply but seems like even an open source project will get better support than this... Not impressed.

- Another Google's attempt at making hardware. Google tried to make it sound like it's maker-friendly, and their intention was to promote "AI Yourself". 
However, by the way that it is executed, I'm not yet convinced. 
It sounds more like a gateway to Google's sound recognition API, 
there is nothing much to learn here. 
All you do is to send the voice data to Google and they return a 
transcription, or you send transcription and they send back voice data. You can't actually train anything. Everything is a black box. 

- You get free 60 minutes per month of the voice transcription API. 
If you actually want to do anything substantial with it, you can as well forget about it.

Overall, I think it's a nice piece of kit, works well, and is cheap, but for learning, it was more meh than I thought. If you want a DAC and don't care about the microphone input, I can actually recommend it.
