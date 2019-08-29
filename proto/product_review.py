import endpoints
from endpoints import messages

class ReviewMessage(messages.Message):
    message = messages.StringField(1)

class ProductReview(messages.Message):
    product_id = messages.IntegerField(1, required=True)

class ReviewRequest(messages.Message):
    product_id = messages.IntegerField(1, required=True)
    name = messages.StringField(2, required=True)
    review = messages.StringField(3, required=True)
    stars = messages.IntegerField(4, required=True)


class Review(messages.Message):
    name = messages.StringField(1)
    review = messages.StringField(2)
    stars = messages.IntegerField(3)
    date = messages.DateTimeField(4)


class ReviewResponse(messages.Message):
    reviews = messages.MessageField(Review, 1, repeated=True)


REVIEW_RESOURCE = endpoints.ResourceContainer(ReviewRequest)