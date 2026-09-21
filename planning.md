# TakeMeter — Planning

**Community:** Goodreads book reviewers
**Task:** 3-way classification of review discourse (`analysis` / `impression` / `logbook`)
**Data source:** UCSD Book Graph `goodreads_reviews_dedup.json` (Wan & McAuley), public research dump

---

## 1. Community

I chose **Goodreads reviewers** — the people who write free-text reviews attached to books on
goodreads.com. It's a community built entirely around one activity: telling other people what you
thought of a book. Every review is a take, and the takes are public, text-only, and attached to a
star rating that lets me sanity-check what I'm reading.

It's a good fit for a classification task because the discourse is *enormously* varied in
substance while being uniform in topic. I read ~38 reviews from the dump before writing any labels,
and the range within that one sample went from an eight-character review (`"I can't."`) to a
9,000-character chapter-by-chapter breakdown of *Brain Rules*. The interesting part is that this
variation is **not** the same thing as agreement or star rating: two 5-star reviews of the same
book can be "Exciting, fun, entertaining! :)" and a 2,500-word argument about post-apocalyptic
fiction as a canvas for humanity. Star ratings already tell you *whether* someone liked a book.
Nothing on Goodreads tells you *whether the review is worth reading*, which is exactly the gap a
classifier could fill.

This distinction matters to people in the community because Goodreads' own review sort is driven by
vote count and recency, so the top of a popular book's review page is dominated by short, punchy,
funny reactions. Readers deciding whether to buy a book, and readers looking for real criticism,
routinely have to scroll past dozens of "loved it!!!" posts to find the one review that actually
describes the book.

## 2. Labels

Three labels. They form a rough substance gradient, but each is defined by **what the text does**,
not by how good I think it is.

### `analysis`
> The review supports its judgment with at least one specific, checkable claim about the book
> itself — its plot, argument, structure, craft, or a named comparison to another work — such that
> someone who hadn't read the book would learn something about its contents from the review.

**Example A** (`9973a654`, 5★):
> "A \*great\* book for anyone who wants to understan mysql better and how to tune it. I
> particularly liked it because it started at the basics with a conceptual overview, then dived
> into details. There are probably even more details it didn't go into, so I'll start looking for
> the next book. But this one was invaluable."

*Why:* the praise is attached to a structural claim about the book (basics → conceptual overview →
details), plus an admission of what it leaves out.

**Example B** (`f73a70f6`, 4★):
> "Enjoyable read! I liked that Connie is not a typical cold-hearted, sexy, perfect, genius, vampire
> hunter. She's like a real person with flaws and weaknesses and fears. I really enjoyed the style
> of writing. I'm not usually a big fan of first person perspective, but I feel the author used a
> great balance of dialogue, descriptive text, and the character's 'voice' really shone through
> without being too colloquial..."

*Why:* specific claims about characterization and narrative perspective, including the reviewer
naming their own prior bias and saying why the book overcame it.

### `impression`
> The review delivers a verdict or an emotional response — how the book made the reader feel, or
> who they'd recommend it to — without giving any book-specific reason for it; strip the star
> rating and you still know how they felt but nothing about the book.

**Example A** (`c52e2317`, 5★):
> "Exciting, fun, entertaining! :)"

**Example B** (`8e1ec346`, 4★):
> "Soooo good and NOT a disappointment from the first book! but it makes u want to read the next one
> SOOOO bad ;) AMAZING :)"

*Why both:* pure affect. The second one refers to a series, which is a fact about the reader's
queue, not a claim about this book's content.

### `logbook`
> The review is primarily a note about the reader's own circumstances — where, when, or how they
> read or acquired the book, who gave or recommended it to them, or what other people say about it
> — rather than about the book's qualities.

**Example A** (`9bfeb32b`, 4★):
> "How I learned Java - my first language after college."

**Example B** (`b4535347`, unrated):
> "6 of my smartest friends rated this 4 or higher. Hmmm..."

*Why both:* Goodreads is a reading tracker as much as a review site, and a large share of reviews
are shelf notes the author wrote for themselves. `logbook` exists because these are not weak
`impression` posts — they aren't evaluating the book at all. Folding them into `impression` would
make that class a grab-bag of "everything short," which is the failure mode the assignment warns
about.

### Mutual exclusivity

The labels overlap in practice (a long review can open with an anecdote and end with criticism), so
they're made exclusive by an explicit **precedence rule** applied in order:

1. Does the text make at least one specific, checkable claim about the book's contents or craft?
   → **`analysis`**, regardless of how much personal material surrounds it.
2. Otherwise, is the text mostly about the reader's circumstances, acquisition, or other people's
   opinions? → **`logbook`**.
3. Otherwise → **`impression`**.

### What does not count as evidence at step 1

These four carve-outs all came out of the stress test in §3, and they exist because each one is a
phrase that *sounds* like a reason without being one:

- **Bare audience tags** — "good for beginners," "great book for some CSS best practices." A
  verdict with a target attached, not a reason.
- **Unsupported craft adjectives** — "beautifully written," "well-paced," "great worldbuilding."
  These name a dimension but assert rather than describe. *"Beautifully written"* is `impression`;
  *"she writes the battle scenes in present tense and the rest in past"* is `analysis`.
- **Undimensioned comparisons** — "better than her last one," "the weakest Sanderson." A comparison
  is evidence only if it names *what* is being compared. "Weaker than *Mistborn*" is a ranking;
  "weaker than *Mistborn* because the magic system's rules are never made explicit" is a claim.
- **Edition and format complaints** — audiobook narrator, cover art, print size, typos. These are
  claims about the object, not the text, so they don't make a review `analysis`. **Exception:**
  translation quality is a claim about the text and does count.

### Tiebreak between `logbook` and `impression`

When a review is half circumstance and half verdict with no book claim — *"Got this from my sister
who said it changed her life. It did not change my life."* — steps 2 and 3 both have a case. The
tiebreak is **the subject of the final evaluative clause**: if the review lands on a judgment of
the book, it's `impression`; if it lands on the reader's own situation, it's `logbook`. The example
above ends on a verdict about the book → `impression`.

## 3. Hard edge cases

**The predictable ambiguity is `logbook` vs. `analysis`** in long reviews, and **`impression` vs.
`analysis`** in recommendation-shaped one-liners. Three real cases from the sample:

**Case 1 — anecdote wrapper around real criticism** (`5347a776`, *Pride and Prejudice*, 5★). Opens
with 100 words about his wife talking him into reading it and him making her read *Dune* in
exchange — textbook `logbook`. Then: *"Austen... has a particular talent for explaining her
characters deep motivations (or prejudices) in a few defining sentences. I think my favorite part
of it is the unwinding of Elizabeths' prejudices against Mr Darcy. It is done so slowly and
artfully and believably..."* → **`analysis`** by rule 1. The social framing is packaging; the
checkable claim about Austen's characterization is the payload.

**Case 2 — personal context plus vague praise** (`99478bd0`, 4★):
> "I read this in Australia, and remember being very inspired by it. Its a great story, and one of
> the first books I ever read that dealt with the spiritual side of things. There seems to be some
> controversy around it now (see amazon reviews) - but I don't know why..."

Could be `analysis` ("dealt with the spiritual side of things" is about content) or `logbook`
(where he read it, what Amazon reviewers say). → **`logbook`**. That clause is a fact about *his
reading history*, not about the book, and the closing move is deferring to other people's opinions.
This is the case that made me write the "checkable claim about the book" wording rather than
"mentions the book's content."

**Case 3 — recommendation with a topic attached** (`3f184341`, 4★): *"Great book for some CSS best
practices."* vs. the MySQL review in §2. Both are short recommendations naming a technical topic.
The CSS one asserts the book is good at a subject; the MySQL one says *how* it's organized. →
**`impression`** and **`analysis`** respectively. This is the boundary I expect the model to get
wrong most often, and the one I'll watch in the confusion matrix.

### Stress test results (run before annotating, per §9)

I wrote 10 synthetic boundary reviews and classified each using only the written rule, to find
places where I'd have to invent a criterion on the spot. Seven resolved cleanly. Three broke the
rule as originally written, and all three fixes are now folded into §2:

| Probe | Problem | Fix |
|---|---|---|
| *"I've read every book Sanderson has written and this is the weakest one."* | Original wording said "a named comparison to another work" counts as a checkable claim → forced `analysis`, but this is a bare ranking with no reasoning. | Added the **undimensioned comparison** carve-out. → `impression` |
| *"Got this from my sister who said it changed her life. It did not change my life."* | Roughly half circumstance, half verdict, no book claim. Steps 2 and 3 of the precedence rule both applied and nothing broke the tie. | Added the **final evaluative clause** tiebreak. → `impression` |
| *"The audiobook narrator's accent was distracting."* | Specific and checkable, so step 1 forced `analysis` — but it's a claim about the recording, not the book. | Added the **edition/format** carve-out, with a translation exception. → `impression` |

One probe was a useful negative result rather than a bug: *"The pacing in the middle third drags"*
is six words and is correctly `analysis`. I checked that no part of the definition smuggles in a
length requirement, since length is exactly the confound §6 is trying to defend against. A very
short `analysis` and a very long `impression` are both legal under these rules, and I want both in
the dataset as adversarial examples.

These 10 synthetic posts are rule tests only. **None of them go into the training CSV.**

**Handling during annotation:** I apply the precedence rule, log the case in the `notes` column of
the CSV with the two candidate labels and my reason, and move on — I don't leave anything unlabeled.
If I accumulate more than ~15 genuinely agonizing cases of the same shape, that's evidence the
boundary is wrong, and I'll revise the definition and re-label the affected examples rather than
keep annotating against a rule I don't believe.

## 4. Data collection plan

**Source.** `goodreads_reviews_dedup.json` from the UCSD Book Graph — a public dump of Goodreads
reviews (16.7 GB, JSON Lines, one review object per line, fields include `review_text`, `rating`,
`n_votes`, `user_id`, `book_id`). No authentication, no private content, no scraping.

**Sampling — the problem I have to design around.** The file is **grouped by user**. I pulled the
first 400 lines into `goodreads_reviews_400.json` and they came from only **14 unique users, with
288 of the 400 from a single account** (which, from the content, appears to be a Goodreads
employee — several reviews discuss making Goodreads better). Training on a contiguous head of this
file would teach the model one person's writing habits, not the community's. So:

- Draw candidates by **reservoir sampling over lines**, not from the head. Specifically *not* by
  seeking to random byte offsets — that oversamples long reviews, and review length correlates with
  the label I'm predicting, so the bias would land straight in the training data.
- **Cap at 3 reviews per `user_id`** so no voice dominates.
- Filter: drop reviews under 20 characters, drop non-English, drop reviews that are only a
  `** spoiler alert **` marker.
- Keep `review_id` in the CSV so every label is traceable back to the source record.

**Volume and target mix.** Collect a pool of ~260 candidates, label 200+ for the final CSV. Target
**≥55 per label** so the smallest class is ~27% — well inside the assignment's 70% ceiling, and I'm
holding myself to a stricter self-imposed cap of **45% for any single class**.

**If a label is underrepresented after 200.** From the sample I read, class correlates with length
(median review is 306 characters; the bottom 30% are under ~100 characters and are almost all
`impression` or `logbook`). So targeted top-ups are easy:

- short on `analysis` → oversample from the long tail (>800 chars);
- short on `logbook` → oversample short reviews containing first-person circumstance markers
  ("gave me," "got this," "read this on/in," "my uncle," "recommended");
- short on `impression` → oversample the 30–150 character band.

I'll do this by drawing a fresh pool with those filters and labeling it under the same rules — **not**
by relabeling examples I've already decided.

**The cost of doing that, stated up front:** stratified top-ups make the training distribution
different from the natural one. To keep evaluation honest, I'll also label a **separate random
sample of 100 reviews** (no stratification) to estimate the true base rates, report those base
rates alongside my training distribution, and note in the writeup that test-set metrics are
measured on the stratified distribution.

**Sample as actually drawn.** One streaming pass over the full dump: **15,739,967 reviews**, from
which 20,000 were reservoir-sampled uniformly (20 seconds). Those 20,000 came from **16,611
distinct users** — roughly one review per user, versus 14 users in the first 400 lines. After
filtering (≥20 chars, ≥90% ASCII, spoiler-marker-only removed) 19,198 survived, and the
≤3-per-user cap barely bound at all. From that pool:

- `takemeter_annotation.csv` — **260 candidates** to label down to the final 200+
- `takemeter_baserate_100.csv` — **100 candidates**, disjoint from the above, for the unstratified
  base-rate estimate

Both are drawn at random with no length or content stratification, so the 260 reflects the natural
distribution *before* any top-ups. Median length in the annotation pool is 360 characters
(range 20–6,644).

**Deliverable.** One CSV in the repo root, columns: `review_id`, `text`, `label`, `notes`,
`pre_labeled`, plus `rating` and `n_votes` carried through as metadata (not model inputs — they're
there so I can check whether my labels are accidentally tracking star rating). One complete labeled
file — the notebook does the 70/15/15 split itself.

## 5. Annotation workflow

**Where the labeling happens.** In a spreadsheet — `takemeter_annotation.csv` opened in Excel,
Numbers, or Google Sheets, typing into the empty `label` column. The file is built to survive that:
whitespace in every review is collapsed to single spaces so no cell contains a newline (embedded
newlines are what silently shift rows out of alignment when a spreadsheet re-saves a CSV), and no
cell begins with `=`, `+`, `-`, or `@`, which Excel would interpret as a formula.

**The rules live in their own file.** `CODEBOOK.md` restates §2 and §3 — definitions, the
precedence rule, the four carve-outs, the tiebreak, and the three hard cases — as a standalone
document. It exists because the second annotator (§7) has to work from the same written rules I do.
If I explain the taxonomy to them verbally, a low agreement score tells me nothing about whether my
taxonomy is sound, only that I explained it badly.

**Order of work.** First 50 by hand with no AI involvement, then LLM pre-labeling in batches of 25
with full review of every row (§9).

**Validation.** `check_labels.py` runs over the labeled CSV before any training. Spreadsheet
labeling introduces a specific failure I can't catch by eye across 260 rows: a handful of cells
reading `Analysis` or `impression ` become distinct classes at train time and quietly shrink the
real ones. The script flags case and whitespace variants, invalid labels, blanks, and duplicate
`review_id`s; reports class counts against the §4 targets; and prints **median length per class**,
which is my early warning for the length confound — if the three medians are widely separated, I
should expect the length-only baseline in §6 to be hard to beat and I want to know that before
training, not after.

## 6. Evaluation metrics

**Why accuracy alone fails here.** Two reasons specific to this task. First, the classes won't be
balanced in the wild, so a model that always says `impression` could post a respectable accuracy
while being useless. Second and more importantly, **length is a massive confound** in this dataset:
`analysis` reviews are systematically longer, so a classifier that has learned nothing but "long =
analysis" would score well on accuracy. Accuracy can't tell me whether I trained a discourse
classifier or a character counter.

What I'll report:

| Metric | Why this one |
|---|---|
| **Macro-F1** (headline) | Weights all three classes equally, so a model that ignores the smallest class is penalized. This is the number I'll quote as *the* result. |
| **Per-class precision & recall** | The errors aren't symmetric. If TakeMeter surfaces substantive reviews, a false `analysis` (junk promoted as insight) costs a user's trust; a missed `analysis` just means one good review stays buried. So `analysis` **precision** is the metric that governs usefulness. |
| **Confusion matrix** | Tests my §3 prediction directly. I expect `analysis`↔`impression` to be the dominant confusion and `logbook` to be mostly separable. If instead `logbook` smears across the other two, the label is unsound and I'll say so. |
| **Length-only baseline** | Logistic regression on character count alone. The fine-tune has to beat it by a clear margin or I haven't demonstrated anything. |
| **Majority-class baseline** | Floor. |
| **Self-agreement (Cohen's κ)** | I re-label 40 examples ≥5 days later, blind to my original labels. This is the human ceiling. If my own κ with myself is ~0.75, a model at 0.80 macro-F1 is at ceiling and I should not chase 0.95. |
| **Bootstrap 95% CI on macro-F1** | At n=200 the test split is ~30 examples. A single example is ~3 points of accuracy. Reporting a point estimate without a CI would be dishonest about the precision of the result. |

## 7. Inter-annotator reliability (stretch goal)

Everything in §6 measures the model against *my* labels. This section asks a prior question: are my
labels reproducible by anyone but me? If they aren't, then a high macro-F1 only proves the model
learned my idiosyncrasies, and the taxonomy — which the assignment calls the hardest part of the
project — hasn't been validated at all.

**Setup.** One other person independently labels **40 reviews** drawn at random from my 260
(`annotator2_40.csv`, labels stripped). 40 rather than the required 30 gives slack if they skip
any. Conditions that make the number meaningful:

- They work only from `CODEBOOK.md`. No verbal coaching, no worked examples beyond the ones in the
  document.
- **No discussion while they label.** If we talk cases through as we go we converge, and the
  agreement score measures our conversation rather than the codebook.
- They label blind — they never see my labels for those 40.
- They fill the `notes` column on hard cases. Their reasoning on a disagreement is worth more than
  the disagreement itself.

**What I'll report.** Simple percentage agreement *and* Cohen's κ, computed by `check_labels.py`.
Both, because with three unbalanced classes raw agreement is inflated by chance — if 45% of the
data is `analysis`, two annotators guessing randomly in proportion would still agree about 35% of
the time. κ corrects for that; percentage agreement is the more intuitive number to quote
alongside it. Plus the full 3×3 confusion matrix between the two of us.

**How I'll read the result.**

| κ | What it means for this project |
|---|---|
| ≥ 0.80 | Taxonomy is reproducible. Model scores are trustworthy. |
| 0.60–0.80 | Substantial — usable. Report it honestly and treat it as the ceiling: a model scoring above my human agreement is fitting noise, not doing better than people. |
| 0.40–0.60 | The definitions are underspecified. I'll identify which boundary is leaking and say so in the writeup rather than papering over it. |
| < 0.40 | The taxonomy failed. That's a legitimate finding and I'd write it up as one — it would mean "substance" in book reviews doesn't decompose the way §2 claims. |

**Disagreement analysis.** `check_labels.py` prints every disagreement with the full review text and
both annotators' notes. I'll classify each one into:

1. **Boundary disagreements** — we applied the same rule and read the evidence differently. These
   are the interesting ones and they should cluster on `analysis`↔`impression`, which is the
   boundary §3 predicts is hardest. If they cluster somewhere I *didn't* predict, my §3 analysis
   was wrong and I'll say so.
2. **Rule-comprehension failures** — one of us missed a carve-out. These are codebook bugs, not
   taxonomy bugs, and the fix is clearer wording.
3. **Attention slips** — someone skimmed a long review. Noise, but worth counting, because a high
   slip rate means my own 260 labels have a similar error rate baked in.

**What I will not do:** reconcile the disagreements and relabel to inflate the score. The
disagreement rate on independent labeling *is* the measurement. I'll fix the codebook for future
work and report the original number.

## 8. Definition of success

Stated so it's objectively checkable on the held-out test split at the end:

**Must hit (the "it works" bar):**
1. **Macro-F1 ≥ 0.75** on the held-out test set.
2. **Beats the length-only baseline by ≥ 10 points** of macro-F1, absolute. This is the one that
   proves the model learned discourse structure rather than review length.
3. **No individual class below 0.60 F1.** A model that nails two classes and can't find the third
   hasn't validated my taxonomy.
4. **`analysis` precision ≥ 0.80.**

**Deployment bar (higher, and for a specific use).** For the realistic application — a "show me the
substantive reviews first" re-ranker on a book page — the governing number is **`analysis` precision
≥ 0.85**, at whatever recall that costs. Readers will forgive a tool that misses some good reviews;
they'll abandon one that promotes "AMAZING :)" as insight. I'd ship at ≥0.85 precision / ≥0.60
recall on `analysis`, and I would *not* ship a model that clears 0.75 macro-F1 by being excellent at
`impression` and mediocre at `analysis`.

**Honest caveats I'm committing to in the writeup.** The ~30-example test split gives a macro-F1
confidence interval of roughly ±0.15, so a 0.78 result is not meaningfully different from 0.72 and I
won't present it as though it is. All labels come from one annotator (me), so the ceiling is my own
consistency, measured in §6 and §7 and reported. And the dataset is a snapshot of one platform's reviewers,
skewed toward English-language and toward books that get reviewed at all.

## 9. AI tool plan

**Label stress-testing — done, results in §3.** Generated 10 synthetic reviews engineered to sit on
the `analysis`/`impression` and `logbook`/`analysis` boundaries, then classified each using only the
written rule. Three broke it; all three produced concrete tightenings to §2 (undimensioned
comparisons, the logbook/impression tiebreak, edition-vs-text claims). This was done **before**
annotating, which is the whole point — those three holes would otherwise have shown up as
inconsistent labels scattered through the 200 and been invisible to me afterward.

**Annotation assistance.** I will pre-label with an LLM, in batches of 25, prompted with the §2
definitions and the §3 precedence rule verbatim, and I'll review and correct every single one by
reading the full review text. Tracking: a `pre_labeled` column in the CSV (`yes`/`no`) plus a
`notes` entry recording every case where I overrode the model. Two guardrails: (a) I'll hand-label
the first 50 myself with no AI involvement, so I've formed my own judgment before seeing any
machine suggestion; (b) I'll report my override rate — if I'm overriding under ~10%, that's a sign
I'm rubber-stamping rather than reviewing, and I'll switch the remainder to blind hand-labeling.
Pre-labeling that I skim is worse than no pre-labeling, because it launders the model's biases into
the ground truth and then measures the model against itself.

**Failure analysis (after training).** I'll export every test-set misprediction with its true label,
predicted label, full text, and character count, and ask an LLM to propose patterns in the errors.
Specifically looking for: (1) is the model just thresholding on length — are the misses
disproportionately long `impression` and short `analysis`? (2) does it key on surface markers like
quotation marks, bullet lists, or named comparisons rather than on whether a claim is actually made?
(3) are errors concentrated in a genre or in one `user_id`'s writing style? Verification: every
pattern the model proposes, I check by hand against the actual examples and against the *correct*
predictions too — a pattern that's equally common in the model's successes explains nothing. Nothing
goes in the writeup unless I've confirmed it in the data myself.

**AI usage disclosure.** All three uses above, the override rate, and the count of pre-labeled rows
go in the AI usage section of the final writeup.

--
