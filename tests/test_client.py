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

    def test_create_post(self):
        # Given a blogger posts create response
        blog_id = "4660844935009290279"
        posts_create_response = fixtures["posts_create"]

        data = {
            "blog_id": blog_id,
            "title": "new post!",
            "html_content": "<h1>hello there</h1>",
        }

        # And the session returns the response
        session, _ = create_mock_session(
            {
                "post": {
                    f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts": posts_create_response
                }
            }
        )
        client = BloggerClient.from_authorized_session(session)

        # When the client receives a request to create a post
        new_post = client.create_post(
            blog_id=data["blog_id"],
            title=data["title"],
            html_content=data["html_content"],
        )

        # Then it creates the post
        assert new_post.id == posts_create_response["id"]
        assert new_post.html_content == posts_create_response["content"]

    def test_update_post(self):
        # Given a blogger posts create response
        blog_id = "4660844935009290279"
        posts_create_response = fixtures[
            "posts_create"
        ]  # this works for patch requests also

        data = {
            "blog_id": blog_id,
            "post_id": "342342342342",
            "title": "new post!",
            "html_content": "<h1>hello there</h1>",
        }

        # And the session returns the response
        session, _ = create_mock_session(
            {
                "post": {
                    f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts/{data['post_id']}": posts_create_response
                }
            }
        )
        client = BloggerClient.from_authorized_session(session)

        # When the client receives a request to update a post
        new_post = client.update_post(
            blog_id=data["blog_id"],
            post_id=data["post_id"],
            title=data["title"],
            html_content=data["html_content"],
        )

        # Then it creates the post
        assert new_post.id == posts_create_response["id"]
        assert new_post.html_content == posts_create_response["content"]


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
