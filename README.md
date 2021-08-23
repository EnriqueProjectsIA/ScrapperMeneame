# Scrapper Meneame

## 1. Why meneame is interesting?

Meneame is one of the most popular news aggregators within Spain and it has social netwok features. Due to its structure, its present several characteristics which make it quite interesting for natural language processing (NLP) tasks. Among other possibilities:
  * Meneame allows a distinction between queue news and news that reach front page. That gives a natural splitting between TOP and NO-TOP news.
  * News typically have a significant number of comments, which allows sentiment analysis linked to a particular topic.
  *	News and comments, in first approximation, are not recommended to a list of friends or contacts (everyone has access to everything). That has interesting implications in the field of network analysis.

## 2. Goal

The main goal is to facilitate the collection of public information and perform several NLP and network analysis tasks on dataset which has the potential to be evolving continuously.

## 3. Methods for the class meneame

All the methods listed bellow are in the file meneame.py

  * *construct_page*: Helper function to construct the appropiate page to get information from.
  * *get_html*: It has a double purpose: get the html text and hep to iterate over several pages.
  * *get_news_from_section* It can be used to extract information from published news and queue news.
  * *get_comment_info* gets all the comments of a particular new and the information related with the comments.
  * *get_user_info* The method can be used to get the main stats from a user.
  * *get_user_comments* The method can be used to extract all the comments from a user.
  * *get_user_send_histories* The method can be used to extract all the news send by a user.
  * *get_user_shaken_comments* The method can be used to get all the comments voted by a user.
  * *get_user_shaken_shaken_news* The method can be used to get all the news voted by a user.

  ## 4. Examples

  * *get_news_from_front_page.py*: It captures infromation from the last 30 days.
  * *get_comments_from_news.py*: Capture all the comments from a list of news which has to be provided.
  * *get_news_from_queue_page.py* Capture all the non-top news from the last 30 day.
  * *top_news_data.csv.* Dataset obtained using "get_news_from_section". It includes news for 30 days.

  ## 5. Further considerations

  * The dataset top_news_data.csv can be used as an input for "get_comments_from_news.py"
  * *Send time or send new* refers to when a user has sent a story or new.
  * *Publish time or publish new* refers to when a particular story or new has reach TOP or front page.

