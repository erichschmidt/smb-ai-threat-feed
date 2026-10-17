# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Most of this repo is **published output** of a daily threat-intel pipeline for small businesses running AI and automation. The only source code is `collector/collector.py`. The AI drafting, self-check and publishing steps run outside this repo. They push a `Daily threat feed MM-DD-YYYY: brief + structured data` commit to `main` most mornings. Run `git pull --ff-only` before you edit anything, because `main` is usually behind.

Read `README.md` for the full pipeline description and the severity rubric, and `SCHEMA.md` for the data contract.

## Commands

There are no tests, linter or build step.

```bash
cd collector
pip install -r requirements.txt
export ABUSE_CH_KEY=...          # optional; only ThreatFox/URLhaus need it (also read from a local .env)
python collector.py --out /some/scratch/dir
```

The collector writes `<out>/MM-DD-YYYY.json` for **today** and prints a BRIEF PLAN plus a digest. It reads the earlier `MM-DD-YYYY.json` files in `<out>` as history, so copy `data/*.json` into the scratch dir first to get realistic `first_seen` values and a realistic plan. If you run it with `--out ../data`, it overwrites that day's published data file, so point it at a scratch directory when testing.

## How the pieces fit

1. **Collect.** `collector.py` → `data/MM-DD-YYYY.json`. This step is deterministic and uses no AI. The same file is copied to `latest.json`, which consumers poll, so the two should be identical for the newest day.
2. **Plan.** In the same run, `plan_brief()` writes `brief_plan`: up to 3 findings (AI tools first, one per product, nothing repeated unless it escalated), their severities from `rate_severity()`, "on the radar" one-liners, a quiet-day flag, and a Monday AI-risk topic. Selection is code so that a small drafting model only has to write prose.
3. **Draft.** Outside this repo, AI writes `briefs/Threat-Feed-MM-DD-YYYY.md` from `brief_plan`, under about 900 prose words. Brief layout:
   - YAML front matter, the disclosure line, and a 3-line "How to read the scores"
   - numbered findings `## N. <SEVERITY>: <headline>` (a dash before 10-17-2026), each with *What broke / Why it matters to an SMB running AI tools / What you do Monday / Sources*
   - optional "Also on the radar" and "AI risk of the week"
   - "Jargon buster"
   - an "Appendix" with the KEV table, a ransomware pulse line and a link to `latest.json`

   Briefs before 10-12-2026 used an older, longer layout.
4. **Gate and publish.** Outside this repo, a code check compares the brief with `brief_plan` and blocks the publish on hard failures: missing disclosure line, a finding without a source link, a severity or ID that doesn't match the plan, or brand terms. `feed.xml` (Atom) gets one entry per brief, newest first, linking to the brief on GitHub. The HTML inside `<content type="html">` must be entity-escaped so the feed stays W3C-valid (see commit be2dff2). `GLOSSARY.md` is a living A–Z list. Every term used in a brief must appear there. Add terms but never remove them.

`collector/collector.py` is a public mirror of the production collector's logic. Keep its CLI stable (`--out` and `ABUSE_CH_KEY` from env/.env). If the collection logic changes, the published data's shape changes too.

## Collector conventions

- **Source isolation.** Every `fetch_*` function catches its own errors and returns either `{"count", "items"}` or `{"_error": ..., "items": []}`. It never raises. `build_packet()` turns that into `sources.<name>.status` (`"ok"` or the error string). A new source therefore needs a fetcher, a `sources` entry, a top-level packet key, a section in `SCHEMA.md` and a line in the README source list.
- **Dates are `MM-DD-YYYY`** in file names, `date`, and KEV `added`/`due`. Upstream ISO dates are converted with `iso_to_mmdd()` at the end of `build_packet()`. `generated` is the only field that stays an ISO-8601 UTC timestamp. An earlier bug left KEV dates as `YYYY-MM-DD` in old data files until 52ded78, so check any date handling against `SCHEMA.md`.
- **EPSS enrichment** runs once, after all fetches, over the CVE IDs from KEV, the CIRCL aliases and the AI advisories. Unscored CVEs get `null`.
- CIRCL's `/api/last` returns a mix of OSV-style records and raw CVE 5.x records. `fetch_circl()` normalizes both shapes.
- **AI coverage** comes from `fetch_ai_advisories()`: GitHub-reviewed advisories from OSV.dev, unauthenticated, with one batch query for the whole `AI_WATCHLIST`. Packages in `AI_SMB_COMMON` rank first. If that source fails at all, `brief_plan.ai_advisories_checked` is false and the day is never reported as quiet. `AI_TERMS` decides whether a KEV or CIRCL entry counts as AI.
- **History.** `annotate_history()` sets `first_seen` and `prev_epss` from earlier packets, tracking KEV separately from CIRCL and AI advisories. Today's own file is ignored, so same-day re-runs give the same plan.
- **Planning.** Change what the brief covers in `plan_brief()`, `rate_severity()` or `AI_RISK_TOPICS`, not in the drafting prompt. Keep `brief_plan` JSON-serializable; it is published in the data file.

## Hard rules (stated in README / collector README)

- Use only public, free, read-only sources. No exploit instructions, payloads or scanning of public targets.
- Never emit ransomware leak-site (`.onion`) links. Ransomware links are limited to `ransomware.live` pages.
- Every finding carries a source link: "No link, no claim."
- Severity labels follow the README rubric (CRITICAL / HIGH / WATCH), implemented in `rate_severity()`. When in doubt, choose the lower label. Briefs from before 10-09-2026 predate the rubric.
- This repo is public: never add the names of the systems, hosts, employers or businesses behind the pipeline, or internal paths.
- Credentials come only from the environment or `.env`, both gitignored.
- Licensing: briefs and data are CC BY 4.0 (root `LICENSE`). `collector/` is MIT.
