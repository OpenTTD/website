---
title: Why no release (or nightly) yet?
author: Rubidium
---

A post on a security mailing list notified the world about a backdoor in the LZMA library, which is part of XZ Utils, on the 29th of March.
This library has been used for over a decade for compressing OpenTTD's saves.
Given the current knowledge about the backdoor, it seems OpenTTD is not vulnerable.

Most distributions have reverted back to an older version of the library that does not seem to have the backdoor.
This includes the (vcpkg) package management system that OpenTTD uses to build its executables.
However, GitHub has removed access to the source of the library and as such our build infrastructure cannot build the executables.
As far as we are aware, we have never released an OpenTTD (nightly) with the known vulnerable version of the library.

We do not know when, and in what fashion, access to the library will be restored.
Until then there will be no releases, as making a release in which you cannot open any of your recent savegames would be a bad experience.


<!-- more -->

## What is OpenTTD doing about this?

Practically nothing, but still a lot.
A work-around for the removed access to the library on GitHub is to use a fork of that library.
The question is, how safe is such a fork?
Might that contain another backdoor?
Who knows?

What we are doing is leaving the "heavy" work to the security researchers that are currently at work trying to get to the bottom of the problem, and check all of the recent changes to the library.
We are hoping that this work will be completed soon, but we rather have that the work is done correctly.
We assume that at that point the (vpckg) package management system will update their configuration, so we can get a safe version of that library.
At that moment the nightlies should start being built automatically, and once that is completed we will follow that up with the 14.0 release of OpenTTD.


## Why were there nightlies after the 29th?

OpenTTD has caches for libraries downloaded via the (vcpkg) package management system.
This means that normally we do not need to redownload and rebuild all libraries during our builds.
As a result we can keep building until the caches get invalidated.
On one of the platforms this cache got invalidated after the nightly of the 31st, so the nightlies are failing since then.

And if the nightlies fail, then the build for the release will fail too, as it would be using the same caches.
