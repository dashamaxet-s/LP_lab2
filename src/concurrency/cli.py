"""CLI for comparing threading, multiprocessing and asyncio on CPU and I/O loads."""

import argparse
import asyncio
import time

from concurrency.core import (
    run_cpu_asyncio,
    run_cpu_multiprocessing,
    run_cpu_threading,
    run_io_asyncio,
    run_io_multiprocessing,
    run_io_threading,
)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Compare threading, multiprocessing and asyncio on CPU and I/O loads"
    )
    parser.add_argument(
        "--load",
        choices=["cpu", "io"],
        required=True,
        help="Type of load: cpu or io",
    )
    parser.add_argument(
        "--mode",
        choices=["threading", "multiprocessing", "asyncio"],
        required=True,
        help="Concurrency model: threading, multiprocessing, asyncio",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10000,
        help="Parameter N for CPU load (limit for prime numbers)",
    )
    parser.add_argument(
        "--m",
        type=int,
        default=100,
        help="Parameter M for I/O load (number of HTTP requests)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of workers for pools",
    )

    args = parser.parse_args()

    if args.load == "cpu":
        limits = [args.n] * args.workers
        start = time.perf_counter()
        if args.mode == "threading":
            results = run_cpu_threading(limits, max_workers=args.workers)
        elif args.mode == "multiprocessing":
            results = run_cpu_multiprocessing(limits, max_workers=args.workers)
        else:  # asyncio
            results = asyncio.run(run_cpu_asyncio(limits, max_workers=args.workers))
        elapsed = time.perf_counter() - start
    else:  # io
        urls = ["http://127.0.0.1:8000/test"] * args.m
        start = time.perf_counter()
        if args.mode == "threading":
            results = run_io_threading(urls, max_workers=args.workers)
        elif args.mode == "multiprocessing":
            results = run_io_multiprocessing(urls, max_workers=args.workers)
        else:  # asyncio
            results = asyncio.run(run_io_asyncio(urls))
        elapsed = time.perf_counter() - start

    print(f"Load: {args.load}")
    print(f"Mode: {args.mode}")
    print(f"Results: {results}")
    print(f"Elapsed: {elapsed:.4f} seconds")


if __name__ == "__main__":
    main()