# COMPSCI 235 Repository for Assignment 2
This is a  repository for the assignment 2 of CompSci 235 in Semester 2, 2022. This project is made by Ruth Kha (rkha332) and Jason Gao (jgao134).


## Description
This application allows user to browse and query tracks from the provided database, as well as make playlists. 

Navigation Bar functions:

Browse Tracks: 

User can browse all tracks in the dataset by navigating through pages. They can click "Add" to add track to playlist or "Review" to leave a comment. 

Browse Artists: 

User can browse artists. If user clicks on artist's name, they are redirected to a page of tracks by said artist. 

Browse Genres: 

User can browse all genres. Genre names do not have function on click as this is an MVP. 

Browse Albums: 

User can browse albums - no onclick function as above. 

Search Tracks:

User can query tracks by title, genre, artist or album.

Playists: 

User can browse the pre-loaded playlist 'Developer's Picks', create their own playlist or generate a random one. A design report on this feature is located in the root directory.

Authentication is used to restrict leaving reviews and creating playlists to existing users. 

## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

 
## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.
