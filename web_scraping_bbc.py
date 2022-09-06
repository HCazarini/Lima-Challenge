from pydoc import classname
from turtle import title
from typing import NewType
import requests #importanto a biblioteca requests, para acesso do site
from bs4 import BeautifulSoup #biblioteca para organizar e tratar os dados obtidos via HTML
import pandas as pd #utilizando a biblioteca para criar tabelas com os dados
from google.cloud import bigquery
import schedule
import time 

def findItemList(list, itemToFind):
    for item in list:
        if itemToFind == item:
            return True
    
    return False

list_news = [] #criando uma lista para organizar as news

response = requests.get('https://www.bbc.com/') #solicitando acesso ao site via função do BeutifulSoup

url = 'https://www.bbc.com'

conteudo = response.content #criando variável com base na requisição de acesso e conteúdo

site = BeautifulSoup(conteudo, 'html.parser') # determinando que o BeutifilSOup olhe para os dados como um HTML

modules = site.findAll('section', attrs={'class': 'module'})

for module in modules:
    #print('module: ', module)
    
    category = module.find('a', attrs={'class': 'module__title__link'})    
    if (category is None):
        category = module.find('span', attrs={'class': 'module__title__link'})

#searching for the top 1 news on tha page, who has a different tag
    news = module.findAll('div', attrs={'class': 'media__content'})
    classNameList = module['class']
    #print('-------->', type(className))
    #print(';;;>', ['a','b'].index('a'))
    #print('------->', (news[1].find('a', attrs={'class': 'media__link'})).text.strip())
    
    itemFound = findItemList(module['class'], 'module--content-block')
    if (news is not None) and (not itemFound):
        ct = ''
        mt = ''
        st = ''
        tp = ''
        lk = ''
        if (category is not None):
            
            #print('CATEGORY: ', category.text.strip())
            ct = category.text.strip()

        for new in news:
            #for the title we need to search for the text only, thats why im using the for structure
            mainTitle = new.find('a', attrs={'class': 'media__link'}) 
            if (mainTitle is not None):
                #print('MAIN TITLE: ',mainTitle.text.strip())
                mt = mainTitle.text.strip()
            else:
                difNew = new.find('h3')
                #print('MAIN TITLE: ',difNew.text.strip())
                mt = difNew.text.strip()
            
            subTitle = new.find('p', attrs={'class': 'media__summary'})
            if (subTitle is not None):
                #print('SUB TITLE: ',subTitle.text.strip()) 
                st = subTitle.text.strip()

            newType = new.find('a', attrs={'class':'media__tag'})
            if (newType is not None):
                #print('TYPE: ',newType.text.strip())
                tp = newType.text.strip()

            newLink = new.find('a', attrs={'class':'media__link'})
            if (newLink is not None):
                if 'http' in newLink['href']:
                    #print('LINK: ', newLink['href'])
                    lk = newLink['href']

                else:
                    #print('LINK: ', url + newLink['href'])
                    lk = url + newLink['href']
                #print('\n')     
            else:
                difLink = new.find_parent('a')
                if 'http' in difLink['href']:
                    #print('LINK: ', difLink['href'])
                    lk = difLink['href']

                else:
                    #print('LINK: ', url + difLink['href'])
                    lk = url + difLink['href']
                #print('\n')   
        
            list_news.append({'Category': ct,'Main_Title': mt, 'Sub_Title': st , 'Type': tp , 'Link': lk})  
#print(list_news)
panda_news = pd.DataFrame(list_news)
#panda_news.to_excel('web_scraping.xlsx', index=False)
panda_news.to_gbq(destination_table='news_list.news_table', project_id='limachallenge', if_exists='replace')