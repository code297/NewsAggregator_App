from flaskr import app, db


class Headline(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String())
	image = db.Column(db.String())
	url = db.Column(db.String())

	def __repr__(self):
		return 'Title: '+ (self.title) + ', URL: ' + (self.url) + ', IMG: ' + self.image

	def __init__(self, id, title,image, url):
		self.id = id 
		self.title = title
		self.image = image
		self.url = url
