from Folder import Folder

class Movie(Folder):
    def __init__(self, Folder, id, url, title, year, plot, director_box, actor_box):
        super().__init__(Folder.home_path, Folder.name, Folder.dir, Folder.atime, Folder.ctime, Folder.size, Folder.ext)
        self.id = id
        self.url = url
        self.title = title
        self.year = year
        self.plot = plot
        self.director_box = director_box
        self.actor_box = actor_box