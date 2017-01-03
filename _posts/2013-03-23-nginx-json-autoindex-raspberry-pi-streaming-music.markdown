---
layout : "post"
title : "Streaming keygen music from my Raspberry Pi"
---

Since I have my Raspberry Pi "server" in ~~my butt~~ the
[cloud](https://github.com/panicsteve/cloud-to-butt) co-lo'ed in Austria
(thanks to
[EDIS](http://www.edis.at/en/server/colocation/austria/raspberrypi/)), I
wanted to make it a media server that is accessible anywhere, and
supports streaming music to my computers at work as well as my Android
phone.

While I'm sure that there are people who did this before, this time I
really don't want the streaming server/functionality to consume RAM and
CPU power as my model only has 256MB and I want to run other stuff on
the poor thing. So in other words, I don't want to have a whole bunch of
PHP/nodejs/go processes creeping on my server and bog it down. So I
decided to hack around the nginx webserver that I already have running.

Luckily [Zed A. Shaw](http://zedshaw.com/) already made a handy hack for
nginx, that replaces the normal HTML directory listing with a JSON feed.
So my part? Making the patch to work on the new version of nginx,
compile nginx on the Pi, write an HTML5 interface, and enjoy [my keygen
music](http://lily.tnhh.net/1911/). The interface is completely static
HTML, no dynamic back-end needed.

So how does it fare out? Very decently. RAM usage has increased 0MB! 

![](/assets/posts-images/streamingpi1.png)

Of course the front-end works with Chrome on desktop. What's also
amazing is that if you have Chrome on your phone, it can stream to the
background with automatic track change too.

So no, there isn't an app for that, it _just works_! O' glory 8-bit music on my phone)!

![](/assets/posts-images/streamingpi2.png)

<amp-youtube
        layout="responsive"
        data-videoid="Vnq9zcTPnTc"
        width="480" height="270"></amp-youtube>

And my jimmes are totally unrustled today.

If you're interested, [go ahead and grab it](https://github.com/htruong/1911-player) while it's still
hot or head right on to the [demo](http://lily.tnhh.net/1911/).

Caveats: I haven't been able to make the rules file so nginx would
produce the packaged deb file, so if someone could help me with that,
it's great. Also, if you have special characters in the filenames, the
thing would just get very confused. Will fix later when I have time...
