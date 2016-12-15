---
layout : "post"
title : "This fast, rock-solid website and some others are powered by a single Raspberry Pi"
hidetitle : true
---


Recently I've been thinking about getting super cheap. Since I have not much contents on my website, $25/year for websites that hardly anyone visits is certainly something that can be optimized. Also, the PHP-based blogging system called Chyrp that I was using has some problems:

1. It is slow, and if anyone puts any load on it, it will not be able to cope with the load. 
2. People have figured out ways to spam my blog. 
3. The platofrm is dying and is unsupported. 
4. Moving MySQL databases every time I change my host is a pain in the butt (not necessarily Chyrp's fault).
5. I am tired of patching security holes whenever I don't have time (and graduate school takes a lot of time).

But "blogging systems" or CMS in general all have a very nice property, that the pages are dynamically generated from a [lightweight markup language](http://en.wikipedia.org/wiki/Lightweight_markup_language). So I don't have to screw around with both the content and the design at the same time that I really want to keep.

So since I have a Raspberry Pi hosted at EDIS for free, I have decided that the free Raspberry Pi will be powering my sites.

The Pi is very weak, and probably not the most unreliable thing ever, so it's probably not wise to host my sites on the Pi itself.

So my solution? Host the source somewhere else, but let the Pi do the generation with a [static site generator](http://www.mickgardner.com/2012/12/an-introduction-to-static-site.html), then put the generated site on somewhere rock-solid. I'm also inspired by the idea that I can manage my pages with git, and the Pi would automatically be triggered when I do a push.

So here comes jekyll-baas (blog-as-a-service). What it does:

1. Watch a whole bunch of sites at once.
2. Can push the generated files to Amazon S3.
3. Has a web interface so that a simple _push_ on git would automatically trigger the site generation.
4. It would only trigger what has changed about the site.
5. Consumes only 6MB on the Pi.
6. Creates a rock-solid website that is also fast!

The source code, based on jkl is available [here](https://github.com/htruong/jkl-baas) -- probably needs a lot of clean-up and documentation before it's usable... But nonetheless, it is working fine for me now. And you can't take my site down (I hope you don't _try_ to take it down, as if you do my bill for S3 would be pretty high).

_Note that you would have to use toml for the decoration, as we don't have a good native go-yaml support, and getting cgo to cross compile is painful._