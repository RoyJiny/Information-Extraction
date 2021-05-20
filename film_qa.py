from Question import Question
from Onthology import Onthology
from Query import query
from Tester.Tester import test_all

import sys
import os
import rdflib
import timeit

ONTHOLOGY_FILE_PATH = "./onthology.nt"

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
    stop = timeit.default_timer()
    print(f"    done creating onthology, onthology creation runtime: {stop-start} seconds")

def load_onthology():
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
            print(usage,"\nNo question provided")
            exit(1)
        question = sys.argv[2]
        g = load_onthology()
        parse_qst = Question(question)
        print(query(parse_qst,g))
    elif sys.argv[1] == "test":
        g = load_onthology()
        color = False
        if len(sys.argv) > 2 and sys.argv[2] == "--colored": color = True
        if len(sys.argv) > 3 and sys.argv[3] == "--sanity": test_all(g,color,True)
        else: test_all(g,color)
    else:
        print(usage)
        exit(1)
    
    exit(0)
