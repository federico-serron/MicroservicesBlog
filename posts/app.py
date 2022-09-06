from distutils.log import debug
import time
from flask import jsonify, request
from config import create_app, db
from models import Posts


app = create_app()
app.app_context().push()


@app.route('/')
def info():
    return jsonify({
        'Enviroment': 'Testing',
        'Version': '1.0',
        'Author': 'Federico Serron'
    }), 200
    
    
    
@app.route('/blog')
def list_all_posts():
    posts = Posts.query.all()
    if len(posts) > 0:
        for post in posts:
            return jsonify([{
                'Title': post.title,
                'Description': post.description,
                'Image': post.image_url,
                'Status': post.status,
                'Author': post.author,
                'Date': post.date
            } for post in posts]), 200
    else:
        return 'No posts published for the moment.', 404
    
    



if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    app.run(debug=True, port=5001, host='0.0.0.0')