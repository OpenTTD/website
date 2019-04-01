---
title: Monthly Dev Post of April 2019
author: People
---

Welcome to our Monthly Dev Post of April 2019.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

<!-- more -->

## Development

### Highlights

The 1.9 release branch had barely been made, before a ton of pending pull requests were merged.
Several changes in queue were pretty much waiting on 1.9 being branched off from master, since they were rather high-risk, and merging them in to 1.9 could have introduced new bugs with too little time to discover and fix them.
Several of these are talked about at length below, but here are some short ones.

* Many performance improvements have been made, through the use of smarter algorithms and data structures.
dP from the [CityMania](https://citymania.org/) community [provided a savegame](https://github.com/OpenTTD/OpenTTD/pull/7235#issuecomment-465280438) with slightly over 50,000 stations, which really brought the game to its knees, both loading and simulating it.
The new fixes together improve performance of this pathological game massively.

* Another big game used for testing is Wentbourne Transport, originally shared on TT-Forums, but unfortunately we can't find the original thread at the time of writing.
Wentbourne is a real game, with a very large number of vehicles: 5499 road vehicles, 4833 trains, 2818 ships, and 749 aircraft.
The pathfinding this this large number of vehicles makes even top-end modern CPUs sweat, and it typically runs at less than 10 fps.
One of the new optimisations added is path caching for road vehicles, similar to the caching introduced for ships in 1.9, and this gives a significant boost to performance.

* A new generic data structure has been added to the library, a [k-dimensional tree ](https://en.wikipedia.org/wiki/K-d_tree) for improving lookup performance of objects in 2D space, in particular "nearest object" and "all objects within rectangle".
(It's not actually k-dimensional in OpenTTDs implementation, it's specialised to two homogenous dimensions.)
This initially helps two cases:
First, and most immediate, is finding the visible viewport signs, that is, station names, town names, player signs.
The second is faster search for which town is local authority for a tile, this especially helps performance of many AIs.

* SamuXarick helped find a particular edge case where world generation took unreasonably long time, and occasionally towns lost their bridges across waterways.
When generating a huge map (4k square) with high number of towns, occasionally towns will end up never building any houses, so get zero population.
These zero-population towns are deleted again during world generation, but it turns out that because bridges owned by towns do not store *which* towns owns them, the game has to search all towns for which is nearest and the potential owner.
When the map is huge (16.8 million tiles) and there are around 10,000-15,000 towns, this search takes a long time.
The fix for this was to look at the road tiles connecting to the bridge, and assume the town owning the roads also owns the bridge.

* Everyone playing OpenTTD, and Transport Tycoon for that matter, have surely experienced stations inside towns eventually getting unmanageably many passengers.
The central bus stop with 3000 passengers waiting is one classic example.
The actual reason for this behaviour is that, when generating passengers, the population of a house is considered twice, one for chance of generating anything at all, and once for upper bound on amount to generate.
A bit of statistics, or making a simulation, will show that the effect is quadratic growth in pax generation: A house with twice the population generates four times as many passengers.
We're adding a setting to control how pax is generated, and offering a new default method, where a house twice the population only generates twice the amount.

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

These changes/fixes can obviously be controversial, so please discuss and ask about them.

### CMake support

Over the last few weeks, we have been working on switching our build system to CMake.
This unifies all build systems into a single one; no more `./configure`, MSVC projects, and others.
This also removes supporting both `awk` and `vbs` scripts, which were doing the same thing.
As CMake also supports (via CPack) releasing NSIS (Windows Installer), Debian, RPM, and more, we will also be switching to that.

This gave us a great oppurtinity to clean up some old and weird quirks in the file structure and build system.
For example, the build folder is no longer in-source.

With support for CMake nearing completion, we are asking for your help.
Please considering testing [this PullRequest](https://github.com/OpenTTD/OpenTTD/pull/7270), and let us know if everything is still working as you expect.
It should support all OSes we support and should auto-detect all libraries.
Please let us know if there are any issues or if you have additional suggestions.
Your feedback will be greatly appreciated!

### DOS support

Years ago someone added DOS as a target, just because we could.
It had some serious drawbacks: no threads, no network, different video-driver (allegro instead of SDL).
This created some huge technical debt:
- We have tons of places where we have to keep in mind that network might also not exist (and DOS is the only one without network support).
- We have special glue to handle threads; and the compiler doesn't follow std::thread (C++11), so we can't switch to that.
- DJGPP (the compiler we use to create DOS binaries) doesn't have support for CMake (to which we are switching).
- Last month we created some test-binaries to see the current state of DOS; turns out, the performance is not good (<1fps).

Considering all these things together, we strongly wondered if having DOS support is worth it.
In the end, especially with the introduction of std::thread, we decided against it.

This doesn't mean we don't love DOS..
If you feel up to it, and can maintain DOS for a longer period, we would love to see a Pull Request reintroducing support for it.
You can simply revert the patch that removed the code, and work from there.

### MorphOS / AmigaOS / BeOS support

In 1.10 we will be dropping support for MorphOS and AmigaOS, as well as BeOS (you can use Haiku instead of BeOS).
We did this as these targets weren't maintained, and were unlikely to work in their current state.
As we are working towards dropping SDL1 in favour of SDL2, and these platforms have no official SDL2 support, that meant either using unofficial SDL2 libraries or dropping support for these targets.
As we have no maintainer, nor anyone to test on these OSes, we decided to drop support for it.

This doesn't mean we don't love any of these targets.
If you feel up to it, and can maintain those targets for a longer period, we would love to see a Pull Request reintroducing for them.
You can simply revert the patch that removed the code, and work from there.

## Extensions & Tools

### Tools

NML gained support for 16 cargoes which was added to OpenTTD earlier.
For NML projects it means that they need to update the code for the production callback.
Check [FIRS](https://dev.openttdcoop.org/projects/firs/repository) for an example.
Existing projects which do not want to make a change will need to use NML versions from the 0.4 branch which will continue to receive updates for the time being.

### Basesets

The basesets [OpenGFX](https://github.com/OpenTTD/OpenGFX), [OpenSFX](https://github.com/OpenTTD/OpenSFX) and [OpenMSX](https://github.com/OpenTTD/OpenMSX) are now hosted under the umbrella of the OpenTTD group.
OpenGFX got a new release (0.5.5) which contains the new GUI sprites for group liveries and lots of translation updates.

## Ponies

A "pony" is a personal pet project of a developer or community member. This section will be used in the future to showcase a project in detail.

### OpenTTD in a browser

For today's showcase, our community member Milek7 has had another go at bringing OpenTTD to the browser using Emscripten:
 - Check it out [here](https://milek7.pl/openttd-wasm/)
 - The changes to the source code this needed are listed [here](https://gist.github.com/Milek7/391554b342d301a3ddb18a9d0a6435a1)
 - And there is also a version [with music](https://milek7.pl/openttd-wasm-music/)

### Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-05-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
