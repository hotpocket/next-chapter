# Project rough draft — repo → podcast (verbatim, 2026-07-20)

Brandon's draft, captured as written; refinement happens against this baseline.
Source idea: `~/git/repo-story`, re-sketched for the admissions project with
AWS services + deploy scripts. Constraint: frontend UI on GitHub Pages per
project requirements; services via AWS (S3 mainly; lambdas only if necessary —
pending pushback after reviewing repo-story and its dependencies, e.g.
~/git/landry-ui).

---

**1 - Problem is:** Small enough to complete / Interesting to you / Easy to
explain / Valuable to another person

Create a system for turning a github repo into a podcast. It will explore the
content in the repo for: history and core concepts. The prose generated will
generated for a tts engine and will follow a historical arc and also talk
about how this repo adds to the historical arc.

**2 - Why would someone use this?**

There is a lot of code out there that does a lot of things, and some repos are
actively developed by leaders and represent the bleeding edge of what is
available that actually works. It's hard to dig through lots of code or pick
it apart manually or even go through a Q & A session with an AI. But I am in
the car a lot and not in front of a computer a lot and could use this time to
come up to speed on things that interest me.

**3 - What is the smallest version of your application that proves your idea
works?**

A process you can hand to an AI with a github url that will produce a
reasonably small number of chapters that I can read online.

**What features are necessary to deliver that value?**

A prompt and an audio output.

**If you finish early, what would you add?**

There are seemingly endless UI features to add to navigate the
audiobook/podcast and a seemingly endless number of quality checks on
generated audio (cadence, pronunciation, etc..)
