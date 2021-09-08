# would be nice to dynamically generate content by replacing ids / names, but that gets too complicated
fixtures = {
    "posts": {
        "kind": "blogger#postList",
        "items": [
            {
                "kind": "blogger#post",
                "id": "5931156232915766060",
                "blog": {"id": "4660844935009290279"},
                "published": "2020-11-26T02:14:00-08:00",
                "updated": "2021-08-08T11:52:42-07:00",
                "url": "http://www.sohailkhan.me/2020/11/testing.html",
                "selfLink": "https://www.googleapis.com/blogger/v3/blogs/4660844935009290279/posts/5931156232915766060",
                "title": "Testing",
                "content": "<h1>lol</h1>",
                "author": {
                    "id": "10424770373055138157",
                    "displayName": "Sohail's Tech Blog",
                    "url": "https://www.blogger.com/profile/10424770373055138157",
                    "image": {"url": "//www.blogger.com/img/blogger_logo_round_35.png"},
                },
                "replies": {
                    "totalItems": "1",
                    "selfLink": "https://www.googleapis.com/blogger/v3/blogs/4660844935009290279/posts/5931156232915766060/comments",
                },
                "etag": '"dGltZXN0YW1wOiAxNjI4NDQ4NzYyOTg3Cm9mZnNldDogLTI1MjAwMDAwCg"',
            }
        ],
        "etag": '"MjAyMS0wOC0wOFQxODo1Mjo0Mi45ODda"',
    }
}
