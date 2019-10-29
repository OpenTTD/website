---
title: Monthly Dev Post of October 2019
author: People
---

Welcome to our Dev Post for October 2019.
Every month (ahem) one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

<!-- more -->

## Development

### 1.9.3 Released

OpenTTD [1.9.3 update](https://www.openttd.org/news/2019/09/16/openttd-1-9-3.html) was released in September.

This wrapped up a bunch of bug fixes and and performance improvements, thanks to all contributors.
Sadly we also added one new bug, and forgot to backport the fix for another, though not on purpose!

1. If you have a station where the tile below the sign is not part of the station, you can't make an order to that station.
The workaround is to force the station sign to move (by building another bit of station), or to (temporarily) build a tile for the station below the sign again.

2. An AI can cause a crash if it attempts to measure distance between a waypoint and something else, with aircraft.
See tickets [#7593](https://github.com/OpenTTD/OpenTTD/issues/7593) and [#7766](https://github.com/OpenTTD/OpenTTD/issues/7766).

Meanwhile [OpenTTD 1.10.0-beta1 is being prepared](https://github.com/OpenTTD/OpenTTD/pull/7726).  No release date is known yet, but find it here when it's announced :)

### Updated SDL driver to SDL2.

[Simple DirectMedia Layer](http://www.libsdl.org) is a cross-platform development library designed to provide low level access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D. OpenTTD (usually) uses it on Linux.

[Pull request #7086](https://github.com/OpenTTD/OpenTTD/pull/7086) updates to SDL2, which has been a long-sought upgrade.
This aids future compatibility.
It may also improve performance on some systems, but results on that are inconclusive at the moment.

### Housekeeping

Maintenance commits and small fixes continue.
In September and October 2019 these include updates to the OpenTTD compilation system, fixes to the midi audio driver for some systems, performance fixes and macOS and Windows 7 compatibility updates.

A [game-crashing bug](https://github.com/OpenTTD/OpenTTD/pull/7755) with relocated station signs was fixed, and a [crash when exiting the scenario editor](https://github.com/OpenTTD/OpenTTD/commit/1e5029563cb68e53e41299a5d92e317566d7ba66).

And of course translations continue to be updated.

All changes to OpenTTD master can always be seen on our [GitHub page](https://github.com/OpenTTD/OpenTTD).

### Projects in progress

There are quite a few interesting experiments underway.
These may or may not get finished.
That's the way it goes :)

Nielsmh is working on an improved approach to newgrf industry layouts, which might enable larger industry layouts to be constructed, whilst also offering newgrf authors an easy way to include more variety in industry layouts.

Michicc has an experimental OpenGL video driver in [PR #7744](https://github.com/OpenTTD/OpenTTD/pull/7744).

Peter1138 has a patch for newgrf docks, unless he's lost it :)

Other experiments can sometimes be found in [pull requests](https://github.com/OpenTTD/OpenTTD/pulls) or in developer's own GitHub repos.

### NML (newgrf compiler)

NML docs have been updated with information about 16-cargo support for industries.

NML support for roadtypes and tramtypes (NRT) is also in progress.
The [major changes are done](https://github.com/OpenTTD/nml/commit/62cab41d4a1f84c4b96cf3e5b1fe2439532ba891), and available in NML master.
[Docs are being updated](https://github.com/OpenTTD/nml/issues/46), and a 0.5 release of NML [is planned](https://github.com/OpenTTD/nml/issues/43), to make NRT support widely available to newgrf authors.

### Website

The website features a wide range of [Screenshots](https://www.openttd.org/screenshots.html), but these have been ...few... since OpenTTD 1.4 :)

This was somewhat because the website was hard to update, but the website is now very easy to update.
The intent is to add screenshots more often, including [forum contest winners](https://www.openttd.org/screenshots.html), and any other nice screenshots we can get permission to include.

Got some great screenshots you'd like to put forward?
Open a [GitHub issue](https://github.com/OpenTTD/website/issues) for them, or a pull request.
We might not be able to include all, but eh, let's try it and see how we go?

## Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?

These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/pulls) before they are made public on the website.

As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.

If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).

## Thanks

Finally, to all contributors, bug reporters, translators, play-testers, and those who donate money or infrastructure to help make OpenTTD what it is: **thanks!**
