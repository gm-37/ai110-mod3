# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.


Real-world recommendations work through a ranking system: they predict how likely you are to engage with a candidate item based on your previous behavior, then show you the highest-scoring ones according to criteria, like implicit signals (skips, watch time, replays) and explicit ratings on a lower scale. They use collaborative (user-based) and content (match) filtering to narrow billions of items down to a few hundred and rank those precisely. My version of the recommender will prioritize the signals the UserProfile indicates (genre first, then mood and energy-closeness, and then acoustic preference). Songs closer to the target energy will be rewarded and the weights in this order will be prioritized (explainability above all).

Plan:

The score for each song is a weighted sum of six signals/categories. Genre is the strongest, and genre+mood outweighs the other signals (energy-esque)

| Signal | Rule | Points |
| --- | --- | --- |
| Genre | `song.genre` in `favorite_genres` | +2 (flat) |
| Mood | `song.mood` in `favorite_moods` | +1 (flat) |
| Energy | closeness to `target_energy` | up to +1.0 |
| Valence | closeness to `target_valence` | up to +0.5 |
| Danceability | closeness to `target_danceability` | up to +0.5 |
| Acousticness | closeness to `target_acousticness` | up to +0.5 |

Max score ≈ **5.5** (categorical 3.0 + numeric 2.5).

- **Categorical signals (genre, mood)** award full points on a list membership match — no bonus for multiple matches, so a broad-taste profile can't inflate every score.
- **Numeric signals** use a closeness formula: `points = MAX_VALUE * (1 - abs(song.value - target))`. All fields are 0–1. Energy is weighted double the other numeric axes.

Possible bias: this system may over-prioritize genre, so mood will be secondary. Valence may match energy a lot so could affect recommendations being too "mono". Danceability may also be correlated similarly.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Captured from `python -m src.main`. The first three are realistic listeners;
the last three are adversarial profiles designed to stress the scoring logic.

**USER 1 (pop / happy)**
```
1. Sunrise City — Neon Echo
   Score: 5.37
   Why:
     • genre match (pop) +2.0
     • mood match (happy) +1.0
     • energy close to target +0.98
     • valence close to target +0.43
     • danceability close to target +0.45
     • non-acoustic match +0.5

2. Gym Hero — Max Pulse
   Score: 4.25
   Why:
     • genre match (pop) +2.0
     • energy close to target +0.87
     • valence close to target +0.46
     • danceability close to target +0.41
     • non-acoustic match +0.5

3. Rooftop Lights — Indigo Parade
   Score: 3.34
   Why:
     • mood match (happy) +1.0
     • energy close to target +0.96
     • valence close to target +0.44
     • danceability close to target +0.44
     • non-acoustic match +0.5

4. Concrete Verses — MC Grid
   Score: 2.37
   Why:
     • energy close to target +0.98
     • valence close to target +0.46
     • danceability close to target +0.42
     • non-acoustic match +0.5

5. Deep Ascent — Tidal Frame
   Score: 2.34
   Why:
     • energy close to target +0.94
     • valence close to target +0.49
     • danceability close to target +0.40
     • non-acoustic match +0.5
```

**USER 2 (lofi / chill)**
```
1. Midnight Coding — LoRoom
   Score: 5.23
   Why:
     • genre match (lofi) +2.0
     • mood match (chill) +1.0
     • energy close to target +0.92
     • valence close to target +0.47
     • danceability close to target +0.34
     • acoustic match +0.5

2. Library Rain — Paper Lanterns
   Score: 5.16
   Why:
     • genre match (lofi) +2.0
     • mood match (chill) +1.0
     • energy close to target +0.85
     • valence close to target +0.45
     • danceability close to target +0.36
     • acoustic match +0.5

3. Focus Flow — LoRoom
   Score: 4.21
   Why:
     • genre match (lofi) +2.0
     • energy close to target +0.90
     • valence close to target +0.46
     • danceability close to target +0.35
     • acoustic match +0.5

4. Spacewalk Thoughts — Orbit Bloom
   Score: 3.15
   Why:
     • mood match (chill) +1.0
     • energy close to target +0.78
     • valence close to target +0.42
     • danceability close to target +0.45
     • acoustic match +0.5

5. Dusty Backroads — Hollis Grange
   Score: 2.29
   Why:
     • energy close to target +0.99
     • valence close to target +0.46
     • danceability close to target +0.33
     • acoustic match +0.5
```

**USER 3 (rock / intense)**
```
1. Storm Runner — Voltline
   Score: 4.76
   Why:
     • genre match (rock) +2.0
     • mood match (intense) +1.0
     • energy close to target +0.89
     • valence close to target +0.39
     • danceability close to target +0.48

2. Gym Hero — Max Pulse
   Score: 2.75
   Why:
     • mood match (intense) +1.0
     • energy close to target +0.87
     • valence close to target +0.46
     • danceability close to target +0.41

3. Velvet Whispers — Aria Sol
   Score: 2.15
   Why:
     • energy close to target +0.66
     • valence close to target +0.49
     • danceability close to target +0.50
     • acoustic match +0.5

4. Dusty Backroads — Hollis Grange
   Score: 2.12
   Why:
     • energy close to target +0.71
     • valence close to target +0.44
     • danceability close to target +0.47
     • acoustic match +0.5

5. Wildflower Trail — The Hearth
   Score: 2.05
   Why:
     • energy close to target +0.64
     • valence close to target +0.48
     • danceability close to target +0.43
     • acoustic match +0.5
```

**ADVERSARIAL: out-of-range targets** — `target_energy=5.0`, `target_valence=-3.0`.
`score_song` now clamps targets into the 0–1 range, so 5.0 → 1.0 and -3.0 → 0.0.
Scores stay positive and the ranking behaves sanely (favoring high-energy,
low-valence songs) instead of inverting. *(Before the clamp fix, every score
went negative and the ranking flipped into "least-penalized" order.)*
```
1. Sunrise City — Neon Echo
   Score: 4.85
   Why:
     • genre match (pop) +2.0
     • mood match (happy) +1.0
     • energy close to target +0.82
     • valence close to target +0.08
     • danceability close to target +0.45
     • non-acoustic match +0.5

2. Gym Hero — Max Pulse
   Score: 3.96
   Why:
     • genre match (pop) +2.0
     • energy close to target +0.93
     • valence close to target +0.11
     • danceability close to target +0.41
     • non-acoustic match +0.5

3. Rooftop Lights — Indigo Parade
   Score: 2.79
   Why:
     • mood match (happy) +1.0
     • energy close to target +0.76
     • valence close to target +0.09
     • danceability close to target +0.44
     • non-acoustic match +0.5

4. Iron Requiem — Blackforge
   Score: 2.25
   Why:
     • energy close to target +0.97
     • valence close to target +0.36
     • danceability close to target +0.43
     • non-acoustic match +0.5

5. Storm Runner — Voltline
   Score: 2.15
   Why:
     • energy close to target +0.91
     • valence close to target +0.26
     • danceability close to target +0.48
     • non-acoustic match +0.5
```

**ADVERSARIAL: contradiction** — asks for angry metal categorically, but the
numeric targets describe a calm/happy/danceable song. The flat +2/+1 bonuses win:
`Iron Requiem` tops the list despite failing every numeric target.
```
1. Iron Requiem — Blackforge
   Score: 4.14
   Why:
     • genre match (metal) +2.0
     • mood match (angry) +1.0
     • energy close to target +0.13
     • valence close to target +0.19
     • danceability close to target +0.33
     • non-acoustic match +0.5

2. Island Time — Sunny Roots
   Score: 1.94
   Why:
     • energy close to target +0.55
     • valence close to target +0.46
     • danceability close to target +0.43
     • non-acoustic match +0.5

3. Rooftop Lights — Indigo Parade
   Score: 1.75
   Why:
     • energy close to target +0.34
     • valence close to target +0.46
     • danceability close to target +0.46
     • non-acoustic match +0.5

4. Sunrise City — Neon Echo
   Score: 1.70
   Why:
     • energy close to target +0.28
     • valence close to target +0.47
     • danceability close to target +0.45
     • non-acoustic match +0.5

5. Concrete Verses — MC Grid
   Score: 1.65
   Why:
     • energy close to target +0.32
     • valence close to target +0.36
     • danceability close to target +0.47
     • non-acoustic match +0.5
```

**ADVERSARIAL: likes everything** — every genre and mood is a favorite, so the
categorical bonus stops discriminating and the top 5 collapse into a ~0.1-point
band decided only by closeness to the 0.5 numeric targets.
```
1. Dusty Backroads — Hollis Grange
   Score: 5.38
   Why:
     • genre match (country) +2.0
     • mood match (nostalgic) +1.0
     • energy close to target +0.99
     • valence close to target +0.46
     • danceability close to target +0.43
     • acoustic match +0.5

2. Midnight Coding — LoRoom
   Score: 5.33
   Why:
     • genre match (lofi) +2.0
     • mood match (chill) +1.0
     • energy close to target +0.92
     • valence close to target +0.47
     • danceability close to target +0.44
     • acoustic match +0.5

3. Focus Flow — LoRoom
   Score: 5.30
   Why:
     • genre match (lofi) +2.0
     • mood match (focused) +1.0
     • energy close to target +0.90
     • valence close to target +0.46
     • danceability close to target +0.45
     • acoustic match +0.5

4. Wildflower Trail — The Hearth
   Score: 5.29
   Why:
     • genre match (folk) +2.0
     • mood match (hopeful) +1.0
     • energy close to target +0.94
     • valence close to target +0.38
     • danceability close to target +0.47
     • acoustic match +0.5

5. Velvet Whispers — Aria Sol
   Score: 5.27
   Why:
     • genre match (r&b) +2.0
     • mood match (romantic) +1.0
     • energy close to target +0.96
     • valence close to target +0.41
     • danceability close to target +0.40
     • acoustic match +0.5
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



