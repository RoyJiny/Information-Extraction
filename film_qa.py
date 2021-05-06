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
    print(f"question: {q.question}")
    print(f"type:     {q.type}")
    print(f"entity:   {q.entity}")
    print(f"relation: {q.relation}\r\n")
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
    _query = f"select ?x where "\
            "{ "f"<{BASIC_URL}{q.entity}> <{BASIC_URL}{q.relation}> ?x ."\
            "}"
    print(_query)
    res = list(g.query(_query))
    print(res)
    clean_res = []
    for element in res:
        clean_res.append(str(element).replace(f"(rdflib.term.URIREf('{BASIC_URL}","").replace("')",""))
    clean_res.sort()
    return clean_res

def query_general(parse_qst):    
    if (q.type == "GENERAL1") or (q.type == "GENERAL2"):
        _query = f"select ?x where "\
            "{ "f"?x <{BASIC_URL}{q.relation}> ?y ."\
                "}"
    elif q.type == "GENERAL3":
        _query = f"select ?x where "\
            "{ "f"?x <{BASIC_URL}occupation> <{BASIC_URL}{q.relation[0]}> ."\
            f" ?x <{BASIC_URL}occupation> <{BASIC_URL}{q.relation[1]}> ."\
            "}"
    print(_query)
    res = list(g.query(_query))
    print(res)
    return len(res)

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
        print(f"Question: {question}")
        parse_qst = parse_question(question)	
        if not parse_qst:
            print (f"{not parse_qst}")
            print("Can't parse question")
            exit (1)
        elif parse_qst.type == "ENTITY":
            print(retuquery_entity(parse_qst))
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
