from imports import *
from src.components.data_ingestion import data_ingestion

class CustomDataRecruiter:
    def __init__(self,resume_list,job_description_file) -> None:
        self.resume_list = resume_list
        self.job_description_file = job_description_file
        # dict of scores 
        self.scores = {}
        self.resume_details={}

    def Savedata(self):
        for resume_file in self.resume_list:
            resume_file.save(os.path.join("static", resume_file.filename))
        self.job_description_file.save(os.path.join("static",self.job_description_file.filename))
    
    def Deletefiles(self):
        try:
            if os.path.exists(os.path.join("static", "Job_description_file.pdf")):
                os.remove(os.path.join("static", "Job_description_file.pdf"))
            for resume_file in self.resume_list:
                if os.path.exists(os.path.join("static", resume_file.filename)):
                    os.remove(os.path.join("static", resume_file.filename))
        except Exception as e:
            raise CustomException(e,sys)
    
    def AssignScore(self):
        # Load the job description
        preprocessor = Preprocessing()
        Scorepredict=ScorePipeline()
        data_ingest=data_ingestion()
        jd_text=preprocessor.extract_resume_text(os.path.join("static",self.job_description_file.filename))
        data_ingest.extract_skills_from_resume(jd_text)
        data_ingest.extract_certifications_from_resume(jd_text)
        job_description_skills=data_ingest.skills
        job_description_certifications=data_ingest.certifications
        # Load the resumes
        resume_files = self.resume_list
        # extract the text from the resumes
        for resume_file in resume_files:
            Resume_Text = preprocessor.extract_resume_text(os.path.join("static",resume_file.filename))
            data_ingest.extract_skills_from_resume(Resume_Text)
            data_ingest.extract_certifications_from_resume(Resume_Text)
            score_percent,skill_percent,certify_percent=0.6,0,0
            resume_skills = data_ingest.skills
            resume_certifications = data_ingest.certifications
            if len(job_description_skills) > 0 and len(job_description_certifications) > 0:
                skill_percent,certify_percent = 20,20
            elif len(job_description_skills) > 0:
                skill_percent = 40
            elif len(job_description_certifications) > 0:
                certify_percent = 40
            else:
                score_percent = 1
            Score_Model_input=[Resume_Text,jd_text]
            Score=0
            resume_score=Scorepredict.predictscore(Score_Model_input)
            Score=Scorepredict.predictscore(Score_Model_input)*score_percent
            if len(job_description_skills):
                skillcount=0
                for skill in job_description_skills:
                    if skill in resume_skills:
                        skillcount+=1
                Score= Score + (skillcount/len(job_description_skills))*skill_percent
            if len(job_description_certifications):
                certificationcount=0
                for certification in job_description_certifications:
                    if certification in resume_certifications:
                        certificationcount+=1
                Score = Score + (certificationcount/len(job_description_certifications))*certify_percent
            email="Unable to fetch"
            email=data_ingest.extract_email(Resume_Text)
            contact_number="Unable to fetch"
            contact_number=data_ingest.extract_contact_number(Resume_Text)
            education="Unable to fetch"
            education=data_ingest.extract_education(Resume_Text)
            self.resume_details[resume_file.filename] = {
                "Score": round(resume_score,3),
                "Email":email,
                "Contact_Number":contact_number,
                "Education":education,
                "resume link": os.path.join("static",resume_file.filename)
            }
            self.scores[resume_file.filename] = Score
            
    def AssignRank(self):
        # sort the scores in descending order 
        self.scores = dict(sorted(self.scores.items(), key=lambda item: item[1],reverse=True))

    def Gettopn(self,n):
        if n > len(self.scores):
            return self.scores
        return dict(list(self.scores.items())[:n])
    
class ScorePipeline:
    def __init__(self):
        pass
    def predictscore(self,Score_Model_input):
        try:
            ob = CountVectorizer()
            matrix = ob.fit_transform(Score_Model_input)
            similarity_matrix =  cosine_similarity(matrix)
            score = similarity_matrix[0][1] * 100
            score = round(score,2)
            return score
        except Exception as e:
            raise CustomException(e,sys)
