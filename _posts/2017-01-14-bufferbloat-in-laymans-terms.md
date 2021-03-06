---
published: true
title: 'Bufferbloat in layman''s terms and router hacking, 101'
layout : "post"
---


TL,DR: If you play games or do voice/video chat, then the latency figure is what you need to pay attention to instead of the bandwidth figure. If the connection to your router is consistently good, yet your internet seems slow at unpredictable times, then you might have the symptom so-called bufferbloat. You will need to setup a thing called Smart-Queue-Management on your router. You will have to install a third-party open source software called LEDE, because no router on the mass market right now has it installed by default.

## What is bufferbloat, why is it bad? Why does my game lag? Why do my "internets" suck so much?

Bufferbloat is the problem where one intensive traffic user or program (for example, BitTorrent or Netflix, or the Windows update that runs silently in the background) makes every other user and program miserable. You probably have suffered it at least once: your game lagged like crazy or your web page decided not to load when you or your roommate had a download or BitTorrent happening in the background. I used to think that it is normal to have a game lagging when I download something via BitTorrent because of the number of connections that it makes. It turned out that we all don't have to suffer that.

An analogy is like the time you went to a supermarket/Wal-mart to buy a pen, and had to wait 15 minutes to check out the pen because all the checkout lanes have queues of people with carts full of stuff in front of you. 

In many ways, games and voice chat need stuff delivered quickly and can be thought of as people needing to check out pens as quickly as possible. Programs streaming movies or downloading data could also be thought of as the people with big carts - and they don't care as much about the time they have to wait.  

![Install the software](/assets/posts-images/Simpsons-Express-Line.jpg)

## Is my internet connection not fast enough?

You will probably conclude that your connection is not fast enough -- and that's a good misconception that your ISP hope you to have so you will buy a faster internet package from them. Just throw more money at the problem. 

![Throw more money at it?](/assets/posts-images/throw_money_at_it.jpg)

Sadly, it is *often a misguided idea*. Here, throughput is mistaken for latency. Latency can be thought of as the time you have to wait before you check out your pen, and throughput is how fast you can walk out with your pen once you start checking out. They are somewhat related, but not quite the same thing. Hiring better people that can check out stuff much faster will help remedy the problem, though. For example, think of hiring faster people that can scan stuff twice as fast (!!!) will help to reduce the wait time for you to check out the pen from 15 minutes to, say, 8 minutes. If you have Amazon-style machines that can tell how much the bill is without scanning anything, then the wait time will be much faster, but they are an expensive solution (that's what we have with a gigabit fiber optics connection). In other words, you don't want your grandma working in the checkout line (56k dial-up connections suck for sure), but hiring Amazon to tag every item so that everything automatically checks out itself is overkill.

**Usually people get upset about how long they have to queue instead of how fast they can check stuff out.** The same thing happens to the internet, programs and people often get upset about latency instead of throughput. 

Contrary to popular beliefs, a good gaming experience doesn't require lots of bandwidth. This is because it doesn't take much bandwidth for the computers to communicate information, such as I'm firing from the position 100,100, with an angle of 30 degree to the north. It takes 3 bytes to do so, when your pre-historic 56K modem can transfer freaking 7,000 bytes a second. In games and voice chat, all that matters is latency. Slower connections do not mean higher latency. In fact, Skype voice calls many games such as StarCraft and Half-life: Counter Strike worked fantastically, and probably still do with a dial-up connection (that is, literally, 100x slower than your typical connection). 

Better throughput only helps when you check out many items very often, i.e. download lots of movies. Streaming movies doesn't count -- it only counts if your connection is slower than what the streaming requires which is often a low bar to pass (Netflix only requires 5Mbps for Full HD). It works the same way in real life, as long as the salesperson can check out faster than people can buy stuff, which is often the case, then hiring faster salespersons won't make the queues go away. If your internet connection is faster than what you need and it still sucks, then you probably suffer from the same problem.

For anyone who managed to read this far -- you might think that there are far better solutions than spending money hiring faster checkout people: Correct. If you just have a lane that says "express checkout" for people with 5 items or less and another that says "bulk checkout" for people with 100 items or more, then we have solved the problem of the person with the full cart making the people with just a pen wait. In other words, allocating queues differently without having to hiring faster people is a better solution here. That was what earlier algorithms tried to do - if you classify yourself as express checkout, then you don't have to wait in the normal lines. The problem was that programs aren't good at classifying themselves (sometimes they don't know beforehand how many items they have in their cart, in real life, people keep buying snack bars on the way out), and it is not clear from the start how many types of lines we should have, and the system is easy to abuse, because everyone wants to be in the express line. 

To remedy that problem, newer and fancier queueing algorithms are much better at controlling the queues, for example, they know how to allow people to drop out of the line after waiting for some time. All in all, you can see this becoming the managing the queues efficiently problem rather than the scanning the barcode fast problem. Think of a having a good algorithm as hiring smart people that handle the queue and tell people where to queue, rather than spending money hiring faster people and buying expensive machines to scan stuff.

**Bufferbloat is essentially "letting too many people queue," which essentially means "proning to lags," and reducing bufferbloat is "shortening the queue."** Bufferbloat happens when you have big jobs interfering with the small jobs so the small ones can't get through quickly. 

The easiest way to tell if you have bufferbloat is to do a speed test while having a ping window open -- you can ping any "website" (more technically, IP address), for example, `ping -t google.com`. If you see a much smaller ping than when you do with a speed test going on, then you have it. Pings are just one of the smallest packages you can send to Google and Google will reply back to you as soon as they hear it. If the ping figure is high, it means that the information from Google takes a long time to come back to you. When it's only high when you have a upload or download, it means that you have bufferbloat. As you can see here my pings took a 400ms hike in lags when there was an upload job going on vs. a 30ms when the upload job is done:

<amp-gfycat data-gfyid="VibrantWetDogfish"
  width="640"
  height="360"
  layout="responsive">
</amp-gfycat>

### Come on, don't just preach. What does that entail?

So you think instead of spending money on a faster connection, you should have something that handles the queues efficiently. Bing bing bing! You're absolutely correct.

Do you need a gaming router, though? No, by "good," I don't mean expensive, and expensive "gaming routers" often weasel words for routers with marked up prices.  Good means it can be "hacked" to run good software, such as OpenWRT and LEDE (for a more technically inclined audience, you might have heard of DD-WRT and Tomato formware, they are the same breed, just that OpenWRT/LEDE are more technically flexible and advanced.)

OpenWRT/LEDE has algorithms that help you combat the latency aka handling the queues, such as CoDel of Cake. As far as I know, no consumer router, no matter how expensive, has those algorithms installed by default yet. OpenWRT and LEDE are the software programs that you can install to replace the "dumb" software that does the queue management that is installed by default on your router. It is free and open-source and I am among thousands of programmers and research scientists contributing to it daily to make a really, really good piece of software. It is very smart, although getting it to work on your router could be somewhat hard if you have never done it before.

First you need to buy a router that supports OpenWRT/LEDE. **The exact model matters** -- [buy one that is listed here](https://lede-project.org/toh/views/toh_available_864), don't go to Wal-mart or BestBuy and buy a random model and then complain that it doesn't work. If you have less than a 100Mbps connection, then an old Netgear WNDR 3800 for $20 will do the job fine, and I recommend it. Reprogram (or "flash") the router with OpenWRT/LEDE -- all you have to do is going to the original web control panel and upgrade the firmware with the "factory" firmware (I personally recommend LEDE, [download here for the WNDR 3800](https://kau.toke.dk/lede/airtime-fairness-builds/ar71xx/generic/)). 

After you have all those done, go to the control panel, go to System>Software, then install the `kmod-cake`, `sqm-scripts`, `sqm-scripts-extra` and `luci-app-sqm` packages so that it shows up as a setting in your control panel, like so:

![Install the software](/assets/posts-images/bufferbloat1.png)

Go to speedtest.net to record your internet connection speed (upload and download), multiple each of those two numbers with 0.8 or 0.9. Don't worry too much about the absolutely maximum figure -- remember: it's not the bandwidth that is important. Go to the control panel and activate SQM-QoS, set it to the two figures you calculated like so (The queue discipline can be set as either Cake or FQ_CoDel, Cake is probably better):

![Set it up](/assets/posts-images/bufferbloat2.png)

![Close](/assets/posts-images/bufferbloat3.png)

Do the same speed test with the ping window open. If the ping figure stays low as if nothing happens even when you speedtest, then you're good to go. 

<amp-gfycat data-gfyid="ScentedSpiritedAmericanbadger"
  width="640"
  height="360"
  layout="responsive">
</amp-gfycat>

All you have left to do is to celebrate it, thank me and buy me a beer. Or fire up some Counter-strike: Global Offensive and murder someone. My gamers friends had an eye-opening experience when I showed them my 30ms ping with Bittorrent downloads in the background.


### Bonus question: *So you're making this long post to tell me that what determines my internet speed isn't the internet speed?* You're preaching voodoo -- I built my own PC!

Your download/upload bandwidth is the new [e-peen - Warning NSFW](http://www.urbandictionary.com/define.php?term=e-penis) - it's literally the top definition there right now. As a former Hanoian, I think your speed on the streets of Hanoi doesn't depend on how many engines your car has, either.

![Streets of Hanoi](/assets/posts-images/rXlHVjf.jpg)



PS: There are concerns that the FCC don't want you to modify your routers. As I am not a US citizen, I can't say much, but I'm sure you can help spreading the words on why not being able to put custom software on your router is bad.

