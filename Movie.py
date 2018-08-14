from Folder import Folder

class Movie(Folder):
    def __init__(self, home_path, name, dir, atime, ctime, size, ext, id, url, title, year, plot, director_id, director_name, actor_id, actor_name):
        super().__init__(home_path, name, dir, atime, ctime, size, ext)
        self.id = id
        self.url = url
        self.title = title
        self.year = year
        self.plot = plot
        self.director_id = director_id
        self.director_name = director_name
        self.actor_name = actor_name
        self.actor_id = actor_id