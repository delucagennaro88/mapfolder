from imdb import IMDb

ia = IMDb()

movie = ia.get_movie('Vacanze romane')

title= movie.get('title')

print(title)

