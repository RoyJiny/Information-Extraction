import lxml.html
import requests
import json

ONTHOLOGY_FILE_NAME = "onthology.nt"

###
# onthology dictionary:
# keys - entity name
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
        """ 
        collect and filter the film list
        """
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
        """ 
        after adding all relation from a film, also add the opposite relation between the entity and the film
        """
        if not entity in self.inverse_film_onthology.keys():
            self.inverse_film_onthology[entity] = []
        for relation in self.inverse_film_onthology[entity]:
            if relation.relation_type == relation_type:
                relation.to.append(film)
                return
        new_relation = Relation(relation_type,film)
        self.inverse_film_onthology[entity].append(new_relation)

    def get_sub_url_if_needed(self,doc,original_url,film):
        """
        test if something is needed to be added at the end of the url (e.g. '(film)').
        return the new url if needed, else return None.
        Notes: we want to test the the url has the film name in it (cut it by special characters for easier search).
               take the last name of the list to make sure that if we have more than one year, we take the latest.
               we identify that we are not in the real movie page by the link to 'Help:Disambiguation'.
        """
        film_name_for_sub_url = film.replace(' ','_').split('\'')[0]
        if len(doc.xpath("//a[contains(@href,'Help:Disambiguation')]")) > 0:
            new_url_ending = doc.xpath(f"//a[contains(@href,'film)') and contains(@href,'/{film_name_for_sub_url}') and not(contains(@href,'//id'))]//@href")[-1].split('/')[-1]
            return f"https://en.wikipedia.org/wiki/{new_url_ending}"
        return None

    def collect_wiki_data_by_url(self,url,film):
        """ 
        collect the data from wikipedia for a single film
        """
        res = requests.get(url)
        doc = lxml.html.fromstring(res.content)
        self.film_onthology[film] = []
        possible_new_url = self.get_sub_url_if_needed(doc,url,film)
        if possible_new_url is not None:
            url = possible_new_url
            res = requests.get(url)
            doc = lxml.html.fromstring(res.content)
        
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

    def collect_wiki_data_for_films(self):
        """
        iterate over the film list and collect data for each one
        """
        for film in self.film_list:
            url = f"https://en.wikipedia.org/wiki/{film.replace(' ','_')}"
            self.collect_wiki_data_by_url(url,film)
            if self.film_onthology[film] == []:
                # certain film names (like 'gravity') lead straight to a different wiki page, and not to a Disambiguation page.
                # for almost all of them, adding the _(film) to the end of the url solves the problem.
                self.collect_wiki_data_by_url(f"{url}_(film)",film)

    def create_onthology_file(self):
        """
        create the onthology file from the collected data
        """
        onthology = {
            "direct film relations": self.film_onthology,
            "inverse film relations": self.inverse_film_onthology
        }
        with open('onthology.nt', 'w') as onthology_file:
            json.dump(onthology, onthology_file, cls=OnthologyEncoder)
