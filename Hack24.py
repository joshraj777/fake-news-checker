def clean_string(text):
    # Convert text to lowercase
    text = str(text)
    text = text.lower()
    
    # Remove punctuation marks
    punctuation = '''!()-[]{};:"\,<>./-?@#$%^&*_~'''
    for char in punctuation:
        text = text.replace(char, ' ')
    
    # Split the text into words
    words = text.split()


    return words

import pandas as pd

data = pd.read_csv('WELFake_Dataset.csv',index_col=0)

countdown = 10
word_counts_dictcon = {} # "word": [Real, Fake]
word_counts_dictit = {} # "word": [Real, Fake]
realtit = 0
faketit = 0
realcon = 0
fakecon = 0
real=0
fake=0

for index, row in data.iterrows():


    Title = clean_string(row[0])
    Content = clean_string(row[1])
    label = row[2]

    

    for s in Title:
        if label == 1:
            if s not in word_counts_dictit:
                word_counts_dictit[s] = {"real": 0, "fake": 0}
                word_counts_dictit[s]["real"] += 1
                realtit +=1
            else:
                word_counts_dictit[s]["real"] += 1
                realtit +=1
                #print("Story is real".format(index))
        if label == 0:
            if s not in word_counts_dictit:
                word_counts_dictit[s] = {"real": 0, "fake": 0}
                word_counts_dictit[s]["fake"] += 1
                faketit +=1
            else:
                word_counts_dictit[s]["fake"] += 1
                faketit +=1

                #print("Story is fake".format(index))
    for s in Content:
            if label == 1:
                if s not in word_counts_dictcon:
                    word_counts_dictcon[s] = {"real": 0, "fake": 0}
                    word_counts_dictcon[s]["real"] += 1
                    realcon +=1
                else:
                    word_counts_dictcon[s]["real"] += 1
                    realcon +=1
                    #print("Story is real".format(index))
            if label == 0:
                if s not in word_counts_dictcon:
                    word_counts_dictcon[s] = {"real": 0, "fake": 0}
                    word_counts_dictcon[s]["fake"] += 1
                    fakecon +=1

                else:
                    word_counts_dictcon[s]["fake"] += 1
                    fakecon +=1

                    #print("Story is fake".format(index))
    
import numpy as np

Probabilities = data['label'].value_counts()
real = Probabilities.get(1)
fake = Probabilities.get(0)

print(real)

Preal = real/(fake+real)
Pfake = fake/(fake+real)

print(Preal)

probabilities_dictit={}
probabilities_dictcon={}

for s in word_counts_dictcon:
    probabilities_dictcon[s] = {"real": 0, "fake": 0}
    probabilities_dictcon[s]["real"] = word_counts_dictcon[s]["real"]/realcon
    probabilities_dictcon[s]["fake"] = word_counts_dictcon[s]["fake"]/fakecon
for s in word_counts_dictit:
    probabilities_dictit[s] = {"real": 0, "fake": 0}
    probabilities_dictit[s]["real"] = word_counts_dictit[s]["real"]/realtit
    probabilities_dictit[s]["fake"] = word_counts_dictit[s]["fake"]/faketit
    
print(probabilities_dictit["the"])
print(probabilities_dictcon["the"])

import math
import csv
import numpy as np

def classify(title, text):
    title = clean_string(title)
    text = clean_string(text)

#TITLE
    #real
    rt = math.log(Preal)
    for s in title:
        if s in probabilities_dictit:
            if probabilities_dictit[s]["real"]!=0:
                rt += math.log(probabilities_dictit[s]["real"])
                    
            #fake
    ft = math.log(Pfake)
    for s in title:
        if s in probabilities_dictit:
            if probabilities_dictit[s]["fake"]!=0:
                ft+= math.log(probabilities_dictit[s]["fake"])
    #CONTENT
        #real
    rc = math.log(Preal)
    for s in title:
        if s in probabilities_dictcon:
            if probabilities_dictcon[s]["real"]!=0:
                rc += math.log(probabilities_dictcon[s]["real"])
                    
            #fake
    fc = math.log(Pfake)
    for s in title:
        if s in probabilities_dictcon:
            if probabilities_dictcon[s]["fake"]!=0:
                fc += math.log(probabilities_dictcon[s]["fake"])
   # print(fc)
    print("Checking Title")
    if (abs(ft-rt)>5):
        if np.argmax([ft, rt]) == 0:
            return "This article is most likely false"
        return "This article is most likely true"
    print("Checking Content")
    if np.argmax([fc, rc])==0:
        return "This article is most likely false"
    return "This article is most likely true"

import requests
from bs4 import BeautifulSoup

url = input("Website URL:")

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.title.string if soup.title else "No title found"
    
    text_content = ""
    for paragraph in soup.find_all('p'):
        text_content += paragraph.get_text() + "\n"
    
else:
    print("Failed to fetch the web page:", response.status_code)

result = classify(title, text_content)
print(result)