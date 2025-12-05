#!/usr/bin/env python3
"""
Substack to Jekyll Migration Script

Usage:
    uv run migrate.py <substack_url> [--permalink PERMALINK] [--date DATE]

Example:
    uv run migrate.py https://substack.com/home/post/p-179958168
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def fetch_substack_post(url: str) -> BeautifulSoup:
    """Fetch and parse a Substack post."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def extract_post_data(soup: BeautifulSoup, url: str) -> dict:
    """Extract post metadata and content from parsed HTML."""
    data = {}
    
    # Extract title
    title_elem = soup.find('h1', class_='post-title') or soup.find('h1')
    data['title'] = title_elem.get_text(strip=True) if title_elem else "Untitled"
    
    # Extract subtitle
    subtitle_elem = soup.find('h3', class_='subtitle') or soup.find('p', class_='subtitle')
    data['subtitle'] = subtitle_elem.get_text(strip=True) if subtitle_elem else ""
    
    # Extract date from meta or URL
    date_meta = soup.find('meta', property='article:published_time')
    if date_meta and date_meta.get('content'):
        date_str = date_meta['content'][:10]  # YYYY-MM-DD
        data['date'] = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        # Try to find date in the page
        time_elem = soup.find('time')
        if time_elem and time_elem.get('datetime'):
            date_str = time_elem['datetime'][:10]
            data['date'] = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            data['date'] = datetime.now()
    
    # Generate slug and permalink
    data['slug'] = slugify(data['title'])
    
    # Find the post body
    body = soup.find('div', class_='body') or soup.find('div', class_='post-content') or soup.find('article')
    
    if not body:
        # Try finding the main content area
        body = soup.find('div', class_='available-content') or soup.find('div', class_='single-post')
    
    data['body'] = body
    data['url'] = url
    
    return data


def download_image(img_url: str, save_dir: Path, index: int) -> str | None:
    """Download an image and return the local filename."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(img_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Determine file extension
        content_type = response.headers.get('content-type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = '.jpg'
        elif 'png' in content_type:
            ext = '.png'
        elif 'gif' in content_type:
            ext = '.gif'
        elif 'webp' in content_type:
            ext = '.webp'
        else:
            # Try to get from URL
            parsed = urlparse(img_url)
            path_ext = os.path.splitext(parsed.path)[1]
            ext = path_ext if path_ext else '.jpg'
        
        filename = f"image-{index}{ext}"
        save_path = save_dir / filename
        
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(response.content)
        
        return filename
    except Exception as e:
        print(f"Warning: Failed to download {img_url}: {e}", file=sys.stderr)
        return None


def clean_caption(caption: str) -> str:
    """Clean up caption text - remove surrounding italics markers."""
    caption = caption.strip()
    # Remove surrounding italic markers
    if caption.startswith('*') and caption.endswith('*'):
        caption = caption[1:-1].strip()
    if caption.startswith('_') and caption.endswith('_'):
        caption = caption[1:-1].strip()
    return caption


def process_content(body, slug: str, assets_dir: Path) -> tuple[str, str | None]:
    """
    Process the post body, downloading images and converting to markdown.
    Returns (markdown_content, thumbnail_path).
    """
    if not body:
        return "", None
    
    img_dir = assets_dir / "img" / slug
    markdown_parts = []
    thumbnail = None
    img_index = 0
    
    # Substack boilerplate patterns to skip
    boilerplate_patterns = [
        "Thanks for reading",
        "Subscribe for free",
        "support my work",
    ]
    
    # Exact matches to skip (case-insensitive)
    boilerplate_exact = ["subscribe", "share"]
    
    # Process each element in the body
    for element in body.children:
        if not hasattr(element, 'name') or element.name is None:
            # Text node
            text = str(element).strip()
            if text:
                markdown_parts.append(text)
            continue
        
        if element.name == 'figure' or (element.name == 'div' and element.find('figure')):
            # Handle figure with image
            fig = element if element.name == 'figure' else element.find('figure')
            img = fig.find('img') if fig else element.find('img')
            
            if img and img.get('src'):
                img_url = img['src']
                
                # Download image
                local_filename = download_image(img_url, img_dir, img_index)
                
                if local_filename:
                    local_path = f"/../assets/img/{slug}/{local_filename}"
                    
                    # Set first image as thumbnail
                    if thumbnail is None:
                        thumbnail = f"/assets/img/{slug}/{local_filename}"
                    
                    # Get caption
                    caption = ""
                    figcaption = fig.find('figcaption') if fig else None
                    if figcaption:
                        # Convert caption HTML to markdown for links
                        caption = md(str(figcaption), strip=['figcaption']).strip()
                        caption = clean_caption(caption)
                    
                    # Create image include
                    img_include = f'{{% include image.html src="{local_path}" alt="" caption="{caption}" width="80%" %}}'
                    markdown_parts.append(f"\n\n{img_include}\n")
                    img_index += 1
                continue
        
        # Check for standalone images
        if element.name == 'img' or (element.name == 'div' and element.find('img') and not element.find('figure')):
            img = element if element.name == 'img' else element.find('img')
            if img and img.get('src'):
                img_url = img['src']
                local_filename = download_image(img_url, img_dir, img_index)
                
                if local_filename:
                    local_path = f"/../assets/img/{slug}/{local_filename}"
                    
                    if thumbnail is None:
                        thumbnail = f"/assets/img/{slug}/{local_filename}"
                    
                    alt_text = img.get('alt', '')
                    img_include = f'{{% include image.html src="{local_path}" alt="{alt_text}" caption="" width="80%" %}}'
                    markdown_parts.append(f"\n\n{img_include}\n")
                    img_index += 1
                continue
        
        # Convert other HTML elements to markdown
        html_str = str(element)
        markdown_text = md(html_str, heading_style='ATX', strip=['div'])
        markdown_text = markdown_text.strip()
        
        # Skip Substack boilerplate
        if markdown_text:
            is_boilerplate = (
                any(pattern.lower() in markdown_text.lower() for pattern in boilerplate_patterns) or
                markdown_text.strip().lower() in boilerplate_exact
            )
            if not is_boilerplate:
                markdown_parts.append(markdown_text)
    
    # Join and clean up the markdown
    content = "\n\n".join(markdown_parts)
    
    # Clean up excessive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip(), thumbnail


def generate_front_matter(data: dict, permalink: str | None = None, thumbnail: str | None = None) -> str:
    """Generate Jekyll front matter."""
    title = data['title'].replace('"', '\\"')
    subtitle = data.get('subtitle', '').replace('"', '\\"')
    
    # Create excerpt from first sentence of the blog post
    excerpt = ""
    if data.get('body'):
        first_p = data['body'].find('p')
        if first_p:
            first_para_text = first_p.get_text(strip=True)
            # Extract first sentence (up to first period, question mark, or exclamation)
            for i, char in enumerate(first_para_text):
                if char in '.!?' and i > 20:  # Minimum length to avoid abbreviations
                    excerpt = first_para_text[:i+1]
                    break
            else:
                # No sentence ending found, use first 200 chars
                excerpt = first_para_text[:200]
    excerpt = excerpt.replace('"', '\\"')
    
    # Use provided permalink or generate from slug
    final_permalink = permalink if permalink else data['slug']
    
    lines = [
        "---",
        "layout: post",
        f'title: "{title}"',
    ]
    
    if subtitle:
        lines.append(f'subtitle: "{subtitle}"')
    
    lines.extend([
        "mathjax: true",
        f'excerpt: "{excerpt}"',
        "hide_from_list: false",
        f"permalink: {final_permalink}",
    ])
    
    if thumbnail:
        lines.append(f"thumbnail-img: {thumbnail}")
    
    lines.append("---")
    
    return "\n".join(lines)


def migrate_post(url: str, output_dir: Path, assets_dir: Path, 
                 permalink: str | None = None, date_override: str | None = None) -> Path:
    """
    Migrate a Substack post to Jekyll format.
    Returns the path to the created markdown file.
    """
    print(f"Fetching {url}...")
    soup = fetch_substack_post(url)
    
    print("Extracting post data...")
    data = extract_post_data(soup, url)
    
    # Override date if provided
    if date_override:
        data['date'] = datetime.strptime(date_override, '%Y-%m-%d')
    
    print(f"Processing content for '{data['title']}'...")
    content, thumbnail = process_content(data['body'], data['slug'], assets_dir)
    
    # Generate front matter
    front_matter = generate_front_matter(data, permalink, thumbnail)
    
    # Create the full markdown content
    markdown = f"{front_matter}\n\n{content}\n"
    
    # Generate filename
    date_str = data['date'].strftime('%Y-%m-%d')
    filename = f"{date_str}-{data['slug']}.md"
    output_path = output_dir / filename
    
    # Write the file
    output_path.write_text(markdown)
    print(f"Created: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Migrate a Substack post to Jekyll format'
    )
    parser.add_argument('url', help='URL of the Substack post')
    parser.add_argument('--permalink', help='Override the permalink')
    parser.add_argument('--date', help='Override the date (YYYY-MM-DD format)')
    parser.add_argument('--output-dir', default='../_posts', 
                        help='Output directory for markdown files')
    parser.add_argument('--assets-dir', default='../assets',
                        help='Assets directory for images')
    
    args = parser.parse_args()
    
    # Resolve paths relative to script location
    script_dir = Path(__file__).parent
    output_dir = (script_dir / args.output_dir).resolve()
    assets_dir = (script_dir / args.assets_dir).resolve()
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        migrate_post(args.url, output_dir, assets_dir, args.permalink, args.date)
        print("Migration complete!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

