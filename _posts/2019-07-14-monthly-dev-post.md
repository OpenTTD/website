---
title: Monthly Dev Post of June/July 2019
author: People
---

Welcome to our Monthly Dev Post of June/July 2019.
Every month (ahem) one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

June and July have been quiet months for changes in OpenTTD master, but there are a couple of nice development things to talk about, and as always, translations have been added and improved.  Thanks translators!

In this issue: Multi-docks, some tids and bits and the start of an exciting new series: Source Code Entrails!

<!-- more -->

## Development

### Master highlights
There is one big new feature in the master branch: Peter1138 has finished multiple-docks-per-station.  
This is now merged to master and will show up in nightly builds (soon, if not already).
Players are no longer restricted to just one dock per station.
This is a great feature, which continues the recent theme of improving ship transport. Find out more about it at the [pull request page](https://github.com/OpenTTD/OpenTTD/pull/7380).

Three new currencies have also been added: New Taiwan Dollar (NTD), Chinese Renminbi (CNY) and Hong Kong Dollar (HKD).

As usual a couple of bugs have been fixed, notably some improvements to music playback on Windows and a crash using the sprite aligner ([#7609](https://github.com/OpenTTD/OpenTTD/issues/7609)).

Finally some other bugs and performance issues have had some attention, including
* possible framerate issues on Mac systems
* other possible performance issue
* an interesting bug where OpenTTD crashes when opening the industry directory window if a newgrf industry has 5 or more output cargos

### Maintenance mayhem

The current stable branch also received some love with the release of the [1.9.2 update](https://www.openttd.org/news/2019/07/08/openttd-1-9-2.html).

Besides the usual bugfixes, it contains one user visible change: A newly-installed OpenTTD will now default to showing internet server instead of LAN servers in the multiplayer lobby window.

## Source Code Entrails I: The Beginning

### The Idea

Many people have ideas and suggestions how OpenTTD could be made better.
In fact, there's a whole [sub-forum](https://www.tt-forums.net/viewforum.php?f=32) full of them.
Every so often, "I want to make this thing but I don't know how" comes up.

And indeed, looking at the [source code](https://github.com/OpenTTD/OpenTTD.git) of OpenTTD for the first time can be a daunting task.
The `src` folder alone contains 1314 files, and is accompanied by a plethora of other ancillary files.
To make it less daunting to get started with realising your idea, we will explore various parts of the OpenTTD source code and try to build some kind of index to the code.
We are going to assume that you have seen source code before and have some familiarity with the C++ language.
There are thousands of introductory tutorials on programming in general and specific to C++ on the internet, thus we don't think it would make sense to replicate them all here.
Also, If you've never compiled OpenTTD before, we've got [general tips](https://github.com/OpenTTD/OpenTTD/blob/master/README.md#70-compiling) and some specific to [Windows](https://github.com/OpenTTD/OpenTTD/blob/master/docs/Readme_Windows_MSVC.md), along with detailed notes on our [wiki](https://wiki.openttd.org/Compiling).

This is planned to be a multi-part series, to be continued as time permits.

Inspiration for this comes from an interesting treaty by MaiZure: [Decoded: OpenTTD](http://www.maizure.org/projects/decoded-openttd/index.html).
It's a nice read if you are interested in the technical innards of the game and already somewhat familiar with the source code.
Unfortunately, if you are not, the parts MaiZure focuses on aren't the parts you'll predominantly need to be able to write your first working code patch.
Even if you read it again and again, you will know all about how memory pools manage memory in OpenTTD, but still have no idea where to look to make all trains run backwards.
Thus the idea of writing a similar exploration of OpenTTD, but more focused on practical things for the patch writer, was born.

### Diving In

With that out of the way, let's start this series by trying to get some structure into those 1314 source files.
We are focusing on the `src` folder for now and will ignore all the other files and folders until some later part of this series.

Inside this folder you'll find a lot of files and some more folders.
Some of the names speak for themselves, but don't let yourself be fooled by some of the others.
Contrary to what the name might imply, the `game` folder is not the most important folder at all, but only contains code for running GameScripts; all the important game logic is contained elsewhere.
The `core` folder is a similar beast, supplying some low-level scaffolding, but not some mystical nugget controlling all objects in the game.
This should in no way imply that this is superfluous code; the scaffolding is essential part of almost all parts of the game.
But unless you are planning to rewrite whole swaths of the game, it is quite unlikely you'll find any need to change these foundations.

Indeed, most of the interesting files are the ones directly in the `src` folder.
If you just browse through the list of files, you might notice groups of similarly named files that refer to an entity or an concept.
There are, for example, groups of files for entities like `aircraft`, `train` or `station`, and concepts like `economy`.
The OpenTTD source code is structured along those entities; code related to the same thing is kept in files with a common base name.
If you want to modify the behaviour of trains, looking into the files whose names start with train is certainly not a bad idea.
Of course, such a strict division is impossible to keep in all cases.
The code that decides what should happen if an aircraft stops at a station conceptually belongs to both `aircraft` and `station`, even if it can exist in only one place in reality.

You might have also noticed that the file names follow a pattern and that you can find similarly named files in each group.
Many files are named after the following schema: `<group>_<suffix>.<extension>`.
The `<group>` part was already explained above.
The `<suffix>` tells you something about the contents of the file without having to open it inside an editor and can be viewed as a kind of *file type*.
The `<extension>` part is for the benefit of the C++ compiler and denotes if the file is a source code file that is passed to the compiler (`.cpp`) or a header file (`.h`) that is included in other source code files.
There's also the hybrid of a header file containing source code (marked `.hpp`) for C++ template implementations, as they have to be included everywhere they are used.

Let's use the `station` group as an example, as it contains almost all of the common *file types* you can find in the source code.

__`station.cpp`__
: The most obviously named file, but the one with the least defined contents.
The file contains the source code for all the station functionality that does not match any of the files described below.
It is a catch-all for everything without a better place.

__`station_cmd.cpp`__
: One of the most interesting file types in the OpenTTD source code.
Command handlers are the foundations of the user interaction with the game.
In this case, they for example encode the logic that determines where and if a station can be built, what happens when a vehicle stops at a station or how a station should be drawn on the screen.

__`station_gui.cpp`__
: This source file forms the second part of the user interaction by providing the windows visible on screen related to stations.
These are e.g. the station window itself, the station building window or the station list window.

__`saveload/station_sl.cpp`__
: A final source code file hides in a sub-folder.
The folder name already gives a hint, and this file indeed contains everything that is needed to read and write information about stations to and from savegame files.

__`station_base.h`__
: The first header file.
The data for a station is kept in a C++ class, like for many of the other game objects.
The base header contains the declaration of this class, which encapsulates and manages most of the information about a station, like for example the owner, the location or the name.

__`station_type.h`__
: While many other parts of the game need to know about stations, not all parts need to know about the innards of the station class.
To speed up compilation, basic type definitions about stations, like for example the type for station IDs or an enumeration of possible station types, are split into this separate header file.

__`station_func.h`__
: This file exists for the same reason as the previous header and contains function prototypes related to stations.

__`station_map.h`__
: The second main header file related to stations.
Stations are objects that occupy space on the game map and as such need to store some information in the *map array*.
This header file contains all the code related to storing and retrieving this information.

__`station_gui.h`__
: Type and class declarations for the user interface code are contained in this file.

__`widgets/station_widget.h`__
: This header is part of the user interface code.
It is split from the `gui` header to facilitate processing by automated build scripts.

__`table/station_land.h`__
: The final header file isn't a header in the classical sense.
It is included by the code that draws the stations on the screen and was split purely to ease code navigation.


Not all file groups have all the different files just described, but if a *file type* is present, it's usage is generally like described.
Files are usually only split if they would contain a sufficient amount of code, there's no advantage of splitting one or two code lines into a separate file.

And with that said, we are going to conclude this very first installment of the Source Code Entrails series.
We hope this has helped you at least a bit with finding your way through the OpenTTD source code files, even if we've neither talked about all the files that don't fit into the name scheme nor have taken a look inside one of these files yet.

Stay tuned for further installments where we are going the explore the various areas of the game in more detail.

### Closing Remarks

We hope this is something at least some of you find interesting.
The exact format of this series is still fluid and we haven't decided yet how technical and specific we are going to get.
We'd love to hear your comments or questions, both regarding the contents of this installment and the idea for this series itself.

There is no roadmap for the topics of further installments yet, but if you tell us what topics you'd be most interested in, we'll certainly take it into account when deciding about future topics.
If you are interested in contributing content for a topic, drop us a line.

## Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/pulls) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
