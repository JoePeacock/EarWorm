import flask
import os
import random
import datetime
import simplejson
import urllib
import db
from tornado.database import Connection
from flask import Flask, request, g

app = Flask(__name__)
app.debug = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# Connects to Database before anything else. Using the file config.py for the db connection
@app.before_request
def open_db():
	g.db = Connection('localhost', 'earworm', 'root', 'whatever')

# After completing the request, the database is closed so there are not multiple connections. 
@app.after_request
def close_db(response):
	g.db.close()
	return response

@app.route("/", methods=['POST', 'GET'])
def hello():
	results = []
	if flask.request.method == 'POST':
		name = flask.request.form['username']
		url =  flask.request.form['youtube-url']
		now = str(datetime.datetime.now())
		title = Youtube(url)
		post = db.Posts(name, title, url, now)
		db.session.add(post)
		db.session.commit()
		# addevent = g.db.execute('INSERT INTO posts (name, song, url, date) values (%s, %s, %s, %s)', name, title, url, now)
		# results = g.db.query('SELECT * FROM posts');
	return flask.render_template("index.html", results=results)

def Youtube(url):
	split = url.split('/')
	watch = split[3].split('=')
	id = watch[1]
	url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
	json = simplejson.load(urllib.urlopen(url))
	title = json['entry']['title']['$t']
	author = json['entry']['author'][0]['name']
	return title

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1337))
    app.run(host='127.0.0.1', port=port, debug=True)
