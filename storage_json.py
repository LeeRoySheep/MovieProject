from istorage import IStorage
import json

class StorageJson(IStorage):
    """
    creating a Storage Json class to handle a storage
    working with a json file as storage file
    """
    def __init__(self, file_path, owner=None):
        self._file_path = file_path
        self._owner = owner


    @property
    def owner(self):
        """
        getter vor owner variable
        :return: name of owner
        """
        return self._owner


    @owner.setter
    def owner(self, new_owner):
        """
        setter to overwrite owner
        :param new_owner: as string
        :return: None
        """
        self._owner = new_owner


    @property
    def file_path(self):
        """magic getter method"""
        return self._file_path


    @file_path.setter
    def file_path(self, new_file_path):
        """magic setter method"""
        self._file_path = new_file_path


    @property
    def list_movies(self):
        """method to create a movie list"""
        with open(self.file_path, 'r') as json_reader:
            movie_dict = json.load(json_reader)
        return {title: movie for title, movie in movie_dict.items()}


    def add_movie(self, title, year, rating, poster=None):
        """method to add movie to database"""
        movie_dict = self.list_movies
        if title not in [movie for movie, info in movie_dict.items()]:
            movie_dict[title] = {"year": year, "rating": rating, "poster": poster}
            with open(self.file_path, "w", encoding="utf8") as file_writer:
                json.dump(movie_dict, file_writer, indent=4)
        else:
            raise ValueError("Sorry but this movie already exists!")


    def delete_movie(self, title):
        """delete file form dtatbase"""
        film_dict = self.list_movies
        if title in [movie for movie, info in film_dict.items()]:
            del film_dict[title]
            with open(self.file_path, 'w', encoding="utf8") as writer:
                json.dump(film_dict, writer, indent=4)
        else:
            raise ValueError(f"Sorry the movie {title} is not in this storage!")


    def update_movie(self, title, rating):
        """ update movie rating in storage"""
        film_dict = self.list_movies
        if title in [movie for movie, info in film_dict.items()]:
            film_dict[title]["rating"] = rating
            with open(self.file_path, 'w', encoding="utf8") as writer:
                json.dump(film_dict, writer, indent=4)
        else:
            raise ValueError("Sorry movie not in this storage!")
