# SI507_project4

<h1>Hello. Thanks for reading about this National Park Service Scraping Program.</h1>

<h2>This project for SI507 requires that you have python 3.7, Beautiful Soup, SQLlite and others that provides opportunity to interact with scaped website data to aggregate it, read and write it in an organized CSV. </h2>
<h3>This program has two main files, and will create 3 - a SQLLite database, CSV and a json cache file. In order for this project to work properly, please refer to the required list of dependencies in requirements.txt and pip-install all dependencies to a virtual environment within the project folder for this application to run.</h3>

<h4> There are two different types of files in this program, the SI507_project4.py code where CSV and beautiful soup are used to scrape the national parks website and create a csv.</h4>
<h4>Secondly, In the code for db_setup, a SQL database is created with SQLAlchemy so you can browse around the data in SQL. There are 3 tables that are created, a relationship table, a states table and a table for the national parks from cached data off the http://www.nps.gov website.</h4>

<h3> What does the main file do? </h3>

<h4> This file defines two different functions: open_cache and cache_data!</h4>
- open_cache function works by taking the file name and then read contents into a dictionary. If there's an error along the way an empty dictionary is created and is returned.

- cache_data function takes in four inputs the cache file name, the cached dictionary, the url as a string for the data, and new data if any; the function adds the new data to the dictionary where the url is a key and the value as the new data, the dictionary is then saved into the cache file.

- this file also creates a csv file after creating a database with the returned data.



<h3>In order for this code to run, you must clone my repository to your local machine. Start off and place it right onto your mac desktop.</h3>

- make sure all dependencies are installed within the project folder as a virtual environment. see this for more information on virtual environments and how to create and use one intelligently: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/ 

- Open up your terminal window and type $ cd desktop (navigate to the location).
- Now in the command prompt window, type $ python SI507_project4.py ( this runs the flask application and creates an empty database)
- You should be able to see something going on in your terminal window. (terminal is displaying the URL calls directed to your local host port)
- The process for creating a database and then csv file after caching all the scraped infromation from nps.gov might take a few seconds or minutes the first time! There's a lot of data being cached and creating a database takes time for the program to scrape every state's individual website.  
