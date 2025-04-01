---
title: Release or not?
author: Rubidium
---

It has been a long tradition to make a new major release around this time.
The notable exception has been 12.0 in October, but all others were in February, March, April or May.

This year we intended to do the same, but some external things have thrown a spanner in the works and when we could make a release, we didn't have the time to do so.

So, what's throwing the spanner, and how do we know it affects releases?
Well, our nightlies are de-facto releases that go through most of the steps of normal releases, so when the nightlies fail we know our releases will fail too.

Mostly it's our building infrastructure, or rather the infrastructure a few levels behind that.
We make use of GitHub's infrastructure which provides so-called runners.
These runners are being updated with the newest versions of compilers and tools every now and then.

The first problem was with Steam's tool to upload binaries.
For some unknown reasons, besides there being a new version of the tool, uploads started to fail.
A few weeks after that a new release of the tool was made, and uploads started to work again.

The current problem lies even deeper.
For our external dependencies we use a tool called vcpkg that packages libraries and arranges most of the difficult work for us.
Now the build tool called CMake has been updated, which has removed support for old versions of their file format, specifically those before 2016.
A few libraries in vcpkg still use this old format because little has changed or to remain compatible with older systems.
Problem is, we are using a few libraries with such an old 'minimum' version of CMake.
The result is that we cannot build OpenTTD with the building infrastructure.

With the appropriate bug reports these issues will be solved, but it takes a while for the release processes to propagate.
Actually, due to there being many runners and them not being all updated at the same time, the problem starts to randomly happen (or disapper) until all runners have been updated.

Is this a bad thing for OpenTTD?
One one hand it is, as it sometimes makes releases/updates harder, but on the other hand it saves us a lot of work.
Back in the days we were running our own building infrastructure, we had to manually maintain updates for the operating system.
We had to manually build libraries to be used in the builds, and then distribute those.
Updating the compiler for Mac OS could literally take days of work to go through all the motions to get it working.
Adding or updating a library could take weeks to coordinate manual builds by several developers, now it's minutes to configure it and half an hour to test it on the building infrastructure.

You as someone who wanted to tinker with the code had to download precompiled libraries and set some very specific configurations for your compiler.
Now you start your IDE and it likely starts automatically configuring (CMake) and fetching the required libraries (vcpkg).
So in the end, it's usually better until some weird package starts failing in mysterious ways.
Luckily those failures are rare occurences.
