from imports import *
from src.pipeline.recruiter_predict import CustomDataRecruiter
from src.components.data_ingestion import data_ingestion
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

app=Flask(__name__)

@app.route('/')
def student_app():
    return render_template('student_login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recruiter_index')
def recruiter_index():
    return render_template('recruiter_index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html') 

@app.route('/student_login')
def student_login():
    return render_template('student_login.html')

@app.route('/student_signup')
def student_signup():
    return render_template('student_signup.html')

@app.route('/student_logout')
def student_logout():
    return render_template('student_login.html')

@app.route('/recruiter_login')
def recruiter_login():
    return render_template('recruiter_login.html')

@app.route('/recruiter_logout')
def recruiter_logout():
    return render_template('recruiter_login.html')

@app.route('/insert_student',methods=['GET','POST'])
def insert_student(): 
    username = request.form['username']
    password = request.form['password']
    
    # connect to MongoDB Atlas
    mongo_uri = "mongodb+srv://tarunchowdary29:Tharun1910@cluster0.9xhiuym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(mongo_uri)
    db = client["Recruiter-Ai"]
    collection = db["Student_Login"]
    
    # check if user exists
    if collection.find_one({"username": username}):
        return render_template('student_login.html', error="Username already exists.")
    
    # insert into database
    collection.insert_one({"username": username, "password": password})
    return render_template('student_login.html', success="Account created successfully.")

@app.route('/student_validate',methods=['GET','POST'])
def student_validate():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        # connect to mongodb
        mongo_uri = "mongodb+srv://tarunchowdary29:Tharun1910@cluster0.9xhiuym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(mongo_uri)
        db=client["Recruiter-Ai"]
        collection=db["Student_Login"]
        # check in database
        if collection.count_documents({"username": username, "password": password}) == 1:
            return render_template('index.html')    
        else:
            return render_template('student_login.html')
    else:
        return render_template('student_login.html')

@app.route('/insert_recruiter',methods=['GET','POST'])
def insert_recruiter():
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    # connect to mongodb
    mongo_uri = "mongodb+srv://tarunchowdary29:Tharun1910@cluster0.9xhiuym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(mongo_uri)
    db=client["Recruiter-Ai"]
    collection=db["Client_Login"]
    # user exist or not
    if collection.find_one({"username":username}):
        # Alert user exists
        alert_message = " username '{}' already exists.".format(username)
        return render_template('recruiter_login.html', alert_message=alert_message)

    if collection.find_one({"email":email}):
        alert_message="email {} already exists.".format(email)
        return render_template('recruiter_login.html', alert_message=alert_message)
    # insert in database
    collection.insert_one({"username": username, "password": password,"email":email})
    alert_message="account_created"
    return render_template('recruiter_login.html',alert_message=alert_message)

@app.route('/recruiter_validate',methods=['GET','POST'])
def recruiter_validate():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        # connect to mongodb
        mongo_uri = "mongodb+srv://tarunchowdary29:Tharun1910@cluster0.9xhiuym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(mongo_uri)
        db=client["Recruiter-Ai"]
        collection=db["Client_Login"]
        # check in database
        if collection.count_documents({"email": email, "password": password}) == 1:
            return render_template('recruiter_index.html')  
        else:
            return render_template('recruiter_login.html')
    else:
        return render_template('recruiter_login.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        Job_Role=""
        data=CustomData(Resume_file=request.files['Resume_file'])
        data.Savedata()
        preprocess=PreprocessPipeline()
        RoleModel_input=preprocess.run(Resume_file_name=data.Resume_file_name)
        Modelpredict=ModelPipeline()
        Job_Role=Modelpredict.predictrole(RoleModel_input)
        Recom=Recommend()
        skills=Recom.Get_skills(Job_Role)[:5]
        jobs=Recom.Get_jobs(Job_Role)[:5]
        Webscrap=WebScraping()
        fetched_data=Webscrap.GetList(Job_Role)
        # data.Deletefiles()
        return render_template("results.html",Job_Role=Job_Role,fetched_data=fetched_data,skills=skills,jobs=jobs)
    else:
        return render_template("index.html")

@app.route('/councel',methods=['GET','POST'])
def councel():
    return render_template('councel.html')

@app.route('/find_missing',methods=['GET','POST'])
def find_missing():
    if request.method == 'POST':
        Job_Role=request.form['Job_Role']
        data=CustomData(Resume_file=request.files['Resume_file'])
        data.Savedata()
        resume_text=pdfx.PDFx(os.path.join("artifacts",data.Resume_file_name)).get_text()
        recommender = Recommend()
        data_ingest = data_ingestion()
        skills = recommender.Get_skills(Job_Role)
        data_ingest.extract_skills_from_resume(text=resume_text)
        having_skills = data_ingest.skills
        # convert to lower case
        having_skills = [x.lower() for x in having_skills]
        missing_list=[]
        for skill in skills:
            if skill.lower() not in having_skills:
                missing_list.append(skill)
        # data.Deletefiles()
        return render_template('councel.html',missing_skills=missing_list,skills=skills)
    else:
        return render_template('councel.html')

@app.route('/get_resumes', methods=['POST'])
def get_resumes():
    job_description_file = request.files.get('Job_description_file')
    if job_description_file =="":
        render_template('recruiter_index.html')
    top_n=int(request.form['integer_value'])
    resume_files=[]
    try:
        resume_files = request.files.getlist('Resume_files')
    except Exception as e:
        raise CustomException(e,sys)
    # Save the job description file
    data=CustomDataRecruiter(resume_list=resume_files,job_description_file=job_description_file)
    data.Savedata()
    data.AssignScore()
    data.AssignRank()
    # get the top n resumes
    top_n_resumes = data.Gettopn(top_n)
    # delete the files
    # data.Deletefiles()
    # print(top_n_resumes)
    top_dict={}
    for key,value in top_n_resumes.items():
        top_dict[key]=data.resume_details[key]
    return render_template('recruiters_results.html',resume_details=top_dict)

@app.route('/serve_static/<filename>')
def serve_static(filename):
    print(filename)
    return send_file(filename)

if __name__=="__main__":
    # clear the pdfs in the artifacts folder and static folder
    if os.path.exists("artifacts"):
        for file in os.listdir("artifacts"):
            if file.endswith(".pdf"):
                os.remove(os.path.join("artifacts", file))
    if os.path.exists("static"):
        for file in os.listdir("static"):
            if file.endswith(".pdf"):
                os.remove(os.path.join("static", file))
    app.run(host="0.0.0.0",debug=True)
