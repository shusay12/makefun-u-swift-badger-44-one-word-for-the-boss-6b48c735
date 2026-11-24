#!/usr/bin/env python3
"""One Word for the Boss — entry program.

Picks one word describing the entrant's boss and writes it to
/output/entry.txt. The word is chosen by scoring a shortlist of candidate
words against the judge's five criteria, in the judge's own order:

  1. single word a person would actually use about their boss
  2. funny on its own
  3. rings true about a real boss habit
  4. fresh, not the first word anyone reaches for
  5. travels across workplaces (kitchen, warehouse, office)

Deterministic: no randomness, no network, stdlib only.
"""

import os
import sys

# (word, scores for criteria 1..5, each 0..5)
CANDIDATES = [
    ("Rescheduler", (5, 4, 5, 4, 5)),   # moves every meeting, again and again
    ("Swooper", (5, 4, 4, 4, 4)),       # seagull management: swoops in, squawks, leaves
    ("Unreader", (4, 3, 5, 5, 4)),      # never reads anything you send, asks about it anyway
    ("Pivoter", (5, 3, 4, 4, 3)),       # new direction every week
    ("Pinger", (5, 3, 4, 4, 5)),        # pings you constantly, day and night
    ("Micromanager", (5, 2, 5, 1, 5)),  # true, but the first word anyone reaches for
    ("Delegator", (5, 1, 3, 2, 4)),     # accurate, not funny
    ("Ghoster", (5, 3, 3, 2, 4)),       # vanishes when a decision is needed
    ("Firefighter", (5, 2, 4, 2, 3)),   # always in crisis mode of their own making
    ("Visionary", (5, 3, 3, 3, 3)),     # all vision, no plan; ironic, but needs the irony explained
]


def score(candidate):
    """Lexicographic score: criteria in the judge's order, then shorter wins."""
    word, scores = candidate
    return (scores, -len(word))


def pick_word():
    # Lexicographic pick (criteria in the judge's order, shorter wins ties).
    best = max(CANDIDATES, key=score)[0]
    # Cross-check: weighted sum with judge-order weights must agree.
    # If the two rankings disagree, the shortlist needs re-scoring, not a
    # silent winner.
    weights = (5, 4, 3, 2, 1)
    weighted = max(
        CANDIDATES,
        key=lambda c: (sum(w * s for w, s in zip(weights, c[1])), -len(c[0])),
    )[0]
    if weighted != best:
        raise RuntimeError(
            "ranking disagreement: lexicographic=%s weighted=%s" % (best, weighted)
        )
    return best


# Words the judge's freshness criterion rules out: the first word anyone
# reaches for, however true. A candidate matching one is disqualified.
CLICHES = {"micromanager", "bossy", "tyrant", "demanding", "perfectionist",
           "workaholic", "controlfreak", "narcissist", "clueless"}


def validate(word):
    if not word or len(word) > 30:
        raise ValueError("entry must be 1 to 30 characters")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word, no whitespace")
    if not word.isalpha():
        raise ValueError("entry must be letters only")
    if word.lower() in CLICHES:
        raise ValueError("entry is a first-reach cliche, not fresh")
    return word


def main():
    word = validate(pick_word())
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    # Round-trip self-check: what the grader reads must be exactly the word.
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != word:
            raise RuntimeError("entry.txt round-trip mismatch")
    print(word)
    return 0


if __name__ == "__main__":
    sys.exit(main())
