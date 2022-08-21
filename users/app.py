import time
from flask import jsonify, request
from config import create_app, db
from models import Users


app = create_app()
app.app_context().push()

@app.route('/')
def info():
    info = {
        'Enviroment': 'Testing',
        'Version': '1.0',
        'Author': 'Federico Serron'
    }
    return jsonify(info)


@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    if 'username' not in user_data:
        return 'Username/password are required', 412
    elif 'password' not in user_data:
        return 'Username/password are required', 412
    else:
        try:
            new_signup = Users(username = user_data['username'], password = user_data['password'])
            db.session.add(new_signup)
            db.session.commit()
        except Exception:
            return 'There was an error, please try again', 412 
        
        return 'Successfully registered', 200
        


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
            
    app.run(debug=True, port=5000, host='0.0.0.0')
    
    