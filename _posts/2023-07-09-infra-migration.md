---
title: The 2023 infrastructure migration
author: TrueBrain
---

This post is part of a two-part series, of which this is the second.
In the [first post](/news/2023/07/08/our-infrastructure), we went into a bit into the infrastructure that runs OpenTTD, from BaNaNaS to our main website.
In this post, we will explain a bit about the migration we just did to get to this infrastructure.

After over 2 months of work, I am happy to announce we finished ([another](https://www.openttd.org/news/2020/12/01/infrastructure-migration-finished)) infrastructure migration.
Today is the day I removed the last few DNS entries pointing to [AWS](https://aws.amazon.com/)'s DNS servers, and I am proud to mention that (almost) all traffic is now routed via [Cloudflare](https://cloudflare.com/) (and we aren't even receiving sponsoring to say so).

In this post I want to take you with me why this migration was needed, what the benefits are, and why you possibly care.
But in short summary:

- (Much) smaller monthly bill as AWS charges insane amounts for bandwidth.
- Faster download speeds for you (ranging from the in-game content service to downloading the game from our website).
- Easier maintainability of our infrastructure with thanks to [Pulumi](https://pulumi.com/).

This will be a bit nerdy, so if you like these kind of things, continue the read!

<!-- more -->

## History

As with every migration post, it starts with a bit of history.
Just to catch you up to a few months ago.

In 2020 we started the migration from our own dedicated hosts to AWS.
Back then, AWS was offering Open Source credits, which meant we didn't have to worry so much about money.
Additionally, they had everything we needed, and it seemed like a good fit.

This has been a very good call; not only did I personally have far less worries about things like security, stability, etc, we also had the fewest interruption till date.
More than 99.99% uptime over all our services since then.
This means it has been very unlikely you couldn't download the game, or use the in-game content service, etc.
Even big companies would be very happy with 99.99%, but given we run this with only a handful of people in their free time ... most excellent, if you ask me.

The fun thing is, with such uptime, when we got a report of a problem: it is very likely to be a user-problem, and not a backend-problem.
This is a great spot to be in!

## Problems on the horizon

But, for more than a year now, there have been some issues that were hard to deal with.
Let's explain a few in a bit more detail.

### AWS's bandwidth price

The Open Source credits ran out after the first year; and where we hoped (and somewhat assumed) the AWS bandwidth prices would go down over time, they did not.
For those who don't know, AWS charges 0.09 USD per GB of bandwidth.
Back in ~2000 (yes, 23 years ago), when I worked in datacenters, the cost per 300GB was about 15 euros per month.
So 0.05 euro per GB.
AWS charges almost double that, in 2023.
And although it is understandable that they have some costs, it is a bit absurd.

We already knew this when migrating to AWS, so we made sure to host our most bandwidth hungry subdomain, the in-game content service, on [OVH](https://www.ovhcloud.com/).
On OVH we used (very) cheap VPSes which only job was to serve these binary files.
And OVH charged us ~10 USD per month for this, unrelated to the amount of bandwidth we consumed.
For reference, this is about 6 TB per month.
If we would have hosted this on AWS, it would have cost 540 USD per month.

But, when you have an infrastructure that is splintered over two parts: one part on AWS, one part on VPSes, maintaining it becomes a bit tricky.
And, as it turns out, we never (ever) updated those OVH VPSes, not in the 2.5 years they have been running.
Shame on us.

Anyway, we still racked up a pretty decent bill in bandwidth costs on AWS, despite offloading our biggest subdomain.
On average, we pay around 100 USD a month on bandwidth alone.

Other than the bandwidth-bill, it has to be added: AWS has been great.
Their services have very low downtime, if any at all, and VPSes (called EC2-instances) run for months, even years, without any disruptions.

### AWS's CDK (Infrastructure-as-Code)

When migrating to AWS, we also wanted to have our infrastructure defined as code.
This way it is easier for others to understand what is done, where, and how.
It also avoids human mistakes of pressing the wrong button, etc.

After looking around in 2020, there were three options:
- Ansible
- Terraform
- AWS's CDK

Ansible isn't a good fit, for various of (personal) reasons.
Terraform was an option, but it only supported their own HCL back then.
What was nice about AWS's CDK, that it allowed us to write the infrastructure in a language we knew better: Python.

So we went for AWS's CDK.

And what a terrible decision this has been.

AWS's CDK on its own is great.
But the biggest problem is: they make a new release every N weeks, and more often than not, it totally breaks your current project.
And staying behind on an older version also really isn't a possibility, as slowly things start to act weird.
And forget about using that new shiny thing, of course.

In the beginning I tried to keep up with CDK releases ... but more and more often I had to spend weeks (yes, weeks) doing an upgrade.
The whole concept of Infrastructure-as-Code is that you don't have to spend so much time on this.
But, I had to.
And the longer it took, the less I did ... in the end, the EC2-instances weren't renewed for over a year, because I couldn't update them to the latest AMI.
And the CDK used is terribly old by now, and hard to work with.

The concept of AWS's CDK is still solid; if only they would take more care on migrations.
And although I fully understand that the way the project is run, that is not really feasible, it does mean AWS's CDK just isn't production-ready unless you have a decent-sized team on it.

Additionally, over the years we noticed we also wanted to bring things like GitHub and other parts under Infrastructure-as-Code; this is not possible with AWS's CDK, it only works with AWS.

Lastly, AWS's CDK makes AWS Cloudformation templates in the backend.
And let me tell you, they are insanely difficult to work with.

If AWS Cloudformation templates work, they work.
But if they don't, they really do not.
This mostly is a problem when renaming objects, or moving them around a bit.
And guess what you often had to do when you tried to update to a newer version of AWS's CDK?
You guessed right!

In short, this has been the worst decision we could have made back in 2020.
I still don't actually regret it, but I would not advise anyone to use AWS's CDK ever.
(and if you want to know more, as there are many more reasons, feel free to send me an email or a [Discord](https://discord.gg/openttd) DM; I am happy to rant some more.)

### The bill

OpenTTD lives on donations.
We haven't had a fundraiser in years, mainly because at a certain moment we had more than 5000 pounds in reserve.
This meant we also weren't that scared that AWS would cost a bit more than dedicated servers.
If it would mean we all had to work less to keep things running, and that it would be more secure too, that would be worth the money.

But, the cost of AWS did mean the funds started to go down.
We yearly got less donations than the costs.

An average month on AWS currently costs us 280 USD (so yearly roughly 3500 USD).
Of course this is peanuts for most companies, but for an Open Source project, that is a lot.
As mentioned earlier, 1/3rd of that bill is for bandwidth alone.
Other parts are for things like EC2-instances, Application Load Balancer, Redis-server, and .. surprisingly: metrics.

With AWS it is very easy to start using something where it doesn't cost anything, but slowly over the months you see the bill going up and up.
Metrics is a nice example of this: currently we pay more than 10 USD a month on metrics.
And really, they are not that important; if we look at it once a year, it is a lot.

Anyway, I digress.
A few months ago, orudge, who keeps track of our donations, notified me that if we would continue this way, we would need a fundraiser within 12 months, or the funds would run out.
A clear signal we started to run out of reserves, and some actions was needed.

This action could be either of the following, or a combination of:
- Reduce the bill.
- Increase the donations (by offering different ways to donate).
- Have a (yearly) fundraiser.

This migration attempts to address the first.
These two posts the second.
And I hope we can avoid the third.
It is just a hassle to ask for money every year.

## So why migrate?

As I had some (real-life) time on my hands, the three problems on the horizon above made me wonder: can't we do better?

A few months back I migrated our wiki and main website to [Cloudflare](https://cloudflare.com/), to improve the experience for end-users.
In general, websites on Cloudflare load a bit faster, and it is easier to deal with a ton of things for sites on Cloudflare.

While doing so, I was very pleasantly surprised about the things you get "extra" on Cloudflare.
Not only do they give very solid (and privacy-minded) insights in your visitors, they also do not charge anything for bandwidth.
Yes, you read that right: 0 USD per GB.
Nothing.

Additionally, on the 16th of May, they finally made a policy change that made me go: let's move as much as we can to Cloudflare:

[https://blog.cloudflare.com/updated-tos/](https://blog.cloudflare.com/updated-tos/)

Basically, before this policy change, it was a bit unclear if you could host binary files on their Cloudflare R2 (a bucket-service).
Years ago, we contacted Cloudflare if it would be okay to host for example our in-game content-service content on Cloudflare, and the answer was a very clear: NO.
Most of your traffic had to be HTML files.

But with this TOS update, that all changed.
When you use their Cloudflare R2 or Cloudflare Workers, you are allowed to host binary files.
In fact, the policy finally states R2 was designed for that.

So ... why not move our BaNaNaS content to it?
It gives a much faster experience to most of the end-users, as files will be cached very close to the end-user, and it will cost us exactly 0 USD.
Well, not exactly 0 USD, our current estimate is that it will cost 2 USD a month; but this is for the storage cost, not bandwidth.
Which means it doesn't scale with the amount of visitors; just with the amount of content.

But now if you migrate that one service to Cloudflare ... why not migrate everything?
They have tons of other tools that would actually help us.

And so that is why this migration started.
And it was a big one.
And I am happy we did it!

## Infrastructure-as-Code, again

So now we made the decision: migrate to Cloudflare, the next question becomes: but what to do about AWS's CDK?
As the other two problems are tackled: no more high costs for bandwidth, and good reduction of the bill.

We, well, I, looked around and found two possibilities:

Terraform or Pulumi.

Terraform has been around longer, and although they do offer a CDK now, where you can use Python to write Terraform (instead of their custom HCL), it still isn't really there yet.
But then there is Pulumi, which offers exactly what we need.
And, what is always nice, they also offer Open Source [a free account](https://github.com/pulumi/team-edition-for-open-source/issues/14) to use their Pulumi Cloud.

So, we went for Pulumi.
And I have enjoyed the experience very much.

The most beautiful moment was when I read they had a new version released .. and of course I was: meh, this will take me a while.

Nope.

Two minutes.
All done.
That just makes you cry of happiness.

In the background most of Pulumi's registries use Terraform, so there is a lot of reuse of existing known-good work.
And this makes me pretty sure we made a solid choice here.

Pulumi allows us to provision infrastructure for:
- AWS
- Nomad (more on that in a bit)
- Cloudflare
- GitHub

and possibly anything else we will find in the next few years.
This means that one place, our [infrastructure repository](https://github.com/OpenTTD/infra), defines everything infra-related for all parts it touches.
Our infrastructure isn't small: 3500 lines of code to define it.
And everyone can see how we did things, and some parts might be even useful for you.
And of course, if you spot a mistake, you can help out making our infrastructure better.

What mostly has been of great help, that I no longer manually have to copy secrets from one system to the other.
This is now all handled by Pulumi.
This is important, as it makes rotating keys much easier.
And less error-prone.

## AWS ECS, and vendor-lock-in

As I full well realise this migration also means being less depending on AWS, the next question that came to mind: do we still want to use [AWS ECS](https://aws.amazon.com/ecs/).
AWS ECS allows for us to quickly spin up our backend services, that run in a container, and not worry about things like crashes.
AWS ECS will just restart the services, etc.

It has been absolutely great, AWS ECS.
The one downside is that the metrics you get for free are poor.
And the metrics I actually want, would cost so much money a month, that I didn't find that reasonable.

So after looking around a bit, I quickly found [Nomad](https://www.nomadproject.io/), from Hashicorp.
It basically does the same as AWS ECS, but you can host it on what-ever you want.
As you might have guess: that is what we are running as our backend now, and all containers are running happily.

Using Nomad hasn't been a flawless experience.
As we want to be as cheap as possible (which happens when you depend on donations), we are using AWS's T4g EC2-instances.
These machines are ARM64.
And Nomad had some open issues in those regards.

But, nothing that can't be fixed, and so far they have been great accepting contributions.
That is the lovely thing about a company that makes their products Open Source: others can contribute to make it better.
So by now I fixed the two problems that were holding me back from using it on ARM64, and I hope others enjoy those fixes too.

With Nomad, I have full insight what a service is doing.
How much memory, how much CPU, how often they crashed, etc.
The one small thing I am still missing: I cannot see which service uses how much bandwidth.
But I plan on addressing that soon ... I have some ideas.

And I haven't setup log collection yet; I intend to use [Loki](https://grafana.com/oss/loki/) for this, as their Free offering is excellent for our goal.
With Loki, we can look back in logs of services, even if the Nomad client crashed and died.

A short side-step: Nomad runs on an AWS Autoscaling Group.
We automated this completely, which means we can scale up the amount of nodes and scale down easily.
This means that updating to a new Nomad or OS is not some manual work: you just scale up the cluster, and slowly scale it down again.
That way, new machines are created with the latest version, and the old ones are slowly shut down.
Far far easier than trying to manually update machines; and much less likely to break.

## GitHub Workflows

The one thing not talked about above, is that we also really badly needed to address our [GitHub Workflows](https://docs.github.com/en/actions/using-workflows).
GitHub Workflows automate our repositories, but were written in a time where [Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) didn't exist yet.

The problem was maintaining the GitHub Workflows; it would require changes in ~20 repositories.
This was very time consuming and error-prone.

By switching to Reusing Workflows, it means we have a [single repository](https://github.com/OpenTTD/actions) which hosts all our workflows.
By changing things in a single place, all repositories will be updated.

This will make our life so much easier.

While at it, we also noticed that making releases of those repositories to get things to production wasn't really working, and was an annoying task.
So we decided to also change that: if we now merge a Pull Request, it is deployed to production.
No delay.

And to compensate for the missing staging, we can now label a Pull Request with a preview label in any of the repositories, and it will deploy this to a preview site.
Here we can review the changes, and if we like it, merge the Pull Request.
And boom, it is in production.

## Migration finished; what did we gain?

Now after a few weeks, well, months of work, I can finally say we migrated everything over.
And I am, so far at least, very happy with the result.

The AWS bill is reduced with at least 50%.
Cloudflare does cost us a bit of money: 20 USD a month for Pro-plan, 5 USD a month for Cloudflare Workers, and like 2 USD a month for Cloudflare R2.
But overall the total bill should be reduced with at least 100 USD a month (so 1/3rd), but most likely more.
We will have to wait another month to get a better picture of the bill.

We also applied for the Cloudflare Open Source, but haven't heard back from them yet.
Maybe they have forgotten us.
It would reduce our bill with the above mentioned 27 USD per month.
But honestly, even if they did forget about us, the amount of money Cloudflare costs versus AWS: it is totally worth paying for it.
The contrast between these two companies really is day and night, in many ways.
Not only about how they charge customers, and what they charge them for.
But also [Cloudflare's documentation](https://developers.cloudflare.com/) is one of the best I know.

Further more, over 50% of the BaNaNaS content is cached by Cloudflare.
This means that it is very likely that if you download something from the in-game content-service, it is served from a location near you, instead of from France (where it used to come from).
So if you are living in America or China, it is very likely downloads are now a lot faster.

Over 60% of the content on our CDN, like releases etc, are cached by Cloudflare.
So there too, it is very likely that if you download the latest release, it goes a lot faster.

And, what I personally enjoy, I have full insight of this data.
I can now tell we consume about 1.3TB of bandwidth a week, and that we have ~57k unique visitors a week.
There are 2.5M request made in the last 7 days.
Knowing this information means we can better anticipate what changes we need to make, and if we change something, what the impact would be.

But, we only finished the migration today; so we will need some more time to say if this was actually a good move.
It sure feels like one.

## In closing

Although we only migrated our infrastructure only 2.5 years ago, this migration was really needed.
And I really hope we don't need another migration in 2.5 years; at least I did my best to set it up as such that it wouldn't be needed.

As for the donations, we are all still surprised how generous you all have been with your donations (without us asking for it).
I really hope that by reducing the monthly bill, we can avoid a fundraiser.
But given I have your attention on the subject anyway, forgive me to just show you the [donate page](https://www.openttd.org/donate).
And please, only if you are able and willing.
No need to miss out on milk on our behalf.
