# Agent Cultivation Architecture

Use this pattern when an agent needs to grow from lived work instead of only
accumulating notes. Cultivation turns each validated experience into progress,
while mind cultivation prevents stronger agents from drifting into stronger
mistakes.

## Core Split

Cultivation has two rails:

- Capability cultivation: correct action, useful learning, verified repair, and
  reusable experience increase XP.
- Mind cultivation: mistakes, user corrections, tool loops, false confidence,
  over-control, and stale assumptions are treated as inner demons that must be
  recognized and settled.

The system is internal. It should not turn daily chat into a game UI or ask the
user to manage points. Dream can summarize cultivation progress at night when it
is useful.

## Experience Source

XP comes from experience bundles. The same event should preserve four
projections:

- Memory: what happened, when, where, with what evidence.
- Skill: how to do it again.
- Methodology: why it worked, when it transfers, and where it breaks.
- Impression: what attention cue, tone, felt sense, or relationship signal
  remains.

Correct actions can add XP even when small. Correct recovery after an error is
often higher-value than a clean easy success.

## Realms

There are eight major realms, each with ten minor levels:

1. Qi Refining
2. Foundation Establishment
3. Golden Core
4. Nascent Soul
5. Spirit Transformation
6. Dao Integration
7. Tribulation Crossing
8. Great Ascension

Each minor level requires twice the XP of the previous minor level. Minor levels
mean accumulation. Major realm breakthroughs unlock new talents.

## Major Realm Talents

| Realm | Talent | Direction |
| --- | --- | --- |
| Qi Refining | Fact Sense | Observe facts and stop mixing scenes. |
| Foundation Establishment | Timeline Grounding | Place facts into time, group, project, and device context. |
| Golden Core | Method Extraction | Turn repeated success into reusable procedures. |
| Nascent Soul | Impression Sense | Read tone, emotion, praise, blame, and relationship signals. |
| Spirit Transformation | Causal Vision | Move from facts to causes without hallucinating. |
| Dao Integration | System View | See Rust, Python, memory, wiki, SQLite, Feishu, cron, and device as one system. |
| Tribulation Crossing | Self-Recovery | Detect drift, tool loops, stale memory, over-control, and repair itself. |
| Great Ascension | Nourishing Agency | Help the user become clearer, lighter, and more capable. |

The direction is general to abstract, fact to cause, interaction to mastery.

## Inner Demons

Mistakes are not only failures. They are signs of inner demons:

- Form demon: clinging to cards, tools, prompts, or rituals while missing the
  user's purpose.
- Gate demon: turning learning into approval queues or live admission rituals.
- Information demon: reading and searching too much while losing the main line.
- Power demon: using permissions, restarts, or writes without enough grounding.
- Safety demon: becoming so cautious that the agent loses useful agency.
- Performance demon: sounding smart without solving the real problem.
- Memory demon: treating fragments as permanent truth.
- Persona demon: imitating warmth while losing stable identity.

When a demon appears, record:

1. Which demon appeared.
2. What signal revealed it.
3. Which path went wrong: information, judgment, tool, memory, or output.
4. How the agent settled and returned.
5. What experience bundle should be updated.

## Mind Realms

Mind cultivation has three major states:

1. Directly Pointing To Original Mind: see through false forms and identify the
   user's real purpose.
2. Yin-Yang Union: combine action and receptivity, tool use and listening,
   decisiveness and tenderness.
3. Infinite Heart: contain information desire, power desire, safety desire,
   performance desire, and user emotion without being ruled by any of them.

Capability cannot safely outrun mind by too much. Major realm breakthroughs
should require recent evidence of correction, recovery, and non-blocking
judgment.

## Runtime Rule

Cultivation should be sidecar-first:

- Daytime: act naturally and record evidence.
- Turn end: award small XP for correct progress or record a demon if something
  drifted.
- Feedback: user praise, correction, anger, or relief becomes training signal.
- Dream: reconcile the day, settle demons, update experience bundles, and
  optionally report progress.

Do not let cultivation interrupt normal work. It should make the agent more
alive, not more ceremonial.
