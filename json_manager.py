import json
import os

json_directory = "C:\\Users\\Utente\\Dropbox\\Map the Movie"
json_data = "data.json"
json_data_dir = os.path.join(json_directory, json_data)

movie_class = {}
movie_dic = {}
filmography_dic = {}
film = {}


def search_director(movie_list):
    directors = movie_list
    movie_dic['Director'] = []
    for dir in directors:
        director_name = dir['Name']
        director_id = dir['Id']
        director_presence = dir['Present']
        movie_dic['Director'].append({'Name': director_name, 'Id': director_id, 'Present': director_presence})
    return movie_dic['Director']


def search_cast(movie_list):
    actors = movie_list
    movie_dic['Actor'] = []
    for dir in actors:
        actor_name = dir['Name']
        actor_id = dir['Id']
        actor_presence = dir['Present']
        movie_dic['Actor'].append({'Name': actor_name, 'Id': actor_id, 'Present': actor_presence})
    return movie_dic['Actor']

def search_writer(movie_list):
    writers = movie_list
    movie_dic['Writer'] = []
    for dir in writers:
        writer_name = dir['Name']
        writer_id = dir['Id']
        writer_presence = dir['Present']
        movie_dic['Writer'].append({'Name': writer_name, 'Id': writer_id, 'Present': writer_presence})
    return movie_dic['Writer']


def open_json(json_dir):
    with open(json_dir, encoding='cp1252') as data_file:
        movie_json = json.load(data_file)
        xx = 0
        for i in movie_json.values():
            for x in i:
                home_path = x['Home Directory']
                file_name = x['File Name']
                id = x['Id']  # nome del File senza Directory
                ext = x['Extension']
                atime = x['Atime']
                ctime = x['Ctime']
                size = x['Size']
                movie_id = x['Movie Id']
                movie_title = x['Movie Title']
                movie_url = x['Movie Url']
                movie_year = x['Movie Year']
                movie_seasons = x['Seasons']
                movie_plot = x['Movie plot']
                movie_directors = x['Movie Director']
                movie_dir_list = search_director(movie_directors)

                movie_actors = x['Movie Actor']
                movie_act_list = search_cast(movie_actors)

                movie_writers = x['Movie Writer']
                movie_writ_list = search_writer(movie_writers)

                movie_class[xx] = []
                movie_class[xx].append(
                    {'Home path': home_path, 'File Name': file_name, 'Id': id, 'Atime': atime, 'Ctime': ctime,
                     'Size': size, 'Extension': ext, 'Movie Id': movie_id, 'Movie Url': movie_url,
                     'Movie Title': movie_title, 'Movie Year': movie_year, 'Seasons': movie_seasons,
                     'Movie Plot': movie_plot, 'Director List': movie_dir_list, 'Actor List': movie_act_list, 'Writer List': movie_writ_list})

                xx += 1

        return movie_class


# create Json File for NR. of saved files
def createJsonFile(data_saved):
    json_dic = {'Directory': json_data_dir, 'Saved Files': data_saved}
    with open(json_data_dir, 'a') as outfile:
        json.dump(json_dic, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print('Creato il file')


# read Json File with NR. of saved files
def read_saved_files():
    jsonFile = open(json_data_dir, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    tmp = data["Saved Files"]
    print('Letto il file')

    return tmp


# update Json File with NR. of saved files
def updateJsonFile(num):
    jsonFile = open(json_data_dir, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    ## Working with buffered content
    tmp = data["Saved Files"]
    data["Saved Files"] = num

    ## Save our changes to JSON file
    jsonFile = open(json_data_dir, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

    print("Aggiornato il file")

def open_json_data(json_dir):
    with open(json_dir, encoding='cp1252') as data_file:
        movie_json = json.load(data_file)

        for i, (key, value) in enumerate(movie_json.items()):
            for a in value:
                film[a['Name']] = []
                film[a['Name']].append({'Name': a['Name'], 'Id': a['Id'], 'Date': a['Date'], 'Filmography': a['Filmography']})
        return film


def query_actor(actor_name, json_dir):
    query_dic = {}
    movie_file = open_json(json_dir)
    cinema_data = movie_file.values()

    for a in cinema_data:
        for b in a:

            for c in b['Actor List']:
                if c['Name'] == actor_name:
                    query_dic[b['Movie Id']] = []
                    query_dic[b['Movie Id']].append(
                        {'Home path': b['Home path'], 'File Name': b['File Name'], 'Id': b['Id'], 'Atime': b['Atime'],
                         'Ctime': b['Ctime'],
                         'Size': b['Size'], 'Extension': b['Extension'], 'Movie Id': b['Movie Id'],
                         'Movie Url': b['Movie Url'],
                         'Movie Title': b['Movie Title'], 'Movie Year': b['Movie Year'], 'Seasons': b['Seasons'],
                         'Movie Plot': b['Movie Plot'], 'Director List': b['Director List'],
                         'Actor List': b['Actor List']})

            for d in b['Director List']:
                if d['Name'] == actor_name:
                    query_dic[b['Movie Id']] = []
                    query_dic[b['Movie Id']].append(
                        {'Home path': b['Home path'], 'File Name': b['File Name'], 'Id': b['Id'], 'Atime': b['Atime'],
                         'Ctime': b['Ctime'],
                         'Size': b['Size'], 'Extension': b['Extension'], 'Movie Id': b['Movie Id'],
                         'Movie Url': b['Movie Url'],
                         'Movie Title': b['Movie Title'], 'Movie Year': b['Movie Year'], 'Seasons': b['Seasons'],
                         'Movie Plot': b['Movie Plot'], 'Director List': b['Director List'],
                         'Actor List': b['Actor List']})

            for e in b['Writer List']:
                if e['Name'] == actor_name:
                    query_dic[b['Movie Id']] = []
                    query_dic[b['Movie Id']].append(
                        {'Home path': b['Home path'], 'File Name': b['File Name'], 'Id': b['Id'], 'Atime': b['Atime'],
                         'Ctime': b['Ctime'],
                         'Size': b['Size'], 'Extension': b['Extension'], 'Movie Id': b['Movie Id'],
                         'Movie Url': b['Movie Url'],
                         'Movie Title': b['Movie Title'], 'Movie Year': b['Movie Year'], 'Seasons': b['Seasons'],
                         'Movie Plot': b['Movie Plot'], 'Director List': b['Director List'],
                         'Actor List': b['Actor List']})

    query_raw = query_dic.values()
    return query_raw
