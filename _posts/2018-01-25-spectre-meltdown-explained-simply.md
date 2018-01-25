---
layout: post
title: Spectre and Meltdown attack explained, simply, for non-programmers
---

I have seen a lot of discussions online about the Spectre and Meltdown attack. They opened a profoundly new way to think about computer architecture. However, the first time I talked about that idea to my parents, the only feedback I've got was confusion - it was over their head. I've finally figured out a way to convey the idea so my mom who is 63-year old could understand and I received a nod, so I think it passes the dummy test. If you're really a programmer though, you should read [the raspberry pi blog instead](https://www.raspberrypi.org/blog/why-raspberry-pi-isnt-vulnerable-to-spectre-or-meltdown/). 


Let's get back to the future -- you're the heir of a family convenience store in the 80s. Stuff is quite low-tech, you don't have that fancy barcode system, you check out stuff by looking up the price of each item in your book and enter the amount to a calculator-printer. That process takes some time, but all is well. Something like this:

![image of an calculator printer in the 1980s](https://s3-ap-southeast-2.amazonaws.com/wc-prod-pim/JPEG_1000x1000/DAEL2901RH_sharp_sharp_el2901rh_printing_cal_grey.jpg) 


First, you observe that your customers check out items that they don't want others to know. So the first thing you changed in the store was that customers can put goods in an opaque shopping bag that they only give to the cashier at the counter. You don’t let any customer peek into other customers' bags - the person will be asked to leave. It's called "personal privacy protection" rule, and your customers are really happy about that, they buy a lot of discretion items.


Now your convenience store business is booming, you hire Chad to be your cashier. Chad doesn't seem terribly bright and he has a very short-term memory, however, he has good composure, in other words, a good man and thorough. He never leaks out anything any customer bought. 


Next, you also observe that when Chad tells the customer the grand total, it would take some time for them to pull out their wallet and write a check or count money and give the correct change to Chad or run out to get additional items they forgot to put in their bag. That makes Chad standing there doing nothing for minutes, and the next person in line really irritated. So you propose: "Hey Chad, why don't you try to look up the items and calculate the bill for the next person in line while you're waiting for the current person?" Chad agrees. Chad now glances at and looks up the price of the items for the next customer's bag while waiting for the current customer. Sometimes the next-in-line customer leaves the line before they check out, or they actually don't check out some items in their bag. That is alright, Chad can always discard the printed bill if the customer changes their mind. However, if Chad's guess was right - the customer ends up buying the item they had in the bag when they were in line, Chad serves two customers at once! Your line becomes shorter, people waste less time waiting in line, everyone is really happy. Before long, your little idea for Chad catches fire and becomes a national phenomenon, every manager at every store adopts it and subsequently fires half of their cashiers. Your idea, dubbed "speculative checkout," becomes one of the best management techniques of all times and is in every business textbook for decades.


One day Rosie the nosy neighbor does something quite peculiar. When she checks out, she would leave the line for a minute for Chad to "speculatively checks out" Stacy who is behind her. Then Rosie comes back with several kinds of discretion goods in her bag. She then observes whether Chad is able to enter the price of each type of the goods into the calculator quickly without looking up. She knows that Chad doesn't remember prices of stuff -- the only reason he could recall the price of something without looking it up is that he recently looked it up because Stacy has it in her bag. In other words: Rosie exploiting an honest Chad was able to figure out what Stacy is going to buy. "Speculative checkout" -- as a process -- leaks out the information and erodes "personal privacy protection."


Now you have a couple of options. You can ask Chad to stop doing speculative checkouts altogether. Or you can ask Chad to be careful and pretends that he looks up everything even though he could recall the price from his short-term memory. Both suck because Chad is less efficient either way and as a result, you might need more staff to check people out. Furthermore, telling every store in the nation to implement that change takes a long time. But that's the only way you can prevent Rosy from knowing what Stacy buys.


When it comes to computers, Stacy and Rosy are programs running on your computer and your phone. Chad is your hard-working, naive, but always truthful CPU ;^). Let’s say Stacy is Tinder and Rosy is Facebook -- you don’t want Facebook to know your Netflix-and-chill schedule on Tinder because they may splash some Black Mirror ads to your face, and you hate Netflix’s Black Mirror series. In reality though, the details of what you’re able to peek in is different, but the spirit stays the same: Even though the idea of speculatively doing something seems great, but you can exploit it in subtle ways.


Hope that explains it well enough for you. [Here is another layman attempt and you might find it useful]( https://twitter.com/securelyfitz/status/949004862968143873). If you enjoy my explanation of Spectre and Meltdown, you might also enjoy [my explanation of Bufferbloat](https://www-tnhh-net.cdn.ampproject.org/c/www.tnhh.net/mobile/posts/bufferbloat-in-laymans-terms.html). 

_Special thanks to Don and Joe for having a look at my post before it is published._
