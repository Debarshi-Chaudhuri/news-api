# app/core/constants.py
from typing import List, Dict

# Industry categories and their keywords
INDUSTRY_CATEGORIES = {
    "Textiles & Garments": [
        "handlooms", "power looms", "readymade garments", "fabrics", "hosiery",
        "embroidery", "dyeing", "printing units"
    ],
    "Food & Agro Processing": [
        "packaged food", "food products", "snacks", "spices", "dairy",
        "cold storage", "fruit processing", "vegetable processing",
        "flour mills", "rice mills", "oil mills"
    ],
    "Automobile & Auto Components": [
        "spare parts manufacturing", "sheet metal fabrication", "tyre retreading",
        "auto components", "ancillary parts", "OEM suppliers"
    ],
    "Chemicals & Pharmaceuticals": [
        "dyes", "intermediates", "industrial chemicals", "cosmetics",
        "personal care", "bulk drugs", "pharma formulations"
    ],
    "Engineering & Capital Goods": [
        "machine tools", "industrial equipment", "electrical machinery",
        "fabrication units", "welding", "casting", "machining"
    ],
    "Electronics & Electricals": [
        "LED lights", "electrical fittings", "cables", "consumer electronics",
        "solar products"
    ],
    "Plastics & Rubber Products": [
        "molded plastic", "packaging materials", "rubber products",
        "tyres", "rubber belts", "rubber hoses"
    ],
    "Handicrafts & Handlooms": [
        "artisanal crafts", "wood crafts", "metal crafts", "pottery",
        "home décor", "gift articles", "ethnic products"
    ],
    "Construction & Building Materials": [
        "cement products", "blocks", "tiles", "paints", "adhesives",
        "sanitaryware", "pipes", "fittings", "stone crushing", "aggregates"
    ],
    "Leather & Footwear": [
        "tanning units", "leather garments", "leather accessories", "footwear"
    ],
    "Wood & Furniture": [
        "furniture manufacturing", "modular furniture", "carpentry", "woodcraft"
    ],
    "Printing & Packaging": [
        "printing press", "commercial printing", "corrugated box", "label production", 
        "sticker production"
    ],
    "Information Technology & Services": [
        "IT services", "ITES", "BPO", "KPO", "SaaS", "startups", "digital marketing"
    ],
    "Logistics & Warehousing": [
        "logistics", "transporters", "last-mile delivery", "cold chain", "warehousing"
    ],
    "Healthcare & Medical Devices": [
        "diagnostic labs", "medical devices", "disposable medical products"
    ],
    "Tourism & Hospitality": [
        "hotels", "lodges", "homestays", "travel agencies", "catering services"
    ],
    "Education & Skill Development": [
        "coaching centers", "edtech", "vocational training"
    ]
}

# Flatten the industry keywords for the scraper
NEWS_KEYWORDS = []

# Add category names
for category in INDUSTRY_CATEGORIES:
    NEWS_KEYWORDS.append(category)
    
# Add all the industry-specific keywords
for category, keywords in INDUSTRY_CATEGORIES.items():
    NEWS_KEYWORDS.extend(keywords)

# Add common business keywords to enhance scraping results
COMMON_BUSINESS_KEYWORDS = [
    "business", "industry", "manufacturing", "MSME", "SME", 
    "small business", "entrepreneurs", "startup", "market growth",
    "sector development", "innovation", "export", "import", "trade"
]

NEWS_KEYWORDS.extend(COMMON_BUSINESS_KEYWORDS)