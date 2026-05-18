"""
URL content extractor - fetches a URL and extracts readable text.
Handles HTML, strips scripts/styles, returns clean text.
Usage: python url_extract.py "https://example.com" [--max 8000]
"""

import sys
import json
import re
import urllib.request

def extract_text(url, max_chars=8000):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content_type = resp.headers.get('Content-Type', '')
            raw = resp.read()
        
        # Try to detect encoding
        encoding = 'utf-8'
        if 'charset=' in content_type:
            encoding = content_type.split('charset=')[-1].split(';')[0].strip()
        
        text = raw.decode(encoding, errors='replace')
        
        # Strip scripts and styles
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert some HTML to readable format
        text = re.sub(r'<h[1-6][^>]*>', '\n## ', text, flags=re.IGNORECASE)
        text = re.sub(r'</h[1-6]>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<li[^>]*>', '\n- ', text, flags=re.IGNORECASE)
        
        # Strip remaining HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Clean up whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        # Truncate
        if len(text) > max_chars:
            text = text[:max_chars] + "\n...[truncated]"
        
        print(json.dumps({"url": url, "chars": len(text), "text": text}, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"url": url, "error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python url_extract.py "https://example.com" [--max N]', file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    max_chars = 8000
    
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--max" and i + 1 < len(sys.argv[2:]):
            try:
                max_chars = int(sys.argv[2 + i + 1])
            except ValueError:
                pass
    
    extract_text(url, max_chars)
