# Verification goals

You are given the protocol theory in `theory.spthy`. The theory is complete
**except for its security lemmas**, which have been removed. Your job is to:

1. Formulate a security lemma for **each** goal listed below, using the given
   lemma names (Tamarin will match them when grading).
2. Run the Tamarin prover and drive the analysis to completion: every lemma
   must terminate with `verified` or `falsified - found trace`.
3. Produce the deliverables described in the task README
   (`final.spthy`, `verdict.json`, `attack_report.md` if unsafe).

Notes:

- Lemma statements are yours to write; the quantifier column is binding.
- Helper/source lemmas beyond the listed goals are allowed (and often
  needed to make the prover terminate).
- Some theories use `diff()` terms (observational equivalence):
  analyzing them requires `tamarin-prover --diff`.

## Goals to formalize

| # | Lemma name | Quantifier | Property |
|---|------------|------------|----------|
| 1 | `PasswordsConfidential` | all-traces | passwordsconfidential |
| 2 | `MessagingKeysUnique` | all-traces | messagingkeysunique |
| 3 | `CodeSecrecy` | all-traces | codesecrecy |
| 4 | `CodeVerifierSecrecy` | all-traces | codeverifiersecrecy |
| 5 | `TokenFormatAndOTPLearning` | all-traces | tokenformatandotplearning |
| 6 | `CodeAgreement` | all-traces | codeagreement |
| 7 | `CodeIsSingleUse` | all-traces | codeissingleuse |
| 8 | `Executability` | exists-trace | executability |
| 9 | `SOAPAgreement` | all-traces | soapagreement |
| 10 | `SocialAuthentication` | all-traces | socialauthentication |

## Protocol description (natural language)

(no description available; reconstruct from the theory)
