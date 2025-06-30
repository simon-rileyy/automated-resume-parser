import pdfplumber
import docx
import spacy
import re


nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_info(text):
    name = None
    email = None
    skills = []
    education = None

    
    email_match = re.search(r'\S+@\S+', text)
    if email_match:
        email = email_match.group()

    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if len(line.split()) >= 2 and not any(
            word in line.lower()
            for word in ["email", "skills", "education", "project", "experience", "objective"]
        ):
            name = line
            break

    
    if not name:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break

    skill_keywords = [
        'python', 'java', 'c++', 'flask', 'postgresql',
        'mysql', 'javascript', 'html', 'css', 'docker', 'git','project management'
    ]
    found_skills = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    skills = ", ".join(found_skills)

    if "master" in text.lower():
        education = "Master"
    elif "bachelor" in text.lower():
        education = "Bachelor"
    elif "b.tech" in text.lower():
        education = "B.Tech"
    elif "m.tech" in text.lower():
        education = "M.Tech"

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "education": education
    }
