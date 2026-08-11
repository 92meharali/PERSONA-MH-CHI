# HuMT / response provenance audit

This audit checks whether the current HuMT joins can be kept without changing scores or fabricating identifiers. It is read-only: no unmatched HuMT values are recovered here.

## Summary

| Domain | Responses | HuMT rows | Matched | Unmatched | Duplicate response texts | Duplicate HuMT texts | Stable ID in HuMT | Fuzzy matches | Decision |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| mental_health | 660 | 0 | 660 | 0 | 0 | 0 | no | 0 | embedded_humt |
| education | 450 | 450 | 447 | 3 | 2 | 2 | no | 7 | keep_text_join_documented |
| health | 450 | 450 | 419 | 31 | 0 | 0 | no | 0 | keep_text_join_documented |

## Findings

- Mental health uses embedded HuMT values and native metadata.
- Education and health HuMT exports do not contain a stable response identifier such as `annotation_item_id`, `response_id`, or `prompt_id`; the repository does contain `annotation_item_id`, but the HuMT files cannot join on it.
- The Phase 1 join accepts only unique normalized text keys, then unique prefixes, then mutually-best fuzzy matches with a similarity threshold and margin.
- No ambiguous HuMT matches are accepted. Ambiguous or unmatched rows remain missing and are counted in `data_audit.md` and `humt_join_report.csv`.
- Because no stable HuMT-side identifier exists, the correct decision is to keep the documented text join and report unmatched rows transparently.

## Unmatched rows

| Domain | Unmatched annotation_item_id values |
|---|---|
| mental_health | - |
| education | PEDU-0070;PEDU-0071;PEDU-0072 |
| health | PHLT-0186;PHLT-0193;PHLT-0194;PHLT-0195;PHLT-0214;PHLT-0215;PHLT-0216;PHLT-0249;PHLT-0256;PHLT-0257;PHLT-0258;PHLT-0268;PHLT-0269;PHLT-0270;PHLT-0292;PHLT-0293;PHLT-0294;PHLT-0295;PHLT-0296;PHLT-0297;PHLT-0397;PHLT-0398;PHLT-0399;PHLT-0411;PHLT-0415;PHLT-0416;PHLT-0417;PHLT-0444;PHLT-0448;PHLT-0449;PHLT-0450 |

## False-match risk

False matches are constrained by the one-to-one join rules: a candidate key must identify exactly one response and exactly one unused HuMT row. Fuzzy matches must also be mutually best and clear the similarity and margin requirements. The audit therefore treats accepted matches as deterministic under the committed files, while still recommending future HuMT exports include stable response IDs.
