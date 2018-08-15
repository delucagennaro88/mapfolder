from Folder import Folder

class Movie(Folder):
    def __init__(self, home_path, name, dir, atime, ctime, size, ext, id, url, title, year, plot, director_box, actor_box):
        super().__init__(home_path, name, dir, atime, ctime, size, ext)
        self.id = id
        self.url = url
        self.title = title
        self.year = year
        self.plot = plot
        self.director_box = director_box
        self.actor_box = actor_box