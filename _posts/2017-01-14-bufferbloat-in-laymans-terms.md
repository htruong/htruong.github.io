---
published: true
title: 'Bufferbloat in layman''s terms, or why your internet connection sucks'
---


Because my post about LEDE/OpenWRT was pretty popular among searches on Google, I think I could as well make a layman's version about this topic.

## What is bufferbloat, why is it bad? Why does your game lag? Why my "internets" suck so much?

Bufferbloat is the problem where one intensive traffic user or program (for example, BitTorrent or Netflix) makes every other user and program miserable. You probably have suffered it at least once: your game lagged like crazy or your web page decided not to load when you or your roommate have a download or BitTorrent happening in the background. I used to think that it is normal to have a game lagging when I download something via BitTorrent because of the number of connections that it makes. It turned out that we all don't have to suffer that.

An analogy is like the time you went to a supermarket/Wal-mart to buy a pen, and had to wait 15 minutes to check out the pen because all the checkout lanes have queues of people with carts full of stuff in front of you. 

In many ways, games and voice chat need stuff delivered quickly and can be thought of as people needing to check out pens as quickly as possible. Programs streaming movies or downloading data could also be thought of as the people with big carts that need to be checked out - and they don't care as much about the time they have to wait.  

![Install the software](/assets/posts-images/Simpsons-Express-Line.jpg)

## Is your internet connection not fast enough?

You will probably conclude that your connection is not fast enough -- and that's a good misconception that your ISP hopes you to have so you will buy a faster internet package from them. Just fucking throw more money at the problem.

![Throw more money at it?](/assets/posts-images/throw_money_at_it.jpg)

Sadly, it is **often a misguided idea**. Here, throughput is mistaken for latency. Latency can be thought of as the time you have to wait before you check out your pen, and throughput is how fast you can walk out with your pen once you start checking out. They are somewhat related, but not quite the same thing. Hiring better people that can check out stuff much faster will help remedy the problem. For example, think of hiring faster salespersons that can scan stuff twice as fast will help to reduce the wait time for you to check out the pen from 15 minutes to, say, 8 minutes. If you have machines that can tell how much the bill is without scanning anything, then the wait time will be much faster, but they are an expensive solution (that's what we have with a gigabit fiber optics connection). In other words, you don't want your grandma working in the checkout line (56k dial-up connections suck for sure), but hiring Amazon to tag every item so that everything automatically checks out itself is overkill (having a twice-as-fast connection won't solve your problem).

**Usually people get upset about how long they have to queue instead of how fast can they check stuff out.** The same thing happens to the internet, programs and people often get upset about latency instead of throughput.

In games and voice chat, all that matters is latency. In fact, many modern games work fine with a dial-up connection (that is at least 100x slower than your typical connection), given they don't have to download big updates. Better throughput only helps when you check out many items very often, i.e. download lots of movies. Streaming movies doesn't count -- it only counts if your connection is slower than what the streaming requires which is often a low bar to pass (Netflix only requires 5Mbps for Full HD). It works the same way in real life, as long as the salesperson can check out faster than people can buy stuff, which is often the case, then hiring faster salespersons won't make the queues go away. If your internet connection is faster than what you need that and it still sucks, then you probably suffer from the same problem.

For anyone who managed to read this far might think that there are far better solutions than spending a crazy amount of money buying faster checkout solutions. If you just have a lane that says "express checkout" for people with 5 items or less and another that says "bulk checkout" for people with 100 items or more, then we have solved the problem of the person with the full cart making the people with just a pen wait. In other words, allocating queues differently without having to hiring faster people is a better solution here. That was what earlier algorithms tried to do - if you classify yourself as express checkout, then you don't have to wait in the normal lines. The problem was that programs aren't good at classifying themselves (sometimes they don't know beforehand how many items they have in their cart, people keep buying snack bars on the way out), and it is not clear from the start how many types of lines we should have, and the system is easy to abuse, because everyone wants to be in the express line. 

To remedy that problem, newer and fancier queueing algorithms are much better at controlling the queues, for example, they know how to allow people to drop out of the line after waiting for some time. All in all, you can see this becoming a queue problem rather than the salesperson problem. Think of a having a good algorithm as hiring smart people that handle the queue and tell people where to queue, rather than spending money hiring smart people that check stuff out faster.

The easiest way to tell if you have bufferbloat is to do a speed test while having a ping window open -- you can ping any "website" (more technically, IP address), for example, `ping -t google.com`. If you have the bufferbloat problem, you'll see a much smaller ping than when you do with a speed test going on. It means that the pings are lagging while a big transfer is going on.

### Short version of what you need to do:

So you probably was able to conclude that instead of spending money on a faster connection, you should buy a good router. Bing bing bing! You're correct. 

Do you need a gaming router, though? No, by "good," I don't mean expensive, and expensive "gaming routers" often weasel words for routers with marked up prices.  Good means it can run good software, such as OpenWRT and LEDE (for a more technically inclined audience, you might have heard of DD-WRT and Tomato formware, they are the same breed, just that OpenWRT/LEDE are more bleeding edge.)

OpenWRT/LEDE has algorithms that help you combat the latency aka handling the queues, such as CoDel of Cake. As far as I know, no consumer router, no matter how expensive, has those algorithms installed by default yet. OpenWRT and LEDE are the software programs that you can install to replace the "dumb" software that does the queue management that is installed by default on your router. It is free and open-source and I am among thousands of programmers and research scientists contributing to it daily to make a really, really good piece of software. It is very smart, although getting it to work on your router could be somewhat hard if you have never done it before.

First you need to buy a router that supports OpenWRT/LEDE. **The exact model matters** -- [buy one that is listed here](https://lede-project.org/toh/views/toh_available_864), don't go to Wal-mart or BestBuy and buy a random model and then complain that it doesn't work. If you have less than a 100Mbps connection, then an old Netgear WNDR 3800 for $20 will do the job fine, and I recommend it. Reprogram (or "flash") the router with OpenWRT/LEDE (I personally recommend LEDE, [here for the WNDR 3800](https://kau.toke.dk/lede/airtime-fairness-builds/ar71xx/generic/)). 

After you have all those done, go to the control panel, go to System>Software, then install the `sqm-scripts`, `sqm-scripts-extra` and `luci-app-sqm` packages so that it shows up as a setting opention in your control panel, like so:

![Install the software](/assets/posts-images/bufferbloat1.png)

Go to speedtest.net to record your internet connection speed (upload and download), multiple each of those two numbers with 0.8, go to the control panel and activate SQM-QoS, set it to the two figures you calculated like so (The queue discipline can be set as either Cake or FQ_CoDel, Cake is probably better):

![Set it up](/assets/posts-images/bufferbloat2.png)

![Close](/assets/posts-images/bufferbloat3.png)

Do the same speed test with the ping window open. If the ping figure stays low as if nothing happens, then you're good to go. 

All you have left to do is to celebrate it, thank me and buy me a beer.
