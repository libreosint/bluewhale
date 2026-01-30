from types import SimpleNamespace
from typing import Optional, Union

import requests

BASE_ENDPOINT = "https://public.api.bsky.app/xrpc"


class BlueWhale:
    def __init__(self): ...
    def _to_namespace(
        self, data: dict | list[dict]
    ) -> SimpleNamespace | list[SimpleNamespace]:
        if isinstance(data, list):
            return [self._to_namespace(item) for item in data]

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._to_namespace(value)
            elif isinstance(value, list):
                data[key] = [
                    self._to_namespace(item) if isinstance(item, dict) else item
                    for item in value
                ]

        return SimpleNamespace(**data)

    @staticmethod
    def _send_request(
        url: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Union[dict, list, None]:
        response = requests.get(url=url, headers=headers, params=params)

        if response.status_code != 200:
            return None

        return response.json()

    def user_profile(self, username: str) -> Union[SimpleNamespace, None]:
        data = self._send_request(
            url=f"{BASE_ENDPOINT}/app.bsky.actor.getProfile",
            params={"actor": username},
        )

        return self._to_namespace(data=data)

    def user_feed(
        self, username: str, include_pins: bool = True, limit: int = 25
    ) -> list[SimpleNamespace]:
        # TODO: Might need to make fileter param to be user-customisable.
        data = self._send_request(
            url=f"{BASE_ENDPOINT}/app.bsky.feed.getAuthorFeed",
            params={
                "actor": username,
                "filter": "posts_and_author_threads",
                "includePins": include_pins,
                "limit": limit,
            },
        )

        return self._to_namespace(data=data.get("feed"))

    def user_search(self, query: str) -> list[SimpleNamespace]:
        results = self._send_request(
            f"{BASE_ENDPOINT}/app.bsky.actor.searchActors", params={"q": query}
        )
        return self._to_namespace(data=results.get("actors"))

    def trending_topics(self, limit: int = 25) -> list[SimpleNamespace]:
        topics = self._send_request(
            f"{BASE_ENDPOINT}/app.bsky.unspecced.getTrendingTopics",
            params={"limit": limit},
        )

        return self._to_namespace(data=topics.get("topics"))
