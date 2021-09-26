---
title: New Multiplayer Experience
author: TrueBrain
---

With 12.0 in feature-freeze, it is time to talk about what is in 12.0, and why we release early.

In summary: 12.0 makes setting up multiplayer games painless.
You no longer need to configure anything in your home network.
Playing together are now just four simple steps:
1) You just start a server.
2) You set the server to invite-only/public.
3) You share your invite-code with your friend.
4) Your friend joins your server based on the invite-code.

There is no need to setup port-forwarding, or anything like that.
The above will just work, for everyone, as long as you have a working Internet connection.

Depending on your connection, it costs us extra in infrastructure costs, but we hope to cover that with donations.
If our regular donations (thank you so much for those!) run out, we will let you know, and run some kind of fundraiser.
In a sense, I guess, this post is also a fundraiser ;)

As you might understand, this changes the multiplayer experience drastically, and we felt that waiting 6 more months to deliver that to you is not fair.
In result: we are releasing 12.0 early!

In this post I want to explain in a bit more details how we got here and how it works.

<!-- more -->

After our release on Steam, you guys wrote a lot of positive reviews.
Over 95% of them are positive!
I cannot express how happy that makes me: so many of you still enjoy the game, and this number alone makes it worth continue to work on OpenTTD.

But that leaves the 5% that did not like the game.
Although some reviews are just .. weird, a lot of them had clearly written out what they were missing.

The number 1, without a doubt is: no tutorial.
Okay, we see you, and even agree.
Just there is no simple solution for that .. we have some ideas, but it will take a while before that takes shape.

The number 2 was much more interesting to me: I cannot play with my friend.
I even personally notice that, that I often don't play OpenTTD as I don't fancy playing alone.
And setting up port-forwarding is, even for me, not trivial.
So, I don't.

This made me wonder: how hard is it to solve this problem in 2021?
Back in 2007 (when this network implementation was made), there was no real solution, but we are 14 years later .. so, what can we do?

Initially we looked into how Steam does it: SDR (Steam Datagram Relay).
Basically, games using the Steam Multiplayer are likely to use this, and it means all traffic is routed via Steam.
This means that if you can download Steam, you can play together.
This works really well for a lot of people.
And a lot of games make use of this.

The problem for us is two-fold:
using something like this would mean that all the non-Steam players cannot enjoy it, and we still are not sure how to integrate with the Steam SDK.

This made me wonder.
What happens if we build our own "SDR", where we just relay every session via our servers?
It would be very stable, and a lot lower latency for most players (we use AWS, and their backbone is often quicker than a peer-to-peer connection via your own ISP).
The downside?
We would have to pay the bandwidth for every player on a server.
And this is not cheap.
We did some early math, and realised the bandwidth-bill could peak to an amount we cannot cover by donations.

So, if that doesn't work, what else is out there?
If you look into relaying, you find TURN (I will explain this in a bit).
If you find TURN, you find STUN (I will also explain this in a bit).
And this is how VoIP phones work.
VoIP services don't want to pay for bandwidth if they can help it, so what they do is pretty clever:
- First, try to directly connect to the other phone.
- If it fails, try some clever network tricks to connect two phones together (called STUN).
- If that fails, relay the connection via the VoIP servers (called TURN).

As the first two cover 80% of the connections, instead of paying for 100% of your clients, you only pay for 20%.
Which is a lot better, in every way you look at it.
This sounds like a promising solution for OpenTTD too:
- If the server is using port-forwarding, connect to it directly. We call this "Direct IP".
- Otherwise, try to connect the server and client via some clever network tricks. We call this "STUN".
- If that all fail, use our freshly created relay service. We call this "TURN".

And this is what 12.0 delivers.
A very simple, newbie friendly, no configuration needed, network solution.
This will completely change how you play online with OpenTTD, basically.

But this change is not trivial.
Where in the old situation a server always used port-forwarding, it can now be that a server is not reachable from the Internet.
So how does the server know a client wants to connect to him, so we can execute those network tricks?

To solve this issue, we had to introduce a new service: Game Coordinator.
A server always has a persistent connection to the Game Coordinator.
If a client wishes to connect to the server, it tells the Game Coordinator.
And the Game Coordinator can now coordinate (see where the name comes from?) the connection, as it can talk with both the server and client now.

This is a radical change in how OpenTTD does connection setup, and required some huge changes in our code.
In total, 67 file changes, 5955 insertions, 3475 deletions were needed to make it happen.

As added benefit, it also means OpenTTD no longer listens on UDP for public games.
It still uses UDP to discover LAN games, but no longer do you need to port-forward the UDP port if you want to use "Direct IP".
And as cherry-on-top, the "Search Internet" is now very quick, as it gets all the information from the Game Coordinator directly, instead of polling the information from each server one by one.

While at it, we also addressed a ton of other network related things.
See the 12.0-beta1 changelog for more details on this.

In total, we believe this new multiplayer experience will make it a lot easier for you to play together with your friends.

That all said and done, there is still a lot of future work.
This will not be done for the 12-series, and possibly not even for the 13-series, but are things we see as good additions to this new multiplayer experience:
- Integration with Discord / Steam.
- Automatically download BaNaNaS content if possible.
- Change a singleplayer game into a multiplayer game seamless.
And so much more.
But for all these things, we need more help.
So, if you are interested in helping us out, code-wise, to make the above a reality, drop by on IRC and ask where you can help out!

So, you say, okay, fine, this all sounds amazing, but what are those network tricks you use for STUN, and why on earth does that work?
I left this part as last, as it becomes pretty technical. You have been warned ;)

Network stacks have some properties we can use for this purpose.
The most important one is: if you create an outgoing connection, the other side can return data to you over the same connection.
It is often a misconception that an "outgoing connection" only sends data.
It does not.
The only way for the Internet to work, is if every connection is bi-directional.
The "outgoing connection" part just means from which side the connection was initiated: from the inside (called an outgoing connection) or from the outside (called an incoming connection).
Normally, NATs and firewalls block incoming connections, but not outgoing connections.

With port-forwarding you tell your NATs and firewalls to expect an incoming connection on a certain port, and to send those to your computer.
But outgoing connections normally aren't checked, and you can freely create any to anywhere on the Internet.

So, the trick STUN uses comes down to this:
the client and server at the same time make an outgoing connection to each other.
If done properly, both the NATs and firewalls think it is their outgoing connection, and as such allow bi-directional communication between the client and server.
Without anything sitting between them.

But you say: wuth? how? this .. no, this cannot be possible, can it?

Well, no, not in the way I describe above.
We need an extra trick for it to work: a STUN server.
How this works:

- Client asks the Game Coordinator to connect them to server.
- Game Coordinator tells client and server to make a STUN request.
- Client and server connect to stun.openttd.org.
- The STUN server tells the Game Coordinator what the public IP:port is of those connections (note: we deviate from the standard here, as this way was easier for us).
- The Game Coordinator tells the client to switch its current connection from stun.openttd.org to the public IP:port of the server.
- The Game Coordinator tells the server to do the same, but to the public IP:port of the client.
- Now because both are an outgoing connection from the client/server perspective, they both allow the traffic on the public IP:port in from the server/client respectively.

And ta-da! A bi-directional connection between the client and server.

I will need pages more to describe you in technical detail what is going on here, and why this works, but for now, take my word for it.
And if you don't want to, launch OpenTTD 12.0, and see for yourself.

There are a few scenarios the above fails.
The most noticeable: when the NAT is an expensive NAT.
One that tracks if the packets being received on an outgoing connection are in fact of the address it connected to.
Most NATs do not validate this, as there is no security issue, and it takes a lot of resources (CPU + memory) to track all this.
Performance wise, it is just better not to.
But some NATs do.
The expensive types.
The ones corporations have.
So, there we see STUN failing.

Also important to mention that STUN works best with UDP.
OpenTTD uses TCP.
So, a bit more trickery is needed on a technical level, but this also means some cheaper NATs do not always work the first try.
Our solution?
If it fails, just try again ;)

But this does mean STUN doesn't always work.
And this is where TURN comes in:
if STUN fails, we fall back to relaying the session over our relay network.
Of course, we first ask the client nicely if they are okay with their session being relayed, as there won't be a peer-to-peer connection between client and server as they might expect.

Now in result, combining Direct IP, STUN and TURN, every client should be able to connect to every server no matter what, given they can connect to the Internet properly.
And data from the 12.0-beta series show that roughly 20% of the STUN connections fail and need TURN.
This means that we only have to pay for 20% of the users, instead of 100%.
So although our infrastructure cost will go up slightly, it opens up multiplayer for everyone.
In the end, a small price to pay.

So, there you have it: our new multiplayer experience.
From a technical view, a lot more complex.
From a user view, as trivial as it gets.

If you have any further questions or interests about this, feel free to contact me (TrueBrain) via email, Discord or IRC.
