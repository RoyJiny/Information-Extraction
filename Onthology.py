import lxml.html
import requests
import json
import re
import rdflib

ONTHOLOGY_FILE_NAME = "onthology.nt"
BASIC_URL = "https://en.wikipedia.org/wiki/"

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
        self.other_entity_onthology = {}
        self.other_entity_list = []
        self.graph = rdflib.Graph()

    def collect_film_list(self):
        """ collect and filter the film list """
        res = requests.get(self.URL)
        doc = lxml.html.fromstring(res.content)
        for tablerow in doc.xpath(".//table[1]//tr"):
            try:
                filmname = tablerow.xpath("./td[1]/i//a/@href")[0].split("/")[-1]    # get the exact name by the href url ("/wiki/film_name")
                year = tablerow.xpath("./td[2]/a/text()")[0]
                if int(year) >= 2010:
                    self.film_list.append(filmname)
            except Exception as e:
                pass
    
    def collect_wiki_data_by_url(self,url,film):
        """ collect the data from wikipedia for a single film """
        try:
            res = requests.get(url,timeout=10)
        except:
            print(f"Error: got timeout (after 10 seconds) when fetching web data for film'{film}'\nurl: {url}")
            return
        doc = lxml.html.fromstring(res.content)
        self.film_onthology[film] = []
        
        for tablerow in doc.xpath("//table[contains(@class,'infobox')][1]//tr//th[@class='infobox-label']"):
            try:
                label = tablerow.xpath(".//text()")[0]
                if label not in ["Directed by","Produced by","Based on", "Release date", "Running time", "Starring", "Bday", "Occupation", "Language"]:
                    continue
                value = tablerow.xpath("../td/a//text()") + tablerow.xpath("../td/text()") + tablerow.xpath("../td/i//text()") + tablerow.xpath("../td/span//text()")
                is_under_list = False
                for list_element in tablerow.xpath("../td//div/ul/li")+tablerow.xpath("../td/ul/li"):
                    added_val = ",".join([text for text in list_element.xpath(".//*[not(self::a)]/text()") if not re.search(r"\[[0-9]*\]", text)]) # remove [1],[2]... fields
                    added_val += ",".join([text.replace("/wiki/","") for text in list_element.xpath(".//a/@href")])
                    value.append(added_val)
                    is_under_list = True
                if not is_under_list:
                    value += tablerow.xpath("../td/div//text()")
                
                if value == []:
                    continue

                if label == "Based on":
                    value = ["".join(value)] # for based on the result is ["book name","by","writer"], so concat them all together

                relation = Relation(label,value)
                self.film_onthology[film].append(relation)
                for entity in value:
                    self.other_entity_list.append(entity)
            except Exception as e:
                # print(f"parsing error.\nerror:{str(e)}\nfilm: {film}\nlabel:{label}\nvalue:{value}\n")
                pass

    def collect_wiki_data_for_films(self):
        """ iterate over the film list and collect data for each one """
        for film in self.film_list:
            url = f"https://en.wikipedia.org/wiki/{film.replace(' ','_')}"
            self.collect_wiki_data_by_url(url,film)

    def collect_wiki_data_for_other_entities(self):
        """ collect the wikipedia data for any entity that has a relation to one of the films """
        for entity in self.other_entity_list:
            url = f"https://en.wikipedia.org/wiki/{entity.replace(' ','_')}"
            try:
                res = requests.get(url,timeout=10)
            except:
                print(f"Error: got timeout (after 10 seconds) when fetching web data for entity'{entity}'\nurl: {url}")
                return
            doc = lxml.html.fromstring(res.content)

            value_bday = doc.xpath("//span[@class='bday']//text()")
            if value_bday == []:
                value_bday = doc.xpath("//th[text()='Born']/../td//text()")    
            value_occupation = doc.xpath("//th[text()='Occupation']/../td//text()")
            if value_occupation != []:
                if len(value_occupation) == 1:
                    value_occupation = [text.replace(" ","",1).replace(" ","_") for text in value_occupation[0].split(",") if text != "\n"]
            if value_bday != [] or value_occupation != []:
                relation_bday = Relation("Bday",value_bday)
                relation_occupation = Relation("Occupation",value_occupation)
                self.other_entity_onthology[entity] = [relation_bday,relation_occupation]

    def create_graph(self):
        """ create the rdflib graph """
        filter_regex = re.compile('[^a-zA-Z0-9\-_\.!?$,\\/() ]') # remove weird characters that rdf won't accept as a url
        
        for film in self.film_onthology.keys():
            for relation in self.film_onthology[film]:
                label = relation.relation_type
                for entity in relation.to:
                    filtered_film = filter_regex.sub('',film)
                    filtered_label = filter_regex.sub('',label)
                    filtered_entity = filter_regex.sub('',entity)
                    e1 = rdflib.URIRef(f'{BASIC_URL}{filtered_film.replace(" ","_")}')
                    r = rdflib.URIRef(f'{BASIC_URL}{filtered_label.replace(" ","_")}')
                    e2 = rdflib.URIRef(f'{BASIC_URL}{filtered_entity.replace(" ","_")}')
                    self.graph.add((e1,r,e2))
        
        for entity in self.other_entity_onthology.keys():
            for relation in self.other_entity_onthology[entity]:
                label = relation.relation_type
                for value in relation.to:
                    filtered_entity = filter_regex.sub('',entity)
                    filtered_label = filter_regex.sub('',label)
                    filtered_value = filter_regex.sub('',value)
                    e1 = rdflib.URIRef(f'{BASIC_URL}{filtered_entity.replace(" ","_")}')
                    r = rdflib.URIRef(f'{BASIC_URL}{filtered_label.replace(" ","_")}')
                    e2 = rdflib.URIRef(f'{BASIC_URL}{filtered_value.replace(" ","_")}')
                    self.graph.add((e1,r,e2))

    def create_onthology_file(self):
        """ create the onthology file from the collected data """
        self.graph.serialize("onthology.nt", format="nt")
        self.graph.parse("onthology.nt", format="nt")
