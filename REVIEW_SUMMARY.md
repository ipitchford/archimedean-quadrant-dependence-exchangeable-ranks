# Review summary (internal, AI-assisted)

This is a public summary of the internal checking of version 0.1.0-candidate, without scores. It is not peer review,
independent reproduction or formal verification. No human referee has assessed the paper.

## What was done (24-25 November 2026)

1. **One combined five-perspective Claude review panel** (editor, proof audit, domain, applied-statistics
   perspective, and devil's advocate) on the source drafts: a manuscript on quadrant dependence and concordance, and a
   shorter note on the same conjecture. The cited sources were obtained and read. The panel found no critical issue;
   its major items concerned presentation, merging, explicit parameters, attribution and statistical honesty.
2. **One merged revision round with an extension.** The two drafts became one paper with a context-first
   introduction and notation fixed before use. The local counterexamples are now proved directly for explicit ranges
   (0 < |ε| ≤ 10⁻³ and 0 < |ε| ≤ 10⁻⁸) instead of by an inexplicit perturbation argument; the frailty result uses a
   limit argument with an exact certificate at rates 1, 2 and 200, the MTP2 criterion of Müller and Scarsini and a
   new totally-positive corollary; the conditionally i.i.d. variance lemma credits Fuchs (2024); the counterexamples
   were extended to every finite dimension; closed forms for d_n(s) were added; attributions to Fuchs and Tschimpke,
   Graham, Ansari, Rockel and Steinmaßl, Koike and Hofert, McNeil and Nešlehová, and Konstantopoulos and Yuan were
   sharpened; effect sizes and the population scope are stated. Extensions: the exchangeability theorem now covers
   slopes −n/2 ≤ s < 0, and a new corollary shows that no finite family of comparisons characterises PMI. An
   incorrect draft remark on singular Gini matrices was removed.
3. **Verification re-review with a proof audit** of every new or rewritten proof. One major defect was found and
   fixed: the bound displayed in Remark 6.4 (slopes s < −n/2) was off by a factor n²; it was corrected and verify.py
   now checks the corrected value. Nine minor items (constants, wording, notation, attribution) were applied.
4. **Clean replays** of both scripts from fresh copies, by the lead and again by the publisher, with a negative
   control (see [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)).

No Astra/Codex second-model review took place in this batch.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| "Refuting a conjecture by tiny perturbations is shallow." | The structural results (comparison duality, frailty threshold, exchangeability bounds, Gini matrices) are presented as co-equal contributions; the effect sizes are stated in Section 1 and Section 8. |
| "The perturbation argument gives no usable parameters." | Replaced by elementary proofs with explicit ranges, checked exactly in verify.py. |
| "Do the examples matter for practice?" | Section 8 says they settle the logical question only and say nothing about the power of tests; all results are population statements. |
| "Is the extremal construction for exchangeable ranks really optimal?" | Proved for −n/2 ≤ s ≤ 1, attainment checked exactly in 56 cases, and finite-grid linear programs agree (check_grid.py). For s < −n/2 only a valid bound is given (Remark 6.4). |
| Not addressed | The full attainable set for exchangeable ranks, the full generalised Gini compatibility sets and which standard Archimedean families are PMI are listed as open problems in Section 8. |

## Scope of assurance

Internal AI-assisted review only: written proofs checked by AI reviewers, exact computational checks replayed,
sources read. No human specialist review, no independent reproduction by an unaffiliated party, no proof-assistant
formalisation. Literature searches were of limited scope (see [RESEARCH_GATES.json](RESEARCH_GATES.json)).
