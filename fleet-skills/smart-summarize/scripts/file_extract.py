"""
Local file summarizer - extracts text from local files for summarization.
Supports: .txt, .md, .json, .csv, .srt, .vtt, .html
Usage: python file_extract.py "path/to/file" [--max 8000]
"""

import sys
import json
import os
import re

def extract_file(filepath, max_chars=8000):
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {filepath}"}))
        return
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return
    
    if ext == '.json':
        # For transcript JSONs, extract the text field
        try:
            data = json.loads(content)
            if isinstance(data, dict) and 'text' in data:
                content = data['text']
            elif isinstance(data, dict) and 'segments' in data:
                content = '\n'.join(seg.get('text', '') for seg in data['segments'])
            else:
                content = json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    
    elif ext in ('.srt', '.vtt'):
        # Strip timestamps, keep text
        content = re.sub(r'\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[.,]\d{3}', '', content)
        content = re.sub(r'^\d+\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n{3,}', '\n\n', content)
    
    elif ext == '.html':
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'\s+', ' ', content)
    
    elif ext == '.csv':
        # Keep CSV as-is, it's already structured
        pass
    
    # Truncate
    total_chars = len(content)
    if len(content) > max_chars:
        content = content[:max_chars] + f"\n...[truncated, {total_chars} total chars]"
    
    print(json.dumps({
        "file": filepath,
        "ext": ext,
        "total_chars": total_chars,
        "extracted_chars": len(content),
        "text": content
    }, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python file_extract.py "path/to/file" [--max N]', file=sys.stderr)
        sys.exit(1)
    
    filepath = sys.argv[1]
    max_chars = 8000
    
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--max" and i + 1 < len(sys.argv[2:]):
            try:
                max_chars = int(sys.argv[2 + i + 1])
            except ValueError:
                pass
    
    extract_file(filepath, max_chars)
