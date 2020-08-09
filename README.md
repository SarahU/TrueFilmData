How to run:

Wikipedia Abstract Parser

Reports:


Thoughts:

//explore

Wikipedia file is quite large and contains far more info than is needed.
Definitely worth pre-processing.

Wikipedia articles can have duplicate entries for the same names ie the name of a movie could be based on a book of the same movie

//wikipedia is sorted by title
//title, url, abstract

Movies:
//explore the movies - look at ids & title columns - are they unique?

Movies are not ordered, there are duplicate rows, some missing imdb ids

one might need logic to ensure the film wiki page is selected and not just a page that has the same name as the movie


test: top of mind, you can test structure, data types, row & columns counts and checking for required columns

//clean and process
given the only semi-complete data, the budget and revenue data was updated by using the mean values. This is a normal practice to clean-up and normalise the data, especially for using in machine learning, to reduce anomolies, but of course this needs to be a discussion with the analyst/ stakeholder