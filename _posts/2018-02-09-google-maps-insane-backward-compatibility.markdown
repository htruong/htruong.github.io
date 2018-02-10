---
layout: post
title: The insane amount of backward compatibility in Google Maps
---

I still keep a couple of old favorite phones. Sometimes I use one of them as my primary device for fun. Phones are among the fastest evolving markets, even a year seems like an eternity. One of the biggest challenges with using old phones is the software: they don't run modern software. And old software isn't compatible with new websites, frameworks, encryption standards, APIs. Use an old device, and you will find yourself unable to get anything done. Every app crashes or complains that it can't connect to the server. Even with iOS 10 on iPhone 5, you may notice that many sites and apps have started dropping support for it -- and the iPhone 5 is only 5 years old.

But there is always an unlikely app that consistently works on all of my devices, regardless of their OS and how old they are: **Google Maps**.

Google Maps still works today on Android 1.0, the earliest version available (Maps actually still works with some of the the <1.0 beta versions). Even with 1.0 I believe Maps was only a prototype app. If I recall correctly, Google didn't have any official real device to run Android 1.0. That was back all the way in 2007.

![Google Maps Android 1.0](/assets/posts-images/gmaps/android10.png) ![Google Maps Android 1.0](/assets/posts-images/gmaps/android11.png)

But then, you say, Android is Google's OS for Pete's sake. How about iOS? Google Maps for iOS 1.0, released late 2012, still works just fine. That was the first version of Google Maps ever released as a standalone app after Apple ditched Google's map solution on iOS:

![Google Maps iOS 7](/assets/posts-images/gmaps/ios70.png) ![Google Maps iOS 7](/assets/posts-images/gmaps/ios71.png)

But wait... There is more. This is native iOS Maps on iOS 6, which was released in early 2012, and it still works. I just noticed that the Normal and Hybrid map modes stopped working recently, but that's alright, I can still navigate (plus, I can always download and use Google's official app on iOS 6):

![Google Maps iOS 6](/assets/posts-images/gmaps/ios60.png) ![Google Maps iOS 6](/assets/posts-images/gmaps/ios61.png)

But that's only 6 years ago. Let's go hardcore. How about Google Maps on Java phones (the dumb bricks that run Java "midlets" or whatever the ancient Greeks call it)? It works too. Note that, other than Google Maps and Opera Mini, I do not note many Internet "midlets" that still work, [including Whatsapp that is praised for their willingness to deal with ancient phones](http://blog.textit.in/your-path-to-a-$16b-exit-build-a-j2me-app). Whatsapp actually has a time-bomb programmed in the app of some sort and it will kick you out if it realizes that it hasn't been updated recently. What a dumb idea.

Back to Google Maps. The app (? - applet? midlet?) was last updated in 2008, but even street view works today:

![Google Maps J2ME](/assets/posts-images/gmaps/j2me0.png) ![Google Maps J2ME](/assets/posts-images/gmaps/j2me1.png)

Now if that hasn't impressed you yet, let me introduce you to my Palm Treo 755p, released in 2007. 

The phone runs Palm OS 5. It doesn't understand Unicode. Of course, it has no idea what an "emoji" is. When you send it a text message that has one character outside of the printable ASCII range, it freaks out and corrupts the whole message. It doesn't have Wifi of any kind. It doesn't even connect to the Sprint's 2G EV-DO/1xRTT network (because the data provision server is long dead). In short, it has no easy way to connect to the Internet at all. In order to get the thing to connect to the Internet, I had to fucking emulate a Dial-up Modem over Bluetooth using a Raspberry Pi. Since then, I have repurposed my Raspberry Pi, and it was painful to set up so I don't have a picture of Google Maps working now. 

This was last year: Seemed like there was only one person left in this world who was still using that "app" in 2017, and that was me. The Palm OS didn't even have screenshot functionality. But lo and behold, Google Maps worked (There are some missing loading tiles in the picture because I wanted to test wheter it worked offline with cached tiles, and it did):

![Google Maps PalmOS](/assets/posts-images/gmaps/palmos0.jpg) ![Google Maps PalmOS](/assets/posts-images/gmaps/palmos1.jpg)

The only exception to me on Google Maps, so far, was the WebOS map app (released in 2009). It doesn't work anymore -- but forget about that, there is an unofficial app that runs on WebOS that still works today:

![Google Maps WebOS 2](/assets/posts-images/gmaps/webos0.png) ![Google Maps WebOS 2](/assets/posts-images/gmaps/webos1.png)

And they all work with the [newest maps data](https://www.justinobeirne.com/google-maps-moat/). The Steve Jobs auditorium is in a new building. 

Regardless whether all this compatibility is intentional or not, having that level of backward compatibility and functionality is a crazy feat. 

I noticed that the only other product I see running well on old devices is Google search, it works with many kinds of old browsers. Gmail  in general is bad about legacy support, although in many cases you can still access a limited version of Gmail on a web browser. The lack of legacy support of Gmail is partly due to its encryption protocol requirements. I do understand that: Emails are incredibly personal, giving up legacy compatibility for security is a worthy cause. 

I hope regardless of what feature or architectural change happens to Maps to the future, the team keep testing and maintaining this legendary compatibility in Google Maps. We'll never know how valuable it is until we're lost in the middle of nowhere, and in that moment we'd be so thankful to find out Google Maps still runs on our ancient phones in the glovebox  .

Disclaimer: Except for the Android 1.0 app and the midlet were run emulated on software, everything else ran on real hardware. I do not expect that there is any difference if you actually have the real hardware to run it.