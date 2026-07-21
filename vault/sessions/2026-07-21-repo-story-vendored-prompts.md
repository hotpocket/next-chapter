---
tags: [prompts]
type: prompts
summary: "Verbatim user prompts for session [[2026-07-21-repo-story-vendored]] (21 prompts)"
created: 2026-07-21
---

# Prompts — 2026-07-21-repo-story-vendored

Companion to [[2026-07-21-repo-story-vendored]]. Extracted from the session transcript; tool output and
system events excluded; private data redacted inline.
This transcript continues the session exported in [[2026-07-20-config-mirror-prompts]];
its first 4 prompts live there and are omitted here.

## Prompt 1

pushed. ensure the links to prompts are on the readme. and include any links to resources there (in a section) so the reviewer can navigate easily

## Prompt 2

ok, i'm going to wait to squash that commit until later. what is left before we build this website as per the instructions ?

## Prompt 3

I wrote this "before opening your ai tool" plan before, it is copied here: 

1 - Problem is:
Small enough to complete
Interesting to you
Easy to explain
Valuable to another person

---
Create a system for turning a github repo into a podcast. It will explore the content in the repo for: history and core concepts. The prose generated will generated for a tts engine and will follow a historical arc and also talk about how this repo adds to the historical arc. 
---

2 - Why would someone use this?
There is a lot of code out there that does a lot of things, and some repos are actively developed by leaders and represent the bleeding edge of what is available that actually works. It's hard to dig through lots of code or pick it apart manually or even go through a Q & A session with an AI. But I am in the car a lot and not in front of a computer a lot and could use this time to come up to speed on things that interest me. 

3 - What is the smallest version of your application that proves your idea works?
A process you can hand to an AI with a github url that will produce a reasonably small number of chapters that I can read online.

What features are necessary to deliver that value?
A prompt and an audio output. 

If you finish early, what would you add?
There are seemingly endless UI features to add to navigate the audiobook/podcast and a seemingly endless number of quality checks on generated audio (cadence, pronunciation, etc..)

Remember:
Build value first.
Everything else is optional.
Choose the AI tool you're most comfortable with.
The tool itself is not being evaluated, how you use it is. 









this was the kernel of our journey last time. this should be in local history and session vault history. do you see it?

## Prompt 4

do we have an offical plan yet ?

## Prompt 5

yes, draft for my review

## Prompt 6

<command-message>wargame</command-message>
<command-name>/wargame</command-name>
<command-args>this plan first</command-args>

## Prompt 7

1) the scope of these sample repos will be small, i'll put the m4a files in github. 2) is fine, i'll regenerate and tweak  generation prompts until I see fit to end that loop. 3) rename docs to llm-docs due to the restrictions on folder naming given the restrictions of this project.  4) wav files will be reviewed prior to push, and the billing issue is moot with the decision in 1. Any other questions/concerns ?

## Prompt 8

s3 is dead, deadline is July 24th (2-33 days), invalidate/superseed any ADRs that linger. don't write code yet. let's align. what is left to discuss ?

## Prompt 9

s3 is dead, deadline is July 24th (2-3 days), invalidate/superseed any ADRs that linger. don't write code yet. let's align. what is left to discuss ?

## Prompt 10

1) don't worry about deadlines. that's my concern. 2) we can flip to public so we can do a test render and see the result (this seems to be non-negotiable) 3) use the guidance in repo-story for now until I see fit to modify the prompts that guide the prose generation. 4) ok.  no code yet. any more questions ?

## Prompt 11

run the audit only at this time. i want to do a deep eval/scrub of that repo before I flip it to public. I want to keep as much of the history and files as possible to preserve the cross reference integrity. until I way switch back to the plan for next-chapter applications project, let's focus only on the repo-story scrub

## Prompt 12

yes, let's create this repo as a folder within next-chapter, the build scripts withing next-chapter will point to it, let's replay the commits excluding all personal info and unnecessary info you found (we're not using aws for instance). modify scripts and files as necessary to have it custom tailored to our purposes

## Prompt 13

you can confirm as a result of reading the soruce that f1-f8 data leek concerns are resolved ?

## Prompt 14

this is still private and we can force push to rewrite the remote history. this does expose that we need to scan our prompts also as a source of private data leakage. I suggest removeing them and i'll force push. do you see this as potentially breaking any of our build process or causing any other process issue ?

## Prompt 15

yes, redact, don't delete. go ahead

## Prompt 16

I think the readme needs to be updated to reflect our new arch

## Prompt 17

I know in a normal software develoment project ADRs are supersceeded and not removed, but I feel it's worth an audito of our repo here for the sake of making it as uncluttered and easy to read as possible, given the reviewer from next-chapter will not look at things that are hard to find or hidden behiend lots of clutter. also, I want to add one more repo to the ones that will appear on the project page, this one: next-chapter. the history of it itself will point to the history of repo-story and landry-ui which will complete the journey story of all of it and put a bow on it (so to speak) nicely. thoughts ?

## Prompt 18

that all looks great. do it

## Prompt 19

are these plans ready for a new fresh context window? are they stored in the vault and read in in a new session ?

## Prompt 20

s3 is V2 where we move off of github pages and do this properly (kinda like it's already beind done on at least one domain I own). This I mention because in the project instructions there is a space for "what would you do if you had more time", this clearly is v2 as we have seen appear in our discussions here. update the recap and re-draft for my review

## Prompt 21

approved, write it and commit
