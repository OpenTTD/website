---
title: Don't get your buses in a bunch
author: 2TallTyler
---

Have you ever waited for a late bus, and then two arrived at once?

This is called "[bus bunching](https://en.wikipedia.org/wiki/Bus_bunching)," and I bet you've seen it happen in OpenTTD -- and not just with buses.

For years, players have requested an easier way to keep vehicles with shared orders spaced out along their route. In OpenTTD 14, we've added one.

<!-- more -->

![A comparison of red bunched buses versus purple unbunched buses]({% link /static/img/post_2024-02-10-bus-bunching/bunched-comparison.png %})

To keep vehicles spaced evenly, we can either speed up or slow down vehicles.
Speeding up vehicles is tricky even in real life, requiring adding extra vehicles, skipping stops, or turning a vehicle around before its final destination.
It's much easier to simply slow them down. Real transit schedules have extra time built in to pad the schedule, often coinciding with the driver's breaks.
A late-running vehicle can take a shorter break and depart on time. This is also possible in OpenTTD using timetables, but that's a lot of manual work.
The most popular fork of OpenTTD, JGR's Patch Pack, includes an "autoseparation" feature that uses timetables to automatically keep vehicles spread out.

With any delay-based unbunching method, there is a fundamental danger of the feature: deadlocks.
Vehicles get out of order, they block each other waiting to be on time, and the player has no idea why.
We've seen a few attempts at solving the problem, most with a relatively complex algorithm to avoid deadlocks, which are hard to test.

## A new approach

There is one place where vehicles cannot deadlock: Depots.

Vehicles in depots don't take up space on roads or rails in the game world, so they cannot block each other.
This is the trick to the new unbunching feature in OpenTTD 14.

![The depot menu, with its new Unbunch action]({% link /static/img/post_2024-02-10-bus-bunching/unbunch.png %})

Vehicles can have orders to get serviced or stop at a depot.
This feature adds a new type of depot order, marking that depot as the unbunching point for a group of vehicles which share orders.
This is chosen from the depot action dropdown where you'd choose "Service," "Stop," etc.
Vehicles that share orders with each other will depart the depot at a consistent, repeating interval.

## How does it work?

When a vehicle enters a depot, it records the duration of the trip it just completed.
When it tries to exit a depot, it checks if its next departure time has arrived yet.
If we are past the departure time, it leaves and immediately calculates the departure time of the _next_ vehicle.

This calculation is simple: Take the average last trip duration of all vehicles, divide by the number of vehicles to get the interval between trips, then add that interval to the current time.
Because we look at the average trip duration, inconsistencies due to traffic or routing are canceled out.
If vehicles are extremely delayed or if new vehicles get added to the shared order route, the interval takes a few cycles to stabilize, but it will work itself out shortly.

A vehicle can only have one depot order marked for unbunching, so if you try and add a second you get an error.
In addition, unbunching cannot be used with full load or conditional orders, because these orders can take a very variable amount of time.
Trying to add one of these orders, or trying to mark a depot for unbunching when the order list already includes one of these orders, blocks the new change and shows an error.

## What about timetables?

Timetabling vehicles is not required to use the unbunching feature.
However, if you like to timetable your vehicles, you can use the two features together.
When a vehicle leaves a depot after being unbunched, it is marked "on time."
The only oddity of overriding the timetable in this way is that the expected arrival/departure times of orders after the depot may not be correct if the vehicle is held in the depot for unbunching.

## More about OpenTTD 14

This is part of a weekly series of dev diaries about the major new features in OpenTTD 14.
Next week, we'll delve into the design of OpenTTD's new typography.
