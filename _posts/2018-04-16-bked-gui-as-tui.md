---
layout: post
title: "Tech wonder: BKED -- The Poly-edit program"
category: vietnamese
---

**Blurp**: _**Vietnamese Tech Wonders** is a series of blog posts about technological wonders made by Vietnamese people. This series will be written in English, and published on my blog as a category and [maintained on my Github repository](https://github.com/htruong/vietnamese_tech_wonders/). I suspect that part of the reason that some people think that [the world don't much about the Vietnamese people and its tech industry](https://huyenchip.com/vietnamese/) wasn't because the country lacks talents. I hope that it is because there has been not many people who were willing to document those stories internationally, partly due to being isolated until 1995. So I'm here to blog about amazing stories and hacks by Vietnamese engineers that you might find interesting as a programmer or a tech person, whether you're Vietnamese or otherwise. If you have a story, please feel free to reach out to me, I am constantly looking for wonderful stories to tell._


.

BKED was the de-facto text editor in Vietnam in the 80s-90s. It stands for Bach Khoa EDitor (Polytechnic Editor, for those who don't understand Vietnamese). It carries two meanings by that name. First, the name explains its origin, the University of Polytechnic (now renamed as Hanoi University of Science and Technology). Second, the name suggests it can edit many types of documents.

BKED runs on MS-DOS and [looks just like edit.com](https://i.imgur.com/RZN50oS.jpg), except for it displays and allows the user to input text in Vietnamese. It has nothing really quite special at the first glance.

![](https://www.techsignin.com/wp-content/uploads/2016/05/xBKED-bach-khoa-editor-screenshot-2.png.pagespeed.ic.9AfJugv6PF.png)

_BKED. Picture credits: Techsignin.com._

The Vietnamese alphabet is Latin-extended, and it needs about 100 or so extra characters (caps included) besides the standard Latin alphabet. Thankfully, the extended ASCII character set (code 128-255) was just barely enough to hold the extended Vietnamese alphabet.

Consequently, the obvious way to solve the problem of displaying Vietnamese on DOS was to override and redraw the character set in the [VGA-compatible text mode](https://en.wikipedia.org/wiki/VGA-compatible_text_mode). Its rivaling editor, called VietRES, did just that. With some other [Terminate-and-stay-Resident](https://en.wikipedia.org/wiki/Terminate_and_stay_resident_program) tricks, VietRES made it possible for any text or TUI program on DOS to display and accept Vietnamese. You might have guessed it, RES stands for RESident. However, it has a drawback that is it messed up the TUI of many programs because it had to override almost all of the extended ASCII characters, most notably table-drawing characters. It was an inevitable problem if you ever want to display Vietnamese characters with just ASCII. The problem carried on to even Windows 3.1 and Windows 95. Our Windows-based Vietnamese support program at that time overwrote the MS Sans Serif and turned every '®' in every software install package to an 'â'. Many other character sets had this problem, for example, in Japanese, the '\' was turned into the '¥' symbol.

![](https://i.stack.imgur.com/zOD0C.png)

_Backslashes no mo. [Yen all the way](https://superuser.com/questions/1167662/why-is-windows-10-displaying-as-%C2%A5-on-the-command-line/1167665)._

Two years ago I thought about BKED and realized that BKED had no problems drawing tables. It could even display bold and italic characters at the same time alongside with regular characters. When I tried to run it on DOSBox, it was clear that BKED did something really clever to get around that. First I thought it might have used the secondary table or something. So I updated my status on Facebook praising whatever the author, Dr. Quach Tuan Ngoc, did. Dr. Ngoc, -- now an old man -- somehow is a friend of a friend of mine, saw that and chimed in. He said his editor doesn't run in textmode. My mind was blown! It is a full-blown graphical program in Hercules/CGA/EGA/VGA graphics and just pretends to be a text-mode program. It draws every single character in its UI. It had to do it very quickly and economically -- computers in Vietnam at the time were all old secondhand ones imported from the US recycle centers and such. Now as I looked at it more, it was no surprise to me it could also do quite [sophisticated mathematical formulas and chart drawing](https://i.imgur.com/ofhE0TG.jpg). Thanks to its flexibility, the editor was used to typeset the whole suite of national textbooks on every subject in the 90s. 

The author also wrote several other college-level textbooks. One of which was on Turbo Pascal. Indeed that book was the first I read on programming and Pascal was the first language I learned when I was 12. I remember his book spent a lot of chapters talking about graphics mode in Pascal and how to draw the Vietnamese national flag. It was quite amazing to see a waving flag at the time with a simple Pascal code. He might have been one of the first people to have done which we call now [the demoscene](https://en.wikipedia.org/wiki/Demoscene).

Dr. Ngoc's work and contribution were well paid off -- he is now a very high-ranking official in the National Ministry of Education.
