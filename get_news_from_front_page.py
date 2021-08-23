import meneame as mn
from datetime import datetime, timedelta
import time
import random
import pandas as pd

men=mn.Meneame("https://www.meneame.net")



url=men.construct_page(section='main')

# To capture all the news from the front page for the last 30 days

today=datetime.now()

targetdate= today-timedelta(30)

page_number=1

information_dict={}

while today>=targetdate:

    page_content=men.get_html(url,page_number=page_number)

    status_code=page_content[0]

    html_text=page_content[1]

    # The loop is broken in case non correct code

    if status_code!=200:

        break

    information=men.get_news_from_section(html_text)

    #Add all the information to a dictionary 

    list_of_keys=list(information.keys())

    for k in list_of_keys:
        if k not in information_dict:
            information_dict[k]=[]
        information_dict[k].extend(information[k])
    
    #get the date from the last new

    date_last_new=[int(t) for t in information['send_time'][-1].split()[0].split('-')]

    #update values to iterate

    today = datetime(date_last_new[0], date_last_new[1], date_last_new[2])

    page_number+=1

    #Random sleep between requests

    time.sleep(random.randint(4,8))

    print('Loop over the page {} done!!!'.format(page_number-1))


df=pd.DataFrame(information_dict)

df.to_csv(r'top_news_data.csv',index=False)
