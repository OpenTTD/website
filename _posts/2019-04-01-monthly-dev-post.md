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
