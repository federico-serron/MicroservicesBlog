import datetime
import time
from modules.utilities import slugear
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
                'Date': post.date,
                'Slug': post.slug
            } for post in posts]), 200
    else:
        return 'No posts published for the moment.', 404
    
    
    
@app.route('/admin/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        requested_fields_for_post = ['title', 'description', 'image_url']
        post_data = request.get_json()
        for field in requested_fields_for_post:
            if field not in post_data:
                return f'The field {field} is required', 412
        else:
            try:
                new_post = Posts(title=post_data['title'],
                                 description=post_data['description'],
                                 image_url=post_data['image_url'],
                                 status = 2,
                                 author='Fede manual',
                                 date=datetime.date.today(),
                                 slug=slugear(post_data['title']))
                db.session.add(new_post)
                db.session.commit()
            except Exception:
                return 'There was an error trying to create the new post, please try again.', 412
        return 'The post has been created successfully.', 200
        
    
    
@app.route('/blog/<string:slug>')
def post(slug):
    post = Posts.query.filter_by(slug=slug).first()
    if post:
        return jsonify({
            'Titlte': post.title,
            'Description': post.description
        }), 200
    return 'There was an error, please try again later.', 404
    
    


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