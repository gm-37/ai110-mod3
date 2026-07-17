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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



