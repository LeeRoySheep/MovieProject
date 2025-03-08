from istorage import IStorage
import json

class StorageJson(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def file_path(self):
        """magig getter method"""
        return self._file_path


    @file_path.setter
    def file_path(self, new_file_path):
        """magic setter method"""
        self._file_path = new_file_path

    def list_movies(self):
        """method to create a movie list"""
        with (open(self.file_path, 'r') as json_reader):
            movie_dict = json.load(json_reader)
        return [movie for movie in movie_dict]

    def add_movie(self, title, year, rating, poster):
        """method to add movie to database"""
        with open(self.file_path, 'r') as json_reader:
            movie_dict = json.load(json_reader)
        if title not in [movie for movie, info in movie_dict.items()]:
            movie_dict[title] = {"year": year, "rating": rating, "poster": poster}
            with open(self.file_path, "w") as file_writer:
                json.dump(movie_dict, file_writer, indent=4)
        else:
            raise ValueError("Sorry but this movie already exists!")

    def delete_movie(self, title):
        """delete file form dtatbase"""
        with open(self.file_path, 'r') as file:
            film_dict = json.load(file)
        if title in [movie for movie, info in film_dict]:
            del film_dict[title]
        else:
            raise ValueError(f"Sorry the movie {title} is not in this storage!")

    def update_movie(self, title, rating):
        """ update movie rating in storage"""
        with open(self.file_path, 'r') as file:
            film_dict = json.load(file)
        if title in [movie for movie, info in film_dict]:
            film_dict[title] = rating
        else:
            raise ValueError("Sorry movie not in this storage!")