import sys, imdb

ia = imdb.IMDb()
movie_container = {}
movie_dic = {}

def movie_name(i):
    if not i:
        print("Il file è vuoto")
    else:
        try:
            movies = ia.search_movie(i)
            movie = movies[0]
            title = movie.get('title')
            imdbURL = ia.get_imdbURL(movie)
            movie_id = movie.movieID
            movie_year = movie['year']
            movie_identifier = ia.get_movie(movie_id)
            plot = movie_identifier.get('plot', [''])[0]
            plot = plot.split('::')[0]
            director_box = search_director(movie_identifier)
            actor_box = search_cast(movie_identifier)

        except imdb.IMDbError as e:
            print("Probably you're not connected to Internet.  Complete error report:")
            print(e)
            sys.exit(3)

        if not movie:
            print('It seems that there\'s no movie with movie_id "%s"' % title)
            sys.exit(4)

        movie_container = {'Title': title, 'Url': imdbURL, 'Id': movie_id, 'Year': movie_year, 'Plot': plot,
                           'DirectorBox': director_box, 'ActorBox': actor_box}

        return movie_container

def search_director(movie_identifier):
    directors = movie_identifier['director']
    movie_dic['Director'] = []
    for dir in directors:
        director_name = dir['name']
        director_id = dir.personID
        movie_dic['Director'].append({'Name': director_name, 'Id': director_id})
    return movie_dic['Director']


def search_cast(movie_identifier):
    actors = movie_identifier['cast']
    movie_dic['Actor'] = []
    for actor in actors:
        actor_name = actor['name']
        actor_id = actor.personID
        movie_dic['Actor'].append({'Name': actor_name, 'Id': actor_id})
    return movie_dic['Actor']
