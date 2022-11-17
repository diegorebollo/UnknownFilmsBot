<div align="center">

![](https://static.drebollo.dev/UnknownFilmsBot/ufb_120x120.png)

# Unknown Films Bot
A simple Python Script that tweets a random unknown film using [The Movie Database API](https://www.themoviedb.org/)

----
<div align="left">

  
This repository contains the source code behind the Twitter "bot" account [@unknownfilms_](https://twitter.com/unknownfilms_)
    
The script just picks a random year and queries the TMDB API to find movies from that year that have less than 50 votes. Picks one and if the movie has a poster image and the total length of text is less than 280 characters tweets it.
    
# Dependencies 
* [Requests](https://github.com/psf/requests)
* [Tweepy](https://github.com/tweepy/tweepy)
    
# Licence
GNU General Public License v3.0
