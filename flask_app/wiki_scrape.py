import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import regex as re

def get_wiki_str(year,specific_word): 
    month_list = ['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december']
    wiki_str = ''
    url = "https://nl.wikipedia.org/wiki/"+str(year)
  
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    
    df_events = pd.DataFrame(columns=['date','event'])
    if specific_word.lower() in str(soup).lower():
        n_month_old = 0
        break_loop = False

        for ul_tag in soup.findAll("ul"):
            for li_tag  in ul_tag.find_all('li'):   
                a_tag = li_tag.find('a',href=True)
                if a_tag and re.search('wiki/\d{1,2}',a_tag['href']):

                    date_tag=a_tag['href'].replace('/wiki/','').replace('_',' ')            

                    n_month_new = next((n for n,month in enumerate(month_list) if month in date_tag),-1)
                    if n_month_new>0 and n_month_new<n_month_old:
                        break_loop = True
                        break

                    event_tag = re.sub(r'^[0-9]+\s[-|–]', " ", li_tag.text.strip())
                    n_month_old = n_month_new

                    if specific_word.lower() in event_tag.lower():
                        df_events.loc[len(df_events)]=[date_tag,event_tag]

            if break_loop:
                break
    
    wiki_str=''
    
    if len(df_events)>0:
        wiki_str='In dit jaar waren er de volgende gebeurtenissen die te maken hebben met <mark>'+specific_word+'</mark><br>'
        
        
    for i in range(0,len(df_events)):
        date_str = df_events['date'].loc[i]
        event_str=df_events['event'].loc[i]
        
        event_str_html=''
        for word in event_str.split():
            if specific_word.lower() in word.lower():
                event_str_html = event_str_html+' '+'<mark>' + word + '</mark>'
            else:
                event_str_html = event_str_html+' '+word
        wiki_str=wiki_str + '<h1>'+date_str+':'+event_str_html.strip() +'<h1>'
    
    return wiki_str
    
