import xml.etree.ElementTree as ET
import csv

WIKIPEDIA_DATA_FILE_PATH = './data/enwiki-latest-abstract.xml'
WIKI_MOVIE_OUTPUT_FILE_PATH = './data/wiki_movie_data.csv'


class WikipediaDataFeed:
    def __init__(self, movieDataSource):
        self.movieSource = movieDataSource

    def update_wikipedia_data_source(self):
        movie_name_list = self.movieSource.read_movie_names()
        # path = './data/enwiki-latest-abstract.xml.gz'

        # with gzip.open(path, 'rb') as f:
        #     file_content = f.read()

        element_collection = []

        with open(WIKI_MOVIE_OUTPUT_FILE_PATH, 'w', encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Title', 'Abstract', 'URL'])

            context = ET.iterparse(WIKIPEDIA_DATA_FILE_PATH, events=("start", "end"))

            event, root = next(context)
            for event, elem in context:

                if event == "end" and elem.tag == "doc":

                    title = elem.find('title').text
                    title = title.replace('Wikipedia: ', '').strip()

                    if title in movie_name_list:
                        url = elem.find('url').text
                        abstract = elem.find('abstract').text
                        element = [title, abstract, url]
                        element_collection.append(element)
                        csvwriter.writerow(element)

                    root.clear()

            print(element_collection)

        return element_collection
