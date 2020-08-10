class WikiMovieDBLoader:
    def __init__(self, moviesDataSource, wikipediaDataSource):
        self.movieSource = moviesDataSource
        self.wikipediaMoviesSource = wikipediaDataSource

    def get_wiki_data_for_movies(self):
        imdb_movies_data = self.movieSource.get_data_with_budget_vs_revenue()
        wiki_movie_data = self.wikipediaMoviesSource.wikipediaMoviesSource.get_data()

        full_set = imdb_movies_data.join(wiki_movie_data, lsuffix='title', rsuffix='Title')

        full_set.sort_values(by=['budget_revenue_ratio'])

        return full_set

        # save to Postgres full_set.head(1000)