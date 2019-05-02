---
title: Monthly Dev Post of May 2019
author: People
---

Welcome to our Monthly Dev Post of May 2019.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

In this issue: NotRoadTypes, code modernization, and some smaller things.

<!-- more -->

## Development

### Highlights

Development last month focused mostly on internal code changes and cleanup.
Some of the user-visible changes are highlighted below.

* The [1.9.1 update](https://www.openttd.org/news/2019/04/08/openttd-1-9-1.html) was born after some issues were found in the 1.9.0 release, including a nasty bug that broke certain NewGRF strings.

* A way of viewing the coverage area of built stations and the result of adding a station part was added.
This meshes with the change how the coverage area is defined that was talked about in the last dev post.

* After a long, winding journey and several nearly-complete rewrites, NotRoadTypes (NRT) was finally merged.
NRT allows NewGRFs to define new road and tram types, similar to how it was already possible to define new rail types.
If you want to try it, there are some basic NewGRFs available, like for example [Unspooled](https://www.tt-forums.net/viewtopic.php?f=26&t=75986) or [Docklands](https://www.tt-forums.net/viewtopic.php?f=67&t=75941).
There are also some road vehicle sets which take advantage of NRT's new opportunities, like [MopRV](https://www.tt-forums.net/viewtopic.php?p=1203552#p1203552) or [SUV](https://www.tt-forums.net/viewtopic.php?f=26&t=82984).
This is a brand new feature, so please keep in mind that these NewGRFs aren't yet fully-fledged but showcase some of the possible features.

### Code modernization

The quest to remove home-grown algorithms and data stuctures in favour of using STL features continues.
Last month, the switch to C++11 threading functions was done, as already hinted at in the last dev post.
These data structures were mostly added in the distant past, either before OpenTTD was written in C++ at all or when the STL was not as performant, but are no longer necessary in modern times.
Several specialised data types used in saveload code were removed in favour of using the new features of typed enumerations.
We removed our home-grown variants of sorting algorithms and arrays and replaced them by std::sort and std::vector/std::array.

This process is expected to continue; less custom code means fewer possible bugs (STL issues aside) and automatic performance improvements whenever compiler or library vendors improve their tools, which lets us focus more on the game code.

### Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-06-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
