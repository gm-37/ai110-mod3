"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs1 = {
        "favorite_genres": ["pop"],
        "favorite_moods": ["happy"],
        "target_energy": 0.8,
        "target_valence": 0.7,
        "target_danceability": 0.7,
        "likes_acoustic": False,
    }

    user_prefs2 = {
        "favorite_genres": ["lofi"],
        "favorite_moods": ["chill"],
        "target_energy": 0.5,
        "target_valence": 0.5,
        "target_danceability": 0.3,
        "likes_acoustic": True,
    }

    user_prefs3 = {
        "favorite_genres": ["rock"],
        "favorite_moods": ["intense"],
        "target_energy": 0.8,
        "target_valence": 0.7,
        "target_danceability": 0.7,
        "likes_acoustic": True,
    }

    # ------------------------------------------------------------------
    # Adversarial / edge-case profiles for evaluating the scoring logic.
    # These are designed to "trick" score_song or surface unexpected
    # ranking behavior, not to represent realistic listeners.
    # ------------------------------------------------------------------

    # Out-of-range numeric targets (scale is meant to be 0-1). score_song now
    # clamps targets into [0, 1], so 5.0 -> 1.0 and -3.0 -> 0.0 and scores stay
    # positive with a sane ranking. (Before that fix, the formula
    # points = max_points * (1 - abs(song[field] - target)) drove every score
    # negative and inverted the ranking into "least-penalized" order.)
    adversarial_out_of_range = {
        "favorite_genres": ["pop"],
        "favorite_moods": ["happy"],
        "target_energy": 5.0,
        "target_valence": -3.0,
        "target_danceability": 0.7,
        "likes_acoustic": False,
    }

    # Direct contradiction: asks for angry metal categorically, but the
    # numeric targets describe a calm, happy, danceable song. Tests whether
    # the flat +2 genre / +1 mood bonuses override the numeric "fit".
    adversarial_contradiction = {
        "favorite_genres": ["metal"],
        "favorite_moods": ["angry"],
        "target_energy": 0.1,
        "target_valence": 0.9,
        "target_danceability": 0.9,
        "likes_acoustic": False,
    }

    # "Likes everything": every genre and mood is a favorite, so the
    # categorical bonus stops discriminating and scores collapse into a
    # narrow band decided only by closeness to the 0.5 numeric targets.
    adversarial_everything = {
        "favorite_genres": [
            "pop", "lofi", "rock", "ambient", "jazz", "synthwave", "indie pop",
            "hip hop", "classical", "reggae", "country", "edm", "r&b", "metal",
            "folk", "house",
        ],
        "favorite_moods": [
            "happy", "chill", "intense", "relaxed", "focused", "moody",
            "confident", "melancholy", "energetic", "angry", "nostalgic",
            "euphoric", "romantic", "hopeful",
        ],
        "target_energy": 0.5,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "likes_acoustic": True,
    }

    # Each entry is (label, profile). Add or remove profiles here to
    # change what gets printed.
    profiles = [
        ("USER 1 (pop / happy)", user_prefs1),
        ("USER 2 (lofi / chill)", user_prefs2),
        ("USER 3 (rock / intense)", user_prefs3),
        ("ADVERSARIAL: out-of-range targets", adversarial_out_of_range),
        ("ADVERSARIAL: contradiction", adversarial_contradiction),
        ("ADVERSARIAL: likes everything", adversarial_everything),
    ]

    for label, prefs in profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        print()
        print("=" * 44)
        print(f"  TOP RECOMMENDATIONS — {label}")
        print("=" * 44)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} — {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Why:")
            for reason in explanation.split(", "):
                print(f"     • {reason}")

    print()


if __name__ == "__main__":
    main()
