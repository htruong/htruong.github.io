---
layout: post
title: "#2: My Chumby hacking story: Do you believe in the Users?"
category: crankshaft
---

From day one, I have been always envisioning Crankshaft to be the software package that is easy ("turnkey") for the end user and powerful for the developers. Crankshaft has [proved to be turnkey](https://photos.google.com/share/AF1QipP3hcflM2fty5ziB_yuFl1_4hJL2r1LlWdvdUgCROp0DqsgiTJgm5lJUoDY6aO5aA?key=SmkydlU1eVFEb20xOHFJX0ZZUk9KY3NGR2dlcVhB) [for many users](https://github.com/htruong/crankshaft/issues/2) and I've also [made it fun for newbies to customize it](https://github.com/htruong/crankshaft/wiki/Customizing-Crankshaft), but with the [dev mode introduced last week](https://github.com/htruong/crankshaft/wiki/Crankshaft-dev-mode), I think I have executed my very first baby step in making that a dream for developers. That inspiration came from my many years being a hacker, and a single ill-fated product that affected me the most profound way: The Chumby. 

The sentence I remembered the most from it was: "Do you believe in the Users?" (In turn, from the movie Tron, I think.)

![Inforcast, or Chumby, it doesn't matter](/assets/posts-images/crankshaft-post-2/infocast-1.jpg)

_I still keep my Chumby. It still works. Wait a sec, it's not a Chumby, isn't it? Read on..._

This will be a trip down my memory lane, and not everything is relevant, so I hope you have some free time to read this. First, a disclaimer: the information, and opinions expressed in this blog were solely mine and in no way representative of anyone else's view.

**Apple: Do you believe in your Customers?**

When Steve Jobs did [the infamous funeral for OS 9](https://www.youtube.com/watch?v=G1SLCAiGkVQ), Apple ran an advertisement for OS X on the Macintosh that advertised it as a powerful UNIX machine:

![Inforcast, or Chumby, it doesn't matter](/assets/posts-images/crankshaft-post-2/apple_unix_ad-s.jpg)

_OS X Ad. [Source](xaharts.org/funny/Apple_Mac_OS_X_Unix_ad.html)._

Being born in Vietnam in a middle-class family, I only knew Macs through computer magazines. Vietnam was sanctioned by the US up until 1995. I first touched a computer in 1998 when I was 11. I knew Macintosh was a powerful computer for users, designers, and programmers alike, but never touched one myself. When I was a freshman college student in the Vietnam of Academy of Cryptographic Engineering in 2005, I spent all my money working for a startup for 4 months to buy a crappy Acer laptop for $600 (of which $300 my mom helped me). Later I turned it to a Hackintosh. OS X Tiger was polished, lovely and powerful just like I imagined. I was greeted with this when I tried to do `sudo`:

![mac os x sudo with great power](/assets/posts-images/crankshaft-post-2/TigerSudoCommand.png)

_Tiger used to warn its users this. I don't think newer versions of macOS do this anymore. [Source](http://jf.omnis.ch/archives/2005/05/sudo-in-tiger.html)_

Surely I was somewhat fluent with Linux at that point but somehow I always associated that message with OS X (I think because I would log in as root when I wanted to do stuff on my Linux boxes). I knew at that point I had a powerful tool that just worked normally but also trusted me to break it when I wanted it to. It was memorizing.

**Truck: Do you believe in your Students?**

Then for reasons too long to tell, I dropped out of the college in Vietnam, heartbroken but not any less determined. I got admitted to Truman State, a small liberal arts college in Kirksville - a town in the middle of nowhere, in 2008. For my first two years there, I was just a low-key Business-Administration-turned-CS international student. I worked for the Truman IT department to support a hall that houses a couple of departments, one of which was the Maths and CS department. Across my office was the only CS lab called The Nerdery with around 15 computers. 4 of them ran Linux, specifically an old version of Debian. You can see them in the photo here in the background.

![The Nerdery in Truman State University](/assets/posts-images/crankshaft-post-2/142813348_45c09bf556_z.jpg)

_Good ole time in The Nerdery at Truman State University. Credits: [Ian Monroe on Flickr](http://www.flickriver.com/photos/eean/142813348/)._

The computers were decommissioned Windows Dell PCs. Each had a Pentium 4 CPU with 1GB RAM. They were slow for the time, so not many students used them. On top of that, they also had old browsers and the accounts were unprivileged and they didn't provide much utility so compared to Windows stations. [Dr. Don Bindner](http://dbindner.freeshell.org/), the professor who is charge of the Nerdery, installed an LCD matrix display on one of them to show the department server load with a custom daemon. In March of 2010, I noticed I could do a local kernel exploit on the computer, so I covertly planted a program that wrote "Hello Don, you have been fished!" on the LCD and it would trigger on April fools' day (don't worry, that message was silly and doesn't mean anything). The day finally came. It caught one of the students' attention, and they reported to the Donald. Before he asked a student to investigate it, I came to talk to him: I told him I could have done more malicious things with all other accounts, but that was all I did. He was somewhat impressed and wasn't mad, so we sat down to talk. 

We agreed this would be a nice opportunity to revamp our system. I came up with a proposal, we would install Ubuntu so they look more modern - that was the easy part. And because people who use Linux are power users anyway, I wanted to give everyone root (a.k.a. the Stallmanism approach). But that brought another problem, how were we going to stop people from messing everything up? First, we thought about running Ubuntu as a "live" distro from the HDD. But what if someone dd'ed the HDD? Well,... Let's netboot them! Two problems came up. First, the network ports we had in the room were the "slow" 100Mbps one. Second, for us to do PXE netboot, there will be a ton of changes needed in the IT infrastructure and it would take a long time for the IT department to get to us. Ain't nobody's got time for dat!

Further digging revealed to me that it was possible to flash an extremely powerful bootloader called iPXE run as an [Option ROM](https://en.wikipedia.org/wiki/Option_ROM). That way, we wouldn't have to worry about having PXE support on the DHCP server. One cool thing about the EPROM chip on the network card, if we had one, is that they are writeable, but only when one erased them first. To erase them, one would have to literally pull the chip out and shine a strong UV light on the transparent hole for a while. In short, it would take a ton of work for a student to actually brick a station.  

![EPRON Eraser](/assets/posts-images/crankshaft-post-2/eprom-eraser.jpg)

_You need something like this to erase EPROM chips quickly. [Source](https://electronics.stackexchange.com/questions/34607/erasing-eproms-with-sunlight)_

So we came up with a crazy Frankenstein setup. I bought and donated a cheap gigabit switch to the Nerdery to give all the computers a 1Gbps connection because we actually had a single 1Gbps port. The built-in Ethernet port on those computers were already Gigabit so that was fortunate. We would also buy several old 3M 10Mbps PCI network cards to install one on each computer. Their sole purpose was to house an iPXE EPROM chip to boot the computers. And guess what, that crazy setup worked [after a couple of nights messing around with them](http://lists.ipxe.org/pipermail/ipxe-devel/2010-November/000087.html)! I decided to further foolproof them by optimizing the live image so everything would fit and run on RAM. Lucky for us, Don and I were able to dig up several RAM sticks from decommissioned PCs, so we had 2GB of RAM on each computer in which ~1GB was used for the live image. They were damn fast! If the Windows PC took 2 minutes to log on and 30 seconds to open a browser, it took our workstation 1 seconds to log on and a browser would open instantly. That's not counting gcc, apt, and all kinds of fun stuff we had on them. On top of it, everyone had root! 

If you mess anything up, just hold the power button for 3 seconds and the computer would boot right back up. They were a hit among students then. We called the distro Truck (because everything better to start with the prefix Tru-), a name my friend Erin Clark (she is now working for iXSystems) suggested to me one night. We thought it was a nice name because a truck is a very powerful and solid vehicle. 

Creating Truck was perhaps one of my fondest memories during my time in Truman as an undergrad student. As far as I knew, no one up to when I left Truman actually abused that root privilege to do anything shady (that's one of the perks in a small school).

**Chumby: Do you believe in your Users?**

I graduated Truman at the end of 2011 and was offered a temporary job for 8 months in the IT department as a "Web developer" while waiting for my grad school decision. Part of my job when I was a student was to help design and install AV control systems in classrooms. Each classroom then had a document camera, a computer, potentially laptops, and maybe a tape/DVD player and they needed to be labelled accordingly, and using the remote is too hard and too flaky. We would order the touch panels from Extron that has a couple of physical buttons to allow us to switch the multimedia source to project in the classroom. Their products were very nice, but then the prices were not. They later came up with a touchscreen system that sold for an even higher price. Extron support was nice and efficient though, so, as people often say, "you get what you pay for."

However, I remember we were having budget cuts left and right. It didn't help that Truman isn't a rich school to begin with, it's just a small public education insitution. Partly because of the cost of the AV control system for each classroom, we didn't usually have all the funds allocated at once. We would have to do several rooms at a time whenever funds came in. So among the things I was expected to do, the IT department really hoped I could come up with a more elegant solution. I was planning to design a simpler board with a simple microcontroller with an Ethernet chip with the help of the Donald and get them manufactured. But then it was a very monumental task and 8 months seemed way too short to get it executed. I even had one of the first "preview" Pi boards at the time but wasn't very sure if I were going to use it. It was 2012, the Pi was very rare at the time, the lead time looks like going to be at least another year. How on Earth were we supposed to get hundreds of them for a reasonable price before I left? 

![Raspberry Pi B](/assets/posts-images/crankshaft-post-2/f479307776.jpg)

_My first Raspberry Pi B in early 2012 -- I knew it was something very special. It was a gift of Nokia. Thank you - You were so kind._

One night when I was browsing Hacker News late, [I came across a peculiar comment](https://news.ycombinator.com/item?id=3850973):

>I'm anxiously awaiting the time when I can buy a Pi without jumping through hoops just to check one out. In the meantime, for those interested primarily in the price of the product and the DIY-tinker factor but who haven't been able to snag a Pi yet, you can currently pick up new (well, not new exactly, but never used) Insignia Infocast 3.5" devices for about $25 from various resellers (look on ebay, etc).

OH RLY? I looked on eBay. There was a merchant who was offering the Infocasts for around $20 a pop. I immediately emailed the person to see how many they have, and they said they have a lot. I only heard about the Chumby at the time, and never worked with one. With that price I ordered one of them shipped next-day to me to test. I wasted no time and just enabled the developer mode right after I got it. Thanks to the wiki, after several sleepless nights, [I managed to port Webkit to it](https://www.engadget.com/2012/05/31/developer-runs-webkit-on-chumby/). Shortly after, I was able to get a proof-of-concept web interface to work to control and manage a projector in my office. I showed the department at the meeting, they were amused. That would be all we needed to have to implement such a control system! 

I convinced my manager and the department to pull the biggest heist ever to buy all the remaining stock from that merchant. I can't remember the amount we purchased, but it was hundreds. The shipment came in a truck and we filled literally a quarter of a storage room with new Infocast boxes. I figured with a price that can get 5 rooms going with Extron control units, we could have enough control units for the whole campus for 5 years. It was quite a funny and memorable scene in my mind. I had a picture of it, but my hard drive crashed, so I don't have it now (When I am able to retrieve it from old colleagues, I will post it here). 

At Truman, [we still dearly call them the Chumby/ies](http://ltt.truman.edu/how-do-i/use-the-av-control-unit-chumby/). [I was able to get a control system going by the time I left for grad school 8 months later](http://blogs.truman.edu/itsnews/2012/09/13/new-av-control-units-arriving-in-a-classroom-near-you/). I haven't asked, but last time I checked 6 months ago or so, Truman still use the Chumbies to control projectors :).

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/6DT7zUXXOqs?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

When I had my first Chumby, I knew it was something very special. It was an end-user product and would just work out of the box. Yet I only needed to press on a corner and it would expose as a fully capable hackable Linux computer with all its development bells and whistles. It invited me to repurpose it to do whatever I want.  I'm sure the creators of it believed in their users to do good things with it. 

Because of the hack, I had the pleasure to know and exchange several emails and do some things with bunnie. I don't recall if I ever told him, Duane, or anyone who worked on the Chumby about this story about the big heist and the mass deployment of it.  I really hope everyone who worked on the product is glad their creation still proved to be useful years later after they closed shop. For myself, I am proud of being the person that deployed hundreds of hacked products all around the little beautiful campus that I spent the best years of my life in.

![Truman Campus](/assets/posts-images/crankshaft-post-2/f461124864.jpg)

Throughout the years, I have used custom firmwares and taken part in custom firmware development for a couple of routers, android mobile phones, Chromebooks, game consoles, and handhelds. Many later products reflected somewhat the Chumby spirit: the write protect screw on the Chromebooks or the bootloader unlock command on android phones. But none of them gave me the bold impression that I had with the Chumby. It was the first mass-market product asking to be hacked. In retrospect, it might not have done a fantastic job of being an end-user product for some reason, but to me, it opened a new way of thinking. That way of thinking is to empower the users, not to restrict them. I can ship a product that works out of the box, but might be extended and used in ways I couldn't imagine.




**Crankshaft: Do you believe in your Car computer?**

![Crankshaft](/assets/posts-images/crankshaft-post-2/crankshaft-custom-wallpaper.jpg)

_Crankshaft displaying a custom wallpaper. Just copy a file named `wallpaper.png` to the `boot` partition and it will "just works."_


I still see Crankshaft the distro is just the right thing that came at the right time than it is a challenging product. OpenAuto/aasdk, on the other hand, was a monumental piece of reverse engineer by f1xpl. I just packaged OpenAuto/aasdk in a shiny package so it's accessible to many people who don't know how to compile OpenAuto. But in doing that, I hope it becomes an inspiration. I hope many people will first get attracted to Crankshaft as a shiny product and come out of it as developers/hackers. I have already seen many people who are subscribed to the /r/crankshaft subreddit and followed me on GitHub are coming up with ideas how to make it better. Now I invite all of you to work with me to make your own dreams come true. Because Crankshaft, like the Chumby, is inviting you to hack it further. 

[Find a jumper and enable the "dev mode" on Crankshaft](https://github.com/htruong/crankshaft/wiki/Crankshaft-dev-mode), and it will open its gate to let you hack it, just like the Chumby.

Hacking is fun. I do very much believe in the Users.

.

.

**Plug**: I'm looking for a job soon. Please let me know if you know someone is looking for a hacker. Thanks!
