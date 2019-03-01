---
title: Monthly Dev Post of March 2019
author: Many monkeys
---

Welcome to our first Monthly Dev Post.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

## Development
* road to next release (beta/RCs)
  - regression bugs

* a curated list of notable PRs
  - Network version change

## NewGRF

The following things will not be part of the 1.9 release, however we announce them here because we want to get Feedback from NewGRF authors, before they are made final and put into the master branch

* The first one is additional information about Railtypes, covered in Pull Request [#7000](https://github.com/OpenTTD/OpenTTD/pull/7000), which aims at things like making dual mode vehicles feasible
  - Var4A gets additional information about the railtype the vehicle is on, like speed limit and whether it has a catenary on top.
 
   This should allow for graphical changes like whether or not pantographs are raised. Ideally, you would not only be able to query the speed limit of the railtype, but a collection of all speed limits currently affecting the train (like bridges, curves, station approach, etc.) and whether the train has reached any of these. If you have ideas how to use this in a set, please tell us.
  - A new 60+ var is introduced that lets you query the "vehicle is powered" flag as if the vehicle is made for a different railtype
  
   With this, you can implement dual power vehicles without knowing all the railtypes present. just ask "if this were an ELRL vehicle, would this vehicle be powered?"
  - On a more general level, introduce a new method to have global variables (in the 00-3F range for Varaction 2, or the 80-BF range for Action 7/9/D) with parameters (similar to variables in the 60-7F range)
  - with this new method, a way in action D to detect whether two railtypes you listed in your railtype translation table were actually mapped to the same or different railtype in the game
  
   If for example a railtype GRF according to the [Standardized Railtype Scheme](https://newgrf-specs.tt-wiki.net/wiki/Standardized_Railtype_Scheme) is loaded, you can detect this way if different weight classes are modelled in the GRF, or if they are all mapped to the same basic railtype. Then you can set vehicle availability e.g. for heavier wagon loads accordingly, to avoid useless duplicate wagons.
* The second one is a change to how vehicle introduction works, covered in Pull Request [#7147](https://github.com/OpenTTD/OpenTTD/pull/7147)
  - In the current system, each vehicle gets its own lifespan (randomized introduction date, reliability curve, retirement date)
  - with the proposed change, all vehicles that get introduced on the same "raw" introduction date get the same randomized values
  
  So if you e.g. have a 2-car EMU and a very similar 4-car EMU, you can put them on the same introduction date, and their prototypes will be offered at the same time, they will reach the same peak reliability, and they will go out of service at the same time.
  Also, you can make all freight wagons of the same generation appear on the same date.
  
  If you want to introduce vehicles in a similar timeframe, but they don't need to share the same introduction date and reliability curve, then you can set their "raw" introduction dates very closely apart (in 1 day increments), and it will get different random values (the game will round the final introduction date up to the next full month, so moving the date by 1 day should have no notable difference)

If you want to give feedback to these proposals, like ideas how to use these in a NewGRF, or further requests, or maybe you see a problem with these changes, please reply to the Issues on GitHub or on the [NewGRF Development Forum](https://www.tt-forums.net/viewtopic.php?f=26&t=84875)

## Infrastructure

### Our first (two?) beta since GitHub migration

We had our first (and second) beta in February.
This was a test of the new infrastructure.
[Azure-Pipelines](https://dev.azure.com/openttd/OpenTTD/_build) now generates our releases, which are published on the CDN of DigitalOcean.
Our [main webpage](https://www.openttd.org) links correctly to the new infrastructure for this new beta.
[Many](https://github.com/OpenTTD/website/compare/9858a4952a29535f6912d209dbbace64b6c625ca..48daaf209774131facbddee0f4afb679167c1880)  [issues](https://github.com/OpenTTD/OpenTTD/compare/5b74118ae77cd7c931fc833b174522b77cf00737..6e211908588ab5272336d0d2db3bbb4020f7004f) were found and solved during this process.
A second beta was needed because of a [(network) game breaking bug](https://github.com/OpenTTD/OpenTTD/commit/0151fe998a999b48b67afa5b96d9a4cd72246455) found in beta1 immediately after release.

### Building Pull Request / Patch Packs

We produced the [first binaries](https://www.openttd.org/downloads/openttd-pullrequests/pr6811/latest.html) for a Pull Request, in a safe (in infosec terms) way.
This took a huge effort, and was what we have been building up to for the last 6 months.
This also means we can build and publish PatchPacks now.
If you are interested in building and/or publishing your own PatchPack, please [contact TrueBrain](https://www.openttd.org/contact.html) how to do that (short answer: Azure Pipelines and our CDN are at your service).

### Migration to DigitalOcean

We are still on the slow process of migrating everything to [DigitalOcean](https://www.digitalocean.com).
We make now use of their [managed Kubernetes cluster](https://www.digitalocean.com/products/kubernetes/), and switched this month to their [CDN](https://www.digitalocean.com/products/spaces/).
This last change has been a huge step in the migration towards DigitalOcean.
The latest downloads ([1.9.0-beta2](https://www.openttd.org/downloads/openttd-releases/testing.html) and [nightlies](https://www.openttd.org/downloads/openttd-nightlies/latest.html)) are now on the CDN.
This should drasticly improve download speeds for most people, and increase availability in general.

### Finger / automated tools

On [OpenTTD/website#48](https://github.com/OpenTTD/website/issues/48) we are having a talk about how to create the new 'finger'.
The old way of doing is no longer really viable (as it was not maintainable), and we are now looking into new ways to give tools access to all available downloads.
We are looking for people that use `finger.openttd.org`, and are interested in helping out what would work going forward.
So far the solution has been a low-tech `listing.txt`, but building REST APIs or others solutions are up for discussion!

## Ponies
* features that are hold back until after next release?
  - NRT?

## Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2019-04-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
