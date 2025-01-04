from typing import Any, Optional, Union

import aiohttp
import requests


class ColBERTv2:
    """
    Wrapper for interacting with a remote ColBERTv2 retrieval server.

    Provides methods for querying the server using either GET or POST requests,
    both synchronously and asynchronously.

    Usage (Synchronous):
    ```python
    # Assuming a ColBERTv2 server is running at http://localhost:8893
    retriever = ColBERTv2(url="http://localhost", port=8893)

    # Retrieve top 5 results using GET requests
    results = retriever.call_sync("What is the capital of France?", k=5)
    print(results)

    # Retrieve top 3 results using POST requests and get simplified output
    simplified_results = retriever.call_sync(
        "What is the capital of Germany?", k=3, simplify=True, post_requests=True
    )
    print(simplified_results)
    ```

    Usage (Asynchronous):
    ```python
    import asyncio

    async def main():
        # Assuming a ColBERTv2 server is running at http://localhost:8893
        retriever = ColBERTv2(url="http://localhost", port=8893)

        # Retrieve top 5 results using GET requests
        results = await retriever("What is the capital of France?", k=5)
        print(results)

        # Retrieve top 3 results using POST requests and get simplified output
        simplified_results = await retriever(
            "What is the capital of Germany?", k=3, simplify=True, post_requests=True
        )
        print(simplified_results)

    if __name__ == "__main__":
        asyncio.run(main())
    ```
    """

    def __init__(
        self,
        url: str = "http://0.0.0.0",
        port: Optional[Union[str, int]] = None,
        post_requests: bool = False,
    ):
        """
        Initializes the ColBERTv2 client.

        Args:
            url: The base URL of the ColBERTv2 server.
            port: The port the server is listening on (optional).
            post_requests: Whether to use POST requests (True) or GET requests (False).
        """
        self.post_requests = post_requests
        self.url = f"{url}:{port}" if port else url

    async def __call__(
        self, query: str, k: int = 10, simplify: bool = False
    ) -> Union[list[str], list[dict]]:
        """
        Queries the ColBERTv2 server asynchronously.

        Args:
            query: The search query string.
            k: The number of top results to retrieve.
            simplify: If True, returns only the text of the passages.
                      If False, returns dictionaries with more information.

        Returns:
            A list of strings (if simplify=True) or a list of dictionaries (if simplify=False)
            representing the retrieved passages.
        """
        if self.post_requests:
            topk: list[dict[str, Any]] = await colbertv2_post_request(
                self.url, query, k
            )
        else:
            topk: list[dict[str, Any]] = await colbertv2_get_request(self.url, query, k)

        if simplify:
            return [psg["long_text"] for psg in topk]

        return [dict(psg) for psg in topk]

    def call_sync(
        self, query: str, k: int = 10, simplify: bool = False
    ) -> Union[list[str], list[dict]]:
        """
        Queries the ColBERTv2 server synchronously.

        Args:
            query: The search query string.
            k: The number of top results to retrieve.
            simplify: If True, returns only the text of the passages.
                      If False, returns dictionaries with more information.

        Returns:
            A list of strings (if simplify=True) or a list of dictionaries (if simplify=False)
            representing the retrieved passages.
        """
        if self.post_requests:
            topk: list[dict[str, Any]] = colbertv2_post_request_sync(self.url, query, k)
        else:
            topk: list[dict[str, Any]] = colbertv2_get_request_sync(self.url, query, k)

        if simplify:
            return [psg["long_text"] for psg in topk]

        return [dict(psg) for psg in topk]


async def colbertv2_get_request(url: str, query: str, k: int) -> list[dict[str, Any]]:
    """
    Sends a GET request to the ColBERTv2 server (asynchronous).

    Args:
        url: The URL of the server endpoint.
        query: The search query.
        k: The number of results to return.

    Returns:
        A list of dictionaries representing the retrieved passages.
    """
    assert (
        k <= 100
    ), "Only k <= 100 is supported for the hosted ColBERTv2 server at the moment."

    payload = {"query": query, "k": k}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload, timeout=10) as res:
            topk = (await res.json())["topk"][:k]
            topk = [{**d, "long_text": d["text"]} for d in topk]
    return topk[:k]


def colbertv2_get_request_sync(url: str, query: str, k: int) -> list[dict[str, Any]]:
    """
    Sends a GET request to the ColBERTv2 server (synchronous).

    Args:
        url: The URL of the server endpoint.
        query: The search query.
        k: The number of results to return.

    Returns:
        A list of dictionaries representing the retrieved passages.
    """
    assert (
        k <= 100
    ), "Only k <= 100 is supported for the hosted ColBERTv2 server at the moment."

    payload = {"query": query, "k": k}
    res = requests.get(url, params=payload, timeout=10)

    topk = res.json()["topk"][:k]
    topk = [{**d, "long_text": d["text"]} for d in topk]
    return topk[:k]


async def colbertv2_post_request(url: str, query: str, k: int) -> list[dict[str, Any]]:
    """
    Sends a POST request to the ColBERTv2 server (asynchronous).

    Args:
        url: The URL of the server endpoint.
        query: The search query.
        k: The number of results to return.

    Returns:
        A list of dictionaries representing the retrieved passages.
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {"query": query, "k": k}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers, timeout=10) as res:
            topk = (await res.json())["topk"][:k]
    return topk


def colbertv2_post_request_sync(url: str, query: str, k: int) -> list[dict[str, Any]]:
    """
    Sends a POST request to the ColBERTv2 server (synchronous).

    Args:
        url: The URL of the server endpoint.
        query: The search query.
        k: The number of results to return.

    Returns:
        A list of dictionaries representing the retrieved passages.
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {"query": query, "k": k}
    res = requests.post(url, json=payload, headers=headers, timeout=10)

    return res.json()["topk"][:k]
