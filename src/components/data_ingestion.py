import pdfx
from src.exception import CustomException
import sys
import spacy
from spacy import displacy
import os
import re

class data_ingestion:
    def __init__(self) -> None:
        self.skills_nlp=spacy.load('en_core_web_sm')
        skill_pattern_path=os.path.join("models", "jz_skill_patterns.jsonl")
        ruler =self.skills_nlp.add_pipe('entity_ruler')
        ruler.from_disk(skill_pattern_path)
        other_pipes = [pipe for pipe in self.skills_nlp.pipe_names if pipe != 'entity_ruler'] 
        self.skills_nlp.disable_pipes(*other_pipes)
        self.certifications_nlp=spacy.load('en_core_web_sm')
        certification_pattern_path=os.path.join("models", "certifications.jsonl")
        ruler =self.certifications_nlp.add_pipe('entity_ruler')
        ruler.from_disk(certification_pattern_path)
        other_pipes = [pipe for pipe in self.certifications_nlp.pipe_names if pipe != 'entity_ruler']
        self.certifications_nlp.disable_pipes(*other_pipes)
        self.skills = []
        self.certifications = []

    def extract_skills_from_resume(self,text):
        try:
            self.skills = []
            # Use the loaded NLP model to parse the resume text
            doc =self.skills_nlp(text)
            # Iterate through entities and add skills to the list
            for entity in doc.ents:
                if entity.label_ == "SKILL":
                    self.skills.append(entity.text)
            self.skills=list(set(self.skills))
        except Exception as e:
            raise CustomException(e,sys)
            
    def extract_certifications_from_resume(self,text):
        certifications = []
        # Use the loaded NLP model to parse the resume text
        doc = self.certifications_nlp(text)
        # Iterate through entities and add certifications to the list
        for entity in doc.ents:
            if entity.label_ == "CERTIFICATION":
                certifications.append(entity.text)
        return list(set(certifications))
        
    def extract_email(self,text):
        email = None

        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        if match:
            email = match.group()
        return email

    def extract_contact_number(self,text):
        contact_number = None

        # Use regex pattern to find a potential contact number
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        if match:
            contact_number = match.group()

        return contact_number

    def extract_education(self,text):
        education = []
        # Use regex pattern to find education information
        pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D|B\.Tech|B\.Com|Bachelor\s*of\s*Technology|Bachelor\s*of\s*Commerce)\s(?:\w+\s)*\w+"
        matches = re.findall(pattern, text)
        for match in matches:
            education.append(match.strip())
        return " ".join(education)



