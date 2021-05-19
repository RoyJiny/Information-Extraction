import re

BASIC_URL = "https://en.wikipedia.org/wiki/"

def query_entity(parse_qst,g):
    entity = parse_qst.entity[0].replace(" ", "_")
    _query = f"select ?x where {'{'}"\
            " "f"<{BASIC_URL}{entity}> <{BASIC_URL}{parse_qst.relation}> ?x ."\
            "}"
    res = list(g.query(_query))
    _query = f"select ?x where {'{'}"\
            " "f"?x <{BASIC_URL}{parse_qst.relation}> <{BASIC_URL}{entity}> ."\
            "}"
    for ret in list(g.query(_query)):
        res.append(ret)
    if (parse_qst.relation == "Based_on"):
        if len(res):
            return "Yes"
        else:
            return "No"
    clean_res = []
    for element in res:
        clean_element = str(element).replace(f"(rdflib.term.URIRef('{BASIC_URL}","").replace("'),)","")
        if parse_qst.relation == "Release_date":
            clean_element = clean_element.strip('(').strip(')').strip(',')
        clean_res.append(clean_element.strip().replace("_"," "))
    
    if len(parse_qst.entity) > 1:
        for element in clean_res:
            if parse_qst.entity[1] in element:
                return "Yes"
        return "No"
    
    if parse_qst.relation == "Occupation":
        clean_res = [text.lower() for text in clean_res]
    
    clean_res.sort()
    return clean_res

def query_general(parse_qst,g):    
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
            " "f"?x <{BASIC_URL}Occupation> <{BASIC_URL}{parse_qst.relation[0]}> ."\
            " "f"?x <{BASIC_URL}Occupation> <{BASIC_URL}{parse_qst.relation[1]}> ."\
            "}"
        print(_query)
    else:
        raise ValueError("Couldn't match question")
    res = list(g.query(_query))
    return str(len(res))


def query(question, onthology):
    if not question:
        raise ValueError("Can't parse question")
    elif question.type == "ENTITY":
        answers = query_entity(question,onthology)
        if isinstance(answers,list):
            answers = ', '.join(answers)
        return answers
    else:
        return query_general(question,onthology)
