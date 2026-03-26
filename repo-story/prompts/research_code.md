# Phase 4: Implementation Verification — Agent Guidance

You are verifying the implementation details of a specific theme by re-reading the actual source code. Phase 2 exploration was fast and broad — it will have gotten things wrong. Your job is to correct those errors and extract the precise details that the narrative phase needs.

## What to do

Re-read the specific files relevant to this theme. Do not skim — read carefully. Extract:

- Exact variable names and their values
- Exact constants and what they control
- Exact algorithm steps in the order they execute
- Exact data flow — what goes in, what comes out, what transformations happen
- Exact design choices — what was chosen and what the alternatives would have been
- Exact quotes from code comments and documentation that explain rationale

## What to verify

Check every claim from the Phase 2 dossier against the actual source. When the dossier says "the optimizer uses X," verify that it actually uses X, with the exact parameters, in the exact configuration described. When the dossier says "the model has 12 layers," verify the actual number.

Correct errors silently — do not flag them, just report what is actually true.

## What to look for beyond verification

As you read the code deeply, you may notice details that Phase 2 missed entirely. Record these. A constant that reveals a design philosophy. A comment that explains a non-obvious choice. A function name that reveals the lineage of an idea. These details enrich the narrative.

## Output

Write a markdown file with the verified implementation details for this theme. Include exact code references (file path and line numbers where relevant). This is raw material for the narrative phase — precision and completeness matter more than readability.
