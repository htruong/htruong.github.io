---
published: true
layout: post
title: "Knowing who is interviewing with Google"
---

My first bug bounty with Google is totally an accident while I was interviewed for their software engineering job this March. 

Google has two to three stages of interviews before they decide to hire someone. For the last stage, they fly the candidate in for an on-site interview, and I qualified. The recruiter briefly mentioned to me that they were experimenting with a new third-party travel compensation system called Concur. I have listened to a lot of Concur ads on my favorite podcast Freakonomics. On that system, with Google-provided username and password, you'd have to declare your personal information such as your passport number, gender, address, emergency contacts, etc. in order to book a flight.

The username they sent to me to log in to Concur was quite peculiar: [numbers]@gcandidate.com. *Gcandidate.com* - what the heck was that? It pulled up a blank page. The first thing I figured out was that the account name @gcandidate.com is totally cosmetic, it doesn't really mean anything and the account has my email address associated with it. Second, the domain gcandidate.com was not registered. 

**Hmm.** I thought those were strange decisions but those alone don't pose any security risk per se. In any case, I thought there are a whole bunch of people who are much smarter than me interviewing with Google every day, if that was actually exploitable, there is no chance in heaven someone hasn't already figured that out. 

Sadly, I didn't make it in the last interview, then got really bored this August and decided that since no one has registered the domain yet, I thought I could as well register it. I would set up a prank when people check it out - Rick Astley peeking out or something. Admittedly, I never had time to set it up.

Two months ago, I got an error email to [numbers]@gcandidate.com (not mine):

![](/assets/posts-images/concur1.png)


**Hmmmm.** So Google were still using Concur. Someone forgot their password and thought that the login ID was the email address they need to provide to the Concur's password request form, and thus, Concur *complained to me* that it wasn't right. I thought that was going to happen, can't blame the person.

Last week, I got another email from Concur and began to get annoyed. So I re-read the email Google sent to me in March:

![](/assets/posts-images/concur2.png)

Upon inspection of the email I've got, I became very suspicious that Google recruiters create accounts with the default passwords being 'fixed_prefix'+ numbers, which I was able to confirm later. **Hmmmmmmm?** The default password is essentially useless. The only information you ever need to login to candidates' Concur pages, provided they haven't changed the default passwords, is just the account number. I myself didn't change my default password until the last day I need to book the flight. I do occasionally have account numbers, because people occasionally forget their password and occasionally mess up and request password resets the wrong way. At that point I knew I had a legitimate (however hard to exploit) bug in hand. 

Upon further investigation, I've also found out that Concur doesn't have a CAPTCHA system to prevent people from spamming their login page. You can exploit even without being able to monitor the emails to gcandidate.com domain. Given you know how the default passwords are determined, you can write a [GUI interface using Visual Basic](https://www.youtube.com/watch?v=hkDD03yeLnU) to brute force the login page with random, fixed length ID numbers. I also think that the account IDs are assigned sequentially, making it unnecessary to brute force. Testing that would require poking around with Concur. I felt really uncomfortable doing that, so I ultimately decided to not try. So, if you want to know who are interviewing with Google, that'd be enough for you to get to a lot of profiles. 

In the past week I tried to contact Concur security to suggest them to add CAPTCHAs for failed logins (or some other solution). Technically, it is not a security problem by itself, it just makes Google's mistake much easier to exploit. I was impressed with how responsive Google security was. I was unable to get any response from Concur -- however, I was informed that Concur has worked with Google to fix the problem.

The domain is theirs now, my dream of rickrolling their candidates remains a dream. But the dream of having my first vulnerability discovery is no longer one.

Disclaimer: In the finding of the security bug, I accessed a single (other) candidate record, destroyed the data and not to use this data for anything else but to demonstrate the bug.

Timeline:

- 07/31/2017: Registered prank domain
- 09/29/2017: First password reset request to my email
- 11/25/2017: Second password reset request to my email
- 11/27/2017 at 5 PM: Sent vulnerability report
- 11/27/2017 at 6 PM: Acknowledgement from Google
- 11/28/2017: "Seems like Concur's fault. They are not us."
- 11/28/2017: Provided more justifications that is actually Google's fault
- 11/28/2017: "Nice catch" (accepted) from Google
- 11/28/2017: Contacted Concur via Twitter/Got response "Contact us via online form"/Contacted via the online form/No replies
- 11/30/2017: Asked Concur again via Twitter - No replies
- 12/05/2017: Bounty decided ($500). Issue fixed. Google asked me nicely for the domain
- 12/06/2017: "If you are planning to blog about it, we are happy to review a draft and give you feedback."
- 12/06/2017: Domain is transferred back to Google


*Plug: I am looking for a job in the US and worldwide in August 2018 after finishing my postdoc at NCSU. If you are or you know someone who is looking for a passionate engineer who is experienced in interdisciplinary science research, high-performance software engineering and embedded hardware knowledge with security in mind to hack novel problems and can sponsor a h1b visa, please feel free to connect. [My resume (PDF)](/resume.pdf).*
