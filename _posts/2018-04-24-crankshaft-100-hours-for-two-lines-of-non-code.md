---
layout: post
title: "#4: 100 hours for two lines of non-code"
category: crankshaft
---


One of the challenges while making [Crankshaft](http://getcrankshaft.com/) was the amount of work that is not code. Basically, making Crankshaft means to answer emails, take care of the forums on Reddit, tag issues, documenting features, and getting people on board. It turned out that a feature that isn't well documented and no one uses is a waste of time implementing. So every time I created a feature, I had to spend just as much time testing. After that, I have to spend that amount of time writing about the feature, updating the wiki so users can understand and use it.

If commit is anything to be trusted as a quantitative measurement of the amount of work, then here is a primitive idea. I tried to tag every commit as either documentation or scripting/code or something neither, and it turned out I have made about the same amount of commits in each category:

```bash
htruong2@elsa:~/code/crankshaft$ git shortlog  | grep "\[docs\]" | wc -l
51

htruong2@elsa:~/code/crankshaft$ git shortlog  | grep "\[script\]" | wc -l
59
```

It has been really quite spectacular how time-consuming things can get. I just moved to a new city, so not so much to do, so I can afford to stay at home and work on Crankshaft in the weekend and at nights. 

Recently, there has been something quite itchy for me, that is to have a microphone solution for the Pi. The problem was that Google expects the car head unit to have a microphone, so they disable the phone's microphones input for the "OK Google" command. Although technically the phone can use its microphones, we can't expect Google to help us lifting that (artificial) limitation. The problem was that aasdk and OpenAuto are a reverse-engineered protocol and app. What will we say to Google? We made this Frankenstein totally-unauthorized reverse-engineered distro that sorts of encouraging people to DIY their car hardware so they can use Android Auto. It totally won't cause you PR troubles if anything happens to the users. Please help us by allowing the phone to take phone input for "OK Google" on Android Auto?

No. Of course we can't.

So, in short, we need to engineer a microphone solution of some sort for the head unit. The Pi doesn't have built-in support for microphones. So far, I have been suggesting people to buy a USB microphone/an expensive DAC. But that means we will waste one USB port to achieve the "OK Google" functionality. As a consequence, we can't use a Raspberry A+ and Zero either because we have to use the only available port for the phone connection, not the mic. The Pi A+/Zero are very low-powered compared to the others and does the work just fine, so it'd be a pity if we can never support them. 

Someone suggested on Hacker News to use a I2S microphone and I looked at it: it seemed like the perfect solution. The [Adafruit MEMS mic](https://www.adafruit.com/product/3421) is a very simple and cheap mic that works on the I2S bus. That I2S mic is $6 retailed, the Bill-of-Materials is probably around $2 and thus can be easily integrated into other boards. Except for the I2S solution has a known limitation: It has a very low volume input. The microphone would not produce volume level to an audible level. It needs a workaround called the [ALSA softvol](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-and-test) which boosts the volume to an acceptable level. I have also [documented the behavior here](https://github.com/htruong/snd-i2s_rpi). 

Too bad, the workaround doesn't work with applications that expect the microphone to work out of the box, and anything that uses PulseAudio doesn't work either. Without a configuration that works out of the box for PulseAudio, we can't say we support that configuration. Furthermore, we can't start designing a cheap hardware that will have the mic integrated.

I have tried to look at the kernel module code and see what I could do. I have looked at a number of other sound cards to see how they implemented it to fix it from the source -- and still got stuck. Along the way, I made the module DKMS-compatible and planned to push the code upstream to the Raspberry Pi kernel. I have bought additional DACs to see if I could learn anything from them and see if is there any way I could come up with a simpler/cheaper DAC hardware. I have asked for help from many sources. Nothing seemed to solve my problem.

At the last resort, I tried fixing `ALSA.conf` for 10 hours to make it take the "boosted microphone" as the default mic. It sort-of worked for ALSA programs, but it broke PulseAudio. Which means I got back to square 0.

Turns out I can neither easily fix the hardware nor the kernel driver nor `ALSA.conf`. It's just Pulseaudio that needs two lines of code for it to use the mic with boosted volume.

And after more than 100 hours, what I came up with was a solution that takes [only 2 lines of configuration](https://github.com/htruong/crankshaft/blob/master/hardware_support/adafruit_mems_mic/default.pa):

```
load-module module-alsa-source device=dmic_sv source_name=BoostedMic
set-default-source BoostedMic
```

Looking back, fixing Pulse seems like the obvious solution to take, but it didn't seem that way to me when I faced it. For me, to discover every single paragraph I wrote above, it took me at least 5-10 hours each. The hindsight is 20/20, and you can say someone who knows PulseAudio would know that's the obvious answer. But I didn't know PulseAudio - and I didn't know Linux asound driver development, Raspberry Pi, ALSA configuration, PulseAudio configuration and modules, I2S, MEMS microphone, Google Voice bonnet either. I had to learn all at the same time to come up with that answer.

I think judging the challenge of a problem by the number of lines of code or commits is a dangerous idea. There is code that can be cheaply produced and there is code that requires a lot of time to investigate. Usually implementing features is more exciting and less noble than fixing bugs. But to come up with a bugfix, it might take a surprising of patience and learning. For that two lines to be produced, I have spent around 100 hours and experienced two episodes of literal headaches. I have spent about a hundred dollars out of pocket to have two new pieces of hardware purchased. I have waited two weeks for the hardware to come. I have read pages and pages of manuals, from kernel driver code, dkms to ALSA. I have asked for help on tons of places from forums, Reddit, Github, emails. Only a few suggested what I already knew. No one knows that answer. 

Is what I've done code? I wouldn't call it code, it doesn't have any algorithm, it's just a configuration file. Regardless, I'm incredibly proud of those two lines. I have learned an incredible amount of stuff that are intricate to how every detail of in my issue fits together. 

I'm also very glad that I had the will to tackle the problem. I hope to carry that spirit along as Crankshaft is developed. 

And I wish my life had more blocks of hundreds of hours so I can work on problems like this. But I can never be so sure.