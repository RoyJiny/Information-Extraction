from Question import Question
from Onthology import Onthology

import sys
import os
import json
import re
import rdflib
import timeit

ONTHOLOGY_FILE_PATH = "./onthology.nt"
BASIC_URL = "https://en.wikipedia.org/wiki/"

def parse_question(question_str):
    q = Question(question_str)
    # print(f"question: {q.question}")
    # print(f"type:     {q.type}")
    # print(f"entity:   {q.entity}")
    # print(f"relation: {q.relation}\r\n")
    return q

def create_onthology():
    start = timeit.default_timer()
    print("creating onthology:") 
    onthology = Onthology("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
    print("    collecting films")
    onthology.collect_film_list()
    print("    collecting data for films")
    onthology.collect_wiki_data_for_films()
    print("    collecting data for related entities")
    onthology.collect_wiki_data_for_other_entities()
    print("    creating data graph")
    onthology.create_graph()
    print("    creating onthology.nt")
    onthology.create_onthology_file()
    print("done creating onthology")
    stop = timeit.default_timer()
    print(f"onthology creation runtime: {stop-start} seconds")

def query_entity(parse_qst):
    entity = parse_qst.entity[0].replace(" ", "_")
    _query = f"select ?x where {'{'}"\
            " "f"<{BASIC_URL}{entity}> <{BASIC_URL}{parse_qst.relation}> ?x ."\
            "}"
    # print(_query)
    res = list(g.query(_query))
    _query = f"select ?x where {'{'}"\
            " "f"<{BASIC_URL}{entity}> <{BASIC_URL}inverse/{parse_qst.relation}> ?x ."\
            "}"
    # print(_query)
    for ret in list(g.query(_query)):
        res.append(ret)
    # print(res)
    if (parse_qst.relation == "Based_on"):
        if len(res):
            return "Yes"
        else:
            return "No"
    clean_res = []
    for element in res:
        clean_element = str(element).replace(f"(rdflib.term.URIRef('{BASIC_URL}","").replace("'),)","")
        if (parse_qst.relation == "Release_date"):
            clean_element = clean_element.split(",(,")[1].split(",),")[0]
            # if re.search(",(,", clean_element):
            #     clean_element = clean_element.split(",(,")[1]
            # if re.search(",),", clean_element):
            #     clean_element = clean_element.split(",),")[0]
        clean_res.append(clean_element.strip().replace("_"," "))
    if len(parse_qst.entity) > 1:
        for element in clean_res:
            if re.search(parse_qst.entity[1],element):
                return "Yes"
        return "No"
    clean_res.sort()
    return clean_res

def query_general(parse_qst):    
    if (parse_qst.type == "GENERAL1"):
        _query = f"select ?x where {'{'}"\
            " "f"?x <{BASIC_URL}{parse_qst.relation}> ?y ."\
                "}"
    elif parse_qst.type == "GENERAL2":
        _query = f"select ?x where {'{'}"\
            " "f"?x <{BASIC_URL}{parse_qst.relation}> <{BASIC_URL}{parse_qst.entity}> ."\
                "}"
    elif parse_qst.type == "GENERAL3":
        _query = f"select ?x where {'{'}"\
            " "f"?x <{BASIC_URL}occupation> <{BASIC_URL}{parse_qst.relation[0]}> ."\
            f" ?x <{BASIC_URL}occupation> <{BASIC_URL}{parse_qst.relation[1]}> ."\
            "}"
    else:
        print("Couldn't match question")
        exit(1)
    res = list(g.query(_query))
    return len(res)

def open_file ():
    if not os.path.exists(ONTHOLOGY_FILE_PATH):
        print("file not found")
        exit(1)
    if not os.path.isfile(ONTHOLOGY_FILE_PATH):
        print("file not found")
        exit(1)
    try:
        onthology = rdflib.Graph()
        onthology.parse("onthology.nt", format="nt")
    except:
        print("Can't open onthology file")
        exit(1)
    return onthology


if __name__ == "__main__":
    usage = "USAGE: python film_qa.py create | python film_qa.py question <question>"
    if len(sys.argv) < 2:
        print(usage)
        exit(1)
    if sys.argv[1] == "create":
        create_onthology()
    elif sys.argv[1] == "question":
        if len(sys.argv) < 3:
            print(usage)
            print("No question provided")
            exit(1)
        question = sys.argv[2]
        # print(f"Question: {question}")
        g = open_file()
        parse_qst = parse_question(question)	
        if not parse_qst:
            print (f"{not parse_qst}")
            print("Can't parse question")
            exit (1)
        elif parse_qst.type == "ENTITY":
            answers = query_entity(parse_qst)
            if isinstance(answers,list):
                answers = ', '.join(answers)
            print(answers)
            exit(1)
        else:
            print(query_general(parse_qst))
            exit(1)
    else:
        print(usage)
        exit(1)

    # parse_question("Who directed FILM 2?")
    # parse_question("Who produced FILM 2?")
    # parse_question("Is FILM 2 based on a book?")
    # parse_question("Is The Jungle Book (2016 film) based on a book?")
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
    exit(0)
