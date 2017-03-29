from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# connect to mongodb
try:
    client = MongoClient('mongodb', 27017)
except ConnectionFailure:
    print("Server not available")

# simple url for testing
@app.route('/')
def hello_world():
    return 'Hello World!!!'

# Prints out all users
@app.route('/user', methods=['GET'])
def get_all_users():
    user_db = client.test.user

    output = []
    for user in user_db.find():
        output.append({'first_name' : user['first_name'], 'last_name' : user['last_name']})
    return jsonify({'result' : output})

# Adds a new user
@app.route('/user', methods=['POST'])
def add_user():
  user_db = client.test.user

  first_name = request.form['first_name']
  last_name  = request.form['last_name']

  result = user_db.insert_one({'first_name': first_name, 'last_name': last_name})
  result_id = result.inserted_id

  inserted_test = user_db.find_one({'_id': result_id })
  output = {'first_name' : inserted_test['first_name'], 'last_name' : inserted_test['last_name']}
  return jsonify({'result' : output})

# Displays user information given a first name
@app.route('/user/<first_name>', methods=['GET'])
def get_one_user(first_name):
    user_db = client.test.user

    user = user_db.find_one({'first_name' : first_name})
    if user:
        output = {'first_name' : user['first_name'], 'last_name' : user['last_name']}
        return jsonify({'result' : output})
    else:
        return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)