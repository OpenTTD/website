---
title: New ship pathfinder. Goodbye buoys!
author: Kuhnovic
---

OpenTTD 14.0 comes with a new ship pathfinder which allows ships to travel great distances without the use of buoys.
Gone are the days of long strings of buoys and convoluted ship orders.
Using ships is now as hassle-free as the other modes of transport.
Just add the destination and send the ship on its way!

In this post, I'm going to explain how the new pathfinder works and some of the challenges we had to overcome.

<!-- more -->

## Motivation

Personally, I was never satisfied with the way ships worked.
All other vehicle types "just work" and always find their path, but ships needed buoys to get to their destination.
Placing buoys at the right interval is guesswork at best, and having to add them all to the order (and in the right order) is a pain.
In my opinion, it simply makes ships no fun to use.
I often found myself terraforming narrow stretches of land into the ocean in order to create railways to access oilfields.
Yes, I am "that guy".

Having messed around quite a bit with A* pathfinders and derivatives, I always felt there had to be a better way to achieve this.
I played around with several ideas, but most of them didn't scale well and didn't make it off the drawing board.
Getting things to work smoothly and reliably on a 4096x4096 map turns out to be quite a challenge.
But as they say, "if it was easy, it would have been done already".

## Why is it so difficult?

So why is it so hard for ships to find a path?
If trains can do it, so should ships, right?
The main problem is that open water creates a ton of symmetric paths which are all "equally good".
The pathfinder must explore all of these permutations in order to find the best path. 

Trains don't have this issue because they are restricted by tracks and junctions.
Potential paths branch off far less often, even in complicated networks.
The same is true for road vehicles and trams.
For ships however, the amount of path options grows exponentially as the distance increases.

The pathfinder eventually hits the node limit and has to throw in the towel.
Raising the node limit gets you a bit further, but the impact on game speed becomes more noticable.
Adding more ships further exacerbates the problem, since having twice the number of ships means twice the number of pathfinder calls.
And since larger maps often means more players and large travel distances, one can see that the problem only gets worse as the scale increases.

## The solution

The solution I went for is a two-tiered pathfinding system, somewhat similar to the well-documented HPA* algorithm.
First, we try to find a coarse, high-level path.
If such a path is found, we choose an intermediate destination not too far from the ship.
We use the low-level pathfinder to plan a path to that intermediate destination.
Once we reach it, we run the high-level pathfinder again, and the process repeats. 

Think of it like taking a long trip with the car: instead of planning the entire journey in meticulous detail, you just focus on how to get to the next city.
Ironically, this is similar to how buoys work: they also provide a sequence of intermediate destinations.
But this time it requires no user effort.

To enable the high-level path search, we divide the map into 16x16 tile regions.
Within each region, we identify separate patches of water.
Each tile gets a label, and all tiles with the same label belong to the same patch; i.e. they are interconnected.
We also identify whether a ship can travel across a region edge into any adjacent regions.
Aqueducts crossing into other regions are also taken into account.
The region abstractions allow us to search the map incredibly fast, hopping from region to region instead of from tile to tile.
We are effectively searching the map at a "lower resolution", ignoring the details at the tile level.

![Region with debug printout]({% link /static/img/post_2024-02-24-new-ship-pathfinder/region_debug.png %})

Keeping regions updated after construction and terraforming requires some effort, but the impact on overall performance is minor.
Such changes invalidate the region, which means it has to be updated the next time the pathfinder "bumps into it".
This can be done quickly, and the big benefit of this approach is that once the region is updated, its data can be used for subsequent pathfinder runs without any additional effort (until the region gets invalidated again).

## Suboptimal paths

Searching at a lower resolution unfortunately means that the path is not guaranteed to be the best path.
Locally the path to the intermediate destination is optimal, but globally there might exist a path that is shorter.
This is the tradeoff between speed and optimality that we have to make. Luckily it is not so bad to have a slightly suboptimal path.
Getting a "good enough" path very quickly is much more preferable, especially when dealing many ships traveling great distances.
And that trail of buoys you made before probably wasn't entirely optimal either :).
The pathfinder has been tweaked to produce good paths, and you will probably only find signs of suboptimality if you really look for it.

## In closing

For me personally, the difference is night and day.
I generally avoided using ships, and I know many other players did too.
Now I love using them.
They are a fun mode of transport, and I hope to see more users give them a second chance now that they work well right out of the box.

So go ahead, create a giant map and let ships travel from one side to the other.
No buoys needed!

_P.S. Buoys aren't going to be removed. You can still use them as waypoints._

_P.P.S. We have also added support for faster ships and faster ship acceleration in NewGRFs, for an even more complete ship experience._

## More about OpenTTD 14

This post is part of the series of dev diaries about big new features coming in OpenTTD 14.
Next week, we’ll delve into the integration with Steam, Discord and GOG Galaxy.
From now on, your friends will be able to see how much you love playing this game!
