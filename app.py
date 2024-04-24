from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import pipeline
import nest_asyncio
nest_asyncio.apply()
from requests_html import HTMLSession
import warnings
import pyttsx3
import time
from Crawlers.HeadlinesCrawler import getHeadlines
from Crawlers.CategoryNewsCrawler import getNewsByCategory

engine = pyttsx3.init()
warnings.filterwarnings('ignore') 

app = Flask(__name__)
model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

news = """"""

def getHeadlines():
    headlines = []
    session = HTMLSession()
    url = "https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en"
    # nest_asyncio.apply()
    req = session.get(url)
    req.html.arender(sleep=20, scrolldown=20)
    articles = req.html.find('article')
    newslist = []
    for article in articles:
        try:
            news = article.find('.gPFEn', first=True)
            n = {"Title" : news.text, "Link" : list(news.absolute_links)[0] }
            newslist.append(n)
        except:
            news = article.find('.JtKRv', first=True)
            n = {"Title" : news.text, "Link" : list(news.absolute_links)[0]}
            newslist.append(n)
    for nl in newslist:
        try:
            req_news = session.get(nl['Link'], allow_redirects=True)
            req_news.html.arender(sleep=10, scrolldown=5)
            url = list(req_news.html.find('a')[-1].absolute_links)[0]
            req_news = session.get(url, allow_redirects=True)
            req_news.html.arender(sleep=10, scrolldown=5)
            if "hindustantimes" in url:
                paras = req_news.html.find('.mainContainer')[0].find('p')
                story = ""
                for para in paras:
                    if not (para.find('a') or para.find('script')):
                        story += para.text
            elif "ndtv" in url:
                paras = req_news.html.find('.ins_storybody')[0].find('p')
                story = ""
                for para in paras:
                    if not (para.find('a') or para.find('script')):
                        story += para.text
            elif "timesofindia" in url:
                if req_news.html.find('.KB5o3'):
                    paras = req_news.html.find('.KB5o3')[0].find('p')
                    story = ""
                    for para in paras:
                        if not (para.find('a') or para.find('script')):
                            story += para.text
                else:
                    paras = req_news.html.find('._s30J')[0]
                    story = paras.text
            elif "businesstoday" in url:
                paras = req_news.html.find('.text-formatted')[0].find('p')
                story = ""
                for para in paras:
                    if not (para.find('a') or para.find('script')):
                        story += para.text
            elif "indianexpress" in url :
                paras = req_news.html.find('#pcl-full-content')[0].find('p').extend(req_news.html.find('.ev-meter-content')[0].find('p'))
                story = ""
                for para in paras:
                    story += para.text
                print(story)
            else:
                continue
            headlines.append({
                "title" : nl["Title"],
                "body" : summarizer(story, max_length=min(150,story.count(" ")), min_length=min(50, story.count(" ")), do_sample=False)[0]["summary_text"]
            })
        except:
            pass
    return headlines

def getNewsByCategory(category):
    headlines = []
#     print("Here are the top news on " + category + "... \n\n")
    session = HTMLSession()
    url = ("https://news.google.com/search?q=" + category).replace(" ", "%20")
    req = session.get(url)
    req.html.arender(sleep=5, scrolldown=500)
    articles = req.html.find('article')
    newslinks = []
    count = 0
    for article in articles:
        time = article.find('.hvbAAd')[0].text
        if "minute" in time or "hour" in time:
            n = {}
            news = article.find('.JtKRv', first=True)
            n["Title"] = news.text
            n["Link"] = list(news.absolute_links)[0]
            newslinks.append(n)
            count += 1
        if count >= 10:
            break
    print(newslinks)
    for nl in newslinks:
        try:
            req_news = session.get(nl['Link'], allow_redirects=True)
            req_news.html.arender(sleep=10, scrolldown=5)
            url = list(req_news.html.find('a')[-1].absolute_links)[0]
            if "indianexpress" in url :
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.story_details', first=True).find('p')
                story = ""
                for para in paras:
                    story += para.text
                headlines.append({
                    "title" : nl["Title"],
                    "body" : summarizer(story, max_length=min(150,story.count(" ")), min_length=min(50, story.count(" ")), do_sample=False)[0]["summary_text"]
                })
            elif "timestech" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.td-post-content', first=True).find('p')
                story = ""
                for para in paras:
                    story += para.text
                headlines.append({
                    "title" : nl["Title"],
                    "body" : summarizer(story, max_length=min(150,story.count(" ")), min_length=min(50, story.count(" ")), do_sample=False)[0]["summary_text"]
                })
            elif "livemint" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.paywall', first=True).find('p')
                story = ""
                for para in paras:
                    story += para.text
                headlines.append({
                    "title" : nl["Title"],
                    "body" : summarizer(story, max_length=min(150,story.count(" ")), min_length=min(50, story.count(" ")), do_sample=False)[0]["summary_text"]
                })
            elif "timesofindia" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                try:
                    req_news.html.find('.KB5o3')
                    paras = req_news.html.find('.KB5o3')[0].find('p')
                    story = ""
                    for para in paras:
                        if not (para.find('a') or para.find('script')):
                            story += para.text
                except:
                    try:
                        paras = req_news.html.find('._s30J')[0]
                        story = paras.text
                    except Exception as Argument:
                        print(str(Argument))
                        pass
                headlines.append({
                    "title" : nl["Title"],
                    "body" : summarizer(story, max_length=min(150,story.count(" ")), min_length=min(50, story.count(" ")), do_sample=False)[0]["summary_text"]
                })
        except:
            pass
    return headlines

def getNewsByTopic(topic):
    print("Fetching news about " + topic + "... \n\n")
    session = HTMLSession()
    url = "https://news.google.com/search?q=" + topic + "&hl=en-IN&gl=IN&ceid=IN%3Aen"
    req = session.get(url)
    req.html.arender(sleep=5, scrolldown=500)
    articles = req.html.find('article')
    count = 0
    stories = ""
    for article in articles:
        news = article.find('.JtKRv', first=True) 
        nl = list(news.absolute_links)[0]
        try:
            req_news = session.get(nl, allow_redirects=True)
            req_news.html.arender(sleep=10, scrolldown=5)
            url = list(req_news.html.find('a')[-1].absolute_links)[0]
            if "indianexpress" in url :
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.story_details', first=True).find('p')
                story = ""
                for para in paras:
                    story += para.text
                stories += summarizer(story, max_length=min(300,story.count(" ")), min_length=min(150, story.count(" ")), do_sample=False)[0]["summary_text"]+"\n"
                count += 1
            elif "timestech" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.td-post-content', first=True).find('p')
                story = ""
                for para in paras:
                     story += para.text
                stories += summarizer(story, max_length=min(300,story.count(" ")), min_length=min(150, story.count(" ")), do_sample=False)[0]["summary_text"]+"\n"
                count += 1
            elif "livemint" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                paras = req_news.html.find('.paywall', first=True).find('p')
                story = ""
                for para in paras:
                    story += para.text
                stories += summarizer(story, max_length=min(300,story.count(" ")), min_length=min(150, story.count(" ")), do_sample=False)[0]["summary_text"]+"\n"
                count += 1
            elif "timesofindia" in url:
                req_news = session.get(url, allow_redirects=True)
                req_news.html.arender(sleep=10, scrolldown=5)
                try:
                    req_news.html.find('.KB5o3')
                    paras = req_news.html.find('.KB5o3')[0].find('p')
                    story = ""
                    for para in paras:
                        if not (para.find('a') or para.find('script')):
                            story += para.text
                except:
                    try:
                        paras = req_news.html.find('._s30J')[0]
                        story = paras.text
                    except Exception as Argument:
                        print(str(Argument))
                        pass
                stories += summarizer(story, max_length=min(300,story.count(" ")), min_length=min(150, story.count(" ")), do_sample=False)[0]["summary_text"]+"\n"
                count += 1
        except:
            pass
        if count >= 3:
            return summarizer(stories, max_length=min(300,stories.count(" ")), min_length=min(150, stories.count(" ")), do_sample=False)[0]["summary_text"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def answer_question():
    global news
    data = request.get_json()
    question = data['question']
    print(question)
    if question == "Headlines":
        print("Getting headlines")
        hl = getHeadlines()
        if hl:
            for i in hl:
                news += i["title"] + "\n" + i["body"] + "\n\n"
            return jsonify({'answer': hl})
    elif "CATEGORY" in question:
        question = question.replace("CATEGORY : ", "")
        print("Getting news for the category :", question)
        hl = getNewsByCategory(question)
        if hl:
            for i in hl:
                news += i["title"] + "\n" + i["body"] + "\n\n"
            print(hl)
            return jsonify({'answer': hl})
        else:
            return jsonify({'answer': "Sorry I couldn't find any news for the category you asked for."})
    elif "TOPIC" in question:
        question = question.replace("TOPIC : ", "")
        hl = getNewsByTopic(question)
        if hl:
            print(hl)
            return jsonify({'answer': hl})
        else:
            return jsonify({'answer': "Sorry I couldn't find any news for the topic you asked for."})
    else:
        input_text = "question: {} context: {}".format(question, news)
        encoded_input = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)
        output = model.generate(input_ids=encoded_input.input_ids, attention_mask=encoded_input.attention_mask)
        print(news)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        if answer:
            return jsonify({'answer': answer})
        else:
            return jsonify({'answer': "Sorry, I don't understand what you're asking about."})

if __name__ == '__main__':
    app.run(debug=True)
