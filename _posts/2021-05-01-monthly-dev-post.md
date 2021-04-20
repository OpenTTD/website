---
title: Monthly Dev Post of May 2021
author: People
---

Welcome to your Monthly Dev Post of May 2021.
Every "month" one of these post will be created, to tell you about the latest developments in the world of OpenTTD.

So I haven't written much lately; so what, neither has Shakespeare.

<!-- more -->

## Development

### Highlights

...

### OpenGL issues / crashes on startup

Although we are really happy with the addition of our OpenGL driver, it also seems not all GPUs are as happy with it as we are.
We are tackling the issues as they come in and we can reproduce them .. but especially reproducing is a bit of an issue.
With 1.11.1 we were hoping to fixed most issues, but it seems another subset of (mostly Intel) GPUs seems to say boom now.
Hopefully soon we have it all figured out.

### Steam release

As mentioned in our [OpenTTD Developers Livestream - #3 - Q&A](https://www.youtube.com/watch?v=kFtUGxIGLlg), the Steam release was a huge success.
More than we expected, if we are honest.
The platform seems mostly stable, ignoring the OpenGL issues mentioned above.
As so many users are using the platform, it also gives us incentive to start looking into further integration with Steam.
We will get to this back in a bit.

### Networking

Mostly what stood out from the Steam release, how difficult it is to setup a network game.
And this might sound silly, but it is not something we really realised before.
Back in 2007, from which this network implementation dates, it was one of the only ways available.
But as time went on, better and easier ways to join each other in a game have been invented; and we have not caught up with that.

So, a few days after release, we started work on improving the whole network experience.
This is not an easy task, as there are many moving parts.

The main thing we are addressing, is how multiplayer and singleplayer are more interconnected.
Don't worry, you still won't need an Internet connection to play OpenTTD, but we are making it more fluent.
What this mean is, that when you start a game, you can indicate if you either want a private game (offline, nobody can join), friends-only game (your server is not listed but friends can join, see below) or a public game.

- Private games are what singleplayer is now.
- Friends-only introduces the concept of "invite codes".
This is a short code you can give to your friends.
They can enter it in OpenTTD to join your server.
No fuss, nothing.
It just does works.
- Public games are pretty much like the current public servers.

To allow this to work easier without things like port-forwarding and firewall exceptions etc etc, we will add some modern techniques to OpenTTD to make that all a bit easier.

First of all, we will move away from a mix of UDP and TCP, and switch to TCP only (for now; possibly we go full UDP in the future, but baby-steps).
Additionally, we are changing completely how the master-server (the component responsive for the server-listing) works, and rebranding it to a game-coordinator.

The game-coordinator has a very important task: if player B wants to join the game of player A with the invite code, he should make that happen.
We will use several techniques to make this happen.
- The first is, of course, a direct connect.
This is exactly how the current game works, and only works if you have your network setup for it.
- The second method is a so called STUN.
Not going into any technical details here, but it basically attempts to connect the client and the server in a smart way that doesn't require port-forwarding etc.
The downside? It doesn't work for all network setups.
Especially company networks are known for not allowing this method.
- Third, and this is not 100% sure this will be added, we fall back to TURN.
This is a method where we, as OpenTTD, relay the traffic between the client and server.
If you have a working Internet connection, this method works.
No setup required, no questions asked.
The downside here is that it means we also have to pay for the traffic.
So we have to estimate and test out how likely it is the above methods won't work; hence the "not 100% sure" part.

While we are working on this part of the code, we are improving many other things (mostly as we have to).
But mostly, we are finally redoing the in-game Network GUI.
It should be a lot more user friendly when we are done with it.
Mostly, it will mean you don't have to go to the console that much, to do simple stuff like removing a company or changing your nickname.

As cherry-on-top, we want changing from private-game to friends-only-game to be fully transparent.
That is to say: you say you want to change the visibility of the game, we reload the game in such way that for you nothing changed, but your friend can now join.
Currently multiplayer is not designed with that in mind, but I am confident we will figure it out.

So what does that mean for you?
Well .. no fuss network games.
You or your friend starts a game in "Friends-only" setup.
The other person enters the invite code.
And magic, you are joined together.

Hopefully the end result is a very smooth multiplayer experience for you as user.
As after all, a game is better enjoyed with friends!

### Rich Presence / Steam integration

With this all said and done, it means we can also finally talk a bit about Steam integration, Discord integration (and maybe even GOG integration, who knows).
The main reason we haven't done any of it, is a legal issue: our license (GPLv2) doesn't allow direct integration with non-free licenses like the Steam SDK and Discord SDK.
This is painful to figure out and work around .. but we will get there.

Once we figured that out, the next challenge is a technical one.
In Steam we want to show what you are playing, on which servers, with how many players, etc.
This is information currently not stored.
While reworking the network, we will make sure it is, so this becomes a lot easier.

Additionally, those "invite codes" we mentioned earlier, for platforms like Steam and Discord they will be transparent: you right click your friend and click "join server", and we take care of the rest.
But, as you might understand, it requires all the earlier work to be completely .. it won't be done next month ;)

### Devs playing the game is a horrible idea

So .. while testing if STUN was viable, some devs ended up on the same server.
And they played.
This should never happen, but it did.

Why should it never happen?

We find so many things we want to fix while playing, it is really depressing :P
This happens when you build a game .. you notice everything wrong really easily, which is really frustrating.
So we created a few bugs that really should be addressed .. like for example: there are really few visual cues if rivers go up the hill, making all developers that were online one by one waste a lot of money finding out they have to build really expensive locks.
Shameful.

We have some plans to do some mass-scale testing with the new network changes, which most likely requires a lot of players to show up and test .. so maybe we do this soon again, but together with you .. maybe even on a livestream?
Who knows!

## Extensions & Tools

### Tools

(update about NML here)

### Basesets

(bit of info here about the changes lately)

## Ponies

A "pony" is a personal pet project of a developer or community member. This section will be used in the future to showcase a project in detail.

### ??

### Participate yourself

Do you have an interesting Project you are currently working on in relation to OpenTTD?
These Monthly Dev Posts are prepared in a branch on our [GitHub website project](https://github.com/OpenTTD/website/tree/monthly-dev-post/_posts/2021-06-01-monthly-dev-post.md) before they are made public on the website.
As soon as you are whitelisted as a contributor, it's as simple as editing the file in the web interface.
If you are not a contributor yet, drop by on [IRC](https://www.openttd.org/contact.html) to become one (make sure you have a GitHub account).
