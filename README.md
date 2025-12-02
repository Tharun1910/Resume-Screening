# 📄 Smart Recruitment: AI-Driven Resume Classification and Ranking

## 📌 Project Overview
This project is an AI-powered recruitment assistant designed to simplify and automate both the **job seeker experience** and **recruiter screening process**.  
It uses **Natural Language Processing (NLP)** and **Machine Learning** techniques to:
- Predict the **job domain from a candidate’s resume** using a **pre-trained BERT model**.
- Provide **real-time job recommendations** based on predicted domains (via web scraping).
- Automatically **match and rank candidate resumes against job descriptions** using **cosine similarity**.

---

## 📚 Inspiration & Goal  
Manual resume screening is often time-consuming, inconsistent, and prone to human error. The project aims to:
- **Streamline resume classification and candidate shortlisting.**
- **Assist job seekers** by suggesting job roles aligned with their skills and experience.
- **Help recruiters** automatically identify top candidates for job openings.

---

## 📊 Project Architecture  

### 🧑‍💻 Job Seeker Side:
- **Resume Upload**
- **Text Extraction & Preprocessing**
- **Job Domain Prediction (BERT)**
- **Real-time job scraping and recommendations** 

### 🧑‍💼 Recruiter Side:
- **Job Description Upload**
- **Resume Preprocessing**
- **Cosine Similarity Calculation**
- **Candidate Ranking based on Relevance Score**

---

## 📦 Data Sources  

- **Resume Dataset:** Kaggle dataset with 962 resumes labeled under 24 job domains.
- **Job Descriptions:** Scraped or manually entered job postings.
- **Custom Skills/Certificates JSON File:** Created from open-source resources.
- **Real-time job listings via web scraping (Internsala, Indeed, LinkedIn, etc.)**

---

## 🛠️ Technologies & Tools  

- **Python**  
- **Hugging Face Transformers (BERT)**  
- **Scikit-learn (Cosine Similarity, TF-IDF Vectorizer)**  
- **Pandas & NumPy**  
- **BeautifulSoup / Selenium (for web scraping)**  
- **MongoDB ( for user authentication in the web application)**

---

## 🚀 How It Works  

- **Resume Text Extraction:** Extract text from PDF.
- **Preprocessing:** Clean text, remove stopwords, tokenize.
- **Job Domain Prediction:** Fine-tuned pre-trained BERT model classifies resumes.
- **Similarity Matching:** Convert resumes and job descriptions into vectors using TF-IDF or embeddings. Compute cosine similarity for ranking.

---


## 📖 References  
 
- Hugging Face Model: [Sachinkelenjaguri/resume_classifier](https://huggingface.co/Sachinkelenjaguri/resume_classifier  )  
