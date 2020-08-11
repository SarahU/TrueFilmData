import xml.etree.ElementTree as ET
import csv


class WikipediaDataFeed:
    def __init__(self, movieDataSource):
        self.movieSource = movieDataSource

    def update_wikipedia_data_source(self):
        movie_name_list = self.movieSource.read_movie_names()
        # path = './data/enwiki-latest-abstract.xml.gz'
        path = './data/enwiki-latest-abstract.xml'
        # with gzip.open(path, 'rb') as f:
        #     file_content = f.read()

        element_collection = []

        with open('./data/wiki_movie_data.csv', 'w', encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Title', 'Abstract', 'URL'])

            context = ET.iterparse(path, events=("start", "end"))

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
