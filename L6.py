import pandas as pd, random

df = pd.read_csv('imdb_top_1000.csv')[['Series_Title', 'Genre', 'IMDB_Rating', 'Overview']]

print('Welcome to the IM|Db Movie recommender')
name = input('whats your name?')
print(f'Hi {name}! Let us find something for you, {name}.\n')

mood_map = {'happy': 'comedy', 'sad': 'drama', 'excited': 'action', 'scared': 'horror'}
mood = input('how are you feeling to day?(happy/sad/excited/scared or skip): ')
genre = mood_map.get(mood, input('enter a genre you like: ').strip())#

try:
    rating = float(input('minimum imdb rating (0-10, or enter for any): ')or 0)
except ValueError:
    rating = 0

recs = df[df['Genre'].str.contains(genre, case=False, na=False) & (df['IMDB_Rating'] >= rating)]
if recs.empty:
    print('no movie found.try another genre or lower rating')
else:
    print(f'\nTop picks for {genre.title()} movies:')
    for _, m in recs.sample(min(5, len(recs))).iterrows():
        print(f'{m['Series_Title']} ({m['IMDB_Rating']})\n  {m['Overview'][:80]}...')

print(f'\n enjoy your movie night {name}')