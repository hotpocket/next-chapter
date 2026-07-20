# Mission-brief authoring — template + exemplars

For route mode when no mission brief exists yet. The wargame routes a brief; a
vague brief routes to nowhere — author the brief first, then wargame it.

Source: the original author's fable-wargame-kit (The Laundry List, 2026-07).
Exemplars are his, lightly normalized; craft rules distilled from them. Credit
him if any of this leaves the machine. Kit-isms NOT carried over: same-session
self-grading (this skill grades with a fresh session), the `/goal` contract
(covered by SKILL.md batch mode + harness autonomy), effort-tier advice, and the
unverified Opus-4.8 routing claim.

## The template

```
WARGAME ORDER. You are not executing this mission, you are wargaming it. A
cheaper executor ({{NAME THE ACTUAL EXECUTOR, e.g. Sonnet / Claude Code on a
cheaper model}}) runs the brief below later. Your job is the route it will
follow.

Recon first, read-only: {{NAME THE EXACT ARTIFACTS — the repo, the transcripts,
the statements. A recon scope the wargamer can't misread.}}

Then fight the mission on paper, move by move, and write it to
wargames/{{NN-slug}}.md:
- every move states its expected observation, exactly what you should see if it worked
- every move carries its most likely failure, the cause it signals, and the counter-move
- every fork gets a trigger, if you observe X, take route B
- assumptions recon could not settle get marked RECON NEEDED with the exact check that settles it
- end with abort conditions, and the verification runs the executor must perform with what pass looks like for each

Write it so the executor can run the brief end to end without asking a single
question.

=== THE MISSION BRIEF (the executor's orders, not yours) ===

{{THE BRIEF — see craft rules}}
```

## Brief-craft rules (distilled from the 10 exemplars)

1. **Placeholders are contracts.** Every `{{PLACEHOLDER}}` filled before the
   wargame runs; an unfilled one means the mission is BLOCKED by definition —
   never invented.
2. **Evidence gating.** Claims need receipts, stated in the brief itself:
   "support every pattern with at least one direct quote — if you cannot quote
   it, it does not exist"; "prove it with a failing test, a repro command, or a
   concrete trace — no evidence, no report entry."
3. **Unverified, not smoothed.** "Anything you cannot verify gets marked
   unverified rather than smoothed over. Where sources conflict, say so instead
   of averaging." Never estimate silently.
4. **Named recon scope.** The order tells the wargamer exactly what to read
   before fighting — not "look around."
5. **Verification inside the brief.** The executor verifies before reporting and
   audits each claim in its final summary against something it actually ran or
   read. Give tool fallbacks ("if no browser, verify by reading the logic and
   state which method").
6. **Recommendation first, reasoning after.** Deliverables lead with the
   decision.
7. **Variant caps.** Where alternatives are wanted, cap them explicitly ("two
   alternates for the headline and CTA only, nothing else gets variants") —
   uncapped variants invite sprawl.
8. **Scope fences.** Say what NOT to do: "no style nits, no refactors, no
   hypothetical hardening"; "do the simplest thing that works well, nothing
   beyond this list."
9. **Honest-input demands.** Where the brief needs the user's dirty laundry, ask
   for it plainly ("the objections I hear most: {{LIST THEM HONESTLY}}").
10. **Built-in self-attack.** End the brief with a pressure pass in-role:
    "reread the page as a skeptical {{ICP}} who has seen ten pages like this
    today"; "argue against your own offer as a buyer who almost bought and
    walked away, and patch what that exposes."

## The 10 domain exemplars

Each is the `MISSION BRIEF` half only — pair with the template above. Executor
suggestions in parens are the author's; re-pick per current model economics.

### 01 · Build the website (code; Sonnet-class)

> I'm rebuilding the marketing site for {{BUSINESS}} because the current one
> {{PROBLEM, e.g. looks dated and doesn't convert}}. Visitors are {{AUDIENCE}}
> and the one action I want from them is {{CTA}}.
> Build a complete static site in ./site. Plain HTML, CSS, and JS. No
> frameworks, no build step, opening index.html in a browser shows the finished
> site. Sections: {{LIST THEM}}. Match this reference for tone and palette:
> {{URL OR DESCRIPTION}}.
> Mobile first. No horizontal scroll at 375px. Semantic landmarks, labeled form
> inputs, alt text on every image.
> When you believe you are done, verify before reporting. Open each page,
> exercise every link, every form validation path, and every interactive
> element, and fix what fails. Audit each claim in your final summary against
> something you actually ran or read in this session.
> Do the simplest thing that works well. No features, no abstractions, nothing
> beyond this list.

### 02 · Write the copy (mid-tier model)

> Write the full copy for {{PAGE}}. The reader is {{ICP}}. They arrive {{STATE
> OF MIND, e.g. skeptical, burned by two agencies}}. This page has one job,
> moving them to {{CTA}}.
> Voice: {{THREE ADJECTIVES}}, in the spirit of {{WRITER OR BRAND YOU ADMIRE}}.
> Draft every section. Headline, subhead, three benefit blocks, proof section,
> FAQ, closing CTA. Write two alternates for the headline and the CTA only,
> nothing else gets variants.
> Rules. Lead with the outcome the reader gets. Plain words over clever ones. No
> hype adjectives. Sentences a 7th grader can read. Being readable and being
> concise are different things, and readability wins.
> Before you finish, reread the entire page as a skeptical {{ICP}} who has seen
> ten pages like this today, and cut every line that does not move them toward
> {{CTA}}.

### 03 · Set up local AI (Claude Code, cheaper model)

> I want a fully local, open source AI setup on this machine, private by
> default, nothing leaves the box. My hardware: {{OS AND VERSION}}, {{CHIP}},
> {{RAM}}, {{GPU / VRAM IF ANY}}, {{FREE DISK}}. I'll use it for: {{USE CASES}}.
> My patience for tinkering: {{LOW / MEDIUM / HIGH}}.
> Set up the stack that fits THIS machine, not a generic tutorial. Pick the
> runtime and justify it against my patience level. Pick the exact models with
> the exact quantizations that fit my memory, one daily driver, one small fast
> fallback, plus an embedding model if my use cases need document chat.
> Configure context length and GPU offload for my hardware.
> Verify the whole thing end to end. A test prompt runs on each model with
> tokens per second measured, and each of my use cases gets exercised once.
> Confirm nothing phones home, the setup works with wifi off.
> Everything must be free and open source. If my hardware cannot run a good
> daily driver, say so plainly and name the smallest upgrade that changes that.

### 04 · Tax strategy review (Opus-class)

> I run {{ENTITY TYPE}} in {{JURISDICTION}} doing roughly {{REVENUE}} per year,
> with {{STRUCTURE NOTES}}. Raw materials: {{STATEMENTS / EXPENSE CATEGORIES /
> ANYTHING YOU HAVE}}.
> Act as my accountant's analyst, not my accountant. Produce a tax strategy memo
> I will hand to a professional for review.
> The memo covers. My current posture in plain language. Every deduction,
> deferral, and structure opportunity I appear to be missing, each with the rule
> it relies on, an estimated impact range, and the documentation I would need.
> Aggressive positions flagged separately from safe moves, clearly labeled. And
> the list of questions a good accountant would ask me next.
> Audit every number in the memo against the materials I gave you. Never
> estimate silently. Anything you cannot verify from my materials gets marked
> unverified. This memo informs a conversation, it does not replace one.

### 05 · Refine the high-ticket offer (mid-tier model)

> I sell {{PROGRAM}} at {{PRICE}} to {{ICP}}. Close rate is roughly {{X}}%. The
> objections I hear most: {{LIST THEM HONESTLY}}. Current pitch or sales page:
> {{PASTE}}.
> Rebuild the offer, not the copy.
> Deliver. The one painful, expensive problem this offer should anchor on, in
> the buyer's own words. The promise, restated so the price feels obvious rather
> than defended. What to add, what to cut, and what to guarantee, each with the
> reason. Risk reversal options, ranked by how much backbone they require. And
> the three hardest questions a skeptical {{ICP}} would ask, with honest
> answers, not deflections.
> Then pressure-test it. Argue against your own offer as a buyer who almost
> bought and walked away, and patch whatever that argument exposes.
> Recommendation first, reasoning after.

### 06 · Upgrade the chatbot from real conversations (Sonnet-class)

> Attached are {{N}} real conversations from my {{CHATBOT PURPOSE}} bot: {{FILES
> OR PASTE}}. Its current system prompt: {{PASTE}}.
> Find where it actually fails. Wrong answers, missed handoffs, tone breaks,
> users repeating themselves, conversations that dead-end. Group the failures
> into named patterns, and support every pattern with at least one direct quote
> from the transcripts. If you cannot quote it, it does not exist.
> Then rewrite the system prompt to fix the top patterns. Deliver the new
> prompt, plus a change log, each change paired with the failure pattern it
> prevents. Keep the new prompt as short as it can be while fixing what you
> found.

### 07 · Hunt the bugs (Claude Code, cheaper model)

> Here is my repo: {{PATH}}. Before touching anything, read the README and trace
> the core flow end to end so you understand what the system is supposed to do.
> Then hunt real bugs. Logic errors, unhandled edge cases, race conditions,
> data-loss paths, security holes at the boundaries. For every finding, cite the
> file and line, describe the failure scenario in one sentence, rate the
> severity, and prove it is real with a failing test, a reproduction command, or
> a concrete trace through the code. If you cannot point to evidence, it does
> not go in the report.
> No style nits. No refactors. No hypothetical hardening for scenarios that
> cannot happen.
> Fix only the top {{N}} findings, each with the smallest change that works, and
> run the test suite before and after so the report shows both results.

### 08 · Build the financial model (mid-tier model)

> Build a 12-month financial model for {{BUSINESS}} as a spreadsheet, saved as
> {{NAME}}.xlsx.
> One inputs sheet holding every assumption: {{REVENUE STREAMS}}, {{COST
> LINES}}, {{ASSUMPTIONS}}. Each assumption lives in one labeled cell. Nothing
> gets buried inside a formula.
> Model monthly cash across base, bear, and bull scenarios, driven by the three
> levers I am most likely to change: {{LEVERS}}. Add a summary sheet a
> non-finance person can read in sixty seconds.
> Use real formulas, not hardcoded values. Before reporting, sanity-check the
> model, move each lever and confirm the outputs shift the way reality would.
> Close with the three assumptions the model is most sensitive to, so I know
> what to watch.

### 09 · Tear down the competition (Opus-class)

> I'm positioning {{BUSINESS}} against these competitors: {{3 TO 5 NAMES OR
> URLS}}.
> For each competitor, establish four things. What they actually sell, not what
> their homepage claims. Price points you can verify. The promise their
> positioning makes. And their visible weakness in their own customers' words,
> from reviews, comments, and complaints.
> Cite a source for every claim. Anything you cannot verify gets marked
> unverified rather than smoothed over. Where sources conflict, say so instead
> of averaging.
> Then the deliverable that matters, the gap map. What does {{ICP}} want that
> nobody on this list credibly owns, and what is the one positioning move I
> could defend against all of them? End with that recommendation and the
> evidence trail behind it.

### 10 · Map the automation (Claude Code, cheaper model)

> Here is a process I currently run by hand: {{DESCRIBE IT STEP BY STEP, WITH
> THE TOOLS EACH STEP TOUCHES}}.
> Map it into an automation blueprint. Classify every step as automate fully,
> automate with a human checkpoint, or keep human, with the reason. For each
> automated step, name the tool or script that does it. For the whole pipeline,
> identify what breaks first and the guardrail for it.
> Sequence the build starting with the step that saves the most time per week.
> Each phase of the build gets its own acceptance check, something I can run to
> confirm that phase works before starting the next.
> Delegate independent steps to subagents and keep working while they run. The
> final output is a blueprint I can hand to Claude Code and say, build phase
> one.
