---
title: OpenTTD's infrastructure in 2023
author: TrueBrain
---

This post is part of a two-part series, of which this is the first.
In this post, we go a bit into the infrastructure that runs OpenTTD, from BaNaNaS to our main website.
The [second post](/news/2023/07/09/infra-migration) will explain a bit about the migration we just did to get to this infrastructure.

Often I get comments that people are surprised how complex OpenTTD's infrastructure is, and why that is.
With this post, I will try to explain a bit what is going on in the backend, and why it takes a bit of effort to keep everything running smoothly.

<!-- more -->

The question: how does OpenTTD's infrastructure look, or even: why is it so complex, is a rather complicated question to answer in a few words.
The most accurate answer to the first is: look at over yourself in our [Infrastructure-as-Code](https://github.com/OpenTTD/infra) repository.
But that is hardly helping anyone understand the concepts.

I will highlight some of the services we use from providers like AWS, Cloudflare, etc, and what backend services we deliver ourself.

## Providers and their services

To build OpenTTD's infrastructure, we try to reuse as many existing components as possible.
Sadly, as we have a very specific need, this isn't always possible.
Take for example our in-game content service (called BaNaNaS): this has to be custom made, as there is no service like it.

Nevertheless, even those services use as many existing components as possible.
To give you a bit of a feel for it, let's delve into a few of them.

### Cloudflare Pages

[Cloudflare Pages](https://pages.cloudflare.com/) allows hosting of a website over HTTP(S).
You upload HTML pages, and it takes care of the rest.

It has one drawback: it is meant for (mostly) static sites.
This is changing quickly with the integration with Cloudflare Workers (see below), but even then it is not meant for fully dynamic sites, like BaNaNaS, server-listing, etc.

We use Cloudflare Pages for everything that is mostly static.
This includes our main webpage, the survey-results, but also OpenTTD's Pull Request Previews.

### Cloudflare R2

All binary files are stored in [Cloudflare R2](https://www.cloudflare.com/products/r2/), basically a bucket service.
All BaNaNaS content, releases, nightlies, etc: they all go here.

None of our R2 buckets are connected directly to a public domain; there is always a Cloudflare Worker in between, making sure the requests are valid, making sure our CDN feels like directory listing, etc etc.

~~One important note here is, that Cloudflare's access sucks balls (sorry, there really isn't any reason to sugarcoat this one).
There isn't any RBAC yet, which means that if you create an API token for Cloudflare R2 with Write access, it can write in EVERY BUCKET, including the deletion of files.
This of course is a potential security issue, as we need our services (like BaNaNaS, or when we make a new nightly) to write in those buckets, and that code can make mistakes (we are all human after all).
To harden things a bit more, even writing a new file to R2 is done via a Cloudflare Worker.
An interesting fact is that a Cloudflare Worker can be bound to a single R2 bucket, where it cannot access any other.~~

~~This is really the only real complaint I have about Cloudflare; although AWS's IAM is far far better, if we consider AWS's IAM all the way on the right side of the access rights spectrum, Cloudflare's API tokens are far on the left.
There is a lot of room between those two, and I hope Cloudflare addresses that soon.
Either way, slapping a simple Cloudflare Worker between it really isn't the biggest problem.~~

Update: by now Cloudflare addressed this issue, and R2 API tokens can be scoped per bucket.

### Cloudflare Workers

[Cloudflare Workers](https://workers.cloudflare.com/) allows running small pieces of Javascript or WASM in the Cloudflare network, to handle HTTP(S) traffic.
It can do all kinds of things, like serving files from Cloudflare R2, redirect traffic, cache pages, and much more.

In that sense they are very similar to AWS Lambdas, just way more powerful.

Almost all our websites have a Cloudflare Worker in front of them to handle one thing or the other.
For example, when you visit [https://forum.openttd.org](https://forum.openttd.org) you end up on a Cloudflare Worker, which returns a redirect message.
But also our [CDN](https://cdn.openttd.org) makes use of a Cloudflare Worker: R2 (and any bucket service for that matter) normally doesn't serve `index.html` when you visit a folder.
But to give the CDN the look and feel of a directory listing, it is important that it does.
This is what the Cloudflare Worker is taking care of.
If you visit a folder, it actually requests the `index.html` and serves that; it looks to you like it is listing a directory, but in fact it is just serving a HTML file.

### Nomad

[Nomad](https://www.nomadproject.io/) is similar to Kubernetes, AWS ECS, AWS EKS, Azure AKS, etc, but a bit simpler to work with in a day-to-day.
Where in Kubernetes you can do everything, Nomad is more opinionated, and because of that does a lot more things for you.

A nomad cluster consists of different nodes, or Nomad clients.
A client can run jobs, which either can be a script, or a container, or really anything.

In total we run five Nomad clients for OpenTTD:
- 2 public facing clients.
- 3 internal clients.

All clients are hosted on [AWS EC2 T4g](https://aws.amazon.com/ec2/instance-types/t4/) instance, the cheapest EC2 instances AWS has.
This type is an ARM64.

To keep the AWS infrastructure as cheap as possible, we wanted to avoid needing a NAT gateway: if you use IPv4, you need something that allows you to talk with the outside world.
On AWS you do this by installing NAT gateways.
Sadly, those are (relatively speaking) rather expensive.
So instead, we run as much as we can IPv6-only.
This allows us to use an egress-only gateway, which avoids the need for a NAT gateway.
There are a few issues with using IPv6-only, but we will touch on that in a second.

Ideally we would do without the two public facing clients, but this is not possible (yet).
Although we can route all our HTTP(S) traffic via Cloudflare (see below), our custom TCP protocols can not.

To solve this, there are two solutions:
- Either use an AWS service (read: AWS's NLB), which costs 30 USD a month.
- Or build a Network Load Balancer yourself.

We picked the second option here, and run our own NLB on the two public facing clients.
Nomad made this painfully simple, and took only a few to set up properly.

The other issue to solve for any cluster, is service discovery.
Nomad's built-in service discovery helps out a lot, but it leaves for a last mile: how does an external connection know where a service is running.
For this we run nginx on all clients in the cluster.
Nginx uses Nomad's service discovery information to forward traffic to the right instance.
As example, if a service is running on port 12001 on client B, the nginx on all clients are configured to accept a connection on localhost on port 12001, and redirect this to the correct service.
This makes it very simple to route information, and Nomad automatically updates the configuration when it changes.
This means that if a service is restarted, and launches on client C for example, the nginx is automatically reconfigured to forward all traffic to client C now.

Lastly, most services work with a canary: this means that when a service is updated, first a new instance is launched.
If this turns out to run stable, nginx is reconfigured to use this new instance.
Only then the old instance is shut down.
This should, in theory, gives the least amount of downtime possible.
Even during software updates.

### Cloudflare Access

To reduce the attack surface on our infrastructure, only the two public facing clients have open ports from the Internet.
And only those ports used for our custom TCP protocols are opened.
Everything else is kept internal, including the communication with Cloudflare.

For Cloudflare to talk to our Nomad cluster, we use [Cloudflare Access](https://www.cloudflare.com/products/zero-trust/access/).
Or, more specifically, [Cloudflare Tunnels](https://www.cloudflare.com/products/tunnel/), part of Cloudflare Access.

All three internal clients run an `cloudflared` instance, which creates several outbound connections (over IPv6) to connect to several Cloudflare Point-of-Presence (PoP).
Via this connection, Cloudflare can talk to our internal services and back.
The way Cloudflare Tunnels and our Nomad cluster works, means it is very resilient to outages:
- As `cloudflared` is connected to at least three PoPs, if one goes down, the other two take over instantly.
- When one of the Nomad clients drops, or is replaced, there are at least two more Nomad clients that run `cloudflared`, and Cloudflare will use them instantly.
This means you, as end-user, notice as little as possible from updates, outages, crashes, etc.

An example: say you visit [https://bananas.openttd.org/](https://bananas.openttd.org/).
You first enter Cloudflare, which uses one of the three tunnels to reach one of the three internal clients.
Here, nginx picks up the connection, and routes you to the actual service running in the Nomad cluster.

It is impossible to create a direct HTTP(S) connection to our backend services from the Internet.
It is always routed via Cloudflare.
The benefit of this is that Cloudflare has their [Web Application Firewall](https://www.cloudflare.com/waf/) running on our HTTP(S) communication.
This means that if people want to play nasty and find issues in our services, they first need to bypass Cloudflare's WAF.
And this is not an easy thing to do.

### Internal traffic is IPv6-only

As mentioned above, all internal traffic is IPv6-only.
It is only Cloudflare and the two public facing Nomad clients that listen on IPv4.

There are a few challenges here.
The database for the BaNaNaS backend services is hosted on github.com, and github.com sadly doesn't listen on any IPv6 address.
Similar for Sentry (which we use to monitor for errors in the backend services) and Discord.

To overcome this problem, where we can't talk over IPv6 to these services, we have several proxies running on the Cloudflare network to close this gap.
Basically, we don't call github.com, but we call github-proxy.openttd.org.
Cloudflare routes the request to github.com over IPv4, and everyone is happy.

Owh, and no, you cannot use those proxies yourself.
We whitelisted those proxies on Cloudflare Access to only the IPv6 range used by our Nomad cluster.
Sorry (not sorry).

## OpenTTD's Backends

So now we all talk the same language for the providers and their services used, let's touch upon our own backends.
We will not go in too much detail on those; if you want to know more, I suggest looking up the repositories involved.

### BaNaNaS (in-game content-service)

All our content is stored on Cloudflare R2.
There are three backend services involved:

- [API](https://github.com/OpenTTD/bananas-api), serving a JSON-based REST API for listing and manipulating BaNaNaS content.
- [web](https://github.com/OpenTTD/bananas-frontend-web/), serving [https://bananas.openttd.org/](https://bananas.openttd.org/).
- [server](https://github.com/OpenTTD/bananas-server), serving the custom TCP protocol and the HTTP indexer.

The API can read/write to the R2, and the server can read from it.
The web only uses the API to do its thing.

The HTTP indexer in the server should be moved up to a Cloudflare Worker, and it should only serve the custom TCP protocol.
But this is future work.

As we really like to support older clients for as long as we can, we also have to deal with some silly choices we made in, for example, OpenTTD 0.7.
One of those choices is that the HTTP indexer has to be reachable via HTTP (besides HTTPS), and also listened on [https://binaries.openttd.org/](https://binaries.openttd.org/).
This domain has been deprecated for years now, as it is not really descriptive in what it does.
But as we still want to make sure if you start OpenTTD 0.7, you can still use BaNaNaS, it still exists, and still does its job.
In this specific case, there is a Cloudflare Worker redirect the traffic from one domain to the other.
And in OpenTTD 14 and later, it will use HTTPS instead of HTTP.

On the topic of HTTP vs HTTPS: OpenTTD's infrastructure makes HTTPS mandatory, with the exception of BaNaNaS.
For the above mentioned reasons.
It is hard to let go ...

### Multiplayer

The multiplayer is composed of two parts: an old (pre-12.0) part and a new part.
Between all different components we use [Redis](https://redis.io/) to communicate.
This makes it so you can see both old and new servers in the server-listing, despite them incapable of talking to each other directly.

The best thing about the whole multiplayer, you can shut everything down, and wipe the Redis database.
But after startup, it will be populated with the correct data again in minutes.
Basically, it doesn't need any persistent storage, and as such, it doesn't have any.
This kind of architecture makes it very easy to deal with, as problems only exists temporarily.
Even in the worst case, a restart brings everything back up and running again.

The services involved here are:
- [coordinator](https://github.com/OpenTTD/game-coordinator), handling 12.0+ servers and clients.
- [master](https://github.com/OpenTTD/master-server), handling pre-12.0 servers and clients, and hosts the API.
- [web](https://github.com/OpenTTD/master-server-web), serving [https://servers.openttd.org/](https://servers.openttd.org/).

Needless to say, here too, Cloudflare Workers should take over the API from master, as that is currently just a bit silly how it is implemented.
It can also take over the web part completely, as it is just simple listing.
But this too, future work.

### CDN (releases, etc)

[https://cdn.openttd.org/](https://cdn.openttd.org/) contains all our releases ever made.
Every nightly (or at least the source), is available as far back as 2004.
Release 0.1.1 can be found there.

I hope obvious by now, this is hosted on Cloudflare R2, with a Cloudflare Worker in front of it.
The Worker deals with GET requests, and make sure you see a nice directory listing when you visit the website.
But is also deals with PUT requests, to add new files.

These PUT requests need a `X-Signature`, to validate you are allowed to upload new files.
This signature is signed with a private/public RSA-key, where only the services that need to upload files know the private part.

For example, [https://github.com/OpenTTD/OpenTTD](https://github.com/OpenTTD/OpenTTD) has a GitHub Secret called `CDN_SIGNING_KEY`, which can only be used to upload files in `openttd-releases` and `openttd-nightlies`.
This gives us a bit security that not just everyone can upload files, and prevents accident in scripts to delete or overwrite files; as this is simply impossible.

### Other services (translator, DorpsGek, website, wiki)

There are a ton of other services, like [translator](https://github.com/OpenTTD/eints), [DorpsGek](https://github.com/OpenTTD/DorpsGek) (our Discord / IRC bot), the [website](https://github.com/OpenTTD/website), [wiki](https://github.com/TrueBrain/TrueWiki), etc.

None of them are really all that interesting.

Translator and DorpsGek run in Nomad.
The wiki does too, but Cloudflare caches as much as possible (as it is purely an HTTPS website; just very dynamic).
The website is fully done in Cloudflare Pages: the GitHub workflow uploads a new site every day directly to Cloudflare Pages.

### Other bits and pieces (docs, preview, redirects)

So much more services we run to make things easier.

We publish the documentation on [https://docs.openttd.org/](https://docs.openttd.org/).
This is done when a new nightly is produced, and uploaded to a Cloudflage Pages.

We also allow OpenTTD Pull Requests to be previewed.
The WASM version of OpenTTD is also uploaded to Cloudflare Pages, but as a branch.
And a Cloudflare Worker on [https://preview.openttd.org/](https://preview.openttd.org/) loads the right branch to serve you the latest preview.
This in combination with [GitHub Deployments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment), gives you a nice "View Deployment" button to press on Pull Requests.

Lastly, we have a ton of domains that simply redirect.
[https://bugs.openttd.org/task/1](https://bugs.openttd.org/task/1) redirects to the GitHub issue, [https://forum.openttd.org/](https://forum.openttd.org/) points you to the subforum on tt-forums.net, etc.
The list is long, and not all that interesting.

## Wrap-up

I hope that with this post you have a bit more insight what is actually going on in OpenTTD's infrastructure, and that it is not a simple website.
In total, we store over 150GiB of data, transfer over 6TiB of data monthly, have more than 10M requests a month, and serve thousands of unique visitors every week.

If, after reading this story, you still have questions or are just curious, feel free to drop by on [Discord](https://discord.gg/openttd) in `#openttd-development` and ask your question.
Or if you just want to express your happiness with the insight this post gave you, you are also very welcome!
