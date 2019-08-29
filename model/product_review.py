from google.appengine.ext import ndb

class ProductReview(ndb.Model):

    name = ndb.StringProperty(indexed=False)
    review = ndb.TextProperty(indexed=False)
    stars = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_reviews(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date);