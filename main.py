from flask import Flask, request, jsonify, abort, make_response
import sqlite3


app = Flask(__name__)
db_path = '//Users/karolmucha/test.db'

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({ 'error': 'Invalid arguments defined' }), 400)

@app.route('/hello')
def index():
    return "Hello, World!"

@app.route('/users/add', methods=['POST'])
def add_user():
	if 'username' not in request.json or 'password' not in request.json:
		abort(400)

	conn = sqlite3.connect(db_path)

	try:
		conn.execute("INSERT INTO users (username, password, active, is_admin) VALUES (?, ?, 1, 0)", 
			(request.json['username'],(request.json['password'])))
		conn.commit()
	except:
		return jsonify({'error': "username already taken"})
	cursor = conn.execute("SELECT MAX(id) FROM users")
	result = cursor.fetchone()
	conn.close()
	return jsonify({'id': result})

@app.route('/users/get_by_id', methods=['GET'])
def get_user():
	if 'id' not in request.json:
		abort(400)
	conn = sqlite3.connect(db_path)

	try:
		cursor = conn.execute("SELECT username, password FROM users WHERE id = " + str(request.json['id']))
	except:
		return jsonify({ 'error': 'No such id' })

	result = cursor.fetchone()
	conn.close()
	return jsonify({'username': result[0], 'password': result[1]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)