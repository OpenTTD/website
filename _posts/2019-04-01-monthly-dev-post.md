---
title: Monthly Dev Post of April 2019
author: People
---

Welcome to our Monthly Dev Post of April 2019.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

<!-- more -->

## Development

### Highlights

* Optimisation work, talk about the weird massive saves that have been tested with

### Fixing old exploits?

We have added two changes to the master (future 1.10) that can be described as fixes for old exploits.

The first is a new optional feature:
Prevent player stations from serving industries that have their own neutral stations.
This for example prevents a player's train station next to an oil rig from receiving oil from the oil rig.
To transport the oil from the oil rig, the player must instead send ships (or aircraft) to the oil rig, and would not be able to deliver passengers to the oil rig via train either.
The default for this feature is the old behaviour, i.e. you have to opt-in to the more challenging gameplay.

The second is not optional, as we have agreed to classify it as a bug fix:
Changing the way catchment area works for "sparse" stations, i.e. stations with multiple parts, that don't form a single rectangle.
Intuitively, the radius and shape of one station part's catchment area should not affect the size and shape of other station parts' catchment areas, but it did.
In fact, the catchment area was calculated from the station's bounding rectangle, such that a single bus stop distant-joined to an airport could expand the catchment area massively.
This is now changed, so the bus stop distant-joined to the airport only extends the catchment area in the 7x7 area immediately around it, and there may even be a gap between the total catchment area parts.
As an added bonus, the fixed code is even faster than the old, through the magic of improved data structures.

These changes/fixes can obviously be controversial, so please discuss and ask aobut them.

### DOS support

Years ago someone added DOS as a target, just because we could.
It had some serious drawbacks: no threads, no network, different video-driver (allegro instead of SDL).
This created some huge technical debt.
We have tons of places where we have to keep in mind that network might also not exist (and DOS is the only one without network support).
We have special glue to handle threads; and the compiler doesn't follow std::thread (C++11), so we can't switch to that.
Additionally, we are working towards CMake support.
DJGPP (the compiler we use to create DOS binaries) doesn't have support for that.
Last month we created some test-binaries to see the current state of DOS.
Turns out, the performance is not good (<1fps).
Considering all these things together, we strongly wonder if having DOS support is worth it.
So we ask you: would anyone mind of we drop DOS support, so we can use modern techniques to build OpenTTD?
Let us know on the forum thread what you think!

### MorphOS / AmigoOS / BeOS support

In 1.10 we will be dropping support for MorphOS and AmigoOS, as well as BeOS (you can use Haiku instead of BeOS).
We did this as these targets weren't maintained, and were unlikely to work in their current state.
As we are working towards dropping SDL1 in favour of SDL2, and these platforms have no official SDL2 support, that meant either using unofficial SDL2 libraries or dropping support for these targets.
As we have no maintainer, nor anyone to test on these OSes, we decided to drop support for it.
This doesn't mean we don't love any of these targets.
If you feel up to it, and can maintain those targets for a longer period, we would love to see a Pull Request reintroducing them.
You can simply revert the patch that removed the code, and work from there.

## NewGRF

## Ponies

A "pony" is a personal pet project of a developer or community member. This section will be used in the future to showcase a project in detail.

 ### Participate yourself

 Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-04-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
