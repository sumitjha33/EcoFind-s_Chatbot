import re

def search_parser_tool(query: str) -> dict:
    """Parse natural language search queries into structured filters for marketplace search"""
    
    query_lower = query.lower().strip()
    
    # Extract price ranges with comprehensive patterns
    price_patterns = [
        r'under (\d+)k?', r'below (\d+)k?', r'less than (\d+)k?',
        r'(\d+)k?\s*to\s*(\d+)k?', r'between (\d+)k?\s*and\s*(\d+)k?',
        r'max (\d+)k?', r'maximum (\d+)k?', r'up to (\d+)k?',
        r'from (\d+)k?\s*to\s*(\d+)k?', r'(\d+)k?\s*-\s*(\d+)k?'
    ]
    
    price_max = None
    price_min = None
    
    for pattern in price_patterns:
        match = re.search(pattern, query_lower)
        if match:
            if len(match.groups()) == 2:  # Range patterns
                price_min = int(match.group(1)) * (1000 if 'k' in match.group(0) else 1)
                price_max = int(match.group(2)) * (1000 if 'k' in match.group(0) else 1)
            else:  # Single value patterns
                price_max = int(match.group(1)) * (1000 if 'k' in match.group(0) else 1)
            break
    
    # Enhanced category detection
    categories = {
        # Electronics
        'electronics': 'Electronics', 'phone': 'Electronics', 'laptop': 'Electronics',
        'mobile': 'Electronics', 'computer': 'Electronics', 'tv': 'Electronics',
        'iphone': 'Electronics', 'samsung': 'Electronics', 'macbook': 'Electronics',
        'ipad': 'Electronics', 'android': 'Electronics', 'gadget': 'Electronics',
        
        # Fashion
        'fashion': 'Fashion', 'clothes': 'Fashion', 'clothing': 'Fashion',
        'shirt': 'Fashion', 'jeans': 'Fashion', 'shoes': 'Fashion',
        'dress': 'Fashion', 'jacket': 'Fashion', 'sneakers': 'Fashion',
        'bag': 'Fashion', 'watch': 'Fashion', 'handbag': 'Fashion',
        
        # Home & Garden
        'home': 'Home & Garden', 'furniture': 'Home & Garden',
        'sofa': 'Home & Garden', 'table': 'Home & Garden', 'chair': 'Home & Garden',
        'bed': 'Home & Garden', 'mirror': 'Home & Garden', 'lamp': 'Home & Garden',
        'garden': 'Home & Garden', 'kitchen': 'Home & Garden',
        
        # Sports
        'sports': 'Sports', 'fitness': 'Sports', 'gym': 'Sports',
        'bike': 'Sports', 'bicycle': 'Sports', 'football': 'Sports',
        'cricket': 'Sports', 'tennis': 'Sports', 'badminton': 'Sports',
        
        # Books
        'books': 'Books', 'novel': 'Books', 'textbook': 'Books',
        'magazine': 'Books', 'comic': 'Books', 'manual': 'Books'
    }
    
    category = None
    for key, cat in categories.items():
        if key in query_lower:
            category = cat
            break
    
    # Extract condition with more variations
    condition = "any"
    if any(word in query_lower for word in ['new', 'brand new', 'unused']):
        condition = "new"
    elif any(word in query_lower for word in ['used', 'second hand', 'pre-owned']):
        condition = "used"
    elif 'excellent' in query_lower:
        condition = "excellent"
    elif 'good' in query_lower:
        condition = "good"
    elif 'fair' in query_lower:
        condition = "fair"
    
    # Extract location hints
    location = None
    location_keywords = ['near me', 'nearby', 'local', 'delhi', 'mumbai', 'bangalore', 'chennai', 'hyderabad', 'pune', 'kolkata']
    for loc in location_keywords:
        if loc in query_lower:
            location = loc
            break
    
    # Extract sort preferences
    sort_by = "relevance"
    if any(word in query_lower for word in ['cheap', 'budget', 'low price', 'affordable']):
        sort_by = "price_low"
    elif any(word in query_lower for word in ['expensive', 'premium', 'high price']):
        sort_by = "price_high"
    elif any(word in query_lower for word in ['latest', 'newest', 'recent']):
        sort_by = "newest"
    elif 'popular' in query_lower:
        sort_by = "popular"
    
    # Extract keywords (remove common stop words and price/condition words)
    stop_words = {
        'show', 'find', 'get', 'under', 'in', 'for', 'with', 'the', 'a', 'an', 
        'me', 'i', 'want', 'need', 'looking', 'search', 'budget', 'cheap',
        'expensive', 'new', 'used', 'good', 'excellent', 'fair', 'poor',
        'to', 'from', 'between', 'and', 'or', 'is', 'are', 'be', 'have'
    }
    
    # Extract meaningful words
    words = re.findall(r'\b\w+\b', query_lower)
    keywords = []
    
    for word in words:
        if (word not in stop_words and 
            not word.isdigit() and 
            len(word) > 2 and
            not re.match(r'\d+k?', word)):  # Exclude price patterns
            keywords.append(word)
    
    # Remove duplicates while preserving order
    keywords = list(dict.fromkeys(keywords))
    
    return {
        "category": category,
        "price_min": price_min,
        "price_max": price_max,
        "keywords": keywords,
        "condition": condition,
        "location": location,
        "sort_by": sort_by,
        "filters": {
            "has_photos": True if 'photos' in query_lower else None,
            "negotiable": True if 'negotiable' in query_lower else None,
            "urgent": True if any(word in query_lower for word in ['urgent', 'asap', 'quick']) else None
        }
    }
