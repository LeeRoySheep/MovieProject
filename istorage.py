from abc import ABC, abstractmethod


class IStorage(ABC):
    """Abstract Movie Storage class"""



    @property
    @abstractmethod
    def list_movies(self)->dict:
        """abtract method to return movie list as dictionary from Storage object"""
        pass


    @list_movies.setter
    @abstractmethod
    def list_movies(self, movie_dict):
        """abtract method to set movie list as dictionary from Storage object"""
        pass


    def add_movie(self, title, year, rating, poster=None):
        """
        function to write a new movie to storage file
        :param title:
        :param year:
        :param rating:
        :param poster:
        :return: None
        """
        movie_dict = self.list_movies
        if title not in [movie for movie, info in movie_dict.items()]:
            movie_dict[title] = {"year": year, "rating": rating, "poster": poster}
            self.list_movies = movie_dict
        else:
            raise ValueError("Sorry but this movie already exists!")


    def delete_movie(self, title):
        """
        function to delete movie with given title form storage
        :param title:
        :return:
        """
        movies = self.list_movies
        for movie in movies.keys():
            if title in movie:
                del movies[title]
                self.list_movies = movies
                return None
        raise ValueError(f"{title} not in Database!")


    def update_movie(self, title, note):
        """
        function to update rating from movie in storage
        :param title:
        :param rating:
        :return:
        """
        movies = self.list_movies
        if title not in [movie for movie, info in movies.items()]:
            raise ValueError("Sorry movie not in this storage!")
        movies[title]["note"] = note
        self.list_movies = movies
