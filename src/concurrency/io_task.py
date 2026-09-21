import httpx


def fetch_size_sync(url: str) -> int:
    """Fetch URL and return body size in bytes (blocking)."""
    response = httpx.get(url, timeout=10.0)
    return len(response.content)



async def fetch_size_async(client: httpx.AsyncClient, url: str) -> int:
    """Fetch URL and return body size in bytes (non-blocking)."""
    response = await client.get(url, timeout=10.0)
    return len(response.content)