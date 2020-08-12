import pandas as pd

IMDB_MOVIE_DATA_PATH = './data/3405_6663_compressed_movies_metadata.csv.zip'
WIKIPEDIA_MOVIE_DATA = './data/wiki_movie_data.csv'


class MovieDataSource:

    def get_movie_wikipedia_data(self):
        return pd.read_csv(WIKIPEDIA_MOVIE_DATA)

    def get_imdb_movie_data(self):
        movie_data = pd.read_csv(IMDB_MOVIE_DATA_PATH, compression='zip', parse_dates=['release_date'])

        movie_data = movie_data.drop_duplicates()
        movie_data = movie_data.drop(movie_data[movie_data.imdb_id == '0'].index)

        movie_data['revenue'] = movie_data['revenue'].apply(pd.to_numeric)
        revenue_mean = movie_data['revenue'].mean()
        movie_data['revenue'].loc[movie_data['revenue'] == 0] = revenue_mean

        movie_data['budget'] = movie_data['budget'].apply(pd.to_numeric)
        budget_mean = movie_data['budget'].mean()
        movie_data['budget'].loc[movie_data['budget'] == 0] = budget_mean

        return movie_data

    def read_movie_names(self):
        movies = self.get_imdb_movie_data()
        names = movies['title'].unique()

        return names

    def get_data_with_budget_vs_revenue(self):
        movies_data = self.get_imdb_movie_data()

        movies_data['budget_revenue_ratio'] = movies_data.apply(lambda row: (row.budget / row.revenue) * 100, axis=1)
        return movies_data
