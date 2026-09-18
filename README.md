# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

The Unofficial Guide is a retrieval-based question-answering system built using
the `campus_life` corpus. It searches short student posts about topics such as
courses, housing, dining, campus services, and administrative policies. When a
user asks a question, the system retrieves relevant chunks from the corpus and
uses them to generate an answer grounded in those documents. It also names its
sources and refuses to answer when the retrieved information is not relevant
enough.

## Chunking Strategy

**Chunk size:** 400 characters  
**Overlap:** 0 characters

I chose a paragraph-based chunking strategy because the `campus_life` corpus
contains short posts where useful information is usually contained in a sentence
or short paragraph. The starter used 800-character windows with 120 characters
of overlap, which produced 88 chunks from 88 documents and therefore did not
split most posts at all.

My `split_documents` function groups complete neighboring paragraphs while they
fit within 400 characters. I used no overlap because the chunks are divided at
paragraph boundaries instead of arbitrary character positions. With this
strategy, the corpus produced 100 chunks averaging 278 characters, compared
with the starter's 88 chunks averaging 317 characters.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_210.txt#0` — produced by: `chunker.py::split_documents`

```
CS 210 Data Structures

I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Expect 8 to 10 hours a week outside class.
```

**Chunk 3** — source: `course_math_220_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for MATH 220 Linear Algebra

People keep asking so: 6 to 8 hours a week, almost all of it on problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#1` — produced by: `chunker.py::split_documents`

```
Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** What are the walk-in hours at the health centre?

**Answer:**

```
The walk-in hours at the health centre are 8am to 11am (health_center.txt).

Sources retrieved: dining_the_atrium.txt, dining_the_ridgeway_cafe_followup.txt, health_center.txt, transit_shuttle.txt, transit_walking.txt
```

**My relevance cutoff:** 0.6

I kept the relevance cutoff at 0.6 after comparing the best retrieval distances
for five questions covered by the corpus with five questions outside the corpus.
The in-corpus questions ranged from 0.1680 to 0.3632, while the out-of-scope
questions ranged from 0.8246 to 0.9340. This left a large gap between the two
groups, and 0.6 falls comfortably inside that gap.

| Question | In corpus? | Best distance |
|---|---|---:|
| Is the housing lottery completely random? | Yes | 0.2514 |
| What material are the CS 210 exams based on? | Yes | 0.3002 |
| How long are wait times at Kestrel Commons during lunch? | Yes | 0.1680 |
| Does Innisfree Hall have air conditioning? | Yes | 0.3632 |
| What are the walk-in hours at the health centre? | Yes | 0.2156 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8907 |

## How I Used AI

**1.** I used ChatGPT to help me design a chunking strategy after examining the
short documents in the `campus_life` corpus. It suggested grouping complete
paragraphs up to a character limit instead of using the starter's fixed
character windows. I used that approach with a 400-character limit and no
overlap, then indexed the corpus and inspected the resulting chunks to make
sure they contained complete thoughts.

**2.** I used ChatGPT to help interpret the retrieval distances from my five
in-corpus questions and five out-of-scope questions. We compared the two
groups and found that the in-corpus distances ranged from 0.1680 to 0.3632,
while the out-of-scope distances ranged from 0.8246 to 0.9340. Based on that
comparison, I kept the 0.6 relevance cutoff because it falls clearly between
the two groups.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks contain complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected information | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Evidence from the before run

**Criterion 1 — Retrieved chunks contain the answer**

For the health centre question, the top retrieved chunk was from `health_center.txt` and contained:

> Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out.

Produced by `store.py::search`, using chunks from `chunker.py::split_documents`.

**Criterion 2 — Every answer names a source**

One generated answer was:

> The walk-in hours at the health centre are 8am to 11am (health_center.txt).

Produced by `generate.py::answer_from_chunks`.

**Criterion 3 — Gate stops out-of-corpus questions**

`run_eval.py::check_out_of_scope` tested all five out-of-corpus questions. The gate refused 5 of 5. Best distances ranged from 0.825 to 0.934 against the 0.6 cutoff.

**Criterion 4 — Chunks contain complete thoughts**

One sampled chunk from `course_cs_210_exams.txt` was:

> CS 210 Data Structures — assessment
>
> Two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.
>
> Do the labs even though they're only 10% — the exams reuse the lab problems.

Produced by `chunker.py::split_documents`. All five sampled answer-bearing chunks began and ended on complete thoughts.

**Criterion 5 — Answers contain the expected information**

For Innisfree Hall, the expected phrase was `no air conditioning`, but all three generated answers used equivalent wording instead:

> No, Innisfree Hall does not have air conditioning.
>
> Source: housing_innisfree_hall.txt

The substring scorer therefore marked this question as a failure on all three runs. The other four questions passed, producing 4/5 on each run.

Full before-run evidence is in `results/run_2026-09-18_0950_before.md`.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| Criterion | Verdict | How I decided |
|---|---|---|
| 1 | MET | All five test questions retrieved at least one chunk containing the answer, exceeding my 4 of 5 target. |
| 2 | MET | All five generated answers named at least one source document in all three runs. |
| 3 | MET | The relevance gate refused all 5 out-of-corpus questions, exceeding my 4 of 5 target. |
| 4 | MET | All five sampled answer-bearing chunks contained complete thoughts without cutting a sentence in half at either boundary. |
| 5 | MET | The scorer produced 4/5 in all three runs, which met my target of at least 4 of 5. The Innisfree answer was semantically correct but did not contain the literal `expects` phrase. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I did not miss any of my five acceptance criteria, so there was no missed criterion to trace to a pipeline stage.

The result that surprised me most was Criterion 5. The Innisfree Hall answer was correct in all three runs, but the scorer marked it as a failure because `questions.py` expected the literal phrase `no air conditioning` while the model answered `does not have air conditioning`. This showed a limitation of exact substring scoring even though the overall criterion still met its 4 of 5 target.

Because every criterion passed, I considered whether any of my original targets were set too low. Criterion 5 is the one I would tighten in a future evaluation, from 4 of 5 to 5 of 5. I would also change how I measure it so equivalent correct wording can count instead of relying only on a literal substring.

## The Improvement

**What I changed:**

I reduced `TOP_K` in `config.py` from 5 to 3, so the system retrieves three chunks per question instead of five.

**Why I picked it:**

All five acceptance criteria passed in the before run, so there was no failed criterion to repair. However, inspecting the retrieval results showed that the system often returned extra unrelated chunks along with the answer-bearing chunk. Before making the change, I tested retrieval with `top-k 3` and found that an answer-bearing chunk was still retrieved for all five test questions. I therefore reduced `TOP_K` to test whether the system could preserve its results while sending less unnecessary context to the model.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->


### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks contain complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected information | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

### Before and after

Reducing `TOP_K` from 5 to 3 preserved the verdict on all five acceptance criteria. Criterion 5 remained at 4/5 in each run because the Innisfree Hall answers again used `does not have air conditioning` instead of the literal `expects` phrase `no air conditioning`.

The change did reduce the amount of context sent to the model. The before evaluation used 9,096 input tokens and 9,761 total tokens. The after evaluation used 6,180 input tokens and 6,853 total tokens. That is a reduction of 2,916 input tokens, or about 32.1%, while preserving the same acceptance-criterion results.

Full after-run evidence is in `results/run_2026-09-18_1006_after.md`.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

No acceptance criterion was still missed after the improvement.

There are still limitations that the current criteria do not fully capture. Retrieval still includes some unrelated chunks even with `TOP_K = 3`; for example, the health centre question also retrieved a transit document and a dining document. Criterion 1 only checks whether an answer-bearing chunk is present, not how much irrelevant context is retrieved.

The other limitation is the literal substring scorer. The Innisfree Hall answer was correct in all three before and after runs, but it failed the automated check because `does not have air conditioning` does not literally contain `no air conditioning`. I stopped after the single `TOP_K` change because the assignment calls for one system improvement, and changing the scorer would be a separate evaluation change rather than the system change being measured.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I would write Criterion 5 differently. Requiring the literal `expects` phrase made the measurement repeatable, but the Innisfree Hall result showed that it can mark a semantically correct answer as wrong simply because the model uses different wording.

Knowing that now, I would define correctness around the expected fact rather than one exact phrase and specify a repeatable way to judge equivalent wording. I would also consider adding a retrieval-precision criterion, because the current retrieval criterion only checks whether the answer is somewhere in the retrieved chunks and does not penalize unnecessary unrelated context.
