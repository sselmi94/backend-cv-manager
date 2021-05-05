import json
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
import slate3k as slate
import spacy
import random
import nltk
nltk.download("words")
from .models import Terme,Category
class CvManagerUtilties():
    lines = []
    sentences = []
    tokens = []
    def sayHello(self):
        return "say hello"
    def pdfextract(self,file):
        with open(file,'rb') as f:
            extracted_text = slate.PDF(f)
        return extracted_text[0]
    def extract_email_addresses(self,string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        return r.findall(string) 
    
    def extract_phone_number(self,text):
        r = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        phone_numbers = r.findall(text)
        return phone_numbers
    def extract_date(self,text):
        r = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
        dateOfBirth = r.findall(text)
        return dateOfBirth
    def extract_address(self,text):
        r = re.compile(r'[\w\.-]+,[\w\.-]+,[\w\.-]+')
        return r.findall(text) 
    def parseCV(self,pathOfResume):
        # Open pdf file
        mytext = self.pdfextract(pathOfResume)
        email = "a@a"

        text = mytext
        text = text.lower()
        self.lines = [el.strip() for el in text.split("\n") if len(el) > 0]
        self.lines = [nltk.word_tokenize(el) for el in self.lines]
        self.lines = [nltk.pos_tag(el) for el in self.lines]
        self.sentences = nltk.sent_tokenize(text)    # Split/Tokenize into sentences (List of strings)
        self.sentences = [nltk.word_tokenize(sent) for sent in self.sentences]    # Split/Tokenize sentences into words (List of lists of strings)
        self.tokens = self.sentences
        experience = self.getExperience(text,True)
        extractedname,other = self.getName(text,True)
        #extract_names(text)
        # spacy
        nlp = spacy.load("fr_core_news_sm")
        doc = nlp(text)
        textterms = [ent.text for ent in doc.ents]
        entity = [ent.label_ for ent in doc.ents]
        for ent in doc.ents:
            if(ent.label_ == 'PER'):
                print(ent.text)
            break
        #phone
        #print([re.sub(r'\D', '', number) for number in phone_numbers])
        # Remove numbers
        email = self.extract_email_addresses(text)
        phone_numbers = self.extract_phone_number(text)
        dateOfBirth = self.extract_date(text)
        location = self.extract_address(text)

        #text = re.sub(r'\d+','',text)

    
        # Obtain the scores for each area
        dataFromDatabase = self.fillArrayOfTermesFromDatabase()
        items = dataFromDatabase['items']
        categories = dataFromDatabase['categories']
        iCategory = 0
        iCategorySum = 0
        result = []
        for item in items:
            for currentTerme in item:
                if text.find(currentTerme) != -1 or text.lower().find(currentTerme.lower()) != -1:
                    iCategorySum += 1
            result.append({"name":categories[iCategory],"score":iCategorySum})
            iCategory += 1
            iCategorySum = 0
       #   summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
        return {
            "Nom" : extractedname,"Email": email,"Telephone": phone_numbers,"Date de naissance" : dateOfBirth,"Adresse": location,
            "Scores" : result,
            "Experience": experience
        }
    def fillArrayOfTermesFromDatabase(self):
        queryset = Terme.objects.all()
        dictionaries = [ obj.as_dict() for obj in queryset]
        arrayOfCategories = []
        arrayOfItems = []
        arrayOfScores = []
        for item in dictionaries:
            categoryName = item['category']
            try:
               idx = arrayOfCategories.index(categoryName)
               arrayOfItems[idx].append(item['title'])
            except ValueError:
                arrayOfCategories.append(categoryName)
                arrayOfItems.append([item['title']])
                arrayOfScores.append(0)

        return {
        "items":arrayOfItems,
        "categories":arrayOfCategories,
        "scores":arrayOfScores
        }
    def getName(self, inputString,  debug=False):
           
            listOfNames = open("./upload/allNames.txt", "r").read().lower()
            # Lookup in a set is much faster
            listOfNames = set(listOfNames.split())
            

            otherNameHits = []
            nameHits = []
            name = None

            try:
                tokens, lines, sentences = self.tokens, self.lines, self.sentences

                # Try a regex chunk parser
                # grammar = r'NAME: {<NN.*><NN.*>|<NN.*><NN.*><NN.*>}'
                grammar = r'NAME: {<NN.*><NN.*>}'
                # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
                # Note the correction to the rule. Change has been made later.
                chunkParser = nltk.RegexpParser(grammar)
                all_chunked_tokens = []
                for tagged_tokens in lines:
                    # Creates a parse tree
                    if len(tagged_tokens) == 0: continue # Prevent it from printing warnings
                    chunked_tokens = chunkParser.parse(tagged_tokens)
                    all_chunked_tokens.append(chunked_tokens)
                    for subtree in chunked_tokens.subtrees():
                        #  or subtree.label() == 'S' include in if condition if required
                        if subtree.label() == 'NAME':
                            for ind, leaf in enumerate(subtree.leaves()):
                                if leaf[0].lower() in listOfNames and 'NN' in leaf[1]:
                                    hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                                    # Check for the presence of commas, colons, digits - usually markers of non-named entities 
                                    if re.compile(r'[\d,:]').search(hit): continue
                                    nameHits.append(hit)
                # Going for the first name hit
                if len(nameHits) > 0:
                    nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits] 
                    name = " ".join([el[0].upper()+el[1:].lower() for el in nameHits[0].split() if len(el)>0])
                    otherNameHits = nameHits[1:]

            except Exception as e:
                print(e)        


            if debug:
                print(name)
                print("")
            return name, otherNameHits  
    def getExperience(self,inputString,debug=False):
            experience=[]
            try:
                for sentence in self.lines:#find the index of the sentence where the degree is find and then analyse that sentence
                       # print(sentence)
                        sen=" ".join([words[0].lower() for words in sentence]) #string of words in sentence
                        if re.search('expérience',sen):
                              sen_tokenised= nltk.word_tokenize(sen)
                              tagged = nltk.pos_tag(sen_tokenised)
                              entities = nltk.chunk.ne_chunk(tagged)
                              print(entities)
                              for subtree in entities.subtrees():
                                  for leaf in subtree.leaves():
                                    if leaf[1]=='CD':
                                        experience=leaf[0]
            except Exception as e:
                print(e)
            if experience:
               # infoDict['experience'] = experience
               return experience
            else:
               # infoDict['experience']=0
               return 0
            if debug:
                return experience

   