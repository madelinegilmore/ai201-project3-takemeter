#!/usr/bin/env python3
"""Validate the labeled CSV and report inter-annotator agreement.

Usage:
    python3 check_labels.py                      # validate + class balance
    python3 check_labels.py annotator2_40.csv    # also compute Cohen's kappa

Catches the things that go wrong when you label in a spreadsheet: typo'd labels,
blank rows, dropped or duplicated rows, and class imbalance that would quietly
wreck training.
"""
import csv, sys, os
from collections import Counter

LABELS = {"analysis", "impression", "logbook"}
MAIN = "takemeter_annotated.csv"
MIN_PER_CLASS = 55
MAX_SHARE = 0.70


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(rows, path):
    problems = []
    seen = Counter(r["review_id"] for r in rows)
    for rid, n in seen.items():
        if n > 1:
            problems.append(f"duplicate review_id {rid} appears {n}x")

    blank = []
    for i, r in enumerate(rows, start=2):  # row 1 is the header in a spreadsheet
        lab = (r.get("label") or "").strip()
        if not lab:
            blank.append(i)
        elif lab not in LABELS:
            if lab.lower().strip() in LABELS:
                problems.append(f"row {i}: '{lab}' -> should be '{lab.lower().strip()}' (case/whitespace)")
            else:
                problems.append(f"row {i}: '{lab}' is not a valid label")

    print(f"\n=== {path} ===")
    print(f"rows: {len(rows)}   labeled: {len(rows) - len(blank)}   unlabeled: {len(blank)}")
    if blank:
        preview = ", ".join(str(x) for x in blank[:10])
        print(f"  unlabeled spreadsheet rows: {preview}{' ...' if len(blank) > 10 else ''}")
    for p in problems:
        print(f"  PROBLEM: {p}")
    return [r for r in rows if (r.get("label") or "").strip() in LABELS], problems


def balance(rows):
    c = Counter(r["label"].strip() for r in rows)
    n = sum(c.values())
    if not n:
        return
    print(f"\nclass balance (n={n}):")
    for lab in sorted(LABELS):
        k = c.get(lab, 0)
        share = k / n
        flags = []
        if k < MIN_PER_CLASS:
            flags.append(f"under target of {MIN_PER_CLASS}")
        if share > MAX_SHARE:
            flags.append(f"over {MAX_SHARE:.0%} ceiling")
        bar = "#" * int(share * 40)
        print(f"  {lab:<11} {k:>4}  {share:>5.1%} {bar} {'  <-- ' + '; '.join(flags) if flags else ''}")

    # the confound planning.md sec.5 is built around
    print("\nmedian length by class (watch for a pure length split):")
    for lab in sorted(LABELS):
        lens = sorted(len(r["text"]) for r in rows if r["label"].strip() == lab)
        if lens:
            print(f"  {lab:<11} {lens[len(lens) // 2]:>6} chars   (n={len(lens)})")


def kappa(a, b):
    """Cohen's kappa for two annotators over the same items."""
    cats = sorted(LABELS)
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca.get(c, 0) / n) * (cb.get(c, 0) / n) for c in cats)
    return po, ((po - pe) / (1 - pe) if pe != 1 else float("nan"))


def interpret(k):
    if k < 0.20: return "poor - taxonomy is not working"
    if k < 0.40: return "fair - definitions need tightening"
    if k < 0.60: return "moderate"
    if k < 0.80: return "substantial - usable"
    return "almost perfect"


def agreement(mine, other_path):
    other, _ = validate(load(other_path), other_path)
    mine_by_id = {r["review_id"]: r for r in mine}
    pairs = [(mine_by_id[r["review_id"]], r) for r in other if r["review_id"] in mine_by_id]

    print("\n=== inter-annotator agreement ===")
    print(f"overlapping labeled items: {len(pairs)}")
    if len(pairs) < 30:
        print(f"  WARNING: stretch goal asks for 30+. You have {len(pairs)}.")
    if not pairs:
        return

    mlab = [m["label"].strip() for m, _ in pairs]
    olab = [o["label"].strip() for _, o in pairs]
    po, k = kappa(mlab, olab)
    print(f"  simple agreement: {po:.1%}")
    print(f"  Cohen's kappa:    {k:.3f}  ({interpret(k)})")

    print("\nconfusion (rows = me, cols = annotator 2):")
    cats = sorted(LABELS)
    print("             " + "".join(f"{c[:9]:>11}" for c in cats))
    for r in cats:
        row = "".join(f"{sum(1 for m, o in zip(mlab, olab) if m == r and o == c):>11}" for c in cats)
        print(f"  {r:<11}{row}")

    dis = [(m, o) for (m, o) in pairs if m["label"].strip() != o["label"].strip()]
    if dis:
        print(f"\n{len(dis)} disagreements - read every one of these before writing up:")
        for m, o in dis:
            print(f"\n  [{m['label'].strip()} vs {o['label'].strip()}] {m['review_id'][:8]}")
            print(f"    {m['text'][:220]}{'...' if len(m['text']) > 220 else ''}")
            for who, r in (("me", m), ("them", o)):
                if (r.get("notes") or "").strip():
                    print(f"    note ({who}): {r['notes'].strip()[:160]}")


if __name__ == "__main__":
    if not os.path.exists(MAIN):
        sys.exit(f"missing {MAIN}")
    mine, _ = validate(load(MAIN), MAIN)
    balance(mine)
    if len(sys.argv) > 1:
        agreement(mine, sys.argv[1])
    print()
