import re

# (regex,relation,entity_extractor)
entity_question_bank = [
    (
        r"Who directed [()a-zA-Z0-9\s]*",
        "Directed_by",
        lambda q_str: [q_str.split("Who directed ")[1]]
    ),
    (
        r"Who produced [()a-zA-Z0-9\s]*",
        "Produced_by",
        lambda q_str: [q_str.split("Who produced ")[1]]
    ),
    (
        r"Is [()a-zA-Z0-9\s]* based on a book",
        "Based_on",
        lambda q_str: [q_str.split("Is ")[1].split(" based on")[0]]
    ),
    (
        r"When was [()a-zA-Z0-9\s]* released",
        "Release_date",
        lambda q_str: [q_str.split("When was ")[1].split(" released")[0]]
    ),
    (
        r"How long is [()a-zA-Z0-9\s]*",
        "Running_time",
        lambda q_str: [q_str.split("How long is ")[1]]
    ),
    (
        r"Who starred in [()a-zA-Z0-9\s]*",
        "Starring",
        lambda q_str: [q_str.split("Who starred in ")[1]]
    ),
    (
        r"Did [()a-zA-Z0-9\s]* star in [()a-zA-Z0-9\s]*",
        "Starring",
        lambda q_str: [q_str.split("Did ")[1].split(" star in")[0], q_str.split("star in ")[1]]
    ),
    (
        r"When was [()a-zA-Z0-9\s]* born",
        "Bday",
        lambda q_str: [q_str.split("When was ")[1].split(" born")[0]]
    ),
    (
        r"What is the occupation of [()a-zA-Z0-9\s]*",
        "Occupation",
        lambda q_str: [q_str.split("What is the occupation of ")[1]]
    )
]

class Question:
    def __init__(self, question_str):
        self.type = None
        self.entity = None
        self.relation = None
        self.question = question_str
        question_str = question_str.replace('?','')

        for question in entity_question_bank:
            if re.search(question[0], question_str):
                self.type = "ENTITY"
                self.relation = question[1]
                self.entity = question[2](question_str)
                for ent in self.entity:     
                    ent.replace(" ", "_")
                return

        # special general questions:
        if re.search(r"How many films are based on books", question_str):
            self.type = "GENERAL1"
            self.relation = "Based_on"
            return
        if re.search(r"How many films starring [()a-zA-Z0-9\s]* won an academy award", question_str):
            self.type = "GENERAL2"
            self.relation = "Starring"
            self.entity = [question_str.split("How many films starring ")[1].split(" won an academy award")[0]][0].replace(" ", "_")
            return
        if re.search(r"How many [()a-zA-Z0-9\s]* are also [()a-zA-Z0-9\s]*", question_str):
            self.type = "GENERAL3"
            self.relation = [question_str.split("How many ")[1].split(" are also")[0],question_str.split(" are also ")[1]]
            return

        print("Couldn't match question")