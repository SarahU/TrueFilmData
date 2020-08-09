import pandas as pd

MOVIES_PATH = './data/3405_6663_compressed_movies_metadata.csv.zip'


class Report:

    def read_cleaned_movies_data(self):
        movie_data = pd.read_csv(MOVIES_PATH, compression='zip')
        movie_data = movie_data.drop_duplicates()
        movie_data = movie_data.drop(movie_data[movie_data.imdb_id == '0'].index)

        movie_data['revenue'] = movie_data['revenue'].apply(pd.to_numeric)
        revenue_mean = movie_data['revenue'].mean()
        movie_data.loc[movie_data['revenue'] == 0] = revenue_mean

        movie_data['budget'] = movie_data['budget'].apply(pd.to_numeric)
        budget_mean = movie_data['budget'].mean()
        movie_data.loc[movie_data['budget'] == 0] = budget_mean

        return movie_data

    def budget_vs_revenue(self):
        movies_data = self.read_cleaned_movies_data()

        movies_data['budget_revenue_ratio'] = movies_data.apply(lambda row: (row.budget / row.revenue) * 100, axis=1)
        return movies_data


