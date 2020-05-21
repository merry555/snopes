import sys
import string
import os
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

def numerical_sort(value):
    number = re.compile(r'(\d+)')
    parts = number.split(value)
    parts[1::2] = map(int,parts[1::2])
    return parts

def get_filepath_list(newsbodypath):
    valuelist = []
    factlist = []
    for(dirpath, dir, files) in os.walk(newsbodypath):
        dir.sort()
        for file in sorted(files, key=numerical_sort):
            if file.endswith('news_body.html'):
                factlist.append(os.path.join(dirpath, file))
            elif file.endswith('.html') and file.startswith('corona'):
                valuelist.append(os.path.join(dirpath,file))
        if not len(valuelist) == len(factlist):
            raise Exception('Different number of files')

    return factlist, valuelist



def get_news_value(htmlbodypath):
    data = []
    with open(htmlbodypath) as file:
        html = file.read()
        soup = BeautifulSoup(html,"html.parser")

        for tag in soup.findAll('div', attrs={'class':'media-body'}):
            file_data = {}
            file_data['title'] = tag.find('h5').text
            file_data['date'] = tag.find('li', attrs={'class':'date breadcrumb-item'}).text.strip()
            file_data['summary'] = tag.p.text

            data.append(file_data)
    return data 

def get_fact(htmlfactpath):
    data = []
    # source, tag 있는 경우 가져오기
    # claim, 
    with open(htmlfactpath) as file:
        html = file.read()
        soup = BeautifulSoup(html,"html.parser")

        for tag in soup.findAll('div', attrs={'class':'media-body'}):
            file_data = {}
            try:
                tag.h5.text
            except:
                pass
            else:
                file_data['check'] = tag.h5.text
                data.append(file_data)
    return data

def get_claim(htmlfactpath):
    data = []
    with open(htmlfactpath) as file:
        html = file.read()
        soup = BeautifulSoup(html,"html.parser")

        for claim in soup.findAll('div', attrs={'class':'claim'}):
            file_data = {}
            file_data['claim'] = claim.p.text

            data.append(file_data)

    return data

 
def make_csv(path):
    newsbodypath = path
    factlist, valuelist = get_filepath_list(newsbodypath)

    htmltitle = []
    htmldate = []
    htmlsubtitle = []
    htmlfact = []
    htmlclaim = []
    htmlbody = []
    htmlsource= []
    htmltags = []
    htmlcitations = []
    htmlcitation_date = []

    for i in range(len(factlist)):
        htmlvalues = get_news_value(valuelist[i])
        factvalues = get_fact(factlist[i])
        clainvalues = get_claim(factlist[i])
        #bodyvalues, infoPrint = get_body(factlist[i])
        #sourcevalues = get_source(factlist[i])

        print(factlist[i])
        # factvalues
        for j in range(len(factvalues)):
            # COVID-19 source_date     
            htmltitle.append(str(htmlvalues[j]['title']))
            htmldate.append(htmlvalues[j]['date'])
            htmlsubtitle.append(str(htmlvalues[j]['summary']))
            htmlfact.append(factvalues[j]['check'])
            htmlclaim.append(clainvalues[j]['claim'])
            #htmlbody.append(bodyvalues[j]['text'])
            #htmltags.append(sourcevalues[j]['tag'])
            #htmlsource.append(sourcevalues[j]['source'])
            #htmlcitations.append(sourcevalues[j]['reference'])
            #htmlcitation_date.append(sourcevalues[j]['source_date'])

    result = pd.DataFrame({'title':htmltitle, 'date':htmldate, 'summary':htmlsubtitle, 'check':htmlfact,'claim':htmlclaim})
    result.to_csv("snoup_news.csv", mode='w')





if __name__ == "__main__":
    path = '/Users/jisu/corona/corona_news/news_body'
    make_csv(path)


    """
            try:
                tags = tag.findAll('li', attrs={'class':'tag'})
            except:
                file_data['tag'] = None
            else:
                for t in tags:
                    file_data['tag'] = t.find('a').text
    """
