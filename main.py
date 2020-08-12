import argparse

from movie_data_source import MovieDataSource
from postgres_movie_feed import ReportingMovieDataDBLoader
from wikipedia_data_feed import WikipediaDataFeed


def get_args():
    parser = argparse.ArgumentParser(description='Movie Data Reporting & Feeds!')
    argparse.ArgumentParser()
    parser.add_argument('job', type=str)

    args = parser.parse_args()
    return args


def run_wikipedia_job():
    feed = WikipediaDataFeed(movie_data_source)
    print('Running...')
    result = feed.update_wikipedia_data_source()
    if result:
        print('Wikipedia Movie data successfully updated')
    else:
        print('Wikipedia feed failed')


def run_db_reload_job():
    loader = ReportingMovieDataDBLoader(movie_data_source)
    print('Running...')
    result = loader.load_top_movies_into_db()
    if result:
        print('Movie database successfully updated')
    else:
        print('Movie database update failed')


if __name__ == '__main__':
    args = get_args()

    ans = args.job

    movie_data_source = MovieDataSource()

    while ans != 'Q':
        if args.job == 'I':
            run_db_reload_job()
            break
        if args.job == 'W':
            run_wikipedia_job()
            break
        if args.job == 'R':
            print('Budget to Revenue Ratio')
            print(movie_data_source.get_data_with_budget_vs_revenue())
            break

        ans = input('Press Q to quit')


