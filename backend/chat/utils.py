import os
import re
from google import genai


def parse_query(query):
    """
    Parse user query to extract intent and filters.

    Returns:
        dict with keys: type, brand, os, budget, feature, compare, explain
    """
    query = query.lower().strip()
    result = {
        "type": "search",
        "brand": None,
        "os": None,
        "budget": None,
        "feature": None,
        "compare": [],
        "explain": None
    }

    # Explain intent
    if query.startswith("explain ") or query.startswith("what is "):
        result['type'] = 'explain'
        result['explain'] = query
        return result

    # Compare intent
    compare_match = re.findall(r'compare ([\w\s\+\-]+?) vs ([\w\s\+\-]+)', query)
    if compare_match:
        result['type'] = 'compare'
        result['compare'] = [m.strip() for m in compare_match[0]]
        return result  

    # Single phone intent
    single_phone_keywords = ["tell me more", "how is", "more info", "specs", "details"]
    if any(kw in query for kw in single_phone_keywords):
        phone_match = re.search(r'[-:]\s*(.+)', query)
        if phone_match:
            result['type'] = 'single_phone'
            result['phone_name'] = phone_match.group(1).strip()
        else:
            result['type'] = 'single_phone'
        return result

    # OS detection
    if 'android' in query:
        result['os'] = 'Android'
    elif 'ios' in query or 'iphone' in query or 'apple' in query:
        result['os'] = 'iOS'

    # Brand detection
    brand_map = {
        "apple": "iOS",
        "samsung": "Android",
        "oneplus": "Android",
        "xiaomi": "Android",
        "realme": "Android",
        "vivo": "Android",
        "oppo": "Android",
        "motorola": "Android",
        "google": "Android",
        "nothing": "Android",
        "iqoo": "Android",
        "infinix": "Android",
        "tecno": "Android",
        "asus": "Android",
    }
    for b, os_type in brand_map.items():
        if b in query:
            result['brand'] = b.capitalize()
            if not result['os']:
                result['os'] = os_type
            break

    # Budget extraction
    budget_match = re.search(r'(?:under|below|less than|upto)\s*₹?\s*([\d.,kKlL]+)', query)
    if budget_match:
        result['budget'] = budget_match.group(1).replace('.', '').strip()

    # Feature extraction
    if 'camera' in query:
        result['feature'] = 'camera'
    elif 'battery' in query or 'charging' in query:
        result['feature'] = 'battery'
    elif 'compact' in query or 'one-hand' in query or 'small screen' in query:
        result['feature'] = 'compact'
    elif 'performance' in query or 'processor' in query:
        result['feature'] = 'performance'
    elif 'display' in query or 'screen' in query:
        result['feature'] = 'display'

    return result


def normalize_price(value):
    """Convert price strings like '₹30,000', '25k', '1.5L' to integer."""
    if not value:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    
    s = str(value).lower().replace('₹', '').replace(',', '').strip()
    multiplier = 1
    if 'k' in s:
        multiplier = 1000
        s = s.replace('k', '')
    elif 'l' in s:  # lakh
        multiplier = 100000
        s = s.replace('l', '')
    try:
        return int(float(s) * multiplier)
    except ValueError:
        return None


def get_gemini_explanation(query):
    """Return short, human-readable explanation using Gemini API."""
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"Explain this in simple, short, human-readable form (2-3 sentences): {query}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

