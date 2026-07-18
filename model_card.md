# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**Name: MagicalVibes 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender is designed to take a user profile with preferences inputted like favorite genres, moods, target energy, valence (emotional positivity), danceability, and whether or not they like acoustic. It assumes the user will know their preferences for each of these and that genre is most important when scoring each song before recommending the top 5 songs that "match" their preferences. This is right now in the exploration stage and can be adjusted after more data collection for real users, as the song collection is limited currently.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Genre, mood, energy, valence, danceability, and acousticness of each song are used and compared to the same of the user's profile. Genre matches are awarded +2, mood +1, and the other values are on a numeric scale measured by "closeness" to the target value, using the formula: max_points * (1 - abs(song[field] - target)), and extraneous values are clamped to the range 0.0-1.0. This is different from the starter logic in that it accounts for out-of-range markers and takes more into account than just energy, mood, and genre.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

There are 20 songs in the catalog from genres like pop, lofi, rock, ambient, jazz, synthwave, indie, hop hop, reggae, classical, country, edm, r&b, metal, folk, house, and blues. Moods include happy, chill, intense, relaxed, moody, focused, nostalgic, energetic, romantic, angry, hopeful, somber, and more. 10 new songs were added to the original data for a total of 20 songs, but there are definitely more songs needed as each genre/mood has like 1 song with the exception of pop/happy songs which have more.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

For typical users with simpler profiles like happy pop, chill lofi, intense rock, etc, the results are better and more reasonable, capturing similar patterns in energy, mood, genre, danceability, and valence. In these cases, the recommendations definitely matches my intuition and the scores were higher, especially for happy pop. Some were less because of a lack of data but otherwise okay.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Happy/pop is more represented in the data set, so the recommender is more likely toreccomend those types of songs to matching users while users who like sadder music are left behind. Further, acousticness is currently like a binary cliff: anything less that 0.5 acoustic is recommended to users with no acoustic taste and anything above is for users that like acoustin. 0.49 acousticness vs 0.51 acousticness are treated oppositely. Lastly, genre and mood are weighed more than the numeric preferences, but when genre and mood conflict genre will always take preference which is fine for some cases but won't be as good if the numerics are lower 50 and mood is sad but genre is pop.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested classic user profiles like happy pop, chill lofi, intense rock, and then edge cases like a user who likes everything (all genres & moods), a user that uses numeric values out of range, and a user who has condradictory moods, genres, and numeric values. I used general music resoning to check if the recommendations had higher scores (>3) which means they matches the user's taste for the regular profiles. For the edge cases i checked if there were a variety of songs in the recommendations. What surprised me was how low some of the top 5 recommendations scored, which led me to compare genre vs mood weighing in comparison to numerics, and it turned out genre weighed the most followed by energy numbers.

Happy pop is associated with higher energy songs, while chill lofi is less danceable/lower energy. Angry rock has more energy too. Sadder and chiller songs have similar energy and danceability levels compared to rock or pop or more happy songs with intense emotion.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

More song data would definitely improve the recommender, like at least 100-200 songs. There could be more sentence recommendations instead of smaller bullets with random numbers, but the more song data would improve diversity as well. As for more complex user tastes, sometimes more factors will need to be taken into account and weighted differently, like maybe in that case value the numerics higher than the lists of genre/mood. And maybe a way to get feedback from the user to better tailor recommendations in the future.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned a lot about how streaming services gather data for better user recommendations through many different methods, and how negative reactions are weighted more than positive ones. I also realized how it's really hard to predict what the user willlike since most are complex in their tastes which is a human quality, so I have more respect for when the recommenders actually get it right (especially for me, since my taste can be broad and picky at the same time). I never realized it was simply algorithms running in the background, so that's pretty cool.

I used Claude to help me figure out how to improve my scoring algorithm for the recommender, which was pretty helpful. Howver, it wanted to include a lot of data from the user profile which got a little cluttered for me so I veto'd that.

If I extended the project, I would definitely add a larger song collection and maybe implement a way for the user to include what they don't like, either from previous experience or based on the recommendations so the system can improve to be more accurate.
