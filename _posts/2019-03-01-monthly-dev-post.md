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

Slowly we are migrating everything to the new infrastructure (Kubernetes on DigitalOcean).
One of the biggest step so far, is using the DigitalOcean CDN.
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
