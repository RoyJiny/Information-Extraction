import lxml.html
import requests

class Onthology:
    def __init__(self,URL):
        self.URL = URL
        self.film_list = []

    def collect_film_list(self):
        res = requests.get(self.URL)
        doc = lxml.html.fromstring(res.content)
        for tablerow in doc.xpath(".//table[1]//tr"):
            try:
                filmname = tablerow.xpath("./td[1]/i/a/text()")[0]
                year = tablerow.xpath("./td[2]/a/text()")[0]
                if int(year) >= 2010:
                    self.film_list.append(filmname)
            except:
                pass

    def collect_wiki_data_for_films(self):
        for film in self.film_list:
            url = f"https://en.wikipedia.org/wiki/{film.replace(' ','_')}"
            # print(f"film: {film}")
            res = requests.get(url)
            doc = lxml.html.fromstring(res.content)
            for tablerow in doc.xpath("//table[contains(@class,'infobox')]//tr//th[@class='infobox-label']"):
                try:
                    label = tablerow.xpath(".//text()")[0]
                    value = tablerow.xpath("../td/a//text()") + tablerow.xpath("../td/text()") + tablerow.xpath("../td//li//text()")
                    # print(label,value)
                except:
                    pass
