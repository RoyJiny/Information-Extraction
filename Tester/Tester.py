from Query import query
from Question import Question
from colorama import Fore, init, Style

def test(question,answer,onthology,colored):
    if colored: print(Fore.WHITE, end="")
    print(f"\nQ: {question}")
    q = Question(question)
    res = query(q,onthology)
    if res != answer:
        if colored: print(Fore.RED, end="")
        print(f"Expected: '{answer}'")
        if colored: print(Fore.RED, end="")
        print(f"Actual:   '{res}'")
        return 1
    else:
        if colored: print(Fore.GREEN, end="")
        print(f"A: {res}")
        return 0

questions = [
    # given questions:
    ("Who directed Bao (film)?","Domee Shi"),
    ("Who produced 12 Years a Slave (film)","Anthony Katagas, Arnon Milchan, Bill Pohlad, Brad Pitt, Dede Gardner, Jeremy Kleiner, Steve McQueen"),
    ("Is The Jungle Book (2016 film) based on a book?","Yes"),
    ("When was The Great Gatsby (2013 film) released?","2013-05-01, 2013-05-10, 2013-05-30"),
    ("How long is Coco (2017 film)?","105 minutes"),
    ("Who starred in The Shape of Water?","Doug Jones (actor), Michael Shannon, Michael Stuhlbarg, Octavia Spencer, Richard Jenkins, Sally Hawkins"),
    ("Did Octavia Spencer star in The Shape of Water?","Yes"),
    ("When was Chadwick Boseman born?","1976-11-29"),
    ("What is the occupation of Emma Watson?","activist, actress, model"),
    ("How many films starring Meryl Streep won an academy award?","2"),
    ("Who produced Brave (2012 film)?","Katherine Sarafian"),
    ("Is The Brave (2012 film) based on a book?","No"),
    # uniqe question
    ("In what language is the film Colette_(2020_film)?","French")    
]


def test_all(onthology,colored,just_sanity=False):
    if colored: init()
    print("Running Tester\n")
    if just_sanity: print("[just sanity check]")
    error_count = 0
    
    if not just_sanity:
        q_file = open("./Tester/questions.txt",'r')
        a_file = open("./Tester/answers.txt",'r')
        for q_line in q_file:
            a_line = a_file.readline()
            questions.append((q_line.replace('\n','').replace('\r',''),a_line.replace('\n','').replace('\r','')))    
        q_file.close()
        a_file.close()

    for q in questions:
        try:
            error_count += test(q[0],q[1],onthology,colored)
        except Exception as e:
            if colored: print(Fore.RED, end="")
            print(f"Error: {str(e)}")
            error_count += 1
    
    if colored: print(Style.RESET_ALL)
    print(f"\n\ncorrect: {len(questions)-error_count}")
    print(f"wrong: {error_count}")
    print(f"correctness: {(1-error_count/len(questions))*100} %")
