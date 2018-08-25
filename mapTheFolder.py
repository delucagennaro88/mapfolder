from file_manager import save_info
import os, datetime
from flask import Flask, flash, render_template
from json_manager import open_json, open_json_data
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from person_manager import check_presence, attori_amati

directory = "C:\\Users\\Utente\\Desktop\\FILM"
json_directory = "C:\\Users\\Utente\\Dropbox\\Map the Movie"

cinema_json_file = "cinema.json"
json_file = "attori_amati.json"
json_actor_dir = os.path.join(json_directory, json_file)
json_dir = os.path.join(json_directory, cinema_json_file)

class ActorForm(FlaskForm):
    actor_name = StringField('Personaggio', validators=[DataRequired()])
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
    data_collection = open_json(json_dir)
    data = data_collection.values()
    return render_template('show_all.html', data=data)

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

if __name__ == '__main__':
    app.run(debug=True)


