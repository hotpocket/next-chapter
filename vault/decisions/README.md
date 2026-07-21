# Decisions index

Read top-to-bottom for the architecture's story; **Active** rows are the
current design. Superseded ADRs are kept — the audiobooks narrate how
decisions evolved, and this trail is the record.

| ADR | Decision | Status |
|-----|----------|--------|
| [0001](0001-pages-ui-s3-audio.md) | UI on Pages, audio on S3, no playback backend | Superseded by 0008 (Pages-UI half carries forward) |
| [0002](0002-minimal-player-first.md) | Build a minimal player fresh | Superseded by 0006 |
| [0003](0003-generation-offline-boundary.md) | Generation is offline, machine-side; reviewer plays, never regenerates | **Active** |
| [0004](0004-ingestion-pipeline-lambda-tailscale.md) | V2 visitor-submitted ingestion (Lambda → home GPU) | Deferred; presumed S3 — would need redesign |
| [0005](0005-two-books-self-demonstrating.md) | Books narrate the project's own sources | **Active**, extended by 0009 |
| [0006](0006-reuse-landry-ui-player.md) | Reuse the landry-ui player; demonstration is the assembly | **Active**, deploy framing amended by 0008 |
| [0007](0007-repo-local-claude-mirror.md) | AI config mirrored in-tree at `.claude/` | **Active** |
| [0008](0008-audio-in-repo-pages-only.md) | Audio in-repo, Pages serves everything; S3/CloudFront hosting is the V2 path | **Active** |
| [0009](0009-three-books-trilogy.md) | Three books: landry-ui → repo-story → next-chapter (generated last, range pinned) | **Active** |
