#!/usr/bin/env python3
"""
Substack Post Lister

Lists all posts from a Substack blog, organized by sections/tabs.

Usage:
    uv run list_posts.py <substack_username_or_url> [--output FILE]

Examples:
    uv run list_posts.py xiqo
    uv run list_posts.py https://xiqo.substack.com/
    uv run list_posts.py xiqo --output posts.json
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from urllib.parse import urlparse
import requests


def normalize_substack_url(input_str: str) -> str:
    """Convert username or URL to base Substack URL."""
    if input_str.startswith('http://') or input_str.startswith('https://'):
        parsed = urlparse(input_str)
        return f"https://{parsed.netloc}"
    else:
        # Assume it's a username
        return f"https://{input_str}.substack.com"


def fetch_posts_from_api(base_url: str, limit: int = 12, offset: int = 0) -> list:
    """Fetch posts from Substack API."""
    api_url = f"{base_url}/api/v1/archive"
    params = {
        'sort': 'new',
        'limit': limit,
        'offset': offset
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def list_all_posts(substack_input: str, delay: float = 0.5, max_requests: int = None) -> dict:
    """List all posts organized by section."""
    base_url = normalize_substack_url(substack_input)

    print(f"Fetching posts from {base_url}...", file=sys.stderr)

    all_posts = []
    offset = 0
    limit = 50  # Fetch more per request to be efficient
    request_count = 0
    retry_delay = 5

    while True:
        # Check max requests limit
        if max_requests is not None and request_count >= max_requests:
            print(f"Reached max requests limit ({max_requests})", file=sys.stderr)
            break

        request_count += 1

        try:
            posts = fetch_posts_from_api(base_url, limit=limit, offset=offset)

            if not posts:
                print(f"No more posts found at offset {offset}", file=sys.stderr)
                break

            all_posts.extend(posts)
            print(f"Fetched {len(posts)} posts (total: {len(all_posts)})", file=sys.stderr)

            offset += len(posts)
            time.sleep(delay)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # Rate limited - wait and retry
                print(f"Rate limited, waiting {retry_delay}s before retrying...", file=sys.stderr)
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
                continue
            else:
                raise

    # Organize posts by section
    results = defaultdict(list)

    for post in all_posts:
        # Construct proper URL from slug
        slug = post.get('slug')

        if slug:
            # Use base_url (which we already have) + /p/ + slug
            url = f"{base_url}/p/{slug}"
        else:
            # Fall back to canonical_url
            url = post.get('canonical_url')

        if not url:
            continue

        # Get section name, default to "All Posts" if no section
        section_name = post.get('section_name') or 'All Posts'

        # Avoid duplicates
        if url not in results[section_name]:
            results[section_name].append(url)

    # Convert defaultdict to regular dict
    return dict(results)


def main():
    parser = argparse.ArgumentParser(
        description='List all posts from a Substack blog, organized by sections.'
    )
    parser.add_argument(
        'substack',
        help='Substack username or URL (e.g., "xiqo" or "https://xiqo.substack.com/")'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output JSON file (default: print to stdout)',
        default=None
    )
    parser.add_argument(
        '--delay', '-d',
        help='Delay between requests in seconds (default: 0.5)',
        type=float,
        default=0.5
    )
    parser.add_argument(
        '--max-requests', '-m',
        help='Maximum number of API requests (default: unlimited)',
        type=int,
        default=None
    )

    args = parser.parse_args()

    try:
        results = list_all_posts(args.substack, delay=args.delay, max_requests=args.max_requests)

        # Output results
        json_output = json.dumps(results, indent=2, ensure_ascii=False)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)

            # Print summary to stderr
            total_posts = sum(len(urls) for urls in results.values())
            print(f"\nResults saved to {args.output}", file=sys.stderr)
            print(f"Total sections: {len(results)}", file=sys.stderr)
            print(f"Total posts: {total_posts}", file=sys.stderr)
        else:
            print(json_output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
