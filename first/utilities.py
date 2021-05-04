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
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(text)
        print([re.sub(r'\D', '', number) for number in phone_numbers])
        # Remove numbers
        email = self.extract_email_addresses(text)
        #text = re.sub(r'\d+','',text)

        terms = {'Programming':['JAVA','C++','C#','Python','PHP','SCALA',
                                    'Javascript'],      
                'Web':['Angular','NodeJs','Spring Boot','React','Jquery','Html','CSS','WebRTC'],
                'Devops':['Docker','Git','Jenkins','Terraform','Ansible','Chef','Puppet','Azure Devops'],
                'Bigdata':['Hadoop','Hive','Spark','Kafka','Flink','Azure Databricks',
                                    'Storm'],
                'Cloud':['Azure','AWS','GCP'],
                'Mobile':['React Native','Android','Ios','Kotlin']}
        # Initializie score counters for each area
        programming = 0
        web = 0
        devops = 0
        bigdata = 0
        cloud = 0
        mobile = 0
        # Create an empty list where the scores will be stored
        scores = []
        # Obtain the scores for each area
        for area in terms.keys():
                
            if area == 'Programming':
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        programming +=1
                scores.append(programming)
                
            elif area == 'Web':
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        web +=1
                scores.append(web)
                
            elif area == 'Devops':
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        devops +=1
                scores.append(devops)
                
            elif area == 'Bigdata':
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        bigdata +=1
                scores.append(bigdata)
                
            elif area == 'Cloud':
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        cloud +=1
                scores.append(cloud)
                
            else:
                for word in terms[area]:
                    if text.find(word) != -1 or text.find(word.lower()) != -1:
                        mobile +=1
                scores.append(mobile)
        # Create a data frame with the scores summary
        summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
        return {
           "Scores" : {
            "Programming": programming,
            "Web": web,
            "Bigdata": bigdata
            # other stuff
            },
            "email": email
        }
