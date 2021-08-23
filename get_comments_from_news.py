import meneame as mn
import pandas as pd
from tqdm import tqdm
import time
import random
import requests
from bs4 import BeautifulSoup as bs

df_news=pd.read_csv(r'top_news_data.csv')
men=mn.Meneame("https://www.meneame.net")
dict_comments={}
list_of_errors=[]


for row in tqdm(df_news.iterrows()):

    new_id,story_link=row[1]['new_id'],row[1]['ref_men_url']

    url=men.construct_page(section="story",link_story=story_link)

    code=men.get_html(url,page_number=1)[0]

    html_text=men.get_html(url,page_number=1)[1]

    if code!=404:

        dict_comments_from_story=men.get_comment_info(html_text)

        list_of_keys=list(dict_comments_from_story.keys())

        number_of_comments=len(dict_comments_from_story[list_of_keys[0]])

        reference_story=[new_id]*number_of_comments

        dict_comments_from_story['new_id']=reference_story

        list_of_keys=list(dict_comments_from_story.keys())

        for k in list_of_keys:
            if k not in dict_comments:
                dict_comments[k]=[]

            dict_comments[k].extend(dict_comments_from_story[k])
    else:

        list_of_errors.append((new_id,story_link))

    
    time.sleep(random.randint(2,5))

df=pd.DataFrame(dict_comments)

df.to_csv(r'comments_top_news_data.csv',index=False)