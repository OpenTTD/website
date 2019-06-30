---
title: Monthly Dev Post of June 2019
author: People
---

Welcome to our Monthly Dev Post of June 2019.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

June has been a quiet month for changes in OpenTTD master, but there are a couple of nice development things to talk about, and as always, translations have been added and improved.  Thanks translators!

<!-- more -->

## Development

There is one big new feature: Peter1138 has finished multiple-docks-per-station.  This is now merged to master and will show up in nightly builds (soon, if not already).  Players are no longer restricted to just one dock per station.  This is a great feature, which continues the recent theme of improving ship transport. Find out more about it here: https://github.com/OpenTTD/OpenTTD/pull/7380

Three new currencies have also been added: New Taiwan Dollar (NTD), Chinese Renminbi (CNY) and Hong Kong Dollar (HKD).

As usual a couple of bugs have been fixed
* https://github.com/OpenTTD/OpenTTD/commit/6396ec05fe9ce865a8642231bdb75b45cfb19627
* https://github.com/OpenTTD/OpenTTD/commit/846fc8fe097689ef2fa1498708b3244fb4ad84ac

Finally some other bugs and performance issues have had some attention, including
* possible framerate issues on Mac systems
* other possible performance issue
* an interesting bug where OpenTTD crashes when opening the industry directory window if a newgrf industry has 5 or more output cargos

### Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-07-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
