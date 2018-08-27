from random import *
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask import Flask, render_template, jsonify

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={"/api/*": {"origins": "*"}})

app.config['MONGODB_SETTINGS'] = {
    'db': 'jianshu',
    'host': '127.0.0.1',
    'port': 27017
    }
db = MongoEngine(app)

class Dailyinfo(db.Document):
    meta = {
        'collection': 'author_info',
        'ordering': ['date'],
        'strict': False,
    }

    uid = db.StringField()
    name = db.StringField()
    img = db.StringField()
    date = db.StringField()
    following = db.StringField()
    follows = db.StringField()
    article_nums = db.StringField()
    word_nums = db.StringField()
    like_nums = db.StringField()
    article_details = db.ListField()
    follows_details = db.ListField()

@app.route('/api/base/<uid>')
def base(uid):
    baseinfo = Dailyinfo.objects(uid=uid).order_by('-date').all()
    new_follows = int(baseinfo[0]['follows']) - int(baseinfo[1]['follows'])
    new_article = int(baseinfo[0]['article_nums']) - int(baseinfo[1]['article_nums'])
    new_word = int(baseinfo[0]['word_nums']) - int(baseinfo[1]['word_nums'])
    new_like = int(baseinfo[0]['like_nums']) - int(baseinfo[1]['like_nums'])
    info = Dailyinfo.objects(uid=uid).all()
    date = []
    follows = []
    following = []
    article_nums = []
    word_nums = []
    like_nums = []
    read_nums = []
    review_nums = []
    most_read = {}
    most_review = {}
    most_like = {}
    follows_words = {}
    follows_follows = {}
    follows_likes = {}
    follows_articles = {}
    follows_following = {}
    name = info[0]['name']
    img = info[0]['img']
    for i in info:
        date.append(i['date'])
        follows.append(i['follows'])
        following.append(i['following'])
        article_nums.append(i['article_nums'])
        word_nums.append(i['word_nums'])
        like_nums.append(i['like_nums'])
        read_nums.append(sum([int(a['read_num']) for a in i['article_details']]))
        review_nums.append(sum([int(a['comment_num']) for a in i['article_details']]))
        #most_read[i['date']] = sorted(i['article_details'], key = lambda e:int(e.__getitem__('read_num')), reverse = True)
        #most_review[i['date']] = sorted(i['article_details'], key = lambda e:int(e.__getitem__('comment_num')), reverse = True)
        #most_like[i['date']] = sorted(i['article_details'], key = lambda e:int(e.__getitem__('heart_num')), reverse = True)
        #follows_words[i['date']] = sum([int(a['word_nums']) for a in i['follows_details']])
        #follows_follows[i['date']] = sum([int(a['follows']) for a in i['follows_details']])
        #follows_likes[i['date']] = sum([int(a['like_nums']) for a in i['follows_details']])
        #follows_articles[i['date']] = sum([int(a['article_nums']) for a in i['follows_details']])
        #follows_following[i['date']] = sum([int(a['following']) for a in i['follows_details']])
    res = {
        'follows':follows,
        'following': following,
        'article_nums': article_nums,
        'word_nums': word_nums,
        'like_nums': like_nums,
        'read_nums': read_nums,
        'review_nums': review_nums,
        #'most_read': most_read,
        #'most_review': most_review,
        #'most_like': most_like,
        #'follows_words': follows_words,
        #'follows_follows': follows_follows,
        #'follows_likes': follows_likes,
        #'follows_articles': follows_articles,
        #'follows_following': follows_following,
        'date': date,
        'name': name,
        'img': img,
        'uid': uid,
        'new_word': new_word,
        'new_like': new_like,
        'new_article': new_article,
        'new_follows': new_follows
    }
    return jsonify(res)

@app.route('/api/article/<uid>')
def article(uid):
    a = Dailyinfo.objects(uid=uid).order_by('-date').all()
    #article = sorted(a[1]['article_details'], key = lambda e:int(e.__getitem__('heart_num')), reverse = True) if a else None
    article = []
    for i in a[1]['article_details']:
        d = i.copy()
        s = "https://www.jianshu.com"+i['link']
        d.update({'link': s})
        article.append(d)
    res = {
        'article': article
    }
    return jsonify(res)


@app.route('/api/follows/<uid>')
def follows(uid):
    info = Dailyinfo.objects(uid=uid).all()
    date = []
    follows_words = {}
    follows_follows = {}
    follows_likes = {}
    follows_articles = {}
    follows_following = {}
    follows_most_words = {}
    follows_most_follows = {}
    follows_most_likes = {}
    follows_most_articles = {}
    follows_most_following = {}
    for i in info:
        date.append(i['date'])
        follows_follows[i['date']] = sum([int(a['follows']) for a in i['follows_details']])
        follows_likes[i['date']] = sum([int(a['like_nums']) for a in i['follows_details']])
        follows_articles[i['date']] = sum([int(a['article_nums']) for a in i['follows_details']])
        follows_following[i['date']] = sum([int(a['following']) for a in i['follows_details']])
        follows_most_words[i['date']] = sorted(i['follows_details'], key = lambda e:int(e.__getitem__('word_nums')), reverse = True)
        follows_most_follows[i['date']] = sorted(i['follows_details'], key = lambda e:int(e.__getitem__('follows')), reverse = True)
        follows_most_likes[i['date']] = sorted(i['follows_details'], key = lambda e:int(e.__getitem__('like_nums')), reverse = True)
        follows_most_articles[i['date']] = sorted(i['follows_details'], key = lambda e:int(e.__getitem__('article_nums')), reverse = True)
        follows_most_following[i['date']] = sorted(i['follows_details'], key = lambda e:int(e.__getitem__('following')), reverse = True)
    res = {
        'follows_words': follows_words,
        'follows_follows': follows_follows,
        'follows_likes': follows_likes,
        'follows_articles': follows_articles,
        'follows_following': follows_following,
        'follows_most_words': follows_most_words,
        'follows_most_follows': follows_most_follows,
        'follows_most_likes': follows_most_likes,
        'follows_most_articles': follows_most_articles,
        'follows_most_following': follows_most_following,
        'date': date
    }
    return jsonify(res)

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
