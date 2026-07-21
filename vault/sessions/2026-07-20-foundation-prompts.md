---
tags: [prompts]
type: prompts
summary: "Verbatim user prompts for session [[2026-07-20-foundation]] (46 prompts)"
created: 2026-07-21
---

# Prompts — 2026-07-20-foundation

Companion to [[2026-07-20-foundation]]. Extracted from the session transcript; tool output and
system events excluded; private data redacted inline.

## Prompt 1

okay i am going through next chapter and needing to submit a project that uses ai  the material that i have just gone through appears at this url through the eight sections the ninth section being the project confirmed that you can read this:
https://community.nextchapterproject.org/c/pre-course/sections/1066831/lessons/4059927

## Prompt 2

you should be able to browse using gstack and the cookie i currently am using can you confirm?

## Prompt 3

use opus 4.8 to do the grunt work and pull in all 9 sections. this is just for a baseline for future work.

## Prompt 4

[Request interrupted by user]

## Prompt 5

use opus 4.8 to do the grunt work and pull in all 9 sections. this is just for a baseline for future work. spawn multiple agents to do this in parallell, as many agents as you can launch

## Prompt 6

good. i'm on section 9, give me a very brief summary as you understand this section.

## Prompt 7

there is already a large history of me working with ai and specifically the skills that i have put in place to facilitate working with ai the mostly manifest in the .claude directory in my home directory and the things that exist in the .onfigs directory in my ~/git directory ... try to find the history of how these were created and create a config-history.md in this folder as a foundational layer before i begin.

## Prompt 8

my main focus here is on how I use the vault folder in each repo, and the ~/.claude config and how it impacts how claude code behaves. the browse skill in gstack, and the wargame skill are also big parts of my normal ai workflow and should be prominent in this history. I do this to set the stage for the reviewer so they know the tools I am reaching for in my ai workflow as I start this project outlined in section 9

## Prompt 9

<command-message>vet</command-message>
<command-name>/vet</command-name>
<command-args>this thinking and strategy</command-args>

## Prompt 10

sanity check: what problem do you think we're solving and where in this process do you think we are ?

## Prompt 11

sanity check: what problem do you think we're solving and where in this process do you think we are ?

## Prompt 12

Wrong: documenting these skills is the baseline for an as yet to be discussed idea that is the project. The project I will author will use these skills, so documenting them is critical for informing the reviewer on how to interpert the prompts I will submit as part of this project.

## Prompt 13

it could be descirbed as prep/staging given the context I just provided. do you disagree ?

## Prompt 14

<command-message>conduct</command-message>
<command-name>/conduct</command-name>
<command-args>init</command-args>

## Prompt 15

ok, this will be a public repo. add scanning verbage to the claude.md to ensure no private data leeks into commits. Along with this I will want to be publishing the prompts alongside each session note that is captured with a /vault recap.  Describe what actions you'd take to ensure this happens.

## Prompt 16

<bash-input>apt-cache search gitleaks</bash-input>

## Prompt 17

<bash-stdout>gitleaks - protect and discover secrets using Gitleaks 🔑
golang-github-gitleaks-go-gitdiff-dev - Go library for parsing and applying patches created by Git</bash-stdout><bash-stderr></bash-stderr>

## Prompt 18

installed, build export-prompts and wire it in

## Prompt 19

wargame our strategy for securing this as a public repo and also wargame the robustness of this process to provide visibility into any system level dependency that may obsecure understanding by a reviewer of this project at next chapter.

## Prompt 20

yes promote, and yes, make private first and upon a final review I'll flip it public.

## Prompt 21

that's foundational. now here is my rough draft of the project, it will be drawn from ~/git/repo-story , idea resketched here for the purposes of re-creating this idea complete with aws services and deploy scripts.  The project front end UI must live on github pages per project requirements, but services will be hooked up through aws (s3 mainly, lambdas if necessary, althought I don't think that will be necessary, but push back after looking at repo-story and it's dependencies ( ~/git/landry-ui for instance, etc...). ok, here is the rough draft: 

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








## Prompt 22

if I serve this from s3 to a github pages web page, what are my security concerns for the s3 bucket ?

## Prompt 23

Let's start collecting ADRs. And as for improvements that could be made, I want to add the pipeline for injesting the github url. I could have an aws lambda connect to a tailscale server that is running on my home network and feed the heavy pipeline of audio generation there, then have my home machine call another lambda to signal the completion. a web ui could update with status about the current executing stage and there could be a library page that lists content generated.

## Prompt 24

i have a openrouter api key that this would be routed too for the prose generation

## Prompt 25

the orchestrated skill has never been run. it was refactored to save on fable tokens, but the historical version was just prompts, see git history for verification of this

## Prompt 26

the on demand prose and repo injestion is v2. we are building v1 which is just rendering/reading/playing of a pre-generated repo that will happen on my local machine here and uploaded to s3

## Prompt 27

is there sufficient visibility into what repo-story is doing for the reviewer to follow along? what mechanism does this repo provide so that the reviewer has an unambigous breadcrumb trail to follow of how I am building this and what sources I am using?

## Prompt 28

the we must add all three to the version one list but the purpose of this project is to create the github page  the that is the interface to the the audio books that talks about the repositories.   the purposes of this admissions project i want there to be the audiobook for the landry ui repository and the repo story repository.  the this will serve two purposes one to provide detail about the backstory of these projects and my journey in creating them and also to demonstrate the final product that is the user interface that will render the audiobooks.  the i am still conflicted about creating from scratch a reduced functionality user interface as opposed to reusing the landry ui.  the what are your thoughts on that and the rest of this?

## Prompt 29

in the next chapter markdown you listed open router as a tool but that is not version one content version one will be generated locally through the prompts in claude code and python chatterbox scripts.

## Prompt 30

<command-message>vet</command-message>
<command-name>/vet</command-name>
<command-args>this idea to use landry-ui and repo-story as the two initial repo stories.</command-args>

## Prompt 31

<command-message>vet</command-message>
<command-name>/vet</command-name>
<command-args>this idea to use landry-ui and repo-story as the two initial repo stories and compare the results to the analysis you just did via a prompt. use this comparision both to presentto me for review and also to test the vet skill against something real (something we have yet to do)</command-args>

## Prompt 32

what is probe 1 ?

## Prompt 33

are you seeing the concise directive in prompts ?

## Prompt 34

i don't see any conflict. i'm intentionally pointing this tool at my repos not so I can learn something, but so that the reviewer of this applications process project can learn something about my repos that power this page in a way that also demonstrates the functionality provided by the page. does that make sense ?

## Prompt 35

reuse the landry ui, supersede adr 0002, the tool is the audio book generator and player, the demonstration of AI is using it to build this into a github page complete with a script that will deploy to s3 that uses local aws profiles with sso tokens that are never exposed via the web. the process included hardening the deployment process etc. all the things in this context window. store this decision and let me know if you have any other questions that are unclear about how to proceed.

## Prompt 36

this repo will serve the site. do an audit on landry-ui to see if it is safe to flip public. wargame that audit to have as much confidence in the analysis as possible

## Prompt 37

this repo will serve the site. do an audit on landry-ui to see if it is safe to flip public. wargame the senario of security of that repo in going public so that the audit can have as much confidence in the analysis as possible.

## Prompt 38

both acceptable, I'll flip it now

## Prompt 39

run the gh flip command yourself

## Prompt 40

is there any more foundational work to do before we begin? any questions? I want to shore up the foundational commit first before I move forward. what is your evaluation of our readyness to do a first commit ?

## Prompt 41

do 2 and 3, then i'll run the recap myself

## Prompt 42

<command-message>vault</command-message>
<command-name>/vault</command-name>
<command-args>recap</command-args>

## Prompt 43

Reuse landry-ui player; the AI demonstration is assembly + hardened SSO-based S3 deploy ... slight reframe ... the demonstration is composition of the player and generator, the product is the player and generator. does that make sense ?

## Prompt 44

 use my voice, that is fine. fix luinst https path in docs. then drop them from the todo in the session recap. after you fix & drop those two, write it

## Prompt 45

all good to clear context for the next session?

## Prompt 46

all pushed, clearing now
