from numpy.core.fromnumeric import transpose
from pandas.io import html
import requests
from bs4 import BeautifulSoup as bs
from datetime import timedelta
from datetime import datetime, timezone
import pandas as pd
import re


def convert_form_unix_time(input : int):
    '''
    Transforms unix time stamps into formated date Spain local time.

    :param input: unix time stamp

    :return: formatted time
    '''
    Madrid_delta=2
    add_time = timedelta(hours = Madrid_delta)
    time_var = datetime.fromtimestamp(input, tz=timezone.utc) + add_time
    
    formated_time = time_var.strftime('%Y-%m-%d %H:%M:%S')
    return formated_time


def numeric_text_cleaning_and_conversion(text: str):

    '''
    Transforms Spanish formated float numbers into redeable format.

    :param text: Numbers in string format

    :return value: It can be an integer or error message
    '''
    
    pattern_comas=re.compile(r',')
    pattern_points=re.compile(r'\.')
    pattern_K=re.compile(r'K')

    if pattern_comas.findall(text)!=[]:
        text=pattern_comas.sub('.',text)
        value=float(text)
    elif pattern_points.findall(text)!=[]:
        text=pattern_points.sub("",text)
        value=int(text)
    elif pattern_K.findall!=[]:
        text=pattern_K.sub("000",text)
        value=int(text)
    else:
        text=text
        value=int(text)
    return value


def create_dictionary(keys: list, information: list)->dict:
    '''
    Create a dictionary from a list of keys and list of lists
    '''
    dict_to_return={}

    for values in information:

        for k,v in zip(keys,values):
            #creates a new key in case, the value k is not a key in the dictionary
            if k not in dict_to_return:
                dict_to_return[k]=[]

            dict_to_return[k].append(v)
    
    return dict_to_return


class Meneame:

    def __init__(self,INPUT_URL):
        self.url=INPUT_URL
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}

    def construct_page(self,section="main",user="",link_story=""):

        
        """The function will construct the website address to extract information
        
        Parameters
        ----------
        user : str, required
            user name
        
        section : str, required
            section = "main","queue","profile",shaken_comments","commented","history","shaken",story (default="main")

        ----------
        """

        url=self.url

        if section=="main" and user=="" and link_story=="":

            url=url
        elif section=="queue" and user=="" and link_story=="":
            url=url+"/{}".format(section)
        
        elif section=='story' and user=='' and link_story!="":
            url=url+"{}".format(link_story)
            
        
        elif section!="" and user!="" and link_story=="":
            url=url+"/user/{}/".format(user)+"{}".format(section)
        
        return url

    def get_html(self,address,page_number=1):
        """
        The function will get the full html text from a website
        use this function to specify the page number
        
        
        ----------
        :param address: str, required
            web address, use the output from the function construct_page as input
        
        :param page_number: integer, number of page to be scrapped

        :return tuple: status_code and html_text
            

        ----------
        """
        if page_number==1 and 'story' not in address.split('/'):
            page = requests.get(address, headers=self.headers)
            full_html_text = bs(page.content,'html.parser')
            code= page.status_code
        elif page_number>1:
            params={"page":page_number}
            page = requests.get(address, headers=self.headers,params=params)
            full_html_text = bs(page.content,'html.parser')
            code= page.status_code
        else:

            try:
                if 'story'==address.split('/')[3]:
                    code=200
                    i=1
                    full_html_text=[]

                    while code==200:
                        page = requests.get(address+'/'+str(i), headers=self.headers)
                        code= page.status_code
                        if code !=200:
                            break
                        info = bs(page.content,'html.parser')
                        full_html_text.append(info)
                        i+=1
                    code=200
            except:
                code=404
                full_html_text='Error on request data'

                print("Oops!  Page was not constructed properly")



        return(code,full_html_text)

    def get_news_from_section(self,html_text)->dict:

        ''' 
        This function can be used to extract information from front page news and queue page news

        :param html_text: Use output from get_html

        :return: dictionary
        '''


        content=html_text.find_all("div",attrs= {"class":"news-summary"})

        news=[]

        for var in content:

            new=[]

            try:
                shakes=var.find_all("div", attrs= {"class":"votes"})[0].text.strip().split()[0]
            except:
                shakes="Error"
            ##############################
            try:
                new_id=var.find_all("div",attrs={"class":"news-body"})[0]["data-link-id"]
            except:
                new_id="Error"
            ##############################

            try:  
                relevance=var.find_all("div",attrs={"class":"news-body"})[0].div["class"][1]
            except:
                relevance="Error"
            ###########################################
            try:
                cilcs=var.find_all("div", attrs={"class":"clics"})[0].span.text
            except:
                cilcs="Error"
            ########################################
            try:

                header=var.find_all("h2")[0].a.text.strip()
            except:
                header="Error"
            ##########################
            try:
                link=var.find_all("h2")[0].a["href"]
            except:
                link="Error"

            ###############################  
            try:
                user_id=var.find_all("div", attrs= {"class":"news-submitted"})[0].a["class"][1]
                user_id=re.sub("u:","",user_id)
            except:
                user_id="Error"
            ##############################
            try:
            
                user_nick=var.find_all("div", attrs= {"class":"news-submitted"})[0].a["href"]
                user_nick=re.sub("/user/","",user_nick)
            except:
                user_nick="Error"
            ############################
            try:
                main_tag=var.find_all("span", attrs= {"class":"tool sub-name"})[0].text.strip()
            except:
                main_tag="Error"
            ###############################
            try:
                if main_tag=="Artículos":
                    new_source="Menéame Article"
                else:  
                    new_source=var.find_all("span", attrs= {"class":"showmytitle"})[0].text
            except:
                new_source="Error"

            ###############################
            
            try:
                ref_men_url=var.a['href'].strip()
            except:
                ref_men_url='Error'
            #####################################
            try:
                positive_votes=var.find_all("span", attrs= {"class":"positive-vote-number"})[0].text
            except:
                positive_votes="Error"
            ################################

            try:
                anon_votes=var.find_all("span", attrs= {"class":"anonymous-vote-number"})[0].text
            except:
                anon_votes="Error"
            ###############################
            try:
                negative_votes=var.find_all("span", attrs= {"class":"negative-vote-number"})[0].text
            except:
                negative_votes="Error"
            ################################
            try:
                karma=var.find_all("span", attrs= {"class":"karma-number"})[0].text
            except:
                karma="Error"
            #######################################
            try:
                main_tag=var.find_all("span", attrs= {"class":"tool sub-name"})[0].text.strip()
            except:
                main_tag="Error"
            ###############################
            try:
                number_comments=var.find_all("a",attrs={"class":"comments"})[0]["data-comments-number"]
            except:
                number_comments="Error"
            #############################
            try:
                link_thumbnail=var.find_all("img", attrs={"class":"thumbnail lazy"})[0]["data-src"]
            except:
                link_thumbnail="No Thumbnail"
            #################################
            try:
                text=var.find_all("div", attrs= {"class":"news-content"})[0].text.strip()
            except:
                text="Error"
            #####################################
            try:
                send_time=var.find_all("span",attrs={"title":"enviado: "})[0]["data-ts"]
                send_time=convert_form_unix_time(int(send_time))
            except:
                send_time="Error"
            #####################################
            try:
                publish_time=var.find_all("span",attrs={"title":"publicado: "})[0]["data-ts"]#time to reach front page
                publish_time=convert_form_unix_time(int(publish_time))
            except:
                publish_time="Error"

            new=[new_id,shakes,relevance,cilcs,header,link,new_source,ref_men_url,user_id,user_nick,
            positive_votes,anon_votes,negative_votes,karma,
            main_tag,number_comments,link_thumbnail,send_time,publish_time,
            text]
            news.append(new)

        keys=['new_id','shakes','relevance','cilcs','header','link','new_source','ref_men_url','user_id','user_nick',
        'positive_votes','anon_votes','negative_votes','karma',
        'main_tag','number_comments','link_thumbnail','send_time','publish_time',
        'text']

        dict_news=create_dictionary(keys, news)

        return dict_news

    def get_comment_info(self,html_text)->dict:
        ''' 
        Capture the comments from a story

        
        :param html_text: Use output from get_html. The input will be a list of lists.

        :return: dictionary
        '''
        items=[]
        for item in html_text:
            it=item.find_all('div',attrs= {'class':"comment"})
            items.extend(it)

        comms=[]

        for item in items:
            try:
                if len(item['class']) ==2:
                    relevance=item['class'][1]
                    if relevance=='phantom':
                        relevance='Down voted "deleted"'
                else:
                    relevance=item['class'][0]
            except:
                relevance='Error'
        #####################################
            try:
                num_comment=item['id']
            except:
                num_comment='Error'
        #####################################
            try:
                comment_id=item.a['data-id']
            except:
                comment_id='Error'
            #####################################
            try:
                comment_order=item.find('a',attrs={'class':"comment-order"}).text.strip()
            except:
                comment_order='Error'
            #####################################
            try:
                ref=item.find('a',attrs={'class':"comment-order"})['href']
            except:
                ref='Error'
            #####################################
            try:
                reference_comment=item.find('div',attrs= {'class':"comment-text"}).a['class'][1][2:].split('-')[0]
            except:
                reference_comment='Original new'

            #####################################
            try:
                comment_author=item.find('a',attrs={'class':"username"}).text.strip()
            except:
                comment_author='Error'
            ######################################

            try:
                strong=item.strong.text
                if strong=='*':
                    strong='Edited'
            except:
                strong='No'
            ######################################
            try:
                num_votos=item.find('a',attrs={'title':"Votos"}).text.strip()
            except:
                num_votos='0'
            ######################################
            try:
                karma=item.find('span',attrs={'title':"Karma"}).text.strip().split(' ')[1]
            except:
                karma='Error'
            ######################################
            try:
                text=item.find('div',attrs={'class':"comment-text"}).text.strip()
            except:
                text='Error'

            info=[relevance,num_comment,comment_id,comment_order,ref,reference_comment,comment_author,strong,num_votos,karma,text]
            comms.append(info)

        keys=['relevance','num_comment','comment_id','comment_order',
        'ref','reference_comment','comment_author','strong','num_votos','karma','text']

        dict_comms=create_dictionary(keys,comms)
        
        return dict_comms
        
    def get_user_info(self,html_text):

        ###This section gets general stats and returns and construct a dictionary#####
        ##############################################################################
        list_general_stats = html_text.select("html body div#variable div#wrap div#container \
        section.section.section-large.section-profile div.section-profile-header \
            div.section-profile-header-stats div.row div.col-xs-4 strong")


        dict_stats={
            "Karma":0,
            "Ranking":0,
            "Noticias enviadas":0,
            "Noticias publicadas":0,
            "Comentarios":0,
            "Notas":0
        }
        for key,stat in zip(dict_stats.keys(),list_general_stats):
            dict_stats[key] = numeric_text_cleaning_and_conversion(stat.string)
        
        ###Look for more general information
        
        html_table=html_text.select(".contents-body")
        pattern_keys=re.compile(r'<th>(.*?)</th>')
        pattern_values=re.compile(r'<td>(.*?)</td>')
        html_table=str(list(html_table))
        list_of_keys_in_table=pattern_keys.findall(html_table)
        list_of_table_values=pattern_values.findall(html_table)
        list_of_keys_in_table=[re.sub('</th>',"",re.sub(r'<th>',"",k)) for k in list_of_keys_in_table]
        list_of_table_values=[re.sub('</td>',"",re.sub(r'<td>',"",v)) for v in list_of_table_values]

        ###Add missing information
        for idx,key in enumerate(list_of_keys_in_table):
            if key not in dict_stats.keys():
                dict_stats[key]=list_of_table_values[idx]


        return dict_stats

    def get_user_comments(self,html_text)->dict:
        ''' 
        Capture the comments from a user

        
        :param html_text: Use output from get_html. The input will be a list of lists.

        :return: dictionary
        '''

        time_stamp=html_text.find_all("span", attrs={"class":"ts showmytitle comment-date"})
        additional_information=html_text.find_all("ol", attrs={"class":"comments-list"})

        comments=[]

        for stamp,adinf in zip(time_stamp,additional_information):

            try:
                comment_id=adinf.find_all("a",attrs={"class":"comment-expand"})[0]["data-id"]
            except:
                comment_id="Error"

            #####################################################  
            try:
                comment_text=adinf.find("div", attrs={"class":"comment-text"}).text
            except:
                comment_text="Error"

            ######################################################

            try:
                commented_link= adinf.find_all("a",attrs={"class":"comment-order"})[0]["href"]
            
            except:
            
                commented_link="Error"
            #########################################################
            try:
                time_created=stamp.get("data-ts")
                time_created=convert_form_unix_time(int(time_created))
            except:
                time_created="Error"
            
        ############################################################
            try:
                relevance=adinf.li.div["class"]
                if len(relevance)==1:
                    relevance="Normal"
                else:
                    relevance=relevance[1]
            except:

                relevance="Error"
            ###########################################################
            try:
                try:
                    votes=adinf.find("a", attrs={"title":"Votos"}).string
                    
                except:
                    votes=adinf.find("span", attrs={"title":"Votos"}).string
            
                votes=votes.strip()
            except:
                votes="Error"
        #############################################################

            try:
                karma=adinf.find("span", attrs={"title":"Karma"})
                pattern=re.compile(r'</i>\s(.*)\s</span>')
                karma=pattern.findall(str(karma))[0]
            except:
                karma="Error"


            comments.append([comment_id,comment_text,commented_link,time_created,relevance,votes,karma])
        
        keys=['comment_id','comment_text','commented_link','time_created','relevance','votes','karma']

        dict_user_comments=create_dictionary(keys,comments)

        return dict_user_comments

    def get_user_send_histories(self,html_text)->dict:
        content=html_text.find_all("div",attrs={"class":"news-summary"})
        news=[]
        for new in content:
            info=[]
            try:
                strory_link=new.a["href"]
            except:
                strory_link="Error"
            #####################

            try:      
                story_title=new.find_all("h2")[0].text.strip()
            except:
                story_title="Error"
            ##################
            try:
                shaken=new.find_all("div", attrs={"class":"votes"})[0].text.strip().split()[0]
            except:
                shaken="Error"
            ##########################
            try:      
                story_clics=new.find_all("div",attrs={"class":"clics"})[0].span.text
            except:
                story_clics="Error"
            ###############################

            try:
                relevance=new.div.div["class"][1]
            except:
                relevance="Error"
            ################################

            try:

                story_state=new.find_all("div",attrs={"class":"menealo"})[0].span.text
            except:
                story_state="Error"
            #####################################
            try:
            
                tags=[]
                for item in new.find_all("a"):
                    if 'href="/search?' in str(item):
                        tags.append(item.text.strip())
            except:
                tags="Error"
            ########################################
            try:
                publish_time=new.find_all("span",attrs={"class":"ts visible"})[0]["data-ts"]
                publish_time=convert_form_unix_time(int(publish_time))
            except:
                publish_time=n="Error"


            info=[strory_link,story_title,shaken,story_clics,relevance,story_state,tags,publish_time]
            news.append(info)

        keys_info=['strory_link','story_title','shaken','story_clics','relevance','story_state','tags','publish_time']

        dict_info=create_dictionary(keys_info,info)

        
        return dict_info

    def get_user_shaken_comments(self,html_text)->dict:

        ''' 
        Capture the comments voted by a user

        
        :param html_text: Use output from get_html. 

        :return: dictionary
        '''
        var=html_text.find_all("li", attrs= {"style":"position: relative"})
        shaken_comments_info=[]

        for item in var:
            shaken_comment=[]
            try:
                comment_id=item.div["id"]
            except:
                comment_id="Error"
            #########################################

            try:
                relevance=item.div["class"]
                relevance=relevance[1] if len(relevance)!=1 else relevance[0]
            except:
                relevance="Error"
            ###########################################
            try:
                comment_author=item.find_all("a", attrs={"class":"username"})[0].text
            except:
                comment_author="Error"
            ###############################################
            try:
                commnet_send=item.find_all("span", attrs={"title":"creado: "})[0]["data-ts"]
                commnet_send=convert_form_unix_time(int(commnet_send))
            except:
                commnet_send="Error"
            ############################################
            try:
                try:
                    votes=item.find_all("a",attrs= {"title":"Votos"})[0].text.strip()
                except:
                    votes=item.find_all("span", attrs={"title":"Votos"})[0].text.strip()
            except:
                votes="Error"
            #############################################
            try:
                karma=item.find_all("span", attrs={"title":"Karma"})[0].text.strip().split()[1]
            except:
                karma="Error"
            ############################################
            try:
                text=item.find_all("div", attrs= {"class":"comment-text"})[0].text.strip()
            except:
                text="Error"
            ###########################################
            try:
                link_story=item.find_all("a",attrs= {"class":"comment-order"})[0]["href"]
            except:
                link_story="Error"

            shaken_comment=[comment_id,relevance,comment_author,commnet_send,votes,karma,text,link_story]
            shaken_comments_info.append(shaken_comment)

        keys=['comment_id','relevance','comment_author','commnet_send','votes','karma','text','Link_story']

        dict_shaken_comments=create_dictionary(keys,shaken_comments_info)

        return dict_shaken_comments

    def get_user_shaken_news(self,html_text)->dict:

        ''' 
        Capture the stories voted by a usr

        
        :param html_text: Use output from get_html.

        :return: dictionary
        '''
        
        list_news=html_text.find_all("div", attrs={"class":"news-summary"})

        info=[]

        for item in list_news:
            try:
                relevance=item.find_all_next("div",attrs={"class":"news-body"})[0].div["class"][1]
            except:
                relevance="Error"
            #################################
            try:
                story_id=item.div["data-link-id"]
            except:
                story_id="Error"
            ####################################
            try:
                story_title=item.h2.a.text.strip()
            except:
                story_title="Error"
            ####################################
            try:
                ref_url=item.a['href']
            except:
                ref_url="Error"
            ######################################
            try:
                web_ref=item.h2.a['href']
            except:
                web_ref="Error"
            ######################################
            try:
                votes=item.find_all_next("div",attrs= {"class":"votes"})[0].a.text
            except:
                votes="Error"
            #####################################
            try:
                num_clics=item.find_all_next("div",attrs= {"class":"clics"})[0].span.text
            except:
                num_clics="Error"
            #####################################
            try:
                num_comm=item.find_all_next("a", attrs= {"class":"comments"})[0]["data-comments-number"]
            except:
                num_comm="Error"
            #####################################
            try:
                time_send=item.find_all_next("span", attrs={"class":"ts visible"})[0]["data-ts"]
                time_send=convert_form_unix_time(int(time_send))
            except:
                time_send="Error"
            #######################################
            try:
                if relevance=='mnm-published':
                    time_pubilsh=item.find_all('span',attrs={"title":"publicado: "})[0]['data-ts']
                    time_pubilsh=convert_form_unix_time(int(time_pubilsh))
                else:
                    time_publish='Story does not reach main'
            except:

                time_pubilsh= "Error"    
            #######################################
            try:
                user = item.find_all_next("div", attrs= {"class":"news-submitted"})[0].a.text
            except:
                user="Error"
            ########################################
            try:
                tag=item.find_all_next("a",attrs={"class":"subname"})[0].text
            except:
                tag="Error"
            ################################
            try:
                thumb=item.find_all('img', attrs={'class':"thumbnail lazy"})[0]['data-src']
            except:
                thumb='No thumbnail'

            items_list=[story_id,story_title,ref_url,web_ref,relevance,votes,num_clics,num_comm,time_send,time_pubilsh,user,tag,thumb]

            info.append(items_list)

        keys_info=['story_id','story_title','ref_url','web_ref','relevance',
        'votes','num_clics','num_comm','time_send','time_pubilsh','user','tag','thumbnail']

        dict_info=create_dictionary(keys_info,info)

        return(dict_info)

if __name__ == "__main__":

    df=pd.read_csv(r'/Users/alvaro/Desktop/Python/Scrapper/top_news_data.csv')
    story_link=df['ref_men_url'].iloc[0]

    meneame_obj=Meneame("https://www.meneame.net")
    url=meneame_obj.construct_page(section="story",link_story=story_link)

    full_html_text=meneame_obj.get_html(url,page_number=1)[1]

    info=meneame_obj.get_comment_info(full_html_text)

    list_of_keys=list(info.keys())

    number_of_comments=len(info[list_of_keys[0]])


    print(info)











