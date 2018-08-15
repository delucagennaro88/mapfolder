from file_manager import save_info

directory = "C:\\Users\\Utente\\Desktop\\FILM"

# Qui comincia il programma

collection = save_info(directory)

for i in collection:
    print(
        'Informazioni sul file:' + '\n')
    print(i.home_path + '\n' + i.name + '\n' + i.dir + '\n' + str(i.atime) + '\n' + str(
            i.ctime) + '\n' + str(i.size) + '\n' + i.ext + '\n\n\n')
    print('Informazioni sul film:' + '\n')
    print(str(i.id) + '\n' + i.url + '\n' + i.title + '\n' + str(i.year) + '\n' + i.plot + '\n')
    for y in i.director_box:
        print('Regista: ' + y.name + '. Id: ' + y.id + '\n')
    for x in i.actor_box:
        print('Attore: ' + x.name + '. Id: ' + x.id + '\n')
    print('\n\n\n')
