from Question import Question
from Onthology import Onthology

import sys

def parse_question(question_str):
    q = Question(question_str)
    print(f"question: {q.question}")
    print(f"type:     {q.type}")
    print(f"entity:   {q.entity}")
    print(f"relation: {q.relation}\r\n")

def create_onthology():
    print("creating onthology:")
    onthology = Onthology("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
    print("    collecting films")
    onthology.collect_film_list()
    print("    collecting data for films")
    onthology.collect_wiki_data_for_films()
    print("    creating onthology.nt")
    onthology.create_onthology_file()
    print("done creating onthology")


if __name__ == "__main__":
    # usage = "USAGE: python film_qa.py create | python film_qa.py question <question>"
    # if len(sys.argv) < 2:
    #     print(usage)
    #     exit(1)
    # if sys.argv[1] == "create":
    #     print("Creating ontology.nt")
    # elif sys.argv[1] == "question":
    #     if len(sys.argv) < 3:
    #         print("No question provided")
    #         exit(1)
    #     question = sys.argv[2]
    #     print(f"Question: {question}")
    # else:
    #     print(usage)
    #     exit(1)

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

    create_onthology()