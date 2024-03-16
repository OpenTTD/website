---
title: Survey & HTTPS & Infra
author: TrueBrain
---

With OpenTTD 14, we introduce an opt-in survey system; a method where we can finally ground our debates with facts!
Additionally, BaNaNaS content will use HTTPS (instead of HTTP), and many more small infra-related changes.

Time to chat about this for a bit.

<!-- more -->

## Survey

For years now, we can have very passionate discussions about one gameplay style or the other.
And often, sooner or later, someone will drop the "that is how 90% of players play" argument in there.

Do they have anything to back up that 90%?
Of course not.
It is an emotional argument in an often emotional discussion (as we all greatly care about the game).
But it doesn't actually help the discussion further, as the other party goes: "no! That is how only 10% plays!".
And as such, the discussion dies off and we are unable to move forward.

To finally settle which 90% was correct, OpenTTD 14.0 introduces an opt-in survey system where, after every game, a report is sent about the settings used in that game.
This is enabled in the 14.0 betas and is already giving very solid insights how the game is actually played; instead of how we all think it is.
It is extremely valuable for further development, to better balance where to put focus.

It is extremely important to us that this survey mechanism is both transparent and privacy friendly.
As such, a lot of effort has gone into ensuring it is both.

When you first start OpenTTD 14, you are greeted by a dialog asking you if you want to opt-in to the survey.
If you don't (either close the dialog or decline), no survey information will ever be sent to us.
But if you do, at the end of every game, a small file is transmitted to us.

What is in it you ask?
For that we created a "Preview" button, which shows exactly what information would be sent.
Nothing more, nothing less.
What is in there, is what we receive.

And if you change your mind (or want to see the Preview again), under "Game Options" you can change your choice at any time.
No strings attached; no nag-screens "are you sure?!".
We highly appreciate it if you enable it.
But if you don't, that is perfectly fine too.

Once received, the survey is processed and checked whether it is a valid survey, for what version, and stored in an efficient way in the backend.
Every once in a while an analyzer runs over all the surveys to produce survey results.
They can be seen [here](https://survey.openttd.org/summaries) with all their details made available.

There are all kinds of protection against over-representing one population or the other, although we still have work to do to tune that system better.
But, as more surveys arrive, we also have more information to improve on this.

So if you are curious how your playstyle is versus many other people: check out the summaries and get an impression!

Just be warned, and I have to remind people about this almost daily: the summaries are a snapshot of that moment in time and can over-represent one group or the other.
Until the actual 14.0 is released, be aware that the sample size is rather small and summaries can differ widely from week to week.
In other words: be careful to not make wrong conclusions on something, based on a result of a single week.

## Popularity

Often it is rumoured that OpenTTD is dead.
We don't see any evidence of that, however you slice it.

OpenTTD development is doing very well, as the new feature list for 14.0 is showing.
But also: the player-base has not declined.

Take for example the [amount of concurrent players on Steam](https://steamdb.info/app/1536610/charts/#all).
In the last 3 years this amount has grown, from ~600 to ~1000.
That is a huge increase.

From internal Steam financial information (yes, free games also have financial information), we can see that the game has been installed by almost 2 million unique users in the last 3 years.
That is so many more players than I ever expected would play this game.

More information from Steam: we can also see how popular our news posts are.
Our 13.0 release post, for example, has been read by 150,000 unique players (with over 2.5M impressions).
That is a lot; especially for a free game that is 20 years old!

When we look at our wiki, we see that weekly ~100,000 unique players visit the wiki for one page or the other.
Most popular is, of course, the tutorial section on the wiki.

And although normally we get around 100 unique visitors per hour on our main website, sometimes there are posts like [this](https://news.ycombinator.com/item?id=39330797) on popular websites.
These posts increase that number to over 12,000 unique visitors in just an hour.

![Hackernews spike]({% link /static/img/post_2024-03-16-survey-https-infra/hn-spike.png %}){:width="100%"}

All in all, OpenTTD has been as popular as it has ever been and many players still play the game day to day.
In fact, we see a (slow) increase in popularity, especially when looking at bandwidth usage.
More on this in a bit.

## BaNaNaS via HTTPS

When BaNaNaS was added back in OpenTTD 0.7, it was done via a custom TCP protocol.
Very quickly we found out that it was bandwidth hungry and we needed a good way to distribute this load.

HTTP was added in OpenTTD 1.0 for this goal and most downloads you do today are actually done via HTTP.
But, as HTTP is less and less common these days, and more and more companies start to block communication over HTTP, it was time to implement HTTPS.

Where our HTTP downloader was a custom build, with all problems that come with it, for HTTPS we use either WinHttp (Windows) or libcurl (Linux / MacOS).
This means that someone else took care of all the complexity of downloads via HTTPS and we have a simple interface to download a file.

With this change we hope many more people can download BaNaNaS content via HTTPS (instead of TCP); this is not only a lot quicker (as HTTPS uses [Cloudflare](https://www.cloudflare.com/), which ensures downloads come from a local Point of Presence (POP)), it is also a lot cheaper for us if you do.

## BaNaNaS bandwidth bill

Hooking in to the above, the move to HTTPS also has another goal: about 10% of our bandwidth for BaNaNaS is till this day done via TCP.
Although the HTTP(S) downloads are free of charge (thanks to [Cloudflare](https://www.cloudflare.com/)), the TCP downloads are not.

To be more exact, as they are served by AWS, it costs 0.90 dollar per GB transferred.
And this grows to a large number very quickly; over 50% of our monthly bill is only for BaNaNaS downloads traffic.

Now there are many ways to mitigate this, ranging from "migrate away from AWS" to "just disable TCP downloads".
But for now, I have good hope that the change to HTTPS will move even more traffic away from TCP.
Related to that, we also removed the setting that forced usage of TCP over HTTPS: OpenTTD now always tries HTTPS first; and only if that fails, it falls back to TCP.
Hopefully that sufficiently reduces the bandwidth bill.

If not, we will need to take action on this.
I keep hoping Cloudflare releases the ability to route TCP (and not just HTTP(S)) via their infrastructure; they keep teasing this in their blog-posts, but they have since 2021.
So at a certain point I have to give up that hope and find a better solution myself.

## Infrastructure

[Our migration](https://www.openttd.org/news/2023/07/09/infra-migration) in 2023 was a great success and continues to be so.
Deployments have never been easier and maintenance has been a breeze.
Auto-healing and incident resolving work as expected and in general, [Nomad](https://www.nomadproject.io/) has been a good fit.
This combined with our new GitHub workflows, there is a clear noticeable difference in how much time is required to keep everything running (for the better, ofc).

Our Cloudflare bill has been very stable; which is very good for a project like OpenTTD, as predictability means we can try new things, and see their impact.

For example, this year we added a Symbols server.
This server collects all the debug-files for all our OSes, making it easier/faster for us to delve into crash dumps people send us.
Before the Symbols server there were a lot of manual actions required to open up a crash dump; now it is just pressing a single button and waiting for a bit.

We also added much more caching to the wiki.
As wiki pages do not change all that often, we can cache them pretty aggressively.
This means that if you go to our wiki now, Cloudflare serves almost every page from cache.
In the background it does validate if any content is out-of-date.
If any out-of-date content is found, the cache is updated with the latest.
For you this means a much faster website; for us it means a lower AWS bandwidth bill.
Around 5% lower, in case you are curious.

![Wiki cache]({% link /static/img/post_2024-03-16-survey-https-infra/wiki-cache.png %}){:width="100%"}

Lastly, a bunch of backend services gained a Prometheus metrics endpoint, meaning they are easier to monitor, what they are up to, and how they are used.
This for example allows us to see how many (percentage-wise) OpenTTD players have an IPv6 enabled connection (answer: 23%) and what versions of OpenTTD are connecting to BaNaNaS.
This helps us understand where to put effort for the backend services and what is "working as expected".

## Donations

As you might know, the OpenTTD infrastructure is fully paid by donations.
And for years now, we didn't need to do a fundraiser, as you all graciously donate enough money in a year to pay the bills.
What helped, especially in the earlier years, that we were often sponsored by companies with infrastructure related sponsorships.

These days we enjoy fewer sponsorships.
This is not always a bad thing; if you are a paying customer, companies are more likely to help you out.
Especially with infrastructure this hasn't always been the case during sponsorships.

That said, two companies do deserve a shout-out, as they do sponsor us still and we greatly appreciate them.

[Pulimi](https://pulumi.com/), to help manage our infrastructure.
[1Password](https://1password.com/), to ensure we can store all OpenTTD related passwords safely.

We told them by email, but also here: thank you so much for your on-going sponsorship; it is truly appreciated.

As for the rest of our infrastructure, we are on our own and the reserve we had is slowly running dry.
This means it is not unlikely we will once again need a fundraiser sooner or later.
When that moment arrives, we will let you know.
Till then, I would like to thank you all for your donations; we really do appreciate them and they keep the (virtual) lights on.

## Future ahead

As for the future, there is a lot of interest for Cloud Saves: something we are still looking into.
With Cloud Saves you would be able to save your savegame in the cloud and continue playing it from where-ever you are.
And as with all services OpenTTD offers, it will not be only available for Steam players, but for everyone (regardless of what platform you use).

The main trouble here is to figure out what the cost per player will be and making sure we can actually afford it year-to-year.
As you can read above, although we are financially healthy, we have to ensure we stay that way.
Which means it will mostly depend on whether the changes in 14.0 help in reducing the BaNaNaS bandwidth bill, before we start extending our services to include new (not-cost-free) services.

The biggest concern we current have: how big will the average savegame be?
Do most players play small maps? Or very large maps?
This is not an easy answer, but will be answered by the survey results.

To give you a rough estimate: the cost for Cloud Saves will be roughly 0.02 dollar per GB per month stored.
If we assume an average savegame to be ~10MB and we allow storing 10 saves per player, that would mean the average player will cost us 0.002 dollar per month.
Or 0.02 dollar per year per player.
On its own not a lot, but if you remember from earlier: we have ~1000 active players per day ... it could add up to a lot of money really fast.
So we need better metrics to know how many players to expect.
And whether ~10MB is fair.

As you can read, lots to do here before we can even start to think about the technical implementation.
These things just don't come for free!

## More about OpenTTD 14

This post is part of the series of dev diaries about big new features coming in OpenTTD 14.
Next week, we will experience some time dilation, and dive into one of the biggest new features in 14: timekeeping!
