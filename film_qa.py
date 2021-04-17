from Question import Question
# from Onthology import Onthology

import sys
import os
import json
import re

ONTHOLOGY_FILE_PATH = "./onthology.nt"

def parse_question(question_str):
    q = Question(question_str)
    print(f"question: {q.question}")
    print(f"type:     {q.type}")
    print(f"entity:   {q.entity}")
    print(f"relation: {q.relation}\r\n")
    return q

def create_onthology():
    print("creating onthology")
    onthology = Onthology("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
    onthology.collect_film_list()
    onthology.collect_wiki_data_for_films()

def search_in_onthology(parse_qst):
    print("searching in the onthology")
    if parse_qst.type == "ENTITY":
        answer = search_entity_question(parse_qst)
    else: 
        pass
    return answer

def open_file ():
    if not os.path.exists(ONTHOLOGY_FILE_PATH):
        print("file not found")
        exit(1)
    if not os.path.isfile(ONTHOLOGY_FILE_PATH):
        print("file not found")
        exit(1)
    try:
        fd = open(ONTHOLOGY_FILE_PATH, "r")
    except FileNotFoundError :
        print("Can't open onthology file")
        exit(1)
    return fd

def search_entity_question(parse_qst):
    file = open_file()
    data = json.load(file)
    entity_relations = get_entity(data,parse_qst)
    for relation in entity_relations:
        if re.search(parse_qst.relation.lower(), relation.get("relation_type").lower()):
            return relation.get("to")
    print("Can't find entity")
    return

def get_entity(data,parse_qst):
    """ 
    Briff: go over all keys in the json file.
    Return: a list with all the entitys.
    """
    entity_list = []
    for entity in data.get("direct film relations"):
        if parse_qst.entity == entity:
            return data.get("direct film relations").get(entity)
    print("Can't find entity")
    exit(1)


if __name__ == "__main__":
    usage = "USAGE: python film_qa.py create | python film_qa.py question <question>"
    if len(sys.argv) < 2:
        print(usage)
        exit(1)
    if sys.argv[1] == "create":
        print("Creating ontology.nt")
        create_onthology()
    elif sys.argv[1] == "question":
        if len(sys.argv) < 3:
            print("No question provided")
            exit(1)
        question = sys.argv[2]
        print(f"Question: {question}")
        parse_qst = parse_question(question)	
        if not parse_qst:
            print (f"{not parse_qst}")
            print("Can't parse question")
            exit (1)
        else:
           print(search_in_onthology(parse_qst))
    else:
        print(usage)
        exit(1)

    # parse_question("Who directed FILM 2?")
    # parse_question("Who produced FILM 2?")
    # parse_question("Is FILM 2 based on a book?")
    # parse_question("When was FILM 2 released?")
    # parse_question("How long is FILM 2?")
    # parse_question("Who starred in FILM 2?")
    # parse_question("Did Roy Jiny star in FILM 2?")
    # parse_question("When was Roy Jiny born?")
    # parse_question("What is the occupation of Roy Jiny?")
    # parse_question("How many films are based on books?")
    # parse_question("How many films starring Roy Jiny won an academy award?")
    # parse_question("How many teachers are also dancers?")

    # create_onthology()