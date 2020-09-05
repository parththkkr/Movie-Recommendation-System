from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def movie(request):

  return render(request, "index.html")

def recommendation(request):

  movie_user_likes = request.GET.get('movie_user_likes','')
  no_of_movie =request.GET.get('no_of_movie','')
  if no_of_movie=='':
    no_of_movie=10


  #no_of_movie=print(int(str(no_of_movie)))
  movies=[]
  ###### helper functions. Use them when needed #######
  def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

  def get_index_from_title(title):
    return df[df.title == title]['index'].values[0]

  ##Step 1: Read CSV File
  df = pd.read_csv('movie_dataset.csv')
  # df.head()
  #print(df.columns)
  ##Step 2: Select Features

  fetures = ['keywords', 'cast', 'genres', 'director']
  df[fetures] = df[fetures].fillna('')

  ##Step 3: Create a column in DF which combines all selected features
  def combine_fetures(row):
    try:
      return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']
    except:
      print("error", row)

  df['combine_fetures'] = combine_fetures(df)
 # print(df['combine_fetures'].head())

  ##Step 4: Create count matrix from this new combined column
  cv = CountVectorizer()
  count_matrix = cv.fit_transform(df['combine_fetures'])

  ##Step 5: Compute the Cosine Similarity based on the count_matrix
  cosine_sim = cosine_similarity(count_matrix)
  #movie_user_likes = 'Avatar'
  #print(cosine_sim)

  ## Step 6: Get index of this movie from its title
  try:
    movie_index = get_index_from_title(movie_user_likes.capitalize())
  except:

    contex = {'movie_user_likes': movie_user_likes}
    return render(request, "error.html",contex)
  # print(movie_index)
  similar_movies = list(enumerate(cosine_sim[movie_index]))
  # print(similar_movies)

  ## Step 7: Get a list of similar movies in descending order of similarity score
  sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

  ## Step 8: Print titles of first 50 movies
  i = 0


  for movie in sorted_similar_movies:
    if(i==0):
      i+=1
    else:
        movies.append(get_title_from_index(movie[0]))
        #movies+=","
        if i >= int(no_of_movie):
          print(type(i))
          print(type(no_of_movie))
          break
        i += 1
        #print("movies=="+movies+"==")



  print(movies)
  contex = {'movies': movies,'movie_user_likes':movie_user_likes}
  return render(request, "recommender.html",contex)