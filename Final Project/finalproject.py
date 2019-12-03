# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:40:33 2019

@author: jcbol
"""
from math import log

def compare_dictionaries(d1, d2):
    """
    return a similarity score for two dictionaries
    """
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    for x in d2:
        if x in d1:
            log_sim_score =  d2[x]*log(d1[x]/total)
        else:
            log_sim_score =  d2[x]*log(0.5/total)
        score+=log_sim_score
    return log_sim_score
            

def test():
    """ test w generic string sources """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
    
def run_tests():
    """ test with txt files """
    source1 = TextModel('atlantic')
    source1.add_file('atlantic.txt')

    source2 = TextModel('breitbart')
    source2.add_file('breitbart.txt')

    new1 = TextModel('test')
    new1.add_file('motherjones.txt')
    new1.classify(source1, source2)
    
    
    
def stem(s):
    """accepts a string as a parameter and returns the stem of that string"""
    if (s[-3:]=='ing' or s[-3:]=="ity" or s[-3:] == "ily" or s[-3:] == "ers") and len(s)>3:
        s = s[:-3]
    if (s[-4:] == "tion" or s[-4:] == "sion" or s[-4:] == "ible") and len(s)>4:
        s = s[:-4]
    if s[:3] == "con":
        s = s[3:]
    if (s[:2] == "un" or s[:2] == "re" or s[:2] == "es") and len(s)>2:
        s = s[2:]
    if s[:4] == "anti" and len(s)>4:
        s = s[4:]
    if s[-1] == 'e' and len(s)>1:
        s = s[:-1]
    if s[-1] == 'y' and len(s)>1:
        s = s[:-1]
        s += 'i'
    return s
        
        
        
def clean_text(txt):
    """remove punctuation and other symbols from string"""
    for x in ",.!?\()*&^%$#@/[]":
        txt = txt.replace(x, "")
    txt = txt.replace("\n","")
    txt = txt.lower()
    return txt.split(" ")
    
    
    
class TextModel:
    def __init__(self, model_name):
       """constructor"""
       self.name = model_name
       self.words = {}
       self.word_lengths = {}
       self.stems = {}
       self.sentence_lengths = {}
       self.punctuation = {}
       
    def __repr__(self):
        """a representation of the class when printed"""
        return "text model name: " + self.name + "\nnumber of words: " + str(len(self.words)) + "\nnumber of word lengths: " + str(len(self.word_lengths)) + "\nnumber of stems: " + str(len(self.stems)) + "\nnumber of sentence lengths: " + str(len(self.sentence_lengths))  + "\nnumber of punctuation/symbols: " + str(len(self.punctuation)) 
    
    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        counter = 1
        for i in s:
            if i == " ":
                counter += 1
            if i in "!.?":
                if str(counter) not in self.sentence_lengths:
                    self.sentence_lengths[str(counter)] = 1
                else:
                    self.sentence_lengths[str(counter)] += 1
                counter = 1
            if i in "!,.?/@#$%^&*()-+{}[]":
                if i not in self.punctuation:
                    self.punctuation[i] = 1
                else:
                    self.punctuation[i] += 1
            
        
        word_list = clean_text(s)
    
        # Template for updating the words dictionary.
        for w in range(len(word_list)):
            if word_list[w] != "":
                if word_list[w] not in self.words:
                    try:
                        self.words[word_list[w]] = 1
                    except:
                        print(w)
                else:
                    if w+1 < len(word_list):
                        self.words[word_list[w]] = self.words[word_list[w]] + 1
                if str(len(word_list[w])) not in self.word_lengths:
                    self.word_lengths[str(len(word_list[w]))] = 1
                else:
                    self.word_lengths[str(len(word_list[w]))] += 1
               
                if stem(word_list[w]) not in self.stems:
                    self.stems[stem(word_list[w])] = 1
                else:
                    self.stems[stem(word_list[w])] += 1
           
                
                
    def add_file(self, filename):
        """adds a file to the model through filename
        """
        
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file = f.read()
        self.add_string(file)
        f.close()
        
    def read_model(self):
        """reads _words and _word_lengths file in parent dictionary for
            dictionary named in self.name
        """
        # open words dict
        f = open(self.name + "_words", 'r', encoding='utf8', errors='ignore')
        file = f.read()
        f.close()
        self.words = dict(eval(file))
        # open word lengths dict
        g = open(self.name + "_word_lengths", 'r', encoding='utf8', errors='ignore')
        file = g.read()
        g.close()
        self.word_lengths = dict(eval(file))
        # open stems
        h = open(self.name + "_stems", 'r', encoding='utf8', errors='ignore')
        file = h.read()
        h.close()
        self.stems = dict(eval(file))
        # open sentence lengths
        i = open(self.name + "_sentence_lengths", 'r', encoding='utf8', errors='ignore')
        file = i.read()
        i.close()
        self.sentence_lengths = dict(eval(file))
        # open punctuation freq
        j = open(self.name + "_punctuation", 'r', encoding='utf8', errors='ignore')
        file = j.read()
        j.close()
        self.punctuation = dict(eval(file))
    def save_model(self):
        """Saves words dictionary in self.name + words and word_lengths in
            the same pattern for word_lengths
        """
        f = open(self.name + "_words", 'w')      # Open word dictionary
        f.write(str(self.words))            
        f.close()                   
        g = open(self.name+"_word_lengths", 'w') # Open word length dict
        g. write(str(self.word_lengths))
        g.close()
        h = open(self.name+"_stems", 'w') # Open stem dict
        h. write(str(self.stems))
        h.close()
        i = open(self.name+"_sentence_lengths", 'w') # Open sentence length dict
        i. write(str(self.sentence_lengths))
        i.close()
        j = open(self.name+"_punctuation", 'w') # Open punctuation dict
        j. write(str(self.punctuation))
        j.close()
        
        
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring 
            the similarity of self and other – one score for each type of 
            feature (words, word lengths, stems, sentence lengths, and 
            your additional feature).
        """
        scores = []
        scores += [compare_dictionaries(other.words, self.words)]
        scores += [compare_dictionaries(other.word_lengths, self.word_lengths)]
        scores += [compare_dictionaries(other.stems, self.stems)]
        scores += [compare_dictionaries(other.sentence_lengths, self.sentence_lengths)]
        scores += [compare_dictionaries(other.punctuation, self.punctuation)]
        return scores
    
    
    def classify(self, source1, source2):
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print("Scores for " + source1.name + ": " + str(scores1)) 
        print("Scores for " + source2.name + ": " + str(scores2))
        
        weighted_sum_1 = 10*scores1[0] + 4*scores1[1] + 6*scores1[2] + 5*scores1[3] + 3*scores1[4] 
        weighted_sum_2 = 10*scores2[0] + 4*scores2[1] + 6*scores2[2] + 5*scores2[3] + 3*scores2[4] 
        
        if weighted_sum_1 > weighted_sum_2:
            print(self.name + " is more likely to have come from " + source1.name)
        elif weighted_sum_2 > weighted_sum_1:
            print(self.name + " is more likely to have come from " + source2.name)
        else:
            print(self.name + " is equally likely to have come from " + source1.name + " or " + source2.name)
                
                