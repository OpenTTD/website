---
title: Monthly Dev Post of March 2019
author: Many monkeys
---

Welcome to our first Monthly Dev Post.
Every month one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

## Development
- road to next release (beta/RCs)
- a curated list of notable PRs

## NewGRF

## Infrastructure

### Our first beta since GitHub migration

We had our first beta in February.
This was a test of the new infrastructure.
[Azure-Pipelines](https://dev.azure.com/openttd/OpenTTD/_build) now generates our releases, which are published on the CDN of DigitalOcean.
Our [main webpage](https://www.openttd.org) links correctly to the new infrastructure for this new beta.
[Many issues](https://github.com/OpenTTD/website/compare/9858a4952a29535f6912d209dbbace64b6c625ca..48daaf209774131facbddee0f4afb679167c1880) were found and solved during this process.

### Building Pull Request / Patch Packs

We produced the [first binaries](https://www.openttd.org/downloads/openttd-pullrequests/pr6811/latest.html) for a Pull Request, in a (infosec) safe way.
This took a huge effort, and was what we have been building up to for the last 6 months.
This also means we can build and publish PatchPacks now.
If you are interested in building and/or publishing your own PatchPack, please [contact TrueBrain](https://www.openttd.org/contact.html) how to do that (short answer: Azure Pipelines and our CDN are at your service).

### Migration to DigitalOcean

Slowly we are migrating everything to the new Infrastructure (Kubernetes on DigitalOcean).
One of the biggest step so far, is using the DigitalOcean CDN.
The latest downloads ([1.9.0-beta2](https://www.openttd.org/downloads/openttd-releases/testing.html) and [nightlies](https://www.openttd.org/downloads/openttd-nightlies/latest.html)) are now on the CDN.
This should drasticly improve download speeds for most people, and increase availability in general.

### Finger / automated tools

On [OpenTTD/#48](https://github.com/OpenTTD/website/issues/48) we are having a talk about how to create the new 'finger'.
The old way of doing is no longer really viable (as it was not maintainable), and we are now looking into new ways to give tools access to all available downloads.
We are looking for people that use `finger.openttd.org`, and are interested in helping out what would work going forward.
So far the solution has been a low-tech `listing.txt`, but building REST APIs or others solutions are up for discussion!

## Ponies
- features that are hold back until after next release?

## Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD? These developer blog posts are prepared in a branch on [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts) [TODO:link to prepared file for next month] before they are made public on the website. As soon as you are whitelisted as a contributor, it's as simple as editing the file on the webinterface.
