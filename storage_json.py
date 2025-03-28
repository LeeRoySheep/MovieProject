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

    @list_movies.setter
    def list_movies(self, movie_dict):
        with open(self.file_path, 'w', encoding="utf8") as writer:
            json.dump(movie_dict, writer, indent=4)
