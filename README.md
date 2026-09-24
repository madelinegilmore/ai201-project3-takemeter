# ai201-project3-takemeter
In this project, you'll build TakeMeter: a fine-tuned text classifier that evaluates discourse quality in an online community of your choosing. You'll define the labels, collect and annotate the data, fine-tune a model, and then honestly assess where it works and where it falls apart.

**Hard to label examples**


1. 
I got hooked into this real fast! And once Lisbeth came along, wow I was speechless! Can we please have more badass female characters like these, pretty please with cherries on top? Although less heartbreaking backgrounds would be much appreciated. I binge read the trilogy for you, my heroine!

Impression - could be log book because after the first sentence they're not related to the book directly but the least sentence and the first sentence are sentiment related.


2. 
"What'll we do with ourselves this afternoon?" cried Daisy. "and the day after that, and the next thirty years?"

Logbook - hard becasue its only a quote but logbook because it doesn't fall into the other two


3. 
Could you imagine for a second, just a mere little second, the dialogue of Deadpool with the simplicity of Joey from Friends? Perhaps add in a dash or two of the go getter attitude found within Wolverine to go fourth and fight? What if I told you of a man who emboddied all that? Would your brian bits tingle? Would if you were the right person, your loins stir? What if I even added the sex drive of say Casanova? All set in the land of old, where lore and might added with sharp steel and magic. How about centuars? Deliciously funny and terrible evil queens? Monsters and battles and wizards oh my! Have I your attention yet? Let me sweeten the pot then for those casting their gaze upon these words. Who hear from clicking the link alone to be guided through the winding maze of the web saw that glowing image and the emblazoned word BYRON had the immediate thought, however brief, of CONAN enter their mind? If you are raising your hand, and reading with baited breath I have something to share with you. For those of you not raising your hand, you owe it to yourself to go fourth and figure out how to attain a copy. How about Beastmaster? Red Sonja? Fire & Ice? Even if you have never sat down to any of these delightful gems about barbarians, surely you had to have read about them at some point in History. Let me introduce to you a barbarian who you will not only root for, but demand multiple sequels detailing his exploits and adventures. BYRON The Barbarian! If you long for the days where gratuitous sex and violence with thoroughly imagined fantasy were wrought on the screen and in some books I won't mention here because this is about BYRON, you need to read this book. Page after page takes you deeper and deeper into the world of this oafish tower of muscle and wit, never once becoming bored or tired. Everywhere you look in this book will make you go through your own library wanting to continue the exileration you will have felt reading this. BYRON The Barbarian stands on its' own, never guilding the lily of the other barbarian titles mentioned and yet pays respectful amage and nuanced understanding of what the whole mythos is about. The colorful dialogue makes you want to engrain what BYRON says into your brain bits to use in your day to day life. And by the nine Hells you will! And you'll want to know what that means I'm sure and more once you've read BYRON The Barbarian and beg and plead and scream for more after you've finished it. This is a series that having only one book so far to it's name is bound to turn into several if Jeff O'Brien allows it. He has taken hold of something that once actualized and made manifested, is destined to take on a life of it's own. Skillfully and respectfully, his book has done what many strive for that many of the quote un quote "Top Shelf Best Sellers" one can find in their local bookstore actually fall flatter then a wrong note in a clean breezy jazz club. It never takes itself seriously and at the same time is very serious in what it is supposed to be. An adventure! It's supposed to be fun! It's supposed to be gratuitous! It's supposed to be exilerating! This book will make you want to pick up an axe, rip into a Turkey leg, down a pint of ale, plant said axe into a villainous creature and take his/her man/woman for your own! Or if you already have one, then to fight the worlds evils to protect them! All this and so much more await with BYRON The Barbarian. So quit reading my stinking review and go pick up a copy!

analysis - difficult because its full of emotion but its an analysis because it lists details about the plot of the book rather than how the book resonated with the reader as a whole.



🎯 Baseline accuracy: 0.949  (evaluated on 39/39 parseable responses)

Per-class metrics (baseline):
              precision    recall  f1-score   support

    analysis       1.00      0.92      0.96        26
  impression       0.85      1.00      0.92        11
     logbook       1.00      1.00      1.00         2

    accuracy                           0.95        39
   macro avg       0.95      0.97      0.96        39
weighted avg       0.96      0.95      0.95        39


**Sample Classifications**


| Post (truncated) | True label | Predicted | Confidence | Correct? |
|---|---|---|---|---|
| Good enough sandford. THe machoism got to me some in this one - and a bit more extreme (in... | analysis | analysis | 0.37 | yes |
| My Thoughts: This was a very fast read for me and I liked it. We are introduced to Carly w... | analysis | analysis | 0.40 | yes |
| GENIUS is what Nora Roberts is! This novel is Epic Genius! Loved it!!! It's been a long ti... | analysis | analysis | 0.40 | yes |
| FANGIRL MOMENT. Omygoddddddd, this cover is so frickin beautiful. The title is so awesome ... | impression | analysis | 0.38 | no |
| working on some of them now. Good details and plenty of options. | impression | analysis | 0.38 | no |

Paste this table into your README under 'Sample Classifications'.
For at least one correct row, add a sentence on why that prediction is reasonable.


Reflect briefly: where did the baseline struggle? Are there specific labels it consistently confuses? Write down your hypothesis — you'll test it after fine-tuning.

precision 1.00, recall 0.92 → every sample predicted as "analysis" really was analysis, but ~2 true analysis samples got predicted as something else.



🎯 Fine-tuned model accuracy: 0.667

Per-class metrics (fine-tuned model):
              precision    recall  f1-score   support

    analysis       0.67      1.00      0.80        26
  impression       0.00      0.00      0.00        11
     logbook       0.00      0.00      0.00         2

    accuracy                           0.67        39
   macro avg       0.22      0.33      0.27        39
weighted avg       0.44      0.67      0.53        39



**Wrong predictions**

--- #1 ---
Text:      FANGIRL MOMENT. Omygoddddddd, this cover is so frickin beautiful. The title is so awesome and the colors are just awesome!! So much awesomeness!! I don't want to wait until....whenever it comes out. I...
True:      impression
Predicted: analysis  (confidence: 0.38)

--- #2 ---
Text:      working on some of them now. Good details and plenty of options.
True:      impression
Predicted: analysis  (confidence: 0.39)

--- #11 ---
Text:      Oh my word, I loved this book so so much. This entire series was absolutely fantastic and the beauty and the beast vibe in this one just made me really happy. I really liked the way it ended and the e...
True:      impression
Predicted: analysis  (confidence: 0.39)



Correct example:

Good enough sandford. THe machoism got to me some in this one - and a bit more extreme (in opinion and presentation) than like. Plus unsatisfying ending. but still a lucas page turner and good read

Label: analysis
Reason: It offers specific, evaluative judgments about the book's content and craft (calling out the "machoism" as overdone, judging the ending as "unsatisfying," comparing it to expectations), which are the kind of critical assessments that justify an analysis label even though the tone is casual and personal.


## Evaluation Report

### Overall accuracy

| Model | Accuracy |
|---|---|
| Zero-shot baseline (Groq) | 0.9487 |
| Fine-tuned DistilBERT | 0.6667 |
| Improvement from fine-tuning | **−0.2821** |

### Per-class metrics — fine-tuned

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| `analysis` | 0.667 | 1.000 | 0.800 | 26 |
| `impression` | 0.000 | 0.000 | 0.000 | 11 |
| `logbook` | 0.000 | 0.000 | 0.000 | 2 |
| macro avg | 0.222 | 0.333 | **0.267** | 39 |

### Per-class metrics — baseline

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| `analysis` | 1.00 | 0.92 | 0.96 | 26 |
| `impression` | 0.85 | 1.00 | 0.92 | 11 |
| `logbook` | 1.00 | 1.00 | 1.00 | 2 |
| macro avg | 0.95 | 0.97 | **0.96** | 39 |
| accuracy | | | 0.9487 | 39 |

**Macro-F1: baseline 0.96 vs. fine-tuned 0.27.** The gap is wider on macro-F1 than on accuracy,
because accuracy partly conceals a model that never predicts two of its three classes.

### Confusion matrix — fine-tuned

| | → `analysis` | → `impression` | → `logbook` |
|---|---|---|---|
| **`analysis`** | 26 | 0 | 0 |
| **`impression`** | 11 | 0 | 0 |
| **`logbook`** | 2 | 0 | 0 |

### Which labels are confused?

All 13 errors go one direction: `impression`→`analysis` (11) and `logbook`→`analysis` (2). Two
columns are empty. The model predicts `analysis` for all 39 examples, and 0.6667 is exactly 26/39 —
the base rate of `analysis` in the test set. Confidences sit at 0.37–0.40 against a 0.333 chance
floor, on correct and incorrect rows alike. This is majority-class collapse, not a misplaced
boundary: there is no boundary to examine.

### Why these three failed

**#1 — FANGIRL / cover art.** Cover, title and colors are properties of the *object*, not the text,
so the `impression` label is correct under the edition/format carve-out. The review is nonetheless
full of concrete book-related nouns, and specificity is the surface feature that correlates with
`analysis`. Telling "specific about the object" from "specific about the text" needs a semantic
rule, not a lexical pattern.

**#2 — "working on some of them now. Good details and plenty of options."** Correct as `impression`
via the unsupported-craft-adjectives carve-out: "good details" names a dimension without describing
anything. At 64 characters it is the shortest review in the test set, and it starts mid-sentence —
the record is a fragment, which is a data-extraction issue as much as a classification one.

**#3 — "beauty and the beast vibe".** The hardest of the three. The codebook counts a comparison as
`analysis` when it "names what is being compared," and this does name a work. The label rests on
"vibe" being undimensioned. That carve-out was written for rankings ("the weakest Sanderson"), not
allusions, and an allusion carries more content than a ranking. This is a gap in the rule, not a
model error.

### Labeling problem or data problem?

Not labeling. The baseline scored 0.9487 against the same gold labels — inconsistent labels could
not support that. The failure is in training:

- **`warmup_steps=50` exceeds the 36 total training steps** (182 examples ÷ batch 16 = 12 steps ×
  3 epochs). The learning rate never finishes warming up, peaking near 1.44e-5 instead of 2e-5. The
  model is undertrained, which is what near-chance confidence looks like.
- **Training split is 65% / 29% / 5%** (119 / 53 / 10). Predicting the majority class scores 65%, so
  collapse is a local optimum reachable immediately.
- **`metric_for_best_model="accuracy"`** then selects that collapsed checkpoint as "best."

### What would need to change

1. `warmup_steps` 50 → 5. Nothing else is diagnosable until the model actually trains.
2. Select on macro-F1 instead of accuracy.
3. Class weights in the loss, or more `logbook` data — 10 training examples cannot support a class.
4. Raise `max_length` from 256 (it truncates 29% of `analysis` reviews and 0% of the others).


**Error Analysis**

1. **FANGIRL MOMENT** — The true label is `impression`, but the model predicted `analysis` with 0.38 confidence. The review is intensely positive and mentions the cover, title, and colors, but it does not explain anything specific about the book's plot, structure, characters, or craft. The model likely treated those concrete nouns as book evidence, even though the codebook explicitly excludes cover-related comments and unsupported praise.

2. **"working on some of them now"** — The true label is `impression`, but the model predicted `analysis` with 0.39 confidence. "Good details and plenty of options" is vague praise, not a checkable claim about the book. The opening also describes the reader's activity, but the final clause is still only an unsupported verdict. This is a direct test of the boundary between a specific book claim and a general positive reaction.

3. **Beauty-and-the-beast comparison** — The true label is `impression`, but the model predicted `analysis` with 0.39 confidence. The review expresses strong enthusiasm and says the book has a "beauty and the beast vibe," but it does not explain which elements are being compared or how the comparison illuminates the book. Under the codebook, this is an undimensioned comparison and should remain `impression`.



| True \ Predicted | analysis | impression | logbook |
|-------------------|:--------:|:----------:|:-------:|
| **analysis**      |    26    |     0      |    0    |
| **impression**    |    11    |     0      |    0    |
| **logbook**       |     2    |     0      |    0    |


## Confidence calibration

**The confidence scores are not meaningful.** A 90%-confident prediction cannot be compared against
a 60%-confident one, because the model never produces either — every one of the 39 test predictions
falls between 0.37 and 0.40.

| | n | min | max | mean |
|---|---|---|---|---|
| Wrong predictions | 13 | 0.37 | 0.39 | 0.383 |
| Correct predictions (observed) | 3 | 0.37 | 0.40 | 0.390 |

The two ranges overlap almost completely, and **0.37 appears on both a correct prediction and two
errors**. The total spread across all observed predictions is 0.03. No threshold separates right
from wrong: filtering at any cutoff either keeps everything or discards everything.

**Zero predictions exceed 0.50.** With three classes the chance floor is 0.333, so the model's most
confident output is 0.067 above random guessing.

The model is also badly **under-confident in aggregate**: mean confidence ≈ 0.385 against actual
accuracy 0.667, a calibration gap of ~28 points. That gap is not a calibration problem that
temperature scaling would fix — it is what a near-uniform softmax looks like when the constant it
always predicts happens to be right 2/3 of the time.

For the deployed interface this matters concretely: there is no confidence threshold at which
predictions could be trusted and below which they could be flagged for review, which is the normal
way a classifier like this would be deployed safely.

## Error pattern analysis

**The methodological caveat comes first, because it governs everything below.** The model predicts
`analysis` for all 39 test examples, so the 13 errors are *exactly* the 13 non-`analysis` examples
in the test set. Any pattern found in the errors is therefore a description of the `impression` and
`logbook` classes, **not** a behavior the model learned. planning.md §9 requires checking every
proposed pattern against the correct predictions too — and here the correct predictions carry the
same label and the same 0.37–0.40 confidence as the errors. Nothing distinguishes them.

So "the model consistently misclassifies X" is not a claim this data can support. What follows is a
characterization of the boundary a *working* model will have to learn, with a testable prediction.

**Pattern 1 — the errors are concentrated on the carve-out cases.** At least 10 of 13 trip one of
the four carve-outs from CODEBOOK.md — text that sounds like evidence without being evidence:

| # | Chars | Carve-out tripped |
|---|---|---|
| 1 | 230 | edition/format — cover, title, colors |
| 2 | 64 | unsupported craft adjective — "good details" |
| 3 | 290 | undimensioned comparison — "Jane Austen-ish" |
| 4 | 41 | unsupported craft adjectives — "fast paced", "catchy story line" |
| 5 | 265 | undimensioned comparison — another Conroy book, named but not compared |
| 6 | 186 | undimensioned comparison — *Bossypants*; plus "funny and interesting and charming" |
| 7 | 38 | bare audience tag — "King Arthur-related" |
| 11 | 296 | undimensioned comparison — "beauty and the beast vibe" |
| 12 | 85 | bare audience tag + unsupported craft adjective — "Beautifully written" |
| 13 | 757 | circumstance (virtual book tour) + promotional adjectives |

The remaining three are a bare quotation (#8), a bare verdict (#9), and pure affect naming an
author (#10).

This is a real finding about the data: the minority classes consist largely of reviews that
*resemble* `analysis` at the surface. The four carve-outs are doing the bulk of the discriminative
work in this taxonomy, and the training set contains only 63 non-`analysis` examples to teach all
four.

**Pattern 2 — 8 of 13 name a person or a work.** Jane Austen, Conroy / *My Losing Season*, Tina Fey
/ *Bossypants* / Amy Poehler / *Yes Please*, King Arthur, Monika, Patrick Ness, Beauty and the
Beast, Joshua Graham / *Darkroom*. Proper nouns are the surface feature most strongly associated
with `analysis` in the training data, because genuine `analysis` reviews name characters, authors
and comparison works.

**Testable prediction.** If the training bug is fixed and the model retrained, I expect the residual
errors to concentrate on exactly these: short reviews that name a work or author without saying what
is being compared. That hypothesis is falsifiable against a new confusion matrix, which is more than
can be said for any pattern read off the current one.

**Pattern 3 — length, and why it is not usable evidence.** The error set has a median of 133
characters against 626 for `analysis`, and 9 of 13 are under 250. But `impression` has a corpus-wide
median of 111 characters, so short-and-wrong is just short-and-`impression`. Length separates the
classes in the *data*; it says nothing about the model here.

## Deployed interface

[`predict.py`](predict.py) accepts a review, runs it through the fine-tuned checkpoint, and prints
the label, the confidence, and the full probability distribution.

```bash
# one-off
python3 predict.py "The pacing in the middle third drags."

# interactive — paste reviews, Ctrl-D to quit
python3 predict.py

# piped
echo "Exciting, fun, entertaining! :)" | python3 predict.py

# a checkpoint somewhere else
python3 predict.py --model ./takemeter-model/checkpoint-36 "review text"
```

Output:

```
  text       The pacing in the middle third drags.
  prediction analysis
  confidence 0.382
  distribution
    analysis    0.382  ###############
    impression  0.331  #############
    logbook     0.287  ###########
  NOTE: confidence below 0.50 on a 3-class task is barely above the
        0.333 chance floor — treat this prediction as unreliable.
```

**Requirements:** `transformers`, `torch`. It loads `./takemeter-model` by default — the
`output_dir` Section 3 writes to — and exits with instructions if no checkpoint is there. Section 3
must be run first; the checkpoint is not committed to this repo.

The sub-0.50 warning is deliberate. Given the calibration findings above, an interface that
displayed a bare label would imply a confidence the model does not have.

## Reflection: what the model captured vs. what I intended

I intended the model to learn a **functional** distinction — what a review *does* — deliberately
defined so that it cuts across sentiment and length. The codebook says this explicitly: a six-word
review can be `analysis`, a 2,000-word review can be `impression`, and a 1-star review can be
`analysis`.

What the model actually learned is the **prior**. It predicts `analysis` for every input at
0.37–0.40 confidence, so its decision boundary is not a bad approximation of my definition — it is
the absence of one. The 0.667 accuracy measures the frequency of `analysis` in the test set, not
any property of the text.

**What it overfit to: the class distribution, not the language.** With 65% of training examples
labeled `analysis` and only 36 gradient steps at a learning rate that never finished warming up,
constant output is the cheapest way to reduce loss. The model never had to look at a word. This is
overfitting to a *statistic of the labels* rather than to features of the text, which is why the
usual overfitting symptom — high training accuracy, low test accuracy — would not show up here.

**What it missed: everything the taxonomy is actually about.** The precedence rule, the four
carve-outs, the object-vs-text distinction, the difference between a dimensioned and an
undimensioned comparison — none of it was learned. Two labels were never predicted once.

The instructive part is that **the zero-shot baseline captured most of what I intended** (macro-F1
0.96) from the same definitions written as a prompt. So the gap is not between my definitions and
what is learnable; it is between my definitions and what *this training run* learned. The taxonomy
transfers to a model that reads instructions; it did not survive a fine-tuning run that was
misconfigured and trained on an imbalanced set.

One thing I would flag as a genuine limitation of the definitions rather than the training: the
`analysis`/`impression` boundary rests on judgments a surface model has no access to. Deciding that
"this cover is so frickin beautiful" is not evidence while "the pacing in the middle third drags"
is requires knowing that covers are properties of the object and pacing is a property of the text.
Both are specific; only one is about the book. No amount of additional data makes that a lexical
pattern.

## Spec reflection

**Where the spec helped.** planning.md §3 required stress-testing the label definitions against 10
synthetic boundary cases *before* annotating anything. Three of those probes broke the rules as
originally written, and the fixes became the undimensioned-comparison carve-out, the
`logbook`/`impression` tiebreak, and the edition-vs-text carve-out. Those three rules then did real
work: they are what decides all three of the analyzed errors above, and the tiebreak is recorded in
the annotation notes as the reason for labeling "working on some of them now" as `impression`.
Written after annotation instead of before, those holes would have surfaced as inconsistent labels
scattered through 260 rows and been invisible.

**Where the implementation diverged.** §9 committed to hand-labeling the first 50 examples with no
AI involvement, then pre-labeling the rest in batches of 25 with a recorded override rate. In
practice the `pre_labeled` column reads `yes` for all 260 rows, so there is no unassisted subset and
no per-row record of which model suggestions were overridden. The divergence happened because
pre-labeling the whole pool at once was faster than alternating between modes, and the tracking
column was filled in after the fact rather than during. The cost is specific: §9 argued the
unassisted first 50 existed so my own judgment would be formed before seeing machine suggestions,
and the override rate existed as a check against rubber-stamping. Neither check can now be
evaluated, so the possibility that the labels partly launder an LLM's biases into the ground truth
cannot be ruled out from the data as recorded.

Two smaller divergences: §4 targeted ≥55 examples per label and a 45% ceiling on any single class,
and the actual distribution is 170 / 76 / 14 (65.4% / 29.2% / 5.4%), missing both. And the
`takemeter_baserate_100.csv` sample, which §4 specified for estimating true base rates, is still
unlabeled, so the reported distribution cannot be compared against the natural one.

## AI usage

**1. Writing the zero-shot baseline prompt.** I directed Claude to write the `SYSTEM_PROMPT` for
Section 5 from CODEBOOK.md. It produced a ~3,500-character prompt containing the three definitions,
one example each, the ordered precedence rule, all four carve-outs and the tiebreak. I had asked
only for definitions and examples per the notebook template; it included the precedence rule and
carve-outs as well, on the argument that a prompt missing them would understate the baseline and
make the fine-tuning comparison unfair. I kept that. This prompt produced the 0.9487 baseline.

**2. Debugging the notebook.** Section 5 initially returned 39/39 unparseable responses with no
error output. I directed Claude to debug it. Its first diagnosis — a deprecated model — was wrong
and it said so after I pasted the output, which showed zero API errors and therefore ruled out a
failed call. The actual causes were two: `LABEL_MAP` still held the starter's example labels, so no
response could ever match, and later, reasoning models on Groq exhaust `max_tokens=20` on internal
reasoning and return empty content with no exception. I overrode two of its proposals: a rate-limit
retry change to the baseline loop, and a plan to re-run training locally to generate fresh metrics —
I required the committed `evaluation_results.json` and `confusion_matrix.png` be used instead, so
the reported numbers come from my own run.

**3. Annotation assistance — disclosed.** All 260 rows in `takemeter_annotation.csv` are marked
`pre_labeled = yes`: an LLM proposed a label for every row from the §2 definitions and the §3
precedence rule, and I reviewed each against the full review text. As noted in the spec reflection
above, the override rate §9 committed to reporting was not recorded, so I cannot quantify how often
I disagreed with the suggestions. The 37 rows with `notes` entries are the cases where I recorded
reasoning.

**4. Error and evaluation analysis.** I directed Claude to analyze the misclassifications and draft
the evaluation report from the committed artifacts. It derived the per-class metrics from
`confusion_matrix.png`, identified that 0.667 is exactly 26/39, and traced the collapse to
`warmup_steps=50` exceeding the 36 total training steps. I verified the step arithmetic and the
confusion matrix against the committed files. It also proposed relabeling the Lisbeth review from
`impression` to `analysis`; I have left that label as-is pending review.


