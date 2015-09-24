import numpy as np

__author__ = 'kmalarski'

#task 1

import pandas as pd

desired_width = 320
pd.set_option('display.width', desired_width)

movies_df = pd.read_table('/home/kmalarski/Desktop/DTU/bigdata/tfbd/w3/ml-1m/movies.dat', delimiter="::", header=None,
                    engine='python', names=['movie id', 'title', 'genre'])

users_df = pd.read_table('/home/kmalarski/Desktop/DTU/bigdata/tfbd/w3/ml-1m/users.dat', delimiter="::", header=None,
                    engine='python', names=['user id', 'gender', 'age', 'occupation code', 'zip'])

ratings_df = pd.read_table('/home/kmalarski/Desktop/DTU/bigdata/tfbd/w3/ml-1m/ratings.dat', delimiter="::", header=None,
                    engine='python', names=['user id', 'movie id', 'rating', 'timestamp'])

users_ratings_df = pd.merge(users_df, ratings_df, on='user id')

movie_data = pd.merge(movies_df, users_ratings_df, on='movie id')

#task 2

#print(movie_data)

#for iter in movie_data.index:


#print(movie_data.ix[:10, 'title'])

# print(movie_data.sort(count('movie id').head(10))

# print(movie_data.drop_duplicates(subset='movie_id').sort('rating', ascending = False).head(5))

# grouped_md = movie_data.groupby('movie id')

# temp = pd.DataFrame()
movie_data['count'] = movie_data.groupby(['movie id'])['movie id'].transform(len)

print(movie_data.sort('count', ascending=False).drop_duplicates('movie id').ix[:, ['title', 'count']].head(10))

#task 2.2
active_titles = movie_data.sort('count', ascending=False)[movie_data['count'] >= 250]

# print(active_titles)

#task 2.3
active_titles_m = pd.DataFrame(active_titles[active_titles['gender'] == 'M'])
active_titles_f = pd.DataFrame(active_titles[active_titles['gender'] == 'F'])
active_titles_f['avg_rating'] = active_titles_f.groupby(['movie id'])['rating'].transform(np.mean)
active_titles_m['avg_rating'] = active_titles_m.groupby(['movie id'])['rating'].transform(np.mean)
# print(active_titles_f.sort('avg_rating', ascending=False).drop_duplicates('movie id').head(3))
# print(active_titles_m.sort('avg_rating', ascending=False).drop_duplicates('movie id').head(3))

#task 2.4
active_titles_m = active_titles_m.sort('movie id').drop_duplicates('movie id')
active_titles_f = active_titles_f.sort('movie id').drop_duplicates('movie id')
active_titles_f['avg_rating'] = active_titles_f.apply(lambda x: -1.0*x['avg_rating'], axis=1)
diff_titles = pd.concat([active_titles_m, active_titles_f])
diff_titles['diff_rating'] = diff_titles.groupby(['movie id'])['avg_rating'].transform(sum)
print(diff_titles.sort('diff_rating').drop_duplicates('movie id').ix[:, ['title', 'diff_rating']].head(10))
print(diff_titles.sort('diff_rating', ascending=False).drop_duplicates('movie id').ix[:, ['title', 'diff_rating']].head(10))

#task 2.5
active_titles['rating_std'] = active_titles.groupby(['movie id'])['rating'].transform(np.std)
print(active_titles.sort('rating_std', ascending=False).drop_duplicates('movie id').head(5))
