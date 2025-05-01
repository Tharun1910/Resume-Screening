from imports import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys

class PreprocessPipeline:
    def __init__(self):
        pass

    def run(self,Resume_file_name):
        try:
            resume_path = os.path.join("artifacts",Resume_file_name)
            preprocessor = Preprocessing()
            Text = preprocessor.extract_resume_text(resume_path)
            Tokens = preprocessor.preprocess_text(Text)
            Model_input = preprocessor.pos_filter(Tokens)
            return Model_input
        except Exception as e:
            raise CustomException(e,sys)

class ModelPipeline:
    def __init__(self):
        pass
    def predictrole(self,Model_input):
        try:
            labels = {6: 'Data Science', 12: 'HR', 0: 'Advocate', 1: 'Arts', 24: 'Web Designing', 16: 'Mechanical Engineer', 22: 'Sales', 14: 'Health and fitness', 5: 'Civil Engineer', 15: 'Java Developer', 4: 'Business Analyst', 21: 'SAP Developer', 2: 'Automation Testing', 11: 'Electrical Engineering', 18: 'Operations Manager', 20: 'Python Developer', 8: 'DevOps Engineer', 17: 'Network Security Engineer', 19: 'PMO', 7: 'Database', 13: 'Hadoop', 10: 'ETL Developer', 9: 'DotNet Developer', 3: 'Blockchain', 23: 'Testing'}
            tokenizer = AutoTokenizer.from_pretrained("./models/Role_model/")
            model = AutoModelForSequenceClassification.from_pretrained("./models/Role_model/")
            tokens = tokenizer.encode_plus(Model_input,max_length=512, truncation=True,padding="max_length",return_tensors="pt")
            outputs = model(**tokens)
            predicted_label = outputs.logits.argmax().item()
            output=labels[predicted_label]
            return output
        except Exception as e:
            raise CustomException(e,sys)

class Recommend:
    def __init__(self):
        self.Role_recommen_file= pd.read_csv("artifacts/Recom.csv")


    def Get_skills(self,Job_Role):
        category_data = self.Role_recommen_file[self.Role_recommen_file['Category'] == Job_Role]
        skills = eval(category_data['Skills'].iloc[0])
        return skills

    def Get_jobs(self,Job_Role):
        category_data = self.Role_recommen_file[self.Role_recommen_file['Category'] == Job_Role]
        job_roles = eval(category_data['Job_Roles'].iloc[0])
        return job_roles

class WebScraping:
    def __init__(self):
        # Set up headless Chrome options
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

    def internshala_jobs(self, job_url):
        try:
            print(f"Fetching URL with Selenium: {job_url}")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            driver.get(job_url)

            # Wait for job cards to load (adjust class name as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'internship_meta'))
            )

            # Parse the rendered page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            # Find job cards (update class if needed)
            job_cards = soup.find_all('div', class_='internship_meta')
            print(f"Found {len(job_cards)} job cards")

            jobs_list = []
            for card in job_cards:
                job_title_elem = card.find('a', class_='job-title-href')
                company_name_elem = card.find('p', class_='company-name')
                location_elem = card.find('p', class_='row-1-item locations')
                start_date_elem = card.find('div', class_='status-success')
                salary_elem = card.find('span', class_='desktop')
                experience_elem = None  # Experience not explicitly shown in the previous image
                apply_elem = card.find('img', class_='early_applicant_wrapper')

                if not all([job_title_elem, company_name_elem, location_elem, salary_elem]):
                    continue

                job_title = job_title_elem.text.strip()
                company_name = company_name_elem.text.strip()
                location = location_elem.text.strip()
                start_date = start_date_elem.text.replace('Starts', '').strip() if start_date_elem else 'Not Provided'
                salary = salary_elem.text.strip()
                experience = 'Not Mentioned'
                apply = "https://internshala.com" + job_title_elem['href']

                job_info = {
                    'Job_Title': job_title,
                    'Company_Name': company_name,
                    'Location': location,
                    'Start_Date': start_date,
                    'Salary': salary,
                    'Experience': experience,
                    'Apply': apply
                }
                jobs_list.append(job_info)
                print(f"Scraped job: {job_title} at {company_name}")

            print(f"Total jobs scraped: {len(jobs_list)}")
            return jobs_list
        except Exception as e:
            print(f"Error in internshala_jobs: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            raise CustomException(e, sys)

    def fresherworld(self, job_url, Job_Role):
        try:
            r = requests.get(job_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            job_cards = soup.find_all('div', class_='col-md-12 col-lg-12 col-xs-12 padding-none job-container jobs-on-hover top_space')
            jobs_list = []
            for card in job_cards:
                job_title_elem = card.find('span', class_='wrap-title seo_title')
                company_name_elem = card.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name')
                location_elem = card.find('span', class_='job-location display-block modal-open job-details-span')
                start_date_elem = card.find('span', class_='desc')
                apply = card.get('job_display_url')
                experience = card.find('span', class_='experience job-details-span')
                if not all([job_title_elem, company_name_elem, location_elem, start_date_elem, apply, experience]):
                    continue
                company_name = company_name_elem.text.strip()
                location = location_elem.text.strip()
                start_date = start_date_elem.text.strip()
                experience = experience.text.strip()
                salary = "Not Mentioned"
                job_info = {
                    'Job_Title': Job_Role,
                    'Company_Name': company_name,
                    'Location': location,
                    'Start_Date': start_date,
                    'Salary': salary,
                    'Experience': experience,
                    'Apply': apply
                }
                jobs_list.append(job_info)
            return jobs_list
        except Exception as e:
            raise CustomException(e, sys)

    def GetList(self, Job_Role):
        try:
            Job_Role = Job_Role.replace(' ', '-').lower() + "-jobs/"
            jobs_list_internshala = []
            jobs_list_fresherworld = []

            # Scrape Internshala
            job_url_string_internshala = 'https://internshala.com/jobs/' + Job_Role
            jobs_list_internshala = self.internshala_jobs(job_url_string_internshala)

            # Scrape Freshersworld
            job_url_string_fresherworld = 'https://www.freshersworld.com/jobs/jobsearch/' + Job_Role + '-jobs-for-be-btech?course=16'
            jobs_list_fresherworld = self.fresherworld(job_url_string_fresherworld, Job_Role)

            # Combine job lists
            combined_jobs = jobs_list_internshala + jobs_list_fresherworld
            print(f"Total jobs found: {len(combined_jobs)}")
            return combined_jobs
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, Resume_file):
        self.Resume_file = Resume_file
        self.Resume_file_name =Resume_file.filename
    def Savedata(self):
        self.Resume_file.save(os.path.join("artifacts", self.Resume_file_name))
    def Deletefiles(self):
        try:
            if os.path.exists(os.path.join("artifacts", self.Resume_file_name)):
                os.remove(os.path.join("artifacts", self.Resume_file_name))   
        except Exception as e:
            raise CustomException(e,sys)
