import spacy
import pdfminer
import re
import os
import pdf2txt
import pandas as pd

#Load english module of spacy
nlp = spacy.load('en_core_web_sm')

#Convert pdf into text file
def convert_pdf(file):
    output_file = os.path.basename(os.path.splitext(file)[0]) + ".txt"
    outputfile_path = os.path.join('output/txt/',output_file)
    pdf2txt.main(args=[file, '--outfile',outputfile_path])
    print(outputfile_path+"saved successfully")
    return outputfile_path

def convert_dataframe(redict):
    resumedf = pd.DataFrame(redict)
    return resumedf

#For storing candidate info
result_dict = {"name" : [] ,"phone" : [] , "email" : [] , "skills" : [] }
names=[]
phones=[]
emails= []
skills= []

#Parse content of resume and extract necessary information
def parse_content(text):
    skillset = re.compile('python|java|sql|hadoop|tableau')
    phonenum = re.compile(r"\+\d{12}|\d{10}")
    resume=nlp(text)
    try:
        name = [entity.text for entity in resume.ents if entity.label_ == "PERSON"][0]
    except:
        name = [entity.text for entity in resume if (entity.pos_ == "PROPN" or entity.pos_ == "NOUN")][:2]
        name = " ".join(name)
    email = [word for word in resume if word.like_email == True][0]
    phone=str(re.findall(phonenum , text.lower()))
    skills_list = re.findall(skillset,text.lower())
    unique_skill_list = str(set(skills_list))
    names.append(name)
    phones.append(phone)
    emails.append(email)
    skills.append(unique_skill_list)

for file in os.listdir('sample/'):
    if file.endswith(".pdf"):
        txt=convert_pdf(os.path.join("sample/",file))
        f = open(txt,encoding='utf8').read()
        parse_content(f)

#Storing all information into dictionary
result_dict["name"]=names
result_dict["phone"]=phones
result_dict["email"]=emails
result_dict["skills"]=skills

df = convert_dataframe(result_dict)
df.to_csv("output/csv/resume.csv",index=False)