import requests
from flask import Blueprint,render_template,redirect
from bs4 import BeautifulSoup as BSoup
from flaskr.models import Headline
from flaskr import app, db
from sqlalchemy import func


@app.route('/')
@app.route('/scrape' , methods=['GET'])
def scrape():
    try:
        db.drop_all()
        db.create_all() 
        session = requests.Session()
        session.headers = {"User-Agent" : "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        url = "https://www.theonion.com/latest"
 
        content = session.get(url,verify=False).content
        soup = BSoup(content,"html.parser")
        all_news = soup.find_all('article' , {"class" : "cw4lnv-0 iTueKC js_post_item"})

        # max_id_row =db.session.query(func.max(Headline.id).label('max_id')).one()
        # # print(max_id_row)
        # max_id = max_id_row.max_id
        # i=Headline.query.filter_by(id = max_id).one()
        # i=int(i.id)+1
        # print('max Id :', i)
        i=1

        for news in all_news:
            print('OK 1')
            if news is None:
                pass
            else:
                img = (news.find('figure')).find('div' , {"class" : "js_lazy-image"})
                # print(img)
                img_src= (str(img.find('img')['data-srcset']).split(" ")[-4])
                
                article = news.find('div', {"class" : "aoiLP"})
                link = article.find('a', {"class" : "js_link"})["href"]
                title = article.find('h2').text
                
                try:
                    new_headline = Headline(id=i,title = title,image = img_src,url = link)
                    print("headline created!!!!!!!!!!!!")
                                
                    i = i+1

                    db.session.add(new_headline)
                    print('Headline ADDED!')
                
                    #After all the data processing is ready, the commit will be submitted to the database!
                    db.session.commit() 
                    print("Headline SAVED!") 

                except Exception as e:
                    #Join the database commit failed, must be rolled back! ! !
                    db.session.rollback()
                    raise e
               
    except Exception as e:
        raise e

    return redirect('/index')


@app.route('/index', methods=["GET"])
def news_list():
    headlines = Headline.query.all()
    context = headlines 
    # {
    # 'object_list' : headlines
    # }
    
    return render_template('news/news.html' , object_list=context)


# app.register_blueprint(bp)
# app.register_blueprint(bp1)
# app.add_url_rule('/', endpoint='index')