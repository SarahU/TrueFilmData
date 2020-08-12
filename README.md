##**How to run:**

I did not upload the data. Please place the 2 files in a folder called `data` at root level.

###There are 2 applications:

#####Wikipedia Parser (wikpedia_data_feed.py)
You can run this by calling the app with argument `W`
From TrueFilmData
`python main.py W`

#####Postgres Movie loader (postgres_movie_feed.py)
Its just a movie loader but I want to be clear it was for a Postgres DB. This can be generalised if needed but that was not required in this case.
I used a docker container with the following details:
`docker run --rm --name pg-docker-TrueFilm -e POSTGRES_PASSWORD=docker -p 5432:5432 postgres`
To run, install Docker for your operating system (a simple google will bring it up)
Once running, pull the docker image `docker pull postgres`
and then the above run command will start a contain with the postgres image. Note that there is no file storage attached for persistance so once it shuts down, it will disappear. You can provide a volume to mount if needed.

Python - please install Python for your operating system.

You can run this by calling the app with argument `I`
From TrueFilmData
`python main.py W`

####Query the data
You can either query the data in Python via the Movie Data Source class or you check the database
`select * from top_movies` will provide the 1000 movies that had the largest budget to revenue ratio
You can run the budget to revenue ration report using:
From TrueFilmData
`python main.py R`

###My Process & Thoughts:

####Explore the data 
Have a look at the data and see what we are working with. I'm currently on Windows so I opened the movie data in Excel to have a glance. I noticied a few oddities but nothing too bad.
Then I started looking at the data for the 1st query and discovered some data that need cleaning and coercing.
given the only semi-complete data, the budget and revenue data was updated by using the mean values. This is a normal practice to clean-up and normalise the data, especially for using in machine learning, to reduce anomolies, but of course this needs to be a discussion with the analyst/ stakeholder

Look at ids & title columns - are they unique?

Movies are not ordered, there are duplicate rows, some missing imdb ids.

Other rows have bad data. This is especially true for the row where `imdb_id = 0`. Hence these rows removed.


Wikipedia file is quite large and contains far more info than is needed.
Definitely worth pre-processing.

The Wikipedia articles can have duplicate entries for the same names ie the name of a movie could be based on a book of the same movie
Wikipedia is sorted by title
We need: title, url, abstract
but it's not a straight-forward match between the title. Wikipedia has duplicate entries for things that have the same name.
It would take more intelligence in the processing in order to identify the movie data from the other pages (ie people or places which the movies are named after).
I didn't do this in the interest of time but it should be (hopefully) simple to add this and to see where to add this as I read the XML record by record and you can see how the other elements are accessed.
you may need to make use of the link/sublinks to see if a film is mentioned or sometimes it's in the name ie `Puppies (film)`.

####Clean the data
Movies - remove the data that is obviously bad - many missing values, data in the wrong columns, etc
I applied some common sense and known practices but mostly you would go through this with an analyst / data subject expert and discuss
reasonable adjustments to the data. As it is, I do the following:
1 - Remove duplicate entries 
2 - Remove lines with an imdb if of zero - I noticed these rows were all bad data
3 - As the revenue and budget data was relevant to this exercise, I thought I would apply a simple but common process which 
replaces a 0 value with a value that represents the mean of the values in that column. I can see that this is not enough and you'd need to go further 
if you want to mimic realistic values for these fields but this is a start :) There are many ways to try and make bad data more useful.


Wikipedia - data is questionable but good enough to work with.
The only clean-up done here was to remove `Wikipedia: ` from the title field.


####Testing

I usually start with tests, most often integration tests (outside-in but no promises that it's textbook). 
I wrote tests to get the data in the first place and use simple tests of 
structure, data types, row & columns counts and checking for required columns.
These can also test the counts of rows are within a range if you expect some fluctuation though I prefer to keep these static (but that's an option if it's suitable for the domain).
I pulled out a few unit tests as I went.
I left the integration and unit tests together as well having the unit tests using the 'prod' location, like the database but I replace these with either mocks, files or dev databases.
I haven't done this here due to time.

####Iterating

I iterated a few times as I built out the functionality. Ultimately I came out with one class that
provide access to the sources and queries in those sources, and 2 feeds that can be run as jobs:
1 - Wikipedia movie process - this could be run as needed. 
The amount of movie data actually needed is a small subset of the data available in this file.
There is no need to run this everytime you would need to query movie data, so hence this is a separated process.
I also assumed this dataset would not change very often and would only be run maybe weekly? The process took about 45 minutes on my laptop. I think this is acceptable for a weekly process 
but it could be written differently if needed. I wrote it so that you are dealing with a record at a time instead of a line at a item
so that it was easy to understand.
Changes here for optimisation would be to read in line by line and process in a more optimal where once you have title line, if it matches a movie name, process the next lines required.
If it doesn't match, you can discard the other elements immediately, as you know the pattern. In other words, process one line in memory at a time. Personally I thought the complexity would outway the gains as a record in memory at a time and a short search through that for the abstract and url is quick.
Readability over optimisation until you have a good reason to.
2 - Postgres loader process. Anytime of of your inputs changes, you would run this process.
This step could be chained onto an update of either source (imdb or wikpedia) which could well run at different intervals so no need to tie them together :)
I assumed for this that there wouldn't be checking of data and concerns around data in the sources being removed, that you want to retain, so the whole table is re-created everytime.

####Tech Choices
Python. 
I wrote all the jobs in Python because:
1 - it's my most recently familiar language
2 - It keeps the jobs consistent and would be an easier transition for a dev.
3 - Python offers useful data libraries in it's eco-system which are especially useful for cleaning up messy data. It also could be easily ported to a notebook
That being said, it's XML processing is not very sophisticated and I can see the value in other languages that have better tooling for this particular job. 
For this exercise I decided to stick with a consistent approach as it's my preferred approach and I would only change this if needed. For example, in a previous system, we have 1 Spark job in Java because the Pyspark job
was not capable of the customisation we needed.
4 - libraries chosen. I tried to stick with standard and familiar libraries (though I'm sure even that is subjective :) 

Docker for Postgres because it was easier to get a database up and running on my machine

Algorithms - I have favoured space usage over time.
I tried unzipping the file first and then processing it as well as the current configuration. I think the former was slightly faster.
I think this is acceptable especially if you know that the file sizes will be fairly uniform. 
To optimise this, you would be able to make use of threads (in a multi-threaded language) 
to perform different processes (ie reading from files, transforming, writing to output from a queue).