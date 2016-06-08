import re
import json
from mechanize import Browser
from BeautifulSoup import BeautifulSoup


def get_data(movie):
    try:
        movie = '+'.join(movie.split())
        br = Browser()
        br.open("http://www.imdb.com/find?s=tt&q="+movie)
        link = list(br.links(url_regex=re.compile(r"/title/tt*")))[0]
        res = br.follow_link(link)
        soup = BeautifulSoup(res.read())
        title_year = soup.find('span', id='titleYear')
        year_str = str(title_year)
        year = re.search('.*([0-9]{4}).*', year_str).group(1)
        title = soup.find('title').contents[0]
        rate = soup.find('span', itemprop='ratingValue')
        rating = str(rate.contents[0])

        actors = []
        actors_soup = soup.findAll('span', itemprop='actors')
        for actor in actors_soup:
            actor_str = str(actor)
            actor_garbage = actor_str.rpartition('itemprop="name"')[-1]
            actors.append(re.search('\>(.*?)\<', actor_garbage).group(1))

        directors = []
        director_soup = soup.findAll('span', itemprop='director')
        for director in director_soup:
            director_str = str(director)
            director_garbage = director_str.rpartition('itemprop="name"')[-1]
            directors.append(re.search('\>(.*?)\<', director_garbage).group(1))

        votes = soup.find('span', itemprop='ratingCount').contents[0]
        response = []
        response.append({"Movie : ": title})
        response.append({"Rating: ": rating})
        response.append({"Votes ": votes})
        response.append({"Release Year : ": year})
        response.append({"Director : ": directors})
        response.append({"Actors : ": actors})
        return json.dumps(response)
    except:
        print "Not Found! or a future movie"
        exit()

movie = "lagaan"
get_data(movie)
