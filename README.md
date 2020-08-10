##**How to run:**

###There are 2 applications:

#####Wikipedia Abstract Parser

It takes quite long to process the wikipedia data so this was made into a separate application. Theoretically you would run it infrequently to update your wikipedia data
It streams the XML file in in order to not overload the memory of my machine. There are other ways to process this were you can process the data across multiple machines but I created it this way which is to work with my one machine and not overload the memory.

#####Reporting


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
Movies - remove the data that is obviously bad - it adds no value
Wikipedia - data is questionable but good enough to work with. We want to create a new structure that contains only the data we need.
This'll make it quicker to work with the data downstream.

#### Reporting


####Testing

I usually start with tests, most often integration tests (outside-in but no promises that it's textbook). 
I wrote tests to get the data in the first place and use simple tests of 
structure, data types, row & columns counts and checking for required columns.
These can also test the counts of rows are within a range if you expect some fluctuation though I prefer to keep these static (but that's an option if it's suitable for the domain).

####Structure

I ended up moving the functionality into Sources, Feed and Reporting. This didn't take long and helped with splitting out the functionality
