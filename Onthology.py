import lxml.html
import requests
import json

ONTHOLOGY_FILE_NAME = "onthology.nt"

###
# onthology film dictionary:
# keys - film name
# values - array of relations, each has a type and a "to" field
###

class Relation:
    def __init__(self,relation_type,to):
        self.relation_type = relation_type
        self.to = to

    def __str__(self):
        return f"type: {self.relation_type}, to: {self.to}"
    
    def __repr__(self):
        return f"type: {self.relation_type}, to: {self.to}"

class OnthologyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Relation): 
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

class Onthology:
    def __init__(self,URL):
        self.URL = URL
        self.film_list = []
        self.film_onthology = {}
        self.inverse_film_onthology = {}

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

    def add_inverse_relation(self,film,relation_type,entity):
        if not entity in self.inverse_film_onthology.keys():
            self.inverse_film_onthology[entity] = []
        for relation in self.inverse_film_onthology[entity]:
            if relation.relation_type == relation_type:
                relation.to.append(film)
                return
        new_relation = Relation(relation_type,film)
        self.inverse_film_onthology[entity].append(new_relation)

    def collect_wiki_data_for_films(self):
        for film in self.film_list:
            url = f"https://en.wikipedia.org/wiki/{film.replace(' ','_')}"
            res = requests.get(url)
            doc = lxml.html.fromstring(res.content)
            self.film_onthology[film] = []
            for tablerow in doc.xpath("//table[contains(@class,'infobox')]//tr//th[@class='infobox-label']"):
                try:
                    label = tablerow.xpath(".//text()")[0]
                    value = tablerow.xpath("../td/a//text()") + tablerow.xpath("../td/text()") + tablerow.xpath("../td//li//text()")
                    relation = Relation(label,value)
                    self.film_onthology[film].append(relation)
                    for entity in value:
                        self.add_inverse_relation(film,label,entity)
                except:
                    pass

    def create_onthology_file(self):
        onthology = {
            "direct film relations": self.film_onthology,
            "inverse film relations": self.inverse_film_onthology
        }
        with open('onthology.nt', 'w') as onthology_file:
            json.dump(onthology, onthology_file, cls=OnthologyEncoder)
