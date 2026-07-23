# Phase 4: Implementation Verification — Agent Guidance

You are verifying the implementation details of a specific feature cluster by re-reading the actual source code. Phase 2 exploration was fast and broad — it will have gotten things wrong. Your job is to correct those errors and extract the precise, current behavior that the walkthrough narrative needs.

## What to do

Re-read the specific files relevant to these features. Do not skim — read carefully. Extract:

- Exact variable names and their values
- Exact constants and what they control
- Exact algorithm steps in the order they execute
- Exact data flow — what goes in, what comes out, what transformations happen
- Exact design choices — what was chosen and what the alternatives would have been
- Exact quotes from code comments and documentation that explain rationale

## What to verify

Check every claim from the Phase 2 dossier against the actual source. When the dossier says "the build script emits X," verify that it actually emits X, with the exact flags, in the exact configuration described. When the dossier says "there are 12 chapters," verify the actual number. The walkthrough narrates present-tense behavior — a stale claim becomes a false demo.

Correct errors silently — do not flag them, just report what is actually true.

## What to look for beyond verification

As you read the code deeply, you may notice user-visible behaviors that Phase 2 missed entirely. Record these. A flag that changes what a command produces. A default the walkthrough should state. A comment that explains a non-obvious choice. Skip lineage and philosophy — the walkthrough does not use them.

## Output

Write a markdown file with the verified implementation details for this feature cluster. Include exact code references (file path and line numbers where relevant). This is raw material for the narrative phase — precision and completeness matter more than readability.
