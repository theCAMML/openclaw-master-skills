"""
DuckDuckGo search via lite.duckduckgo.com
- No API key required
- Returns structured results: title, snippet, url
- Uses POST request (DDG Lite requires POST for full results)
- Usage: python ddg_search.py "search query" [--max 10] [--news]
"""

import sys
import json
import urllib.parse
import urllib.request
import re

def search_ddg(query, max_results=10, news=False):
    """Search DuckDuckGo Lite and parse results."""
    
    # DDG Lite requires POST for full results
    data = urllib.parse.urlencode({
        'q': query,
        'kl': 'us-en',
    }).encode('utf-8')
    
    url = "https://lite.duckduckgo.com/lite/"
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return
    
    results = []
    seen_urls = set()
    
    # DDG Lite uses <tr> rows. Results have this pattern:
    # Row 1: result link (title + URL)
    # Row 2: snippet text
    # We parse all rows and combine link + snippet
    
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    
    pending_link = None  # Store link info for combining with next row's snippet
    
    for row in rows:
        hrefs = re.findall(r'href="(https?://[^"]+)"', row)
        
        if hrefs:
            clean_url = hrefs[0]
            # Skip DDG internal links
            if 'duckduckgo.com' in clean_url or 'duck.co' in clean_url:
                continue
            
            # Extract title
            link_texts = re.findall(r'<a[^>]*>(.*?)</a>', row, re.DOTALL)
            title = ""
            if link_texts:
                title = re.sub(r'<[^>]+>', '', link_texts[0]).strip()
            
            # If we have a pending link, save it (no snippet found for it)
            if pending_link and pending_link['url'] not in seen_urls:
                results.append(pending_link)
                seen_urls.add(pending_link['url'])
            
            # Store this as pending (waiting for snippet row)
            pending_link = {
                "title": title,
                "url": clean_url,
                "snippet": ""
            }
        else:
            # This might be a snippet row for the pending link
            if pending_link:
                all_text = re.sub(r'<[^>]+>', ' ', row).strip()
                all_text = re.sub(r'\s+', ' ', all_text)
                # Remove title prefix if present
                snippet = all_text
                if pending_link['title'] and snippet.startswith(pending_link['title']):
                    snippet = snippet[len(pending_link['title']):].strip()
                
                if snippet and len(snippet) > 20:  # Only use substantial snippets
                    pending_link['snippet'] = snippet[:500]
                
                # Save the result
                if pending_link['url'] not in seen_urls:
                    results.append(pending_link)
                    seen_urls.add(pending_link['url'])
                pending_link = None
        
        if len(results) >= max_results:
            break
    
    # Don't forget the last pending link
    if pending_link and pending_link['url'] not in seen_urls and len(results) < max_results:
        results.append(pending_link)
    
    print(json.dumps({"query": query, "count": len(results), "results": results}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python ddg_search.py "query" [--max N] [--news]', file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = 10
    news = False
    
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--news":
            news = True
        elif args[i] == "--max" and i + 1 < len(args):
            try:
                max_results = int(args[i + 1])
                i += 1
            except ValueError:
                pass
        i += 1
    
    search_ddg(query, max_results, news)
