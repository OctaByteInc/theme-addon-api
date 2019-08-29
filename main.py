# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample Hello World API implemented using Google Cloud
Endpoints."""

# [START imports]
import endpoints
from endpoints import message_types
from endpoints import messages
from endpoints import remote

from google.appengine.ext import ndb

from custom import Custom

from model.book import Book
#import custom as cs
# [END imports]


# [START messages]
class EchoRequest(messages.Message):
    message = messages.StringField(1)


class EchoResponse(messages.Message):
    """A proto Message that contains a simple string field."""
    message = messages.StringField(1)


ECHO_RESOURCE = endpoints.ResourceContainer(
    EchoRequest,
    n=messages.IntegerField(2, default=1))
# [END messages]


# [START echo_api_class]
@endpoints.api(name='echo', version='v1')
class EchoApi(remote.Service):

    # [START echo_api_method]
    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        ECHO_RESOURCE,
        # This method returns an Echo message.
        EchoResponse,
        path='echo',
        http_method='POST',
        name='echo')
    def echo(self, request):
        output_message = 'New API '.join([request.message] * request.n)
        return EchoResponse(message=output_message)
    # [END echo_api_method]

    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        ECHO_RESOURCE,
        # This method returns an Echo message.
        EchoResponse,
        path='echo/{n}',
        http_method='POST',
        name='echo_path_parameter')
    def echo_path_parameter(self, request):
        output_message = ' '.join([request.message] * request.n)
        return EchoResponse(message=output_message)

    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        message_types.VoidMessage,
        # This method returns an Echo message.
        EchoResponse,
        path='echo/getApiKey',
        http_method='GET',
        name='echo_api_key',
        api_key_required=True)
    def echo_api_key(self, request):
        key, key_type = request.get_unrecognized_field_info('key')
        return EchoResponse(message=key)

    @endpoints.method(
        # This method takes an empty request body.
        message_types.VoidMessage,
        # This method returns an Echo message.
        EchoResponse,
        path='echo/email',
        http_method='GET',
        # Require auth tokens to have the following scopes to access this API.
        scopes=[endpoints.EMAIL_SCOPE],
        # OAuth2 audiences allowed in incoming tokens.
        audiences=['your-oauth-client-id.com'],
        allowed_client_ids=['your-oauth-client-id.com'])
    def get_user_email(self, request):
        user = endpoints.get_current_user()
        # If there's no user defined, the request was unauthenticated, so we
        # raise 401 Unauthorized.
        if not user:
            raise endpoints.UnauthorizedException
        return EchoResponse(message=user.email())

    @endpoints.method(
        message_types.VoidMessage,
        EchoResponse,
        path='test',
        http_method='GET')
    def test(self, request):
        book = Book()
        return EchoResponse(message=book.m)

    @endpoints.method(
        message_types.VoidMessage,
        EchoResponse,
        path='echo2',
        http_method='GET')
    def echo2(self, request):
        m = Custom(parent=ndb.Key("Book", "Book title"), content='content changed')
        m.put()
        return EchoResponse(message='Data saved')
    
    @endpoints.method(
        message_types.VoidMessage,
        EchoResponse,
        path='echo3',
        http_method='GET')
    def echo3(self, request):
        ancestor_key = ndb.Key("Book", "Book title")
        ms = Custom.query_custom(ancestor_key).fetch(1)

        for greeting in ms:
            return EchoResponse(message=greeting.content)

# [END echo_api_class]


# [START api_server]
api = endpoints.api_server([EchoApi])
# [END api_server]
