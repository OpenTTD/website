---
title: The stoppable march of time
author: 2TallTyler
---

I was once the hottest new model on the street.
Newspapers heralded my arrival in every town.
The titans of industry were inspired to produce more goods when I visited their factories.

But as the years have passed, so do their eyes pass over me, to eye curiously my replacements.
Will you try the new style, ma'am?
It's so much better than _that old thing_.

I've watched my friends grow old and die.
My brother got caught in traffic and caused a horrific level crossing collision.
I get sick more often, wheezing to a halt wherever I am.
When I visit the doctor for a spot of renewal, they tell me,
"Sorry, I can't help. You're too old."
When will I be autoreplaced?

Woe is the tale of the Balogh Goods Truck.
But what if we could slow or pause the steady march of time?
In OpenTTD 14, you can.

<!-- more -->

## Time basics

Time in OpenTTD flows in three ways:
The movement of vehicles, which we'll call animation time.
The keeping of economic records, including charging you running costs for vehicles, recording the graphs of your company's income history, recording the production of industries and towns, and vehicle timetables. We'll call this economy time.
The passage of calendar time, affecting the introduction and expiry of vehicles, house styles, and the sub-arctic snowline (if using a variable snowline NewGRF). We'll call this calendar time.

Let's get the easiest out of the way first: we are leaving animation time alone.

Before OpenTTD 14, economy time was not tracked separately from calendar time.
When players wanted to run steam engines for longer, they turned on "Vehicle never expire" or used the date cheat to rewind time when needed.
Somebody wrote a Daylength patch, later included in JGR's Patchpack, that slows down the combined calendar/economy time at the expense of many side effects.

But slowing the economy was not what old Balogh asked for.

## The journey to real-time units

In late 2022, I began the work of splitting economy and calendar time. I was following a vision from my fellow developer nielsm, who proposed a novel solution to a problem that had vexed my previous attempts at this split.

The problem is this: If the economy does not follow the calendar, how do we display economy statistics like an industry's "Production last month," timetable arrival and departure dates, or the myriad other things that refer to time?

The ugliest solution is to display two dates.
But OpenTTD's user interface is confusing enough.
Adding a second date is not a good user experience.

Nielsm's proposal capitalizes on the fact that a day in OpenTTD is about two seconds, meaning that a 30-day month is about a minute.
We can simply make this a bit more precise, then display economy time in real seconds and minutes!

The first step was making the seconds-per-day a bit more precise.
The smallest unit of time in OpenTTD is a tick, of which there are 74 in a standard day.
Prior to OpenTTD 14, one tick lasted 30 milliseconds, making a day 2.22 seconds.
That's close, but not quite close enough when multiplied out to a month or a year.
But in TTD, one tick is 27 milliseconds, making a day 1.998 seconds.
That's about as perfect as we can get.
In OpenTTD, we've gone back to this original TTD value to better align to real-time seconds.

With this the "amount of goods produced in an in-game month" is about the same as the "amount of goods produced in one realtime minute".
A "vehicle service interval of 100 in-game days" is about the same as a "vehicle service interval of 200 real-time seconds".

Of course, not everyone will want to play OpenTTD using real-time units, so the new feature is an opt-in setting called Timekeeping units.

Calendar units are the classic OpenTTD experience, with no changes.
Wallclock units use minutes anywhere months are normally displayed, with 12-minute periods substituting for years.

![Image of some GUIs with wallclock unit stats.]({% link /static/img/post_2024-03-23-time/minutes.png %}){:width="100%"}

Where a date would normally be displayed (timetable start date, subsidy expiration date, etc.), the game shows an offset in seconds or minutes from the current moment.
Timetables are expressed in seconds.

![Image of the timetable GUI showing seconds as the unit.]({% link /static/img/post_2024-03-23-time/timetable.png %}){:width="100%"}

It's also possible to select seconds as the timetable units in any timekeeping mode, in the Settings menu.

## How to slow down time

There are two new settings used to control the flow of calendar time.
1. **Timekeeping**: Select the timekeeping units of the game.
   Calendar is the traditional OpenTTD experience and you won't notice any changes.
   Wallclock displays the new real-time units and is required to adjust the rate of calendar progression.

2. **Minutes per year**: Select how long a year lasts.
   The default is 12 minutes.
   Set this to 0 to freeze calendar time completely.
   The maximum is 10,080 minutes, which is one week of real time!

The timekeeping mode can only be changed before starting a game, so choose wisely!
Minutes per year can be changed at any time.

![A screenshot of the settings window showing the two new settings.]({% link /static/img/post_2024-03-23-time/settings.png %}){:width="100%"}

## What about cargo scaling?

The economy time always progresses at the usual rate, so it has none of the side effects of the Daylength patch.
That said, one of the side effects that players like is the reduced cargo production of houses and industries.
We've added separate settings to scale these, and you can do this in any timekeeping mode.

You may notice some differences with NewGRF industries.
Industries normally produce cargo every 256 ticks, and for base game and simple NewGRF industries we simply scale the amount of cargo produced.
For NewGRF industries which calculate their own cargo consumption and production, this could produce unwanted results.
For these, we instead scale the frequency of this production action, so at a lower scale the industry performs this action less often.

Some industry NewGRFs will have inaccurate helptext because of this change, as they will with wallclock timekeeping — for example, some industries increase production when supplied with boost cargos every three months.
NewGRF authors will have to update their GRFs to display properly in the new modes, although of course there is no change required in Calendar timekeeping mode with 100% cargo scaling.

## Cleaving time in two

Let's get back to new time features.
To actually implement these, we had to work backwards from the ending point.
In order to stay compatible with calendar timekeeping units, the economy time units need to take the same form of years, months, and days, so that in calendar mode they follow the calendar date exactly.
In wallclock mode, however, they diverge: an economy-month always has 30 days to always last one minute, so an economy-year always lasts 12 minutes.
In contrast: the calendar-year lasts 365 or 366 days, so 12 minutes and 10 or 12 seconds.

This difference between calendar and economy dates is why players are not allowed to change timekeeping units in the middle of a game.
OpenTTD's 20-year-old codebase contains a lot of assumptions about how time works and does not react nicely to synchronizing or un-synchronizing two date systems.
For example, if we are in calendar mode on the 31st day of the month and switch to wallclock mode, that day would not exist.
The date would have to be shifted, but that can make company finance data stop being recorded for two thousand years, crash the game when the Cargo Distribution linkgraph checks if it's time to update, or (worst of all) cause some other bug I haven't discovered!
Maybe someday, another contributor will write the code to nicely convert between the two modes and enable the timekeeping mode to be changed mid-game, but now is not that time nor am I that contributor.

## Tech debt comes knocking

Of course, there was a lot of technical debt to be paid off before we could even get here.
The calendar had to be cleaved in two and every reference to it evaluated to determine if it should continue to reference the calendar or be changed to the new economy timer.

My fellow developer TrueBrain was instrumental in helping me with this step, writing a new strongly-typed timer system to help catch any errors.
Strongly-typed does not refer to how hard you bang the keyboard, but to a type of variable that refuses to accept the wrong type of data.
So if I try to pass a calendar date to a variable that stores an economy date, the compiler will give me an error and refuse to compile until I fix it.

With a codebase as old as OpenTTD, anytime we touch something it provides an opportunity to leave the code better than we found it.
With such a wide-ranging project as changing how time works, I touched most of the codebase and found many opportunities to refactor, fix, or clean up old code.

## Conclusion

I have been working on this project for over a year, often putting in 20 hours a week.
Like with most development, my motivation is a mix of wanting to play with this feature myself, and simply enjoying the challenge.
Why optimize my rail network when I can optimize the code that makes it possible?

This is the last Dev Diary before we release OpenTTD 14.0.
Thanks for joining us to learn more about the OpenTTD development process.
If you'd like to learn more, we hope you'll join us in the [official OpenTTD Discord](https://discord.gg/openttd) or on [GitHub](https://github.com/OpenTTD/OpenTTD).
Stay tuned for a release post around April 1st!
