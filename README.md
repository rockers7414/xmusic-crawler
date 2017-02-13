# xmusic

The xmusic is the platform which can provide user to search the music video more easily. It will displays more completed information relative the song which you search.

## Features

* You can use the search function to find the interest.
* Display the artist, artist's album and the tracks of the album.
* Display the lyric.

## Development

### Backend

We are going to use the node.js for the RESTful API and using the PostgreSQL as the database. Currently, we'll use the Python 3.x to develop the crawler. The crawler will try to fetch the artists, albums and tracks from the [Spotify](https://www.spotify.com/), and the music video from the [YouTube.com](http://www.youtube.com/). Once the data is enough, we'll define the RESTful API.

### CLI(Command Line Interface)

Because we don't have any interface to access the data, we must have the cli tool for debugging or testing purpose. Using this tool we can query the specific data in the database and fetch the latest data from data provider. 

### Front-end

We'll use the AngularJS2 to develop the front-end.

TBC

### Android and iOS

TBC

