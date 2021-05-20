import re

# (regex,relation,entity_extractor)
entity_question_bank = [
    (
        r"Who directed .*",
        "Directed_by",
        lambda q_str: [q_str.split("Who directed ")[1]]
    ),
    (
        r"Who produced .*",
        "Produced_by",
        lambda q_str: [q_str.split("Who produced ")[1]]
    ),
    (
        r"Is .* based on a book",
        "Based_on",
        lambda q_str: [q_str[3:].split(" based on")[0]]
    ),
    (
        r"When was .* released",
        "Release_date",
        lambda q_str: [q_str.split("When was ")[1].split(" released")[0]]
    ),
    (
        r"How long is .*",
        "Running_time",
        lambda q_str: [q_str.split("How long is ")[1]]
    ),
    (
        r"Who starred in .*",
        "Starring",
        lambda q_str: [q_str.split("Who starred in ")[1]]
    ),
    (
        r"Did .* star in .*",
        "Starring",
        lambda q_str: [q_str.split("Did ")[1].split(" star in")[0], q_str.split("star in ")[1]]
    ),
    (
        r"When was .* born",
        "Bday",
        lambda q_str: [q_str.split("When was ")[1].split(" born")[0]]
    ),
    (
        r"In what language is the film .*",
        "Language",
        lambda q_str: [q_str.split("In what language is the film ")[1]]
    ),
    (
        r"What is the occupation of .*",
        "Occupation",
        lambda q_str: [q_str.split("What is the occupation of ")[1]]
    )
]

filter_regex = re.compile('[^a-zA-Z0-9\-_\.!?$,\\/() %]') # remove weird characters that rdf won't accept as a url

class Question:
    def __init__(self, question_str):
        self.type = None
        self.entity = None
        self.relation = None
        self.question = filter_regex.sub('',question_str)
        question_str = question_str.replace('?','')
        question_str = question_str.replace(':','')

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
        if re.search(r"How many films starring .* won an academy award", question_str):
            self.type = "GENERAL2"
            self.relation = "Starring"
            self.entity = [question_str.split("How many films starring ")[1].split(" won an academy award")[0]][0].replace(" ", "_")
            return
        if re.search(r"How many .* are also .*", question_str):
            self.type = "GENERAL3"
            self.relation = [question_str.split("How many ")[1].split(" are also")[0].replace(" ", "_"),question_str.split(" are also ")[1].replace(" ", "_")]
            return

        raise ValueError("Couldn't match question")
