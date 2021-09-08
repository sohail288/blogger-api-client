from unittest import mock

import requests

from blogger_client import BloggerClient, constants
from tests.fixtures import fixtures


class TestBloggerClient:
    def test_client(self):
        # Given an authorized session
        session, _ = create_mock_session({})

        # When the client is built with the session
        client = BloggerClient.from_authorized_session(session)

        # Then it successfully uses that session
        assert client._session is session

    def test_get_all_posts(self):
        # Given an authorized session that can access a certain blog
        blog_id = "4660844935009290279"
        session, _ = create_mock_session(
            {
                "get": {
                    f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts": fixtures[
                        "posts"
                    ]
                }
            }
        )
        client = BloggerClient.from_authorized_session(session)

        # When the client lists the posts
        # TODO: should we 'set' a blog_id when initializing the client?
        # or should we configure it after the fact?
        # or is this fine?
        posts = client.list_posts(blog_id)

        # Then it returns the posts
        assert len(posts) == 1

        # And the title is correct
        assert posts[0].title == "Testing"

        assert posts[0].html_content == "<h1>lol</h1>"


def create_mock_session(config):
    def _mock_request(method, url, *args, **kwargs):
        return mock.MagicMock(**{"json.return_value": config[method.lower()][url]})

    def _get_wrapper(method):
        return lambda *args, **kwargs: getattr(requests.Session, method)(
            m, *args, **kwargs
        )

    def mount(method, url, response):
        responses = config.setdefault(method.lower(), {})
        responses[url] = response

    m = mock.MagicMock(name="requests.Session")
    all_methods = set(["get", "post", "patch", "put", "delete"])

    m.configure_mock(
        **{
            "request.side_effect": _mock_request,
            **{method: mock.Mock(wraps=_get_wrapper(method)) for method in all_methods},
        }
    )
    return m, mount
