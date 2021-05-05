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
from .models import Terme,Category
class CvManagerUtilties():
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
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
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
        #extract_names(text)
        # spacy
        nlp = spacy.load("en_core_web_sm")
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
           "Scores" : result,
            "Email": email,
            "Phone number": phone_numbers,
            "date of birth" : dateOfBirth,
            "address": location,
            "Name" : "hard coded"
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