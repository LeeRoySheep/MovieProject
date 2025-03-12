from movie_app import MovieApp
from storage_csv import StorageCsv

storage = StorageCsv('storageFiles/movies.csv')
movie_app = MovieApp(storage)
movie_app.run()