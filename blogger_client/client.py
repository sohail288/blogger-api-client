from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import requests

from blogger_client import constants


@dataclass
class BloggerPost:
    id: str
    blog_id: int
    author_id: int
    title: str
    html_content: str
    url: str
    blogger_url: str
    published_at: datetime
    updated_at: datetime
    # comments: Optional[list["Comment"]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "BloggerPost":
        return cls(
            id=data["id"],
            blog_id=data["blog"]["id"],
            author_id=data["author"]["id"],
            title=data["title"],
            html_content=data["content"],
            url=data["url"],
            blogger_url=data["selfLink"],
            published_at=datetime.fromisoformat(data["published"]),
            updated_at=datetime.fromisoformat(data["updated"]),
        )


class BloggerClient:
    def __init__(self, *, session: Optional[requests.Session] = None) -> None:
        self._session = session

    @classmethod
    def from_authorized_session(cls, session: requests.Session) -> "BloggerClient":
        if not getattr(session, "credentials"):
            raise ValueError("The given session has an invalid session")
        return cls(session=session)

    def list_posts(self, blog_id: str) -> list[BloggerPost]:
        if self._session is None:
            raise ValueError("session is not initialized")
        resp = self._session.get(
            f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts"
        )
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"unable to get posts for blog: {blog_id} - {e}")
            raise
        json_data = resp.json()
        return [BloggerPost.from_api_response(item) for item in json_data["items"]]

    def create_post(self, blog_id: str, title: str, html_content: str) -> BloggerPost:
        if self._session is None:
            raise ValueError("session is not initialized")
        resp = self._session.post(
            f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts",
            json={"title": title, "content": html_content},
        )

        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"unable to get posts for blog: {blog_id} - {e}")
            raise
        json_data = resp.json()
        return BloggerPost.from_api_response(json_data)

    def update_post(
        self,
        blog_id: str,
        post_id: str,
        title: Optional[str] = None,
        html_content: Optional[str] = None,
    ) -> BloggerPost:
        if self._session is None:
            raise ValueError("session is not initialized")
        payload = {}
        if title is not None:
            payload["title"] = title

        if html_content is not None:
            payload["content"] = html_content

        resp = self._session.post(
            f"{constants.BLOGGER_V3_BASE_URL}/blogs/{blog_id}/posts/{post_id}",
            json=payload,
        )

        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"unable to update post for blog: {blog_id} {post_id} - {e}")
            raise
        json_data = resp.json()
        return BloggerPost.from_api_response(json_data)
