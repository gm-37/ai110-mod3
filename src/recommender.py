from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genres: List[str]
    favorite_moods: List[str]
    target_energy: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    
    print(f"Loading songs from {csv_path}...")
    
    # Columns that must be numeric so we can do math with them later.
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    print(f"Loaded {len(songs)} songs from {csv_path}.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the recipe in README.md.
    Returns (score, reasons), where reasons explains what earned points.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Categorical signals: full points if the song is in the favorites list.
    # No bonus for extra matches, so broad taste can't inflate every score.
    if song["genre"] in user_prefs.get("favorite_genres", []):
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if song["mood"] in user_prefs.get("favorite_moods", []):
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    # Numeric signals: the closer to the target, the more points.
    # points = max_points * (1 - distance), all values are on a 0-1 scale.
    numeric_signals = [
        ("energy", "target_energy", 1.0),
        ("valence", "target_valence", 0.5),
        ("danceability", "target_danceability", 0.5),
    ]
    for field, pref_key, max_points in numeric_signals:
        target = user_prefs.get(pref_key)
        if target is None:
            continue
        # All values live on a 0-1 scale. Clamp the target into range so an
        # out-of-range preference (e.g. 5.0 or -3.0) can't drive points
        # negative and invert the ranking.
        target = min(1.0, max(0.0, target))
        points = max_points * (1 - abs(song[field] - target))
        score += points
        reasons.append(f"{field} close to target +{points:.2f}")

    # Acoustic preference: a song is "acoustic" if more than 50% acoustic.
    # Award points when that matches what the user likes (or doesn't like).
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        song_is_acoustic = song["acousticness"] > 0.5
        if song_is_acoustic == likes_acoustic:
            score += 0.5
            label = "acoustic" if likes_acoustic else "non-acoustic"
            reasons.append(f"{label} match +0.5")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores every song, then returns the top k as (song, score, explanation),
    sorted from highest score to lowest.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))

    # `scored` is a fresh local list we own, so .sort() in place is fine here
    # (the caller's `songs` list is never touched).
    # key picks the score (index 1) to rank by; reverse=True is highest-first.
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
