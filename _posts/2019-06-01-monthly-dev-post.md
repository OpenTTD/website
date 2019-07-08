---
title: Monthly Dev Post of June/July 2019
author: People
---

Welcome to our Monthly Dev Post of June/July 2019.
Every month (ahem) one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

June and July have been a quiet months for changes in OpenTTD master, but there are a couple of nice development things to talk about, and as always, translations have been added and improved.  Thanks translators!

In this issue: Multi-docks and some tids and bits.

<!-- more -->

## Development

### Master highlights
There is one big new feature in the master branch: Peter1138 has finished multiple-docks-per-station.  
This is now merged to master and will show up in nightly builds (soon, if not already).
Players are no longer restricted to just one dock per station.
This is a great feature, which continues the recent theme of improving ship transport. Find out more about it here: https://github.com/OpenTTD/OpenTTD/pull/7380

Three new currencies have also been added: New Taiwan Dollar (NTD), Chinese Renminbi (CNY) and Hong Kong Dollar (HKD).

As usual a couple of bugs have been fixed, notably some improvements to music playback on Windows and a crash using the sprite aligner ([#7609](https://github.com/OpenTTD/OpenTTD/issues/7609)).

Finally some other bugs and performance issues have had some attention, including
* possible framerate issues on Mac systems
* other possible performance issue
* an interesting bug where OpenTTD crashes when opening the industry directory window if a newgrf industry has 5 or more output cargos

### Maintenance mayhem

The current stable branch also received some love with the relase of the [1.9.2 update](https://www.openttd.org/news/2019/07/08/openttd-1-9-2.html).

Besides the usual bugfixes, it contains one user visible change: A newly-installed OpenTTD will now default to showing internet server instead of LAN servers in the multiplayer lobby window.

## Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-08-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
