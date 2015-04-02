from app import mongo

class Phone(mongo.Document):

	brand = mongo.StringField(max_length = 255, required = True)
	model = mongo.StringField(max_length = 255, required = True)

	sentiments = mongo.ListField(db.EmbeddedDocumentField('Sentiment'))
	specifications = mongo.DictField(default = {}, require = True)
	pros_cons = mongo.ListField(db.EmbeddedDocumentField('ProsCons'))

	def __unicode__(self):
		return "%s : %s"%(self.brand, self.model)

class Sentiment(mongo.EmbeddedDocument):
	about = mongo.StringField(required = True)
	positive = mongo.IntField(default = 0, required = True)
	neutral = mongo.IntField(default = 0, required = True)
	negative = mongo.IntField(default = 0, required = True)

class ProsCons(mongo.EmbeddedDocument):
	about = mongo.StringField(required = True)
	positive = mongo.ListField(db.EmbeddedDocumentField('Review'), required = True, default = [])
	negative = mongo.ListField(db.EmbeddedDocumentField('Review'), required = True, default = [])

class Review(mongo.EmbeddedDocument):

	review = mongo.StringField(required = True)
	num_users = mongo.IntField(default = 0, required = True)
