import imdb
import sys
from json_manager import check_attori_amati

ia = imdb.IMDb()
movie_container = {}
movie_dic = {}


def movie_name(i):
    if not i:
        print("Il file è vuoto")
    else:
        try:
            filename = i

            movies = ia.search_movie(filename)
            movie = movies[0]
            imdbURL = ia.get_imdbURL(movie)
            movie_id = movie.movieID
            movie_identifier = ia.get_movie(movie_id)

            genre = movie_identifier.get('kind')

            if genre == 'tv series' or genre == 'tv mini series':
                movie_year = movie_identifier.get('series years')
                seasons = movie_identifier.get('number of seasons')
            else:
                movie_year = movie_identifier.get('year')
                seasons = 0  # quando si va a stampare, si può aggiungere un if che non mostra 'seasons==0'

            movie_title = filename
            '''
            if lingua != "Italian":
                movie_title = title + ' (' + filename + ')'

            else:
                movie_title = title
            '''
            plot = movie_identifier.get('plot', [''])[0]
            plot = plot.split('::')[0]

            director_box = search_director(movie_identifier)
            actor_box = search_cast(movie_identifier)
            writer_box = search_writer(movie_identifier)

        except imdb.IMDbError as e:
            print("Probably you're not connected to Internet.  Complete error report:")
            print(e)
            sys.exit(3)

        if not movie:
            print('It seems that there\'s no movie with movie_id "%s"' % movie_title)
            sys.exit(4)

        movie_container = {'Title': movie_title, 'Url': imdbURL, 'Id': movie_id, 'Year': movie_year, 'Seasons': seasons, 'Plot': plot,
                           'DirectorBox': director_box, 'ActorBox': actor_box, 'WriterBox': writer_box}

        return movie_container



def search_director(movie_identifier):
    directors = movie_identifier['director']
    movie_dic['Director'] = []
    for dir in directors:
        director_name = dir['name']
        director_id = dir.personID
        presence = check_attori_amati(director_id)
        if not presence:
            presence = False
        movie_dic['Director'].append({'Name': director_name, 'Id': director_id, 'Present': presence})
    return movie_dic['Director']


def search_cast(movie_identifier):
    actors = movie_identifier['cast']
    movie_dic['Actor'] = []
    for actor in actors:
        actor_name = actor['name']
        actor_id = actor.personID
        presence = check_attori_amati(actor_id)
        if not presence:
            presence = False
        movie_dic['Actor'].append({'Name': actor_name, 'Id': actor_id, 'Present': presence})
    return movie_dic['Actor']

def search_writer(movie_identifier):
    writers = movie_identifier['writer']
    movie_dic['Writer'] = []
    for writ in writers:
        writer_name = writ['name']
        writer_id = writ.personID
        presence = check_attori_amati(writer_id)
        if not presence:
            presence = False
        movie_dic['Writer'].append({'Name': writer_name, 'Id': writer_id, 'Present': presence})
    return movie_dic['Writer']


def correct_movie_name(i, year):
    correct_movie_container = {}
    filename = i
    movies = ia.search_movie(filename)
    year = int(year)

    for film in movies:
        movie = film
        movie_id = movie.movieID
        movie_identifier = ia.get_movie(movie_id)
        movie_year = movie_identifier.get('year')
        if movie_year == year:
            movie_title = str(i)
            print(movie_title)
            imdbURL = ia.get_imdbURL(movie)

            plot = movie_identifier.get('plot', [''])[0]
            plot = plot.split('::')[0]

            director_box = search_director(movie_identifier)
            actor_box = search_cast(movie_identifier)
            writer_box = search_writer(movie_identifier)

            genre = movie_identifier.get('kind')
            if genre == 'tv series' or genre == 'tv mini series':
                movie_year = movie_identifier.get('series years')
                seasons = movie_identifier.get('number of seasons')
            else:
                movie_year = movie_identifier.get('year')
                seasons = 0  # quando si va a stampare, si può aggiungere un if che non mostra 'seasons==0'

            correct_movie_container[i] = []
            correct_movie_container[i].append({'Movie Title': movie_title, 'Movie Url': imdbURL, 'Movie Id': movie_id, 'Movie Year': movie_year,
                               'Seasons': seasons, 'Movie plot': plot, 'Director List': director_box, 'Actor List': actor_box, 'Writer List': writer_box})

    return correct_movie_container