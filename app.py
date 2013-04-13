import flask
import os
import random
import datetime
import simplejson
import urllib
import db
import time
import json
import ytservice
from time import mktime
from sqlalchemy import desc
from flask import Flask, request, g

app = Flask(__name__)
app.debug = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
yt = ytservice.YoutubeAPI()

@app.route("/earworm", methods=['POST', 'GET'])
def hello():
	results = []
	error = None
	postsHere = True;
	for row in db.session.query(db.Posts).order_by(db.Posts.date.desc()): 
		if row == None:
			postsHere = False
		else:
			currDateTime = datetime.datetime.now()
			dateDiff = compareDate(row.date, currDateTime)
			row = {'name':row.name, 'song':row.song, 'url':row.url, 'date':dateDiff}
			results.append(row)
	if flask.request.method == 'POST':
		name = flask.request.form['username']
		url =  flask.request.form['youtube-url']
		now = str(datetime.datetime.now())
		if url != "":
			title = Youtube(url)
			post = db.Posts(name, title, url, now)
			db.session.add(post)
			db.session.commit()
			results.insert(0, {"name": name, "song": title, "url": url, "date": compareDate(now, now)})
		else:
			error = "Please input a YouTube url."
	return flask.render_template("index.html", results=results, error=error, Posts=postsHere)

@app.route("/test", methods=['POST', 'GET'])
def testsearch():
	return flask.render_template('test.html')

@app.route('/search/<query>', methods=['GET'])
def search(query):
	res = []
	search = request.args['q']
	results = yt.search(search)
	for item in results.entry:
		res.append({'title': unicode(item.media.title.text, 'utf-8', 'ignore'), "url":item.media.player.url, 'img':item.media.thumbnail[0].url})
	test = json.dumps(res)
	print test
	return test

def Youtube(url):
	split = url.split('/')
	watch = split[3].split('=')
	id = watch[1]
	url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id
	json = simplejson.load(urllib.urlopen(url))
	title = json['entry']['title']['$t']
	author = json['entry']['author'][0]['name']
	return title

def compareDate(input, current):
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
	current = str(current)
	ins = input.split('.', 1)[0]
	input = time.strptime(ins, '%Y-%m-%d %H:%M:%S')
	curr = current.split('.', 1)[0]
	current = time.strptime(curr, '%Y-%m-%d %H:%M:%S')
	current = datetime.datetime.fromtimestamp(mktime(current))
	input = datetime.datetime.fromtimestamp(mktime(input))
	deltaDays = current - input
	if deltaDays.days == 0:
		if (current.hour - input.hour) > 0:
			if (current.hour - input.hour) == 1:
				return "1 hour ago"
			return str(current.hour - input.hour) + " hours ago"
		else:
			return str(current.minute - input.minute) + " minutes ago"
	else:
		return str(input.day) + " " + str(month[input.month])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='208.68.37.33', port=port, debug=True)

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 1337))
#     app.run(host='127.0.0.1', port=port, debug=True)
