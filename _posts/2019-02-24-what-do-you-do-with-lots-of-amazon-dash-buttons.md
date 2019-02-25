---
layout: post
title: "Hacking Amazon dash buttons, the hard way, with OpenWRT"
---


I packed up from North Carolina and moved to California a couple of months ago. Because I had a fresh start, I had the chance to organize and set up my new apartment exactly how I wanted. One of the items on my wishlist was to set up my apartment as a smart home. The reason was that I realized I often sleep with the bedroom light being on. I then would wake up at 3 AM in the morning and being too lazy, I tried to sleep with the lights on. That often resulted in shallow sleep. I go to work tired and I don't appreciate that.

So I started with a raspberry pi zero, an ESP32 and the amazing piece of software called [homebridge-mqttthing](https://www.npmjs.com/package/homebridge-mqttthing) to help me set up a HomeKit and mqtt-compatible smart bedroom light switch. This set up is amazing because I get the convenience of Siri and HomeKit. At the same time, I can also control/automate my devices with the openness of mqtt. By the way, ESP32 has an amazing mqtt library in their SDK. 

I was pretty pleased with that for a while and then realized that it didn't really solve my problem: I still sometimes sleep with the bedroom light on. The reason was that from time to time, I fell asleep on my sofa. When I woke up in the middle of the night at 2 AM in the living room to crawl to my bed in the bedroom, I often didn't know where my phone was. I couldn't yell "Hey Siri, turn off my bedroom light" either, because I didn't want to disturb my neighbors. All in all, I need better solutions.

I was looking for some smart buttons of some sort. Last time I passed by a local Fry's, the Samsung's smart buttons were for sale for $15 a pop. Then I would need a smart hub, I presume, to use that smart button. And that hub probably will use some weird-ass proprietary protocol that syncs with the cloud that I can't control, can't understand, can't extend, and will discontinue in X years. When they turn off the lights on their "cloud" server, I will be fucked. I would, in addition, have to shell out money to buy a smart bulb or whatever. And so having two buttons, a hub and a bulb to control my dumb bedroom light would cost me $200.

I ain't got no money fo dat.

So I decided to extend my homegrown smart home protocol to have smart buttons. I know Amazon sells the Dash buttons for 2-3 USD a pop on a good day. That's their tactics to get people to [fall for the Amazon meme](https://danklessons.wordpress.com/2016/03/28/falling-for-a-meme/). I ain't that stupid, I buy their buttons to turn off my bedroom light! So I tried to look around and it turned out that there are people who sell 16 of those button for dirt cheap, like 10 USD with free shopping. They seemed to have bought them in bulk, used exactly once to get some sort of promotions (when did that happen?). So I figured that's a good deal and even if I lose 10 USD, that wasn't going to be the end of the world. Lo and behold, a week later, a big package showed up on my door and there was a treasure inside:

![Dash buttons](/assets/posts-images/amazon-smart-buttons/dash-buttons.jpg)

So what am I supposed to do with them? Hack 'em, of course!

Each of those buttons has a giant... button and an RGB LED next to it. When you press the button, one of those things will happen:

- If it can't connect to the Wi-Fi, then it will flash blue and turn on the "pair mode" of some sort. You use the Amazon app to send the Wi-Fi credentials over and it will connect to the Wi-Fi.
- If it can connect to the Wi-Fi, then it will somehow talk to Amazon by some mean. It will then inspect the response from Amazon. If the response is "OK" then it will flash green. Otherwise, it will flash red. Either way, it will disconnect from the Wi-Fi and go back to sleep. 

Although Wi-Fi is not exactly coin-cell battery-friendly, a simple button that works and does only that can last for a long time, like 2000 presses or so. So now the question is, how do we intercept the button?

It turns out that most tutorials on-line detects the button by [reading the ARP continuously](https://github.com/Nekmo/amazon-dash/blob/develop/amazon_dash/discovery.py). Then they compare it to a list of known ARPs to see what changed and act upon that change. While this solution works, it has the following disadvantages:

1, I have a distaste for reading the ARP and putting those Amazon buttons up with alongside on normal network. My general attitude towards IoT crap is embracing it, but I don't trust it. All my IoT crap has a guest network where each device is isolated from each other and can't see/access my real network (and ideally, no internet access, but I don't enforce that for now).
2, Also, to scan the ARP, the script that I write in Python or whatever has to run as root. I don't like that. What if someone thinks that I'm a big deal and hack my hacky python script that runs as root?

So my idea is to poison my own DNS so that all requests from the button to Amazon gets trapped in my local Raspberry Pi and I would only need to write a normal daemon to track that request. So my exercise becomes to figure out what endpoint do the buttons talk to Amazon. Ignoring all that setup nonsense, I want to know what happens when the buttons get pressed when it can join the Wi-Fi network. Luckily, with an OpenWRT-based router, knowing that is quite simple: We can set the dnsmasq service to log all DNS queries and see what domains get queried when we press the button:

![Snuff the DNS](/assets/posts-images/amazon-smart-buttons/dns-sniff.png)

A-ha! So the button does two things when it gets pressed. First, it queries `0.amazon.pool.ntp.org`. Second, it queries `dash-button-na-aws-opf.amazon.com`.

Why does it query `ntp.org`? Good question. NTP is the protocol that provides time synchronization. So the button does that to figure out what time it is. Why does it need to know what time it is? It probably talks to Amazon over some secure channel and needs some crypto library that requires it to know the time to verify the other end's certificate. Why doesn't it know? Because it needs to be made cheaply, and adding a Real Time Clock circuit ain't cheap.

Alright, so for now, it can talk to `0.amazon.pool.ntp.org` all it wants, we can intercept `dash-button-na-aws-opf.amazon.com` so that we can catch its communication. So my raspberry pi is on my 'trusted' network, and the dash buttons are on my 'untrusted' network. We need to set up a firewall rule to allow communication from the 'untrusted' network to the raspberry pi only, as well as poisoning our own DNS.

![DNS poisoning](/assets/posts-images/amazon-smart-buttons/dns-poisoning.png)

![Firewall rules](/assets/posts-images/amazon-smart-buttons/firewall-rules.png)

We can go ahead and figure out what ports do the button talk to, but from my what people say on the internets, it talks to port 433, and so I don't bother finding that out from scratch anymore. At the same time, the guides on the internet seem to only target the V1 buttons, which really don't talk to `parker-gateway-na`, so blindly following the guides on the internet isn't perhaps the best idea. Oh yeah, port 433 is HTTPS, that's why the button needs to know the time! 

At this point, all we need to do is to cook up a daemon in Python. The general idea is that even we can redirect the buttons, we can't possibly know what the buttons send to the cloud, because they don't really trust our daemon. All that we know is that the button will try to connect to us and give up upon the secure handshake fail. But that's enough for us to know that the button was pressed. We have a map from IP (that identifies what physical button was pressed) to a command we want to run. Let's say we want the button with IP `x.x.x.181` to run the mqtt endpoint `bedroom/toggle`, we can have a script like so:

![daemon script](/assets/posts-images/amazon-smart-buttons/daemon-script.png)

But since all the buttons all get DHCP allocated IPs, how do we know what button has what IP? OpenWRT has a feature called "static leases" that allow you to always give a certain MAC address a certain IP.

![Static leases](/assets/posts-images/amazon-smart-buttons/static-leases.png)

You might be curious why I said the button talks to the Pi on port 433, didn't I write the daemon to listen to port 1433? That's because daemons that run under normal users can't actually listen to low ports. We need an IPtables rule that redirects high ports to low ports like so:

![IPtables rule](/assets/posts-images/amazon-smart-buttons/iptables.png)

So that's it... I've got my two bedroom buttons that are literally stuck on the bed and near the door to toggle the bedroom light, and a Campbell's soup doorbell (I will try to scratch the "Camp" and "s" part). 

![Ah my neighbogh just rang the bell](/assets/posts-images/amazon-smart-buttons/rang-bell.jpg)

I plan to hack several more ESP8266 based switches to have more buttons to control the main lights in the living room, but as-is I am quite happy with the setup. See - I told you having a secure smart home isn't too bad, you just need to have OpenWRT, Raspberry Pi, hack tons of stuff, know about NTP, port redirect, and what-have-yous...

Till next time!
