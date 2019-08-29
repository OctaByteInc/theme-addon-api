# Copyright 2019 OctaByte Inc. All rights reserved.
# Developer Octabyte

"""This is Endpoint API for shopify apps, Which is used
for products reviews"""

import endpoints
from endpoints import message_types
from endpoints import messages
from endpoints import remote

from google.appengine.ext import ndb

from model.propduct_review import ProductReview
from proto.product_review import *

@endpoints.api(name='Theme Addon API', version='v1')
class ThemeAddonAPI(remote.Service):

    @endpoints.method(
        REVIEW_RESOURCE,
        ReviewMessage,
        path='save_review',
        http_method='POST',
        name='save_review')
    def save_review(self, request):
        parent_key = ndb.Key(ProductReview, request.product_id)

        productReview = ProductReview(parent=parent_key)
        productReview.name = request.name
        productReview.review = request.review
        productReview.stars = request.stars

        ProductReview.put()

        return ReviewMessage(message='Your product review is successfully saved')


    @endpoints.method(
        ProductReview,
        ReviewResponse,
        path='get_reviews',
        http_method='GET',
        name='get_reviews')
    def get_reviews(self, request):
        ancestor_key = ndb.Key(ProductReview, request.product_id)

        productReviews = ProductReview.query_reviews(ancestor_key).fetch()

        reviews = []

        for review in productReviews:
            single_review = Review(review.name,
                                   review.review,
                                   review.stars,
                                   review.date)
            reviews.append(single_review)

        return ReviewResponse(reviews)

# [END api class]


# [START api_server]
api = endpoints.api_server([ThemeAddonAPI])
# [END api_server]
