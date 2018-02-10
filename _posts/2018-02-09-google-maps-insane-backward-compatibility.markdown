---
layout: post
title: The insane amount of backward compatibility in Google Maps
---

I have some old phones that I used to like. Sometimes I use them as my primary device for fun. Phones are among the fastest evolving markets, even a year seems like an eternity. One of the biggest challenges with phones is software: old phones don't run modern software. Old software isn't compatible with new websites, frameworks, encryption standards, APIs. Use an old device, and you will find yourself unable to get anything done. Every app crashes or complains that it can't connect to the server. If you have a 5-year-old phone such as the iPhone 5, you will notice that many sites and apps started dropping support for you (that's given Apple is extremely good at providing OS upgrades).

But there is always an app that consistently works on all of my devices, regardless of their OS: Google Maps.

Google Maps still works today on the earliest Android version available, Android 1.0. At that point I believe Maps was only a prototype app. That was back all the way in 2007.

![Google Maps Android 1.0](/assets/posts-images/gmaps/android10.png) ![Google Maps Android 1.0](/assets/posts-images/gmaps/android11.png)

But then, you say, it is Google's OS for Pete's sake. It should work, right? OK, then how about iOS? Google Maps 1.0, released late 2012, still works just fine. That was the first version of Google Maps ever released as a standalone app after Apple ditched Google's map solution on iOS:

![Google Maps iOS 7](/assets/posts-images/gmaps/ios70.png) ![Google Maps iOS 7](/assets/posts-images/gmaps/ios71.png)

But wait... There is more. This is native iOS Maps on iOS 6, which was released in early 2012, and it still works. I just noticed that the Normal and Hybrid map modes stopped working recently, but that's alright, I can still navigate (plus, I can always download and use Google's official app on iOS 6):

![Google Maps iOS 6](/assets/posts-images/gmaps/ios60.png) ![Google Maps iOS 6](/assets/posts-images/gmaps/ios61.png)


But that's only 6 years ago. Let's be hardcore. How about Google Maps on J2ME (the dumb bricks that run Java "midlets" or whatever the ancient Greeks call it)? It works too. Note that, other than Google Maps and Opera Mini, I do not note many Internet "midlets" that still work, [including Whatsapp that is praised for their willingness to deal with ancient phones](http://blog.textit.in/your-path-to-a-$16b-exit-build-a-j2me-app). 

It was 2008 when the app was last updated, but even street view works:

![Google Maps J2ME](/assets/posts-images/gmaps/j2me0.png) ![Google Maps J2ME](/assets/posts-images/gmaps/j2me1.png)

Now if that hasn't impressed you yet, let me introduce you to my Palm Treo 755p, released in 2007. To see how severe of a situation this is, the phone runs Palm OS 5. It doesn't understand Unicode. Of course, it has no idea what an "emoji" is. When you send it a text message that has a character outside of printable ASCII, it freaks out and corrupts the whole message. It doesn't have Wifi of any kind. It doesn't even connect to Sprint's 2G EV-DO/1xRTT network (because the data provision server is long dead). In short, it has no easy way to connect to the internet at all. In order to get the thing to connect to the Internet, I had to fucking emulate a Dial-up Modem over Bluetooth using a Raspberry Pi. Since then, I have repurposed my Raspberry Pi, and it was very painful to set up so I don't have a picture of Google Maps working now. 

This was last year: Seemed like there was only one person in this world who was still using that "app" in 2017, and that was me. The Palm OS didn't even have screenshot functionality. But lo and behold, Google Maps worked (There are some missing loading tiles in the picture because I wanted to test wheter it worked offline with cached tiles, and it did):

![Google Maps PalmOS](/assets/posts-images/gmaps/palmos0.jpg) ![Google Maps PalmOS](/assets/posts-images/gmaps/palmos1.jpg)

The only exception to me on Google Maps, so far, was the WebOS map app. It doesn't work anymore -- but forget about that, there is an unofficial app that runs on WebOS that still works today:

![Google Maps WebOS 2](/assets/posts-images/gmaps/webos0.png) ![Google Maps WebOS 2](/assets/posts-images/gmaps/webos1.png)


And they all work with the [newest maps data](https://www.justinobeirne.com/google-maps-moat/). The Steve Jobs auditorium is a new building. Regardless whether all this compatibility is intentional or not, that's a crazy feat.

I noticed that the only other product I see running well on old devices is Google search, it works with many kinds of old browsers. Gmail app in general is bad about legacy support, although in many cases you can still access a limited version of Gmail on a web browser. The lack of legacy support of Gmail is partly due to its encryption protocol requirements. I do understand that: Emails are incredibly personal, giving up legacy compatibility for security is a worthy cause. 

I hope regardless of whatever happens to the future, Google keep testing and maintaining this legendary compatibility in Google Maps. You'll never know when you save a life lost in the middle of nowhere with an app that runs on an ancient phone.

Disclaimer: Except for the Android 1.0 app and the Midlet app were emulated on software, everything else runs on real hardware. I do not expect there is any difference if you actually have a real hardware.
