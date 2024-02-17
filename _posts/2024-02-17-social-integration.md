---
title: Social Integration
author: TrueBrain
---

Always wanted to know what kind of OpenTTD game your friends are playing on Steam, Discord or GOG Galaxy?
You finally can!

![Discord Example]({% link /static/img/post_2024-02-17-social-integration/discord.png %})

<!-- more -->

In OpenTTD 14.0, we ship a plugin system which allows OpenTTD to integrate with platforms like Steam, Discord, GOG Galaxy, etc.
This didn't come easy, and is the work of many years figuring out what the best approach would be.

When we first released on Steam back in 2021, it became clear that we would love to integrate with Steam.
Only two months after our release on Steam, we started to figure out how to make this happen.
In that same month a first draft was created ... and it took until now to make that a reality.

We have been asked many times over these three years why we didn't integrate with Steam yet; why it is taking this long.
So in this blog post, we will shed some light on what was needed for this to happen.
Answering the question: why does it take so long?

Let's delve in!

## Licensing

The first hurdle we had to take wasn't technical at all: how do we deal with all the different licenses involved with integration on these platforms.

As you might know, OpenTTD is released under GPLv2.
This is a good license for an Open Source game, as it ensures that everyone who makes a modification to the game also have to release the source for that modification.
And, if we would like to, we can integrate that change back into the vanilla game again, allowing everyone to enjoy that modification.

There is one downside of the GPLv2 license: it is not really compatible with many other licenses, as it is kinda strict in the implications.
I am not going to delve too much into the details in this post, but just know once something is GPLv2, everything it touches has to be GPLv2 or compatible with it.

To integrate with social platforms like Steam, Discord, etc, you have to make use of an SDK they supply.
As you might have guessed by now, they are not licensed under a so-called "free" license, which conflicts with our GPLv2 license.

Besides the legal part of the license, we also have the social part of "how people feel about it", if we would integrate such non-free SDKs directly into the game.
And this has always been a debate.

As it goes in the world of Open Source Software, people tend to have a very strong opinion about the "free" part of the license.
And so integrating with something non-free is against the principles, and as such, by their argument, bad.
We can't simply dismiss such arguments because we want to integrate with social platforms.

Which means we needed to find a balance: make sure OpenTTD as a game remains Open Source, free, and GPLv2 licensed.
But also allow integration with social platforms.

The solution, as it turns out?
Make it a choice.

## Plugin system

To ensure the game itself remains licensed under GPLv2, we created a simple plugin system which allows us to extend the game with other binaries which might be licensed differently.
We have been doing this for years and years now, via our [BaNaNaS system](https://bananas.openttd.org).
This delivers in-game content to the user, while the author of such content can license it how ever they like.
The only "demand" we make, is that the author gives us the right to distribute their content, and that it is available free of charge.

In result, we see a wide variety of content on BaNaNaS, under all kinds of licenses.
Some authors embrace the ideology of OpenTTD, and use open or free licenses.
Others are more protective of their work, and do not allow anyone to make derivatives of their work.
From our point of view, we don't actually mind either way: as long as our players can download it for free and enjoy the content, we are more than happy and grateful for your efforts.

The plugin system that is added to 14.0 uses the same logic and mechanism.
Although technically it is very different, more on that later, but from your point of view it is the same: download a plugin, put it in the right folder, and enjoy the added functionality.

Currently we release three plugins: Steam, Discord, and GOG Galaxy.
The source of those plugins are released under MIT licenses; another Open Source license, with much simpler conditions compared to GPLv2.

## Security is a thing

Content uploaded to BaNaNaS is executed in the game via sandboxes: nobody can read files on your computer, make network connections, or anything like that.
They can only do things we allow the addons to do, which is a very restrictive set of actions.

This is a lot harder for a plugin system that integrates with platforms like Steam, Discord, GOG Galaxy, etc.
We can't sandbox those really, as they have to be native binaries (executables) that run on the player's system.

So, we have a dilemma: if we would allow a plugin system in the same way we allow BaNaNaS content, anyone could upload a plugin for anyone to download.
And that plugin could, in theory, contain things that are harmful to the player.
For example, a bitcoin miner or something silly.

This meant we had to find a balance between allowing such plugins and not allowing anyone to just provide any plugin.
What we came up with, is a system where a plugin can only be loaded into OpenTTD, if we, the OpenTTD Development Team, approved the plugin.

We find this less than ideal, as we like that BaNaNaS allows anyone to come up with ideas, try them out, see what people think.
But, we also have to keep the security of players in mind.
And there is just too much potential for harm when we would open up the plugin system to anyone.
As such, we were left with no other choice than to restrict who can make those plugins; or of course, not do it at all (which is even less ideal).

In result, every plugin is released and signed by OpenTTD, and before loaded into the game, it is validated the signature is correct.
If you are a developer and want to design your own plugin, please come talk to us.
We are not against new and different plugins; but we have a responsibility to the players to ensure it doesn't compromise their security.

## Capabilities

With the licensing and security finally addressed, and a solid idea how to build the plugin system, we started work.
But as you can imagine, it was a lot of work, with a lot of moving parts.
Like ... seriously, it took many hours figuring all this out, and getting it right.

An additional challenge was that we release for three OSes: Windows, Linux and MacOS.
And they all deal with plugins in a slightly different way; enough to be challenging.
A lot of testing, failing, trying again went into getting this right.

Which also meant we had to make choices: get something to work now, and build on it later, or try to do everything at once, potentially never finishing it at all.
We went for the first approach, but it also means the current capabilities of the plugin system are rather limited.
So don't think too much of it yet.

The main thing it currently does is announce you are playing the game, whether you are in the Main Menu or in-game, and what kind of map-size you are playing.
Other things like being able to join each others games etc is all not implemented yet, but hopefully someone will pick that up for the next version.
But, as always, no promises there.

## How does it work?

When you first start OpenTTD 14, a new folder "social_integration" will be created in your OpenTTD documents folder.
In here plugins can be installed, for example the [Steam plugin](https://www.openttd.org/downloads/steam-social-releases/latest).
You have to extract its content in this "social_integration" folder, and start the game.

When the game starts, it is validated that the plugins are signed off by OpenTTD, and if they are, they are loaded.
The first step for the plugin is to check whether the social platform is running.
If so, it starts the integration with that platform.
A plugin can only integrate with a platform if it is running when OpenTTD starts; so make sure Steam, Discord, or GOG Galaxy is already running before you start OpenTTD.

Under "Game Options" -> "Social", you will find whether the integration is running.

!["Game Options" -> "Social"]({% link /static/img/post_2024-02-17-social-integration/game-options.png %})

For Steam, we automatically add the Steam and Discord plugins.
For people downloading the game manually, they have to download the plugins manually as well.
This is explained on [the download page](https://www.openttd.org/downloads/openttd-releases/testing).

## The future

With the biggest hurdles out of the way, the future is bright.
We now finally have the ability to extend OpenTTD in a way that doesn't violate our license or the spirit of the license, while still integrating with non-free platforms.
And that in a secure way.

This means that for next versions we can start looking into other parts of these platforms, like making use of their network capabilities (joining people's games, but also maybe making use of Steam's relay network), or possibly even achievements.
We also really would like to deliver these plugins via BaNaNaS, so updating is a lot easier (currently you have to manually download them from our website).

All this will not happen overnight, and maybe not even in a few years.
But instead of having to deal with all the above things, developers can now focus on that what is actually interesting: the plugins themselves.
Of course this requires people working on this, so if you like a challenge and want to help out: please drop by!
Any help is greatly appreciated.

Personally, I am mostly looking forward for the ability to just join someone's game by right clicking on the friends list and clicking Join Game.
A lot of things have to be created to make this possible.
For example, when you are currently in a Single Player game, nobody can join.
But in a modern game this is a very outdated concept; better would be that when someone wants to join a Single Player game, it automatically upgrades to a Multiplayer game and allows your friend to join.
And of course we need to ask you if you are okay with your friend joining.
As you can imagine, a lot of work is required to make this happen.
But I think it will be awesome when it does!

## In closing

I hope by now you understand that integration with social platforms was not only a technical challenge.
We also had to deal with both the legal side of licensing, and with the spirit of our license.
Additionally, finding a way to keep things secure yet configurable wasn't easy either.

In total it took over 3 years of figuring out how we want to do it.
And over 3 months of actual work to program it all and ensure everyone was okay with this implementation.

It was a journey, one could say.
But finally we are here.
And I can't wait for the next step!

## More about OpenTTD 14

This post is part of the series of dev diaries about big new features coming in OpenTTD 14.
Next week, we'll ...
