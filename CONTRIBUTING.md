# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

Help is welcome in English or Chinese. You do not need to know Git, identify an internal location ID or write both languages to point out a problem.

## Report a correction

Use the location-correction issue template, or the Workshop's corrections discussion. If you cannot access GitHub, a Workshop comment is fine.

Please include what you can:

- The location name and country or region; an internal ID is useful if you know it.
- The language, the text that needs changing and, if possible, a screenshot.
- What is wrong and what you suggest instead.
- A source that supports the correction. A page link is enough for an initial report.

Distinguish a settlement from its wider region and a historical name from a modern administrative unit. Wikipedia is a useful starting point; local archives, academic work and other reliable references are welcome too. Do not copy long passages into the mod.

For loading problems, include the game build, mod version, language and other enabled mods. Read the [FAQ](docs/FAQ.md) first. Keep logs relevant and remove account information.

## Ways to help

Local history, place identification, English editing and Simplified Chinese proofreading are all useful. A better source or a short explanation can be more valuable than a complete replacement entry. Feedback in just one language is welcome; the two versions will be reconciled during review.

Other languages can be discussed in a proposal, but the first release ships English and Simplified Chinese. Do not create empty language packs or label machine output as a reviewed translation.

## Propose a text change in a pull request

In a source checkout, find the record with tools/find_location.py or search data/descriptions. Change only the relevant record and explain the sources in your PR. A text PR is a proposal: maintainers review it against the research ledger, apply accepted changes there and regenerate the publication data before merging or releasing. This keeps one authoritative copy of the prose.

Do not edit generated files in dist or change IDs, the official protection list, source pins or review status to make a check pass. Keep the existing source records intact; put additional references in the PR explanation for the maintainer to record properly. If you change only one language, say so rather than inventing a translation.

The historical bilingual_reviewed label means a single-AI self-review, not an independent expert review. Do not promote entries to that status as part of a typo fix.

## Tools and documentation

Keep changes small and explain their effect. Run the source checks and relevant tests from the README. Add tests for a meaningful behaviour change, not for wording edits. Screenshots and compatibility claims must come from an actual test of the identified package.

## Review, credit and licensing

Maintainers may ask for a source, revise wording or leave a proposal open for more research. There is no promised response time. Accepted contributors can be credited by their GitHub handle or another name they choose; do not publish someone else's personal details.

Contributions to tools and technical documentation use MIT. New description text and translations use CC BY-SA 4.0, only to the extent you have the right to license them. Preserve third-party credits and conditions; see [LICENSE](LICENSE). Submitting a contribution confirms that you can share it under the applicable terms. No separate CLA is required.

Keep discussion about evidence, wording and the game. Assume good faith, explain disagreements and avoid personal attacks.
