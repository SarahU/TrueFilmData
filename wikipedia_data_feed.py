import xml.etree.ElementTree as ET
import csv
import gzip

WIKIPEDIA_DATA_FILE_PATH = './data/enwiki-latest-abstract.xml.gz'
WIKI_MOVIE_OUTPUT_FILE_PATH = './data/wikipedia_movie_data.csv'


class WikipediaDataFeed:
    def __init__(self, movieDataSource):
        self.movieSource = movieDataSource

    def update_wikipedia_data_source(self):
        try:
            movie_name_list = self.movieSource.read_movie_names()
            element_collection = []

            with open(WIKI_MOVIE_OUTPUT_FILE_PATH, 'w', encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Title', 'Abstract', 'URL'])

                with gzip.open(WIKIPEDIA_DATA_FILE_PATH, 'rb') as gfile:
                    context = ET.iterparse(gfile, events=("start", "end"))

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

                return True
        except Exception as e:
            print("An issue caused the feed to break", e)
            return False

