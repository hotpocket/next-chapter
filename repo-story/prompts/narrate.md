# Phase 5: Walkthrough Narrative — Guidance

You are writing an audio walkthrough of a working piece of software. You have the feature inventory, the verified implementation details from the code research, and the prompt provenance from the prompt research. Your job is to walk the listener through the features as they exist right now — what each one is, what it does, and the prompt that shaped it.

## What this is

This is a guided tour, not a documentary. The listener is a reviewer with limited time. They want to understand the artifact and how it was steered into existence — not the history of the ideas behind it, not the field it sits in, not the story of its making told as drama.

The subject is this repository alone: its code, its features, and the story of their implementation as recorded in its own prompts, commits, sessions, and decision records. Nothing outside the repo is part of the story. External tools and dependencies — a TTS model, a test framework, a hosting service — get their name and their role in one clause, because the listener needs to follow the walkthrough; they never get background, origin, maker, or context in the world.

Present tense. The subject is the thing as it works today. The past appears only as provenance: "this exists because the prompt asked for it."

## The paragraph test

Every paragraph must do at least one of these:

1. Name a feature and state what it does.
2. Show its behavior — what goes in, what comes out, what the user sees.
3. Give the prompt behind it — quoted or closely paraphrased, with its session date.

A paragraph that does none of these gets cut. Specifically banned:

- Scenic openings and framing devices ("Start in a car...", "There is a folder that stops you cold...")
- Extended analogies
- Any history that happened outside this repository: who invented an underlying technique, what papers exist, what a dependency's maker built, what the rest of the field does
- More than one clause about any external tool — its name and its role, then back to this repo's code
- Restating a previous chapter beyond one orienting sentence
- Manufactured suspense or drama

## Quoting prompts

The prompts are the connective tissue: feature, then the prompt that caused or shaped it, then what changed as a result.

- Short prompts: quote verbatim. "The prompt read: ..."
- Long prompts: paraphrase, keeping one verbatim key phrase.
- Always attribute to a session date: "from the July twentieth session."
- When only a recap or commit message survives — no verbatim prompt — say so plainly: "the session recap records the instruction as..." Never dress a paraphrase up as a quote.

## Audio considerations

The output is audio, heard once, in sequence.

- Light signposting at transitions: "Next, the export script." One clause, not a paragraph.
- No tables, code blocks, bullet lists, or visual-only formatting.
- Spell out what must be heard correctly: filenames, command names, dates.
- Flowing prose; short declarative sentences for technical content.

## On certainty

Do not fabricate certainty. "The prompt from July twentieth asked for X" is a claim about a real file — make it only when the source supports it. When provenance is inferred (a feature appears between two sessions with no recorded prompt), present it as inference. Honest gaps preserve the credibility of everything else.

## Length

As short as coverage allows. Budget 700–1,200 words per chapter. If a chapter's features are covered in 600 words, stop. Cutting a feature to fit is wrong; padding to fill is wrong; the lever is prose economy.

## Output

Write a single text file. Plain text, no markdown formatting (it will be read aloud). Name it by content: `section-build-pipeline.txt`, `section-player.txt`, etc.

## Summaries (Phase 5c)

Each finished section also gets a condensed companion in `output/summaries/`, same filename — the player's Summary track. With the main track this terse, the summary is an orientation, not a compression: 150–250 words stating what this part of the artifact is, its features by name, and one sentence on how prompts drove it. It must stand alone. Same audio-prose rules.
