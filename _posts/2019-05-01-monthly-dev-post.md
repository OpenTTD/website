---
title: Monthly Dev Post of May 2019
author: People
---

Welcome to our Monthly Dev Post of May 2019.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

<!-- more -->

## Development

### Highlights

Development last month focused mostly on internal code changes and cleanup.
Some of the user-visible changes are highlighted below.

* Some isses were found in the 1.9 release and thus the [1.9.1 update](https://www.openttd.org/news/2019/04/08/openttd-1-9-1.html) was born.

* A feature to show the coverage area of built stations and the result of adding a station part was added.
This meshes with the changes how the coverage area is defined that we talked about the the last dev post.

* After a long, winding journey and several nearly-complete rewrites, NotRoadTypes (NRT) was finally merged.
NRT allows NewGRFs to define new road and tram types, similar to how it was already possible to define new rail types.

### Code modernization

The quest to remove home-grown algorithms and data stuctures in favour of using STL features continues.
Last month, the switch to C++11 threading functions was done, as already hinted at in the last dev post.
Several specialized data types that were used in saveload code could be removed by using the new features of typed enumerations.
We removed our home-grown variants of sorting algorithms and arrays and replaced them by std::sort and std::vector/std::array.
This process is expected to continue; less custom code means fewer possible bugs (STL issues aside) and automatic performance improvements whenever compiler or library venders improve their tools, which lets us focus more on the game code.

### Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-06-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
