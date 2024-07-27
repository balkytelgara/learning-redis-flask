from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import g

from . import app
from . import r

@app.before_request
def before_request():
	if not r.get("postcount") or \
		 not r.smembers("posts"):
		r.set("postcount", 0)
		r.sadd("posts", "")

@app.route("/")
def index():
	posts = {}

	if r.smembers("posts"):
		postlist = list(r.smembers("posts"))[1:]

		for i, j in enumerate(postlist):
			posttitle, postcontent = r.hmget(j, "posttitle", "postcontent")
			posts[i] = {
				"posttitle": posttitle,
				"postcontent": postcontent
			}

	return render_template("index.htm", posts=posts)

@app.route("/post", methods=["POST"])
def post():
	posttitle = request.form.get("posttitle")
	postcontent = request.form.get("postcontent")
	postcount = int(r.get("postcount"))
	post = "post:%s" % postcount

	r.hset(post, mapping={
		"posttitle": posttitle,
		"postcontent": postcontent
	})

	r.sadd("posts", post)

	r.set("postcount", postcount + 1)
		
	return redirect(url_for("index"))
