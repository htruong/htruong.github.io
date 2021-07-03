---
layout : "post"
title : "Is your computer too slow to keep up with your typing?"
---


From time to time, I have the pleasure of hearing a claim so outrageous, it's almost unbelievable. One such claim is that the computer/OS being too slow/laggy to type (ordinary documents) on. I heard it from two different people on two different occasions.

So the claim was the computer that can do a bazillion operations on your computer can't even process and display text as fast as your hand can type. Can it possibly be true?

Here is my video summarizing what I found. If you rather read, read on.

<iframe width="560" height="315" src="https://www.youtube.com/embed/UeUN4MRVzAo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Cool storytime
--

First, a little bit of clarification. The stories I heard were not about computers typing English, they were about computers typing Vietnamese. Vietnamese is basically Latin with a couple funny hooks on top of the characters, like this: `Tiếng Việt`. To type Vietnamese, one of the most popular methods (now it has become de-facto) is TELEX. TELEX uses the unmodified Latin keyboard to express the hook by certain simple rules. An example would be to get `Tiếng Việt`, you type `Tieengs Vieetj`. There, two `e`s make the `ê`, `s` makes the `ế`, and `j` makes the `ệ`. Therefore, creating an IME for Vietnamese is a tedious job, but there were no heuristics involved, so it is possible to make a very high-performance IME. This problem is very much solvable and has been solved many times.

The first time I heard about the computer being slow was around 1998 when I was a kid in Vietnam. At the time, there was a profession called "typist," whose job was to digitalize handwriting or poorly photocopied books/documents. That's one of the services provided by then-popular photocopy shops (like FedEx print shops here). At the time, Vietnam's de-facto word processor was Microsoft Office 95/97 on Windows 95. Back then, there was no Unicode, so Vietnamese documents utilize special fonts that have high-ASCII characters replaced by Vietnamese characters. Using the English version of Office with Vietnamese fonts worked well enough for most people. Given the IME program (named ABC, widely used in North Vietnam and in governmental offices) was originally written for Windows 3.1 and the computer has gotten so much faster since working with Vietnamese was already relatively painless.

I visited a photocopy shop one day, and I saw a lady who typed so extraordinarily fast -- I don't think I have seen anyone typing as fast as she did since! Instead of using just Windows and MS Office, the typist switched to MS-DOS from time to time. On MS-DOS, she used a Vietnamese text editor called [BKED that I wrote about](/posts/bked-gui-as-tui.html). BKED has a lot of limitations so I was intrigued as to why she didn't "just" use MS Office. She told me that it's because typing Vietnamese with Windows is slow. With BKED, everything is so limited, but the program is fast and can keep up with her for once. That claim surprised me.

The second time I heard about it was from my friend in 2008 or so. At that point, Unicode was widely accepted as the standard and the IME of choice for most people in Vietnam was the (mostly open-source) program called Unikey that runs on Windows. There were two versions of Unikey, the newer version is 4.x -- that is a core rewrite of 3.x. The 4.x release has so many features (and it was free) that upgrading wasn't even a question. When I hung out with my friend in the coffee shop, I saw her still using 3.x and I inquired. She responded: The 4.x felt slow and 3.x felt fast to her.

So I went on to investigate myself and from my impression, there was something different about Unikey 3.x that makes it actually more pleasant to use. Maybe it was the performance? So I changed some of the features of Unikey 3.x to match what of 4.x (because the author never released the source code for 4.x) and used it myself, and [posted the modded version on my website](/projects.html). 

Since then, I mostly switched to Linux, and I never felt the same kind of responsiveness on Linux typing Vietnamese compared to typing with Unikey on Windows -- there was something odd I couldn't tell why. Maybe it's because the IME in Linux underlines the pre-edit words while Windows doesn't?

Nonetheless, I never had the chance to empirically check the claim of speed myself.

Mythbusting the performance claim
--

I was inspired by prior attempts to understand keyboard latency, notably [Ben Eater's](https://www.youtube.com/watch?v=wdgULBpRoXk)
and [Dan Luu's](https://danluu.com/keyboard-latency/). If you haven't read or watched their attempts, I suggest you watch Ben's video now, it will be relevant to what we discuss here.

I thought it would be possible to do such a latency test for Vietnamese IME across systems. Since the USB latency issue has been investigated by Ben, I don't plan to redo it. I will just use and a USB keyboard and pretend that USB latency is acceptable. This USB keyboard limitation makes it hard to verify the first claim about DOS being faster (because I don't think we have a USB HID keyboard driver for DOS). Overall, I am less concerned about the latency from pressing the key to the character displays on the screen. I am more concerned about whether the overhead of the IME can keep up with the keystrokes I make.

Since I don't type fast enough or consistently enough, I thought to make a piece of hardware to type for me. My initial thought was to use an Arduino to send the keystrokes. However, since I have a Raspberry Pico laying around, I decided it's time for me to learn Raspberry Pi Pico. I modified the tinyUSB's HID composite example so that when I hold the button on the Pico, the Pico will send the HID keys as follows: `### Tieengs Vieetj thaatj giauf vaf ddepj<Enter>`, where `###` is the sequence number, it increases by one for each line. The leading number is typed by the microcontroller itself to help me keep track of how many lines have been typed since I started holding the button. With the help of the IME on the host computer, the computer will output something like `012 Tiếng Việt thật giàu và đẹp`. 

Next is to figure out how fast should we make the keyboard type. Sending keys to the computer via the HID protocol is not straightforward. Ben Eater mentioned that USB is a polling protocol. The host computer checks for the key on the keyboard every so often. TinyUSB library allows the guest device to configure that interval. I configured it to the highest frequency possible -- that is `1000Hz` (the host computer is supposed to poll every `1ms`). It means that theoretically, I can send 1000 keyboard events every second. Now we have to send a key-up event for each key-down event so that halves the number of keyboard events we can send to 500 events per sec.

Other than polling rate, there are other interesting tidbits as well. It seems that the [standard HID protocol allows us to specify 6 simultaneous keyboard scancodes](https://www.devever.net/~hl/usbnkro) on every poll (event). So with effort, we can stress the system to `500*6=3000` keystrokes per second. However, I decided 500 keystrokes per second is probably good enough. 

I don't think any human being can achieve the rate of 500 keystrokes per second consistently. However, we have to keep in mind that human keystrokes are very bursty, we can probably type a word we're familiar with really fast.

So I tested it on a couple of systems. I have the following setups:

- A Thinkpad X1 Nano running Ubuntu 21.04 ("ThinkPad X1 Linux") with 11th-gen Core i5 (Editor: Kate, IME: iBus-bamboo packaged with Ubuntu).
- A vintage Thinkpad X40 running Windows 2000 ("ThinkPad X40 Win2k") with 1.2Ghz Pentium M (Editor: Notepad, IME: Unikey 3.6). The Thinkpad also runs MS-DOS within Windows 2000 ("ThinkPad X40 DOS") (Editor + IME: BKED).
- A vintage Core i5 "Ivy" desktop running Windows 10 64bit ("Ivy Desktop Win10") (Editor: Notepad, IME: Unikey 4.3).
- A Macbook Pro 2015 (Monterey Beta) ("Macbook Pro 2015") (Editor: TextEdit in plaintext mode, IME: Built-in aka Unikey engine). 

To make sure that I didn't have a bug in the Raspberry Pi Pico code, I decided to do a sanity check. I let the Pico type without an IME on the Thinkpad X1 and counted the keystrokes per second. It managed to type 100 (correct) lines of `### tieengs vieetj thaatj giauf vaf ddepj<Enter>` in around 8.78 seconds on my stopwatch. Each line is 42 keystrokes so that makes out to 4200 keystrokes in total. The rate is: `4200/8.78=478` keystrokes/sec. This looks correct. That means any slowdown is due to either the OS or the IME. For every system, I set a baseline with no IME to see the difference that the OS/HW makes.


The table summarizes my results across the system.

| System                | IME     | Editor  | Completion time | Correct? | Remarks     |
| --------------------- | ------- | ------- | -----------     | -------- | ----------- |
| Thinkpad X1 Linux     | None    | Kate    | 8.78            | Y        | Baseline - Doesn't produce Vietnamese              | 
| Thinkpad X1 Linux     | Bamboo  | Kate    | 8.42            | N        | Every now and then have a leading number wrong (1) |
| Ivy Desktop Win10     | None    | Notepad | 11.00           | Y        | Baseline - Seems buffered towards the end                   |
| Ivy Desktop Win10     | Unikey4 | Notepad | 10.57           | Y        |                    |
| Thinkpad X40 Win2k    | None    | Notepad | 8.93            | Y        | Baseline                   |
| Thinkpad X40 Win2k    | Unikey3 | Notepad | 8.50            | N        | First two lines were not good, everything after was good (2) |
| Thinkpad X40 DOS      | None    | EDIT.COM| 50.59           | Y        | Baseline - Extremely buffered            |
| Thinkpad X40 DOS      | BKED    | BKED    | 26.02           | Y        | Extremely buffered (3)            |
| Macbook Pro 2015      | None    | TextEdit| 46.75           | Y        | Baseline - Extremely buffered            |
| Macbook Pro 2015      | Built-in| TextEdit| 120.01           | Y        | Extremely buffered and painful (4)            |

Remarks:

1. It was surprising to me that the IME literally got the numbers wrong. It doesn't have to process anything in that case. Sounds like a bug. When I switched to sublime text, it got a lot of words wrong, but sublime is not native to KDE so I don't know whether I should blame it.
2. It looks like the processor branch prediction needs to be trained for a while for it to be efficient.
3. Really surprised me that BKED is actually 2x faster than DOS 7.1's EDIT.COM running fullscreen.
4. macOS was extremely disappointing in every regard. Even a text without IME fills up the buffer and the text is backed up.


Conclusion
--

It is easy to see that the keyboard feels slow is not just a subjective experience. It is true that with some programs/hardware, the computer can lag behind your keystrokes and can even produce incorrect result when you type too fast. This issue is especially observable when combined with a buggy or slow IME. 

Both macOS and Linux trailed behind Windows in terms of accuracy and performance even when compared to a very old Windows computer.

Even though I wasn't a fan of macOS's Vietnamese IME, it took me by surprise how poorly macOS does with regard to typing text. Even without the IME, macOS does extremely poorly when it comes to processing and rendering text. Loooooong after I stopped holding the button, macOS was still typing and keeping up from the buffer. Something in the stack is very inefficient. 

In most regards, Linux is actually much better than expected, given the Bamboo folks fix the number bug in its engine. The issue is very serious when it comes to Sublime Text, but that's another issue.

Although the performance in DOS was abysmal, I think it's due to the emulation layer in Windows rather than it's the OS that makes it slow. Unfortunately, I haven't found a way to do HID under DOS. USB is not a good implementation to understand the limits of DOS-based programs. The findings in this test do not disprove the fast typist's claims of DOS being faster. 

Windows + Unikey remain the kind of the hill. It has served the Vietnamese community right since early 2000. Huge kudos to Pham Kim Long who wrote this wonderful engine.

If you want to replicate my result, I have uploaded the source code of the [keyboard tester program to github](https://github.com/htruong/tinyusb/commit/1ecd3dc57829f7d89acd319bd8b9dcb33b10bb04). Any microcontroller capable of running the tinyUSB stack should be able to run this program.