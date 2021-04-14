from Question import Question

import sys

def parse_question(question_str):
    q = Question(question_str)
    print(f"question: {q.question}")
    print(f"type:     {q.type}")
    print(f"entity:   {q.entity}")
    print(f"relation: {q.relation}\r\n")


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

    parse_question("Who directed FILM 2?")
    parse_question("Who produced FILM 2?")
    parse_question("Is FILM 2 based on a book?")
    parse_question("When was FILM 2 released?")
    parse_question("How long is FILM 2?")
    parse_question("Who starred in FILM 2?")
    parse_question("Did Roy Jiny star in FILM 2?")
    parse_question("When was Roy Jiny born?")
    parse_question("What is the occupation of Roy Jiny?")
    parse_question("How many films are based on books?")
    parse_question("How many films starring Roy Jiny won an academy award?")
    parse_question("How many teachers are also dancers?")
