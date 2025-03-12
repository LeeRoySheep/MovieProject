from abc import ABC, abstractmethod


class IStorage(ABC):
    """Abstract Movie Storage class"""

    @abstractmethod
    def list_movies(self):
        """abtract method to return movie list as dictionary from Storage object"""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """"add movie to Storage for all Storage types as abstract"""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """delete movie form storage"""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """update movies rating as abstract method """
        pass
