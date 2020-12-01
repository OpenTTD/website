---
title: Infrastructure migration finished
author: TrueBrain
---

Today is a good day.
Today is the day all openttd.org services run on [AWS](https://aws.amazon.com/).
Today is the day I can finally shut down our [OVH dedicated server](https://www.ovhcloud.com/en-gb/bare-metal/).
Today is the day I can finally retire software like:
- [Django](https://www.djangoproject.com/) 1.2 (released May 2010)
- [Debian](https://www.debian.org/) Etch (released April 2007)
- [MediaWiki](https://www.mediawiki.org/) 1.12.0 (released winter 2008)
- [XenServer](https://xenserver.org/) 6.5 (released January 2015)
- An IRC bot that was not upgraded or restarted since 2016.

This was the longest migration I ever did: 11 months in the making.
But we finally did it!

This was mostly made possible by us receiving [AWS Open Source credits](https://aws.amazon.com/blogs/opensource/aws-promotional-credits-open-source-projects/).
This allowed me to try out AWS services, do stupid things (rack up a bill of more than 500 dollar per month .. which is HUGE for us), and all while knowing it wouldn't clean out our donation-funds (read: the credits covered all our costs for 2020).
Sadly, in 2021 we will not receive AWS Open Source credits .. this means no more experimenting.
So a perfect time to write up what happened over the last 16 years, and more specifically, last 2 years.

This is going to be a long post, so strap in!

<!-- more -->

## History

We start with a bit of history:

In 2004 openttd.org was a website, and a wiki, and that was about it.
In the years after, we greatly extended what we offered on openttd.org:
- Master server, so you have in-game server listing
- Content services, so you can download NewGRFs, Scenarios, and so on from in-game
- Bug-tracker
- Mail
- Maillists
- IRC bots
- Developers-space
- Content Delivery Network (just called "mirrors" back in the days)
- NoAI tournament servers
- Centralized accounts
- Subversion

And I am sure that is not a complete list.
We did weird stuff, not all ideas survived, but boy, we were busy.
By 2007, most things were either invented or there was no interest in developing new services.

## 11 years later

In 2018, nothing much had changed on the infrastructure side.
There were some minor additions, some tuning, but nothing really.
BaNaNaS was still running the same software as it was in 2007.
The centralized accounts still had "coming soon" on the profile page.

### Is this a bad thing, you ask?
Well, yes and no.

From a stability point of view, this was perfect.
Our services could handle the weirdest things .. for example:
- We once got [posted on slashdot](https://games.slashdot.org/story/10/04/06/0519206/OpenTTD-100-Released), which is called the slashdot-effect.
- Once, a [popular YouTube channel](https://www.youtube.com/playlist?list=PLz1xmRxpXfWvEefxXiUo0C8stV6TAsKss) played OpenTTD, doubling our player-base overnight.
- And many more (smaller) events.

What this means is that many people come to your website, download the game.
This sounds cool, but it also increases the load on the services.
Often what you see in these cases, that things crack, and break.
But .. not on openttd.org.
The services survived such insane increase in traffic.
To put it in numbers: we went from between 5 to 15 requests per second, to between 60 and 200 requests per seconds, depending on the event.
This is an insane amount of additional traffic to handle.
But, openttd.org could handle it.
Except for the time a user found a bug in our code that crashed the software .. during such event.
That was fun :P

### So this isn't a bad thing?
Well, no, it is a bad thing.

To give an example: our main website was running Django 1.2, heavily modified.
This was released in 2007.
13 years ago.
There are known bugs for Django 1.2.
We patched those we knew about, but .. this became increasingly more difficult.
This means the chances of someone finding a security-issue in any of the services increased more and more.
This is an accident waiting to happen.
Additionally, because of the old code-base, the code was not published anywhere, making it impossible for anyone else to make modifications.
Not really Open Source friendly.

And of course we upgraded other software once in a while .. but it took me a week (as in, 40 hours) to apply patches on all the systems, validate everything was still working, etc etc.
As I too do this for free, in my free time, the older you get, the more difficult this becomes.
So the work started to stack more and more, up to a point that I found out today that 1 services has been running since 2016.
In no uncertain terms, this is not okay.
It is a disaster waiting to happen; no longer an "if", but a "when".

### So, you say, the problem is that you are maintaining this by yourself?
Find someone else to help out, and the problem is solved too!

Yes, yes, yes, thousand times yes.
That would really help.
But .. I have been doing this for 16 years .. I have had many people come by and say: I am going to help you.
When they dive in a bit deeper, they either realise the immense amount of work that would need to be done, or that it is very repetitive work (login to the system every month, update all the software, validate everything is still operating correctly, log off).
To give a few examples:
- BaNaNaS was going to be replaced with [BaNaNaS v2](https://github.com/frosch123/bananas2).
  I believe the first talk about this was somewhere in 2014.
  It would solve many issues with BaNaNaS v1.
  It was very ambitious.
  In 2017 it was given another go.
  It stalled a few months after.
  There is some initial code (code we reused for BaNaNaS v1.5, more on that later), but not much more than that.
- [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) was running a very old version, and several people said they were going to help upgrading it to a newer.
  We supplied VMs with the current version, so people could experiment with it.
  I never heard back from ANY of them.
  Like .. nothing after the initial offer and talk.

There are many more examples, but I am sure you are understanding by now where I am coming from.
And do not get me wrong: all of those people who offered to help, they did it with the best intentions, and I thank them for reaching out.
But creating software and maintaining infrastructure is hard and difficult.
It is not something you can do on a Sunday afternoon and be done with it.
It takes serious time and commitment.
And myself running towards my 40s, time is not something that is ample anymore.
It was when we were in our 20s, and the university allowed many many many many hours of doing these crazy things.

## Change is coming

So, in 2018, we decided this had to change.
A few drastic changes were made, and many more would follow in the next two years.

The big thing to solve: so far we have been using what is called unmanaged hosting.
This means we get access to a server, and after that we have to do everything ourself.
This is very cheap, and the main reason we used to do this; but it also means you have to put in the hours to maintain it.
As pointed out above .. this was not happening.
So we wanted to switch to managed hosting.
This is a lot more expensive, but also would mean we didn't have to put in the work.
With managed hosting, the provider takes care of many things:

- OS updates
- Security patching
- Keeping the application up-to-date, if you're using a [SaaS (Software-as-a-Service)](https://en.wikipedia.org/wiki/Software_as_a_service)

### GitHub

In 2018, one of the easiest gains was migrating from Subversion to git, and using the [GitHub](https://github.com) to host that.
This means we didn't have to maintain that part of the infrastructure.
We also migrated our bug-tracker to GitHub.
I mean, if you are going to use GitHub, do it properly or go home.

### What about all the other services we run?
We tried out several things, but in the end, I decided it was best to use cloud-solutions.
We asked around every cloud provider if they offer anything for Open Source projects to soften the blow of the increase cost.
I had many "fun" conversations .. luckily we found AWS answering the phone, with their [AWS Open Source credits program](https://aws.amazon.com/blogs/opensource/aws-promotional-credits-open-source-projects/).
They funded 2020 for us, allowing me to experiment with all their services.
This really really helped out, and so we got started in migrating to AWS.

The initial work for this started in January 2019, although we were aiming for [DigitalOcean](https://www.digitalocean.com/)'s [Kubernetes](https://www.digitalocean.com/products/kubernetes/) solution at that time.
For various of reasons this did not work out (mainly their lack of IPv6 for Spaces was a bit of a show-stopper; but we had various of other issues).
DigitalOcean is awesome btw, don't get me wrong; they offer cheap solutions with pretty decent quality.
It is just if you try to run something like openttd.org on it, you are going to find limits.
Our services are complex.
More on that later :)

## A new beginning

***By December 2019***, we started the first thing on AWS: the main website.
We completely rewrote it into Jekyll, making it a lot easier for other people to create posts, etc.
This has been very fruitful, as we never had that many different people creating news posts.

Next we moved easier things to AWS:
- Documentation
- Redirect domains (openttd.com for example redirects to openttd.org)

***By January 2020***, we were ready to run [all our binaries on AWS](https://cdn.openttd.org/).
We used to run our own custom-created mirror network for this.
I cannot thank the owners of these servers enough for sponsoring us with free bandwidth!
But now it was time to use a proper CDN (Content Delivery Network).
What this means for you, that downloading the game was a lot quicker from that moment on.
A CDN delivers the downloads from servers near you, drastically increasing the speed you download with.

## BaNaNaS

The next huge problem was BaNaNaS.
As mentioned earlier, it was old.
And other rewrites never took off .. so how are we going to run this on AWS, while making it a lot easier to maintain?
Here I got a lot of help from `frosch`; together we rewrote [BaNaNaS](https://github.com/OpenTTD/bananas-api) completely, from the ground up, where [all data](https://github.com/OpenTTD/BaNaNaS) is stored on GitHub (and AWS S3).
But we kept the functionality nearly the same as the current version.
By scoping it like this, a rewrite became possible.
It was still a huge effort, and took several weeks to complete.
We named this BaNaNaS v1.5, as it is not really v2 as we would have hoped, but it was clearly better than the current v1.

***In April 2020***, this went live.
The [code for BaNaNaS](https://github.com/OpenTTD/bananas-frontend-web) is now on GitHub too, and changes can immediately be deployed.
Don't underestimate this last statement: any change we make to BaNaNaS on GitHub can be live within 5 minutes.
This is a huge Quality of Life, and allows many more people to help out and directly see the results of their labor.
Additionally, we adapted a "staging / production" setup, where we run all services for openttd.org twice:
a smaller version called ["staging"](https://bananas.staging.openttd.org/) where we can test out if our changes are what we expect them to be, and the full version called ["production"](https://bananas.openttd.org) which you normally visit.

By this time we also decided to stop doing our own centralized account system, and start using the GitHub [OAuth2 flow](https://blog.oauth.io/introduction-oauth2-flow-diagrams/) to authenticate people.
This would mean we no longer had to run this service ourself, and no longer had to store (and protect) emails of users.
A win-win.

After bringing BaNaNaS to AWS, our monthly bill skyrocketed.
Where we normally spend ~100 dollar on infrastructure, it was now 500+ dollar.

Why?
Because of two BaNaNaS uploads: [abase](https://bananas.openttd.org/package/base-graphics/61423332) and [zBase](https://bananas.openttd.org/package/base-graphics/7a423332).
These are 32bpp base graphic sets.
Their size is huge (compared to other uploads).
Combined, they cost us ~300 dollar per month of bandwidth.
And this is the downside of cloud-solutions: bandwidth is often very expensive.
Don't worry, we never had to pay for this, as we used our Open Source credits to fund this experiment.
Before 2021, we will offload these files to [a much cheaper solution](https://www.ovhcloud.com/en/vps/), outside of AWS.
As we don't receive enough donations to pay such bills monthly ;) (not a complaint, just an observation)

## Master Server

The next service that needed migration, was the [master server](https://github.com/OpenTTD/master-server).
This too was a bit of a mess.
So the same approach as with BaNaNaS was used.
***By September 2020***, this was also running on AWS.
I can write several posts about the issues of getting this to work .. but as it is one of the more boring services, let's skip that for now.

## Eints

[Eints](https://github.com/OpenTTD/eints), our translation tool, was the next on the list.
After some fixes done by `frosch`, mainly to switch to GitHub OAuth flow for authentication, this was mostly painless.
***By October 2020***, this was running in production.

## Wiki

The last huge pain in our ..., was the wiki.
Running mediawiki on AWS is nearly impossible; if it is possible, it would be very expensive, an amount we wouldn't be able to pay.
Also, the content on the wiki wasn't maintained in years, making it one giant mess.
`frosch` initially set out to "fix" this problem, by looking into other software like [gollum](https://github.com/gollum/gollum/wiki).
They store their data in git, which means massive edits are a lot easier.
After a few weeks of frustration, it became clear this was not really going to happen.
So, I gave a crack at writing my own wiki software, and [TrueWiki](https://github.com/TrueBrain/TrueWiki) was born.
Surprisingly, it only took 2 week (of 40 hours) to write; lot less than for example BaNaNaS.
But the many tricks learned writing BaNaNaS and the master server, helped out a lot.
`frosch` in meantime set out to [restructure the wiki](https://github.com/OpenTTD/wiki-data) completely.
He looked at every single page and decided where it should go.
I often consider maintaining infrastructure boring, but pfft, happy he did it, and not me.
Absolutely respect for that madness.

***In November 2020*** we brought the new wiki online.
Of all the services we revamped, not the smoothest rollout.
Mainly because it turns out google.com has a problem with re-indexing website since October 2020, and still hasn't reindexed the wiki at the time of writing this post.
This caused many players to land on wiki-pages that did not contain what they were looking for.
A rough launch, but it is looking better now.

## Cleanup

Next there were a few remaining services:
- Mail, which is now kindly hosted by [Zernebok](https://www.zernebok.com/) (thank you `orudge`!).
- IRC bot, which is the one I migrated over ***today***.

So that means finally we get to the end of this story: all our services are now hosted on AWS!

## And the result is ..

Maintaining them has never been easier. We only have to do a few things:

- Every month, [pyup.io](https://pyup.io/) comes by and bumps all dependencies for all our (Python) software.
  After merging that Pull Request, we can test it on staging.
  If no issues are found, we can make a new production release.
  Anyone can do this, and me (`TrueBrain`) and `LordAro` have been doing this for the last few months.
  It takes a few minutes per service a month, at most.
- Every month, I have to redeploy some things on AWS, so it gets the most recent version of the OS.
  This is nearly fully automated: I just have to change a 4 into an 8, and a few minutes later the 8 back in the 4.
  In more detail: I scale up the Auto-Scale Groups from 4 instances to 8, and later from 8 back to 4.
  This is enough to fully reinstall the system and get the latest versions.
- Every 6 months, I need to rotate secrets.
  Okay, this is the most boring part, honestly, and it takes ~4 hours to do so.

Now if I compare where we came from: 40 hours a month of maintaining everything, down to ~1 hour a month.
That is an insane difference.

Additionally, everyone can help out!
So the [bus-factor](https://en.wikipedia.org/wiki/Bus_factor) (how many people need to get hit by a bus before you have an issue) is no longer 1, but like .. 10+?

In short, and I know I completely failed at keeping it short: this is truly a very good day.
Finally the burden of maintaining an impossible infrastructure has been lifted.

### The downside?
Our monthly bill doubled, so we might need to do a fundraiser at some point (we haven't done so in years, as you guys are awesome in donating anyway! Thank you so much for that!).

## What's next?
With all this work done, I think we have created an infrastructure that will last us another 10 years.
Hopefully with the same stability as the last infrastructure.

So that brings us to the question: is there anything left to do?
Well, for the migration, no.
But there are other things that can now be picked up.
For example, we have "vanilla", the OpenTTD version you download from [openttd.org](https://www.openttd.org), but there are also other versions out there that are as awesome (or more awesome?) as the "vanilla" version.
Take for example [JGRPP](https://github.com/JGRennison/OpenTTD-patches/releases), an OpenTTD version with many many many patches applied (called a patchpack).
These versions of OpenTTD deserve to be more in the spotlight.
Ideally, what I would like to see, if that the openttd.org services integrate better with such versions.
A lot has been done for this in the background .. and now we finally have the time to bring that to the end-user.

Additionally, there are a few ideas in my head I would love to make a reality.
The biggest would be to have "cloud saves", where you can login in-game, and load/store your savegame online (fully optional, of course).
This means that where-ever you are, you only have to download OpenTTD, and you can continue your savegame.
To put a cherry-on-top, there is [some initial work](https://github.com/OpenTTD/OpenTTD/pull/7510) on making OpenTTD playable from the browser.
Combine these two things, and you have a game you can play where-ever when-ever.
For me, this would be a cool addition to the openttd.org services we offer.
Sadly, with the AWS Open Source credits running out this month, and it being very difficult to estimate what the cost of such addition would be, I am not sure I would be able to pick it up.
Time will tell .. time will tell!

Do you want to contribute, have your own ideas, or think you can help me out? Drop by on IRC (irc.oftc.net, #openttd), and let's chat!

## Closing words
If you managed reading it this far: my compliments, and thank you for reading.

I would also like to thank [OVH](https://www.ovhcloud.com/) for the awesome service of the last 10+ years.
Problems that did arise with our dedicated server(s) were often picked up by OVH staff before I had to tell them, and resolved in a very short time period.
OVH is awesome!

Also thank you to [AWS Open Source program](https://aws.amazon.com/blogs/opensource/aws-promotional-credits-open-source-projects/), without them, we wouldn't be running on AWS.

And mostly, thank you to `frosch`, for together building this new infrastructure.
He even used vacation days to finish up the wiki migration .. how is that for dedication!
Give him some love when you see him, and buy him a (virtual) beer if you can.
