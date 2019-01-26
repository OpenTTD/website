---
title: New website and nightlies are back
author: TrueBrain
---

Modernisation of the hosting infrastructure is proceeding, and we have just brought a new version of this main website online.
But, you say, nothing changed?
You are absolutely correct!

For over the last 15 years, the website was run on Django.
Sadly, over the years, fewer and fewer people knew how to update it, and it stalled.
So, a few weeks back andythenorth and TrueBrain started to port the website to Jekyll, and put it on [GitHub](https://github.com/OpenTTD/website).
It is now connected to a CI/CD.
This means that any contribution can quickly be tested and validated, and anyone with commit rights can update the website.
Including things like news, screenshots, etc!

Additionally, after almost a year of no nightlies, they are finally [back](/downloads/openttd-nightlies/latest.html).
These nightlies are created on new infrastructure, and should be better than ever.
Especially the Mac OS version should be a lot more stable, as it is no longer cross-compiled.

Finally, the new binaries are now served from a CDN; this means downloads should be a lot quicker for a lot more people.

This all took a lot of effort (6+ months of work), and hopefully this makes contributing to these parts of our game a lot easier.

If you find any trains stuck at signals please [let us know](/contact.html), so we can resolve the issue safely without risk of crashes.
