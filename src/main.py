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

    recommendations = recommend_songs(user_prefs1, songs, k=5)

    print()
    print("=" * 44)
    print("  TOP RECOMMENDATIONS FOR YOU")
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
