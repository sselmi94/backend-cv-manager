from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from .models import Terme, Category
import json
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
#import slate3k as slate
import spacy
import random
import nltk
nltk.download("words")
from pyresparser import ResumeParser
import os

class CvManagerUtilties():
    lines = []
    sentences = []
    tokens = []
    beforeToken = []
#    nlp = spacy.load("fr_core_news_sm")

    def pdfextract(self, file):
        #with open(file, 'rb') as f:
            #extracted_text = slate.PDF(f)
        return ""

    def extract_email_addresses(self, string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        return r.findall(string)

    def extract_phone_number(self, text):
        r = re.compile(
            r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        phone_numbers = r.findall(text)
        return phone_numbers

    def extract_date(self, text):
        r = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
        dateOfBirth = r.findall(text)
        return dateOfBirth

    def extract_address(self, text):
        r = re.compile(r'[\w\.-]+,[\w\.-]+,[\w\.-]+')
        return r.findall(text)

    def parseCV(self, pathOfResume):
        # Open pdf file
        text = self.pdf_to_text(pathOfResume)
        text = text.lower()
        self.lines = [el.strip() for el in text.split("\n") if len(el) > 0]
        self.lines = [nltk.word_tokenize(el) for el in self.lines]
        self.lines = [nltk.pos_tag(el) for el in self.lines]
        # Split/Tokenize into sentences (List of strings)
        self.sentences = nltk.sent_tokenize(text)
        # Split/Tokenize sentences into words (List of lists of strings)
        self.sentences = [nltk.word_tokenize(sent) for sent in self.sentences]
        self.tokens = self.sentences
        data = ResumeParser(pathOfResume).get_extracted_data()
        experience = self.getExperience(text, True)

        name = data['name']
        
        splited = ["",""]
        try:
            if(name != None):
                space = name.index(" ")
                splited = name.split(" ")
        except ValueError:
            splited[0] = name
        dataFromDatabase = self.fillArrayOfTermesFromDatabase()
        items = dataFromDatabase['items']
        categories = dataFromDatabase['categories']
        iCategory = 0
        iCategorySum = 0
        result = []
        skillsPerCategory = []
        currentArray = []
        for item in items:
            currentArray = []
            for currentTerme in item:
                if text.find(currentTerme) != -1 or text.lower().find(currentTerme.lower()) != -1:
                    currentArray.append(currentTerme)
                    iCategorySum += 1
            result.append(
                {"name": categories[iCategory], "value": iCategorySum})
            skillsPerCategory.append(
                {"category": categories[iCategory], "skills": currentArray})
            iCategory += 1
            iCategorySum = 0
        location = self.extract_address(text)

        return {
            "Nom": splited[0], "Prenom": splited[1],
            "Email": data['email'], 
            "Telephone": data['mobile_number'], 
            "Adresse": location,
            "Scores": result,
            "Parcours": data['experience'],
            "Experience": experience,
            "Competences": skillsPerCategory,
            "Profil":data['designation'],
            "Education":data['degree']
        }

    def fillArrayOfTermesFromDatabase(self):
        queryset = Terme.objects.all()
        dictionaries = [obj.as_dict() for obj in queryset]
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
            "items": arrayOfItems,
            "categories": arrayOfCategories,
            "scores": arrayOfScores
        }

    def getExperience(self, inputString, debug=False):
        experience = []
        try:
            for sentence in self.lines:  # find the index of the sentence where the degree is find and then analyse that sentence
                # print(sentence)
                # string of words in sentence
                sen = " ".join([words[0].lower() for words in sentence])
                if re.search('expérience', sen):
                    sen_tokenised = nltk.word_tokenize(sen)
                    tagged = nltk.pos_tag(sen_tokenised)
                    entities = nltk.chunk.ne_chunk(tagged)
                    print(entities)
                    for subtree in entities.subtrees():
                        for leaf in subtree.leaves():
                            if leaf[1] == 'CD':
                                experience = leaf[0]
        except Exception as e:
            print(e)
        if experience:
            # infoDict['experience'] = experience
            return experience
        else:
            # infoDict['experience']=0
            return 0
            return 0
        if debug:
            return experience
    def pdf_to_text(self,pdfname):

        # PDFMiner boilerplate
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Extract text
        fp = open(pdfname, 'rb')
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()

        # Get text from StringIO
        text = sio.getvalue()

        # Cleanup
        device.close()
        sio.close()

        return text