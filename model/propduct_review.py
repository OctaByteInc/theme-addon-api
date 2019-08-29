from google.appengine.ext import ndb

class ProductReview(ndb.Model):

    name = ndb.StringProperty(indexed=false)
    review = ndb.TextProperty(indexed=false)
    stars = ndb.IntegerProperty(indexed=false)
    date = ndb.DateTimeProperty(auto_now_add=true)

    @classmethod
    def query_reviews(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date);
