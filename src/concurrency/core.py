"""Common logic: run CPU and I/O tasks via threading, multiprocessing, asyncio."""

import asyncio
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any

import httpx

from concurrency.cpu_task import count_primes
from concurrency.io_task import fetch_size_async, fetch_size_sync


def measure_time(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> tuple[Any, float]:
    """
    Call func with args, measure elapsed time.

    Returns:
        Tuple of (result, elapsed_seconds).
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def run_cpu_threading(limits: list[int], max_workers: int = 4) -> list[int]:
    """Run CPU-bound task via ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(count_primes, limits))
    return results


def run_cpu_multiprocessing(limits: list[int], max_workers: int = 4) -> list[int]:
    """Run CPU-bound task via ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(count_primes, limits))
    return results


async def run_cpu_asyncio(limits: list[int], max_workers: int = 4) -> list[int]:
    """Run CPU-bound task via asyncio with thread pool executor."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = [
            loop.run_in_executor(pool, count_primes, limit) for limit in limits
        ]
        results = await asyncio.gather(*tasks)
    return list(results)


def run_io_threading(urls: list[str], max_workers: int = 10) -> list[int]:
    """Run I/O-bound task via ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(fetch_size_sync, urls))
    return results


def run_io_multiprocessing(urls: list[str], max_workers: int = 4) -> list[int]:
    """Run I/O-bound task via ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(fetch_size_sync, urls))
    return results


async def run_io_asyncio(urls: list[str]) -> list[int]:
    """Run I/O-bound task via asyncio.gather."""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_size_async(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return list(results)