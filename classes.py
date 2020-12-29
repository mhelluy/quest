import re
import time
import functions

class Question:
    def __init__(self, qtype=None, question="", compl = '', choices=None, answer="", expli="", exact_answer=None, time=60, score=100, modact=""):
        self.question = question
        self.choices = choices
        if type(answer) in [int]:
            self.answer = [answer]
        elif type(answer) in [list, tuple, str]:
            self.answer = answer
        self.exact_answer = exact_answer
        self.compl = compl
        self.time = time
        self.score = score
        self.expli = expli
        self.modact = modact
        if qtype is None:
            self.qtype = "choices" if choices is not None else "cash"
        else:
            self.qtype = qtype
        
        self._startime = 0
        self._open = 1

    def isCorrect(self,choice):
        if self.qtype == "choices":
            return 2 if choice in self.answer else 0
        elif self.exact_answer.lower() == choice.lower():
            return 2
        elif re.search(self.answer,choice) is not None:
            return 1
        else:
            return 0
    
    def getAnswer(self,formatted=True):
        if self.qtype == "cash":
            return self.exact_answer
        elif self.qtype == "choices":
            length = len(self.answer)
            toReturn = ""
            for i,answ in enumerate(self.answer):
                toReturn += self.choices[answ]
                if i == length - 2:
                    toReturn += " et "
                elif i != length - 1:
                    toReturn += ", "

            return toReturn
    
    def time_reset(self):
        self._startime = time.time()

    def time_left(self):
        return round(self.time - time.time() + self._startime)
    
    def time_isover(self):
        return time.time() - self._startime >= self.time and self._startime != 0