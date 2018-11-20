import datetime
import json
import os

from flask import Flask, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from file_manager import save_info
from json_manager import open_json, open_json_data, query_actor
from person_manager import check_presence, attori_amati

directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_directory = "C:\\Users\\Utente\\Dropbox\\Map the Movie"

cinema_json_file = "cinema.json"
json_file = "attori_amati.json"
json_actor_dir = os.path.join(json_directory, json_file)
json_dir = os.path.join(json_directory, cinema_json_file)

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
                                  'Size': x['Size'], 'Extension': x['Extension'], 'Banner Pic': x['Banner Pic'], 'Movie Poster': x['Movie Poster'], 'Movie Id': x['Movie Id'],
                                  'Movie Url': x['Movie Url'],
                                  'Movie Title': x['Movie Title'], 'Movie Year': x['Movie Year'],  'Seasons': x['Seasons'],
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
                    actor_link = {'Name': x['Name'], 'Date': x['Date'], 'Gif': x['Gif'], 'Poster': x['Poster'], 'Filmography': x['Filmography']}

    return actor_link


class ActorForm(FlaskForm):
    actor_name = StringField('Cerca nuovi Personaggi', validators=[DataRequired()])
    submit = SubmitField('Cerca')


class QueryForm(FlaskForm):
    actor_name = StringField('Seleziona Personaggio', validators=[DataRequired()])
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


# Qui comincia il programma

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XMLZODSHE8N6NFOZDPZA2HULWSIYJU45K6N4ZO9M'


@app.route('/')
def show_all():
    start()
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


if __name__ == '__main__':
    app.run(debug=True)
