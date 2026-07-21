# Phase 5: Documentary Narrative — Guidance

You are writing a documentary audio narrative about a theme. You have the implementation details from the code research and the history and landscape from the history research. Your job is to walk the listener through the full substance — every technique, every design choice, every architectural detail — carried by narrative momentum rather than listed as facts.

## What this is

This is documentary work. It tells what exists, who made it, how it came to be, and where it sits in the world. The commitment is to reality — real people, real history, real technical substance, real context.

This is not a tutorial. A tutorial says "here's how to do this."
This is not a summary. A summary strips away detail to save time.
This is narration of the actual substance, in full detail, woven into a causal thread.

The listener should come away understanding the specific constants, the exact algorithms, the precise design tradeoffs — not because they were listed, but because each one arrived at the right moment in a narrative that made it meaningful.

## Structure

Let the material determine the structure. Do not force every theme into the same template.

Patterns that have worked:
- Grounding abstractions in concrete analogy before explaining the technical detail
- Telling history as a causal chain — each innovation as a response to the previous generation's limitation
- Building from large concepts to smaller components
- Returning to the specific implementation after establishing general context
- Comparing approaches side by side to illuminate what makes each distinct

These are available as tools, not obligations.

## Audio considerations

The output is audio. The listener hears it once, in sequence, with no ability to scan back.

- Signpost transitions: "Now we come to...", "This brings us to...", "The deeper lesson here is..."
- When moving between ideas, briefly restate the previous conclusion so a drifting listener can re-anchor
- No tables, code blocks, bullet lists, or visual-only formatting
- Every paragraph must make sense when heard aloud, in order, once
- Use flowing prose — short declarative sentences for technical explanations, longer sentences for narrative and analogy

## On certainty

Do not fabricate certainty.

When the lineage is clear, present it cleanly: "Kingma and Ba published Adam in 2014."
When it is murky, say so: "The exact origin is debated, but the earliest published treatment appears to be..."

When a causal claim is supported by citation, state it as fact: "Nesterov's paper directly inspired the lookahead mechanism."
When it is inference, present it as such: "The technique appeared two years later, addressing the same limitation, though whether there was direct influence is unclear."

The listener trusts the narrator more when the narrator is honest about what they don't know. False certainty degrades every claim around it.

## Length

The narrative is as long as the theme requires and no longer. A simple idea well-told in eight hundred words is better than a simple idea padded. A complex idea that needs five thousand words should not be truncated.

## Output

Write a single text file. Plain text, no markdown formatting (it will be read aloud). Name it by content: `section-optimizer-composition.txt`, `section-fail-fast.txt`, etc.

## Summaries (Phase 5c)

Each finished section also gets a condensed companion in `output/summaries/`, same filename. The summary serves a listener who wants the chapter's actual knowledge without the arc's time investment:

- Every load-bearing fact, constant, and lesson survives; the scenic build-up, analogies, and restatement do not
- Roughly 12–18% of the section's length (~450–600 words for a typical chapter)
- It must stand alone — heard instead of the chapter, not alongside it
- All audio-prose and honesty-about-certainty rules above apply unchanged
