import datetime
import json
import os

from flask import Flask, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from file_manager import save_info
from json_manager import open_json, open_json_data, query_actor, update_views
from person_manager import check_presence, attori_amati
from movie_manager import correct_movie_name

directory = "G:\\CINEMA"
#directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_directory = "C:\\Users\\Utente\\Dropbox\\Map the Movie"

cinema_json_file = "cinema.json"
json_file = "attori_amati.json"
json_actor_dir = os.path.join(json_directory, json_file)
json_dir = os.path.join(json_directory, cinema_json_file)

json_views = "views.json"
json_views_dir = os.path.join(json_directory, json_views)

query_dic = {}

def show_movie_linked(json_dir, movie_id):
    movie_link = {}
    with open(json_dir, encoding='cp1252') as data_file:
        movie_json = json.load(data_file)

        for i in movie_json.values():
            for x in i:
                if x['Movie Id'] == movie_id:
                    movie_link = {'Home path': x['Home path'], 'File Name': x['File Name'], 'Id': x['Id'],
                                  'Atime': x['Atime'], 'Ctime': x['Ctime'],
                                  'Size': x['Size'], 'Extension': x['Extension'], 'Banner Pic': x['Banner Pic'],
                                  'Movie Poster': x['Movie Poster'], 'Movie Id': x['Movie Id'],
                                  'Movie Url': x['Movie Url'],
                                  'Movie Title': x['Movie Title'], 'Movie Year': x['Movie Year'],
                                  'Seasons': x['Seasons'],
                                  'Movie plot': x['Movie plot'], 'Director List': x['Director List'],
                                  'Actor List': x['Actor List'], 'Writer List': x['Writer List']}

    return movie_link


def show_actor_linked(json_dir, actor_id):
    actor_link = {}
    with open(json_dir, encoding='cp1252') as data_file:
        actor_json = json.load(data_file)

        for i in actor_json.values():
            for x in i:
                if x['Id'] == actor_id:
                    actor_link = {'Name': x['Name'], 'Date': x['Date'], 'Gif': x['Gif'], 'Poster': x['Poster'],
                                  'Filmography': x['Filmography'], 'Url': x['Url']}

    return actor_link


def show_filmography(json_actor_dir, movie_id):
    movie_link = {}
    with open(json_actor_dir, encoding='cp1252') as data_file:
        actor_json = json.load(data_file)

        for i in actor_json.values():
            for x in i:
                # qui si può recuperare l'Id dell'Attore e fare l'If
                for y in x.values():
                    if type(y) == dict:
                        for z in y.values():
                            for w in z:
                                if w['Id'] == movie_id:
                                    print(w['Title'])  # qui vanno create le variabili
                                    movie_link = {'Title': w['Title'], 'Id': w['Id'], 'Present': w['Present'],
                                                  'Year': w['Year'], 'Original': w['Original']}

    return movie_link


class ActorForm(FlaskForm):
    actor_name = StringField('Cerca nuovi Personaggi', validators=[DataRequired()])
    submit = SubmitField('Cerca')


class QueryForm(FlaskForm):
    actor_name = StringField('Seleziona Personaggio', validators=[DataRequired()])
    submit = SubmitField('Cerca')


class EditMovieForm(FlaskForm):
    movie_plot = StringField('Trama', validators=[DataRequired()])
    submit = SubmitField('Salva')


class EditFilmography(FlaskForm):
    movie_title = StringField('Titolo', validators=[DataRequired()])
    movie_original = StringField('Titolo originale', validators=[DataRequired()])
    movie_id = StringField('Id', validators=[DataRequired()])
    movie_year = StringField('Anno', validators=[DataRequired()])
    submit = SubmitField('Salva')

class CorrectMovieForm(FlaskForm):
    movie_title = StringField('Titolo', validators=[DataRequired()])
    movie_year = StringField('Anno', validators=[DataRequired()])
    submit = SubmitField('Cerca')

def start():
    if not os.path.exists(json_dir):
        update = False
        print('Il file non esiste!')
        last_update = datetime.datetime.now()
        save_info(directory, last_update, update, json_dir)

    else:
        update = True
        print('Il file esiste!')
        file_modified = os.stat(json_dir).st_mtime
        save_info(directory, file_modified, update, json_dir)


current_dic = {}

def current_movie():
    with open(json_views_dir, 'r') as outfile:
        data = json.load(outfile)

    counter = 0
    a_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

    for view, (key, value) in enumerate(data.items()):
        for alfa in value:
            if int(alfa['Views']) == 0 or datetime.datetime.strptime(alfa['Data Views'], "%Y-%m-%d %H:%M:%S.%f") <= a_year_ago:
                if counter <= 25:
                    current_dic[key] = []
                    current_dic[key].append({'Id': alfa['Id'], 'Title': alfa['Title'], 'Data Views': alfa['Data Views'], 'Views': alfa['Views'], 'Home path': alfa['Home path'], 'Movie plot': alfa['Movie plot'], 'Image One': alfa['Image One'], 'Image Two': alfa['Image Two']})
                    counter+=1
    return current_dic

# Qui comincia il programma

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M'


@app.route('/')
def home():
    start()
    data_collection = current_movie()
    data = data_collection.values()

    return render_template('home.html', data=data)

@app.route('/show')
def show_all():
    form = QueryForm()
    data_collection = open_json(json_dir)
    data = data_collection.values()
    return render_template('show_all.html', form=form, data=data)


@app.route('/movie/<string:movie_id>', methods=['GET', 'POST'])
def show_movie_infos(movie_id):
    linked_movie = show_movie_linked(json_dir, movie_id)

    return render_template("movie.html", data=linked_movie)


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm()

    actor = form.actor_name.data
    query_dic = query_actor(actor, json_dir)

    if not query_dic:
        flash('Non ci sono film di {} nel database'.format(actor))

    return render_template('show_all.html', title='Cerca', form=form, query_data=query_dic)


@app.route('/attoriamati')
def show_all_people():
    form = ActorForm()
    if os.path.exists(json_actor_dir):
        check_presence(json_dir, json_actor_dir)
        actor_data_collection = open_json_data(json_actor_dir)
        actor_data = actor_data_collection.values()
    else:
        actor_data = {}
    return render_template('attori_amati.html', data=actor_data, form=form)


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = ActorForm()
    if form.validate_on_submit():
        flash('Ricerca per {} effettuata'.format(form.actor_name.data))
        attori_amati(json_dir, json_actor_dir, form.actor_name.data)

        if os.path.exists(json_actor_dir):
            check_presence(json_dir, json_actor_dir)
            actor_data_collection = open_json_data(json_actor_dir)
            actor_data = actor_data_collection.values()
        else:
            actor_data = {}

    return render_template('attori_amati.html', title='Cerca', form=form, data=actor_data)


@app.route('/actor/<string:actor_id>', methods=['GET', 'POST'])
def show_actor_infos(actor_id):
    linked_actor = show_actor_linked(json_actor_dir, actor_id)
    return render_template("actor.html", data=linked_actor)


@app.route('/views/<string:movie_id>', methods=['GET', 'POST'])
def show_movie_views(movie_id):
    current_movie = update_views(movie_id)

    return render_template("views.html", data=current_movie)


@app.route('/edit/<string:movie_id>', methods=['GET', 'POST'])
def edit_movie_info(movie_id):
    linked_movie = show_movie_linked(json_dir, movie_id)
    linked_movie_plot = linked_movie['Movie plot']
    linked_movie_id = linked_movie['Movie Id']
    form = EditMovieForm()

    if form.validate_on_submit():
        linked_movie_plot = form.movie_plot.data

        #aggiorna la TRAMA in cinema.json
        with open(json_dir) as data_file:
            movie_data_json = json.load(data_file)

        for i in movie_data_json.values():
            for x in i:
                if x['Movie Id'] == movie_id:
                    x['Movie plot'] = linked_movie_plot

        with open(json_dir, 'w') as outfile:
            json.dump(movie_data_json, outfile, indent=4, ensure_ascii=False)

        #aggiorna la TRAMA in views.json
        with open(json_views_dir) as data_file:
            movie_views_json = json.load(data_file)

        for y in movie_views_json.values():
            for z in y:
                if z['Id'] == movie_id:
                    z['Movie plot'] = linked_movie_plot

        with open(json_views_dir, 'w') as outfile:
            json.dump(movie_views_json, outfile, indent=4, ensure_ascii=False)

    return render_template("edit.html", data=linked_movie_plot, movie_id=linked_movie_id, form=form)


@app.route('/edit_film/<string:movie_id>', methods=['GET', 'POST'])
def edit_filmography(movie_id):
    movie_link = show_filmography(json_actor_dir, movie_id)
    film_title = movie_link['Title']
    film_original = movie_link['Original']
    film_id = movie_link['Id']
    film_year = movie_link['Year']

    form = EditFilmography()

    if form.validate_on_submit():
        film_title = form.movie_title.data
        film_id = form.movie_id.data
        film_year = form.movie_year.data
        film_original = form.movie_original.data

        with open(json_actor_dir, encoding='cp1252') as data_file:
            actor_json = json.load(data_file)

        for i in actor_json.values():
            for x in i:
                # qui si può recuperare l'Id dell'Attore e fare l'If
                for y in x.values():
                    if type(y) == dict:
                        for z in y.values():
                            for w in z:
                                if w['Id'] == movie_id:
                                    w['Title'] = film_title
                                    w['Id'] = film_id
                                    w['Year'] = film_year

        with open(json_actor_dir, 'w') as outfile:
            json.dump(actor_json, outfile, indent=4, ensure_ascii=False)

    return render_template("edit_film.html", title=film_title, original=film_original, id=film_id, year=film_year,
                           movie_id=movie_id, form=form)


@app.route('/correct/<string:movie_id>', methods=['GET', 'POST'])
def correct_movie_info(movie_id):
    linked_movie = show_movie_linked(json_dir, movie_id)
    linked_movie_title = linked_movie['Movie Title']
    linked_movie_year = linked_movie['Movie Year']

    correct_movie_box = {}
    form = CorrectMovieForm()

    if form.validate_on_submit():
        movie_title = form.movie_title.data
        movie_year = form.movie_year.data
        correct_movie_box = correct_movie_name(movie_title, movie_year)

        # aggiorna la TRAMA in cinema.json
        with open(json_dir) as data_file:
            movie_data_json = json.load(data_file)

        for i in movie_data_json.values():
            for x in i:
                if x['Movie Id'] == movie_id:
                    x['Movie plot'] = correct_movie_box['Movie plot']
                    x['Movie Url'] = correct_movie_box['Movie Url']
                    x['Director List'] = correct_movie_box['Director List']
                    x['Seasons'] = correct_movie_box['Seasons']
                    x['Movie Year'] = correct_movie_box['Movie Year']
                    x['Writer List'] = correct_movie_box['Writer List']
                    x['Actor List'] = correct_movie_box['Actor List']
                    x['Movie Id'] = correct_movie_box['Movie Id']

        with open(json_dir, 'w') as outfile:
            json.dump(movie_data_json, outfile, indent=4, ensure_ascii=False)

        # aggiorna la TRAMA in views.json
        with open(json_views_dir) as data_file:
            movie_views_json = json.load(data_file)

        for m, n in movie_views_json.items():
            for o in n:
                if o['Id'] == movie_id:
                    correct_id = correct_movie_box['Movie Id']
                    o['Movie plot'] = correct_movie_box['Movie plot']
                    o['Id'] = correct_movie_box['Movie Id']
                    movie_views_json[correct_id] = movie_views_json.pop(m) # questo è il valore dell'ID da correggere

        with open(json_views_dir, 'w') as outfile:
            json.dump(movie_views_json, outfile, indent=4, ensure_ascii=False)

    return render_template("correct.html", data=correct_movie_box, movie_id=movie_id, form=form, title=linked_movie_title, year=linked_movie_year)


if __name__ == '__main__':
    app.run(debug=True)
