# app/core/constants.py
from typing import List, Dict

# Industry categories and their keywords with India focus
INDUSTRY_CATEGORIES = {
    "Textiles & Garments": [
        "handlooms", "power looms", "readymade garments", "fabrics", "hosiery",
        "embroidery", "dyeing", "printing units", "Indian textile", "khadi",
        "silk industry", "cotton mills"
    ],
    "Food & Agro Processing": [
        "packaged food", "food products", "snacks", "spices", "dairy",
        "cold storage", "fruit processing", "vegetable processing",
        "flour mills", "rice mills", "oil mills", "FCI", "FSSAI", 
        "Indian agriculture", "agro exports"
    ],
    "Automobile & Auto Components": [
        "spare parts manufacturing", "sheet metal fabrication", "tyre retreading",
        "auto components", "ancillary parts", "OEM suppliers", "Indian automotive industry",
        "SIAM", "automobile exports", "EV manufacturing"
    ],
    "Chemicals & Pharmaceuticals": [
        "dyes", "intermediates", "industrial chemicals", "cosmetics",
        "personal care", "bulk drugs", "pharma formulations", "API manufacturing",
        "Indian pharma industry", "generic medicines", "DPCO", "drug exports"
    ],
    "Engineering & Capital Goods": [
        "machine tools", "industrial equipment", "electrical machinery",
        "fabrication units", "welding", "casting", "machining", "BHEL",
        "L&T", "make in India", "engineering exports"
    ],
    "Electronics & Electricals": [
        "LED lights", "electrical fittings", "cables", "consumer electronics",
        "solar products", "semiconductor manufacturing", "electronics manufacturing services",
        "PLI scheme", "electronics hardware", "domestic manufacturing"
    ],
    "Plastics & Rubber Products": [
        "molded plastic", "packaging materials", "rubber products",
        "tyres", "rubber belts", "rubber hoses", "plastic manufacturing policy",
        "bioplastics"
    ],
    "Handicrafts & Handlooms": [
        "artisanal crafts", "wood crafts", "metal crafts", "pottery",
        "home décor", "gift articles", "ethnic products", "GI tagged products",
        "traditional crafts", "handloom exports", "handloom board"
    ],
    "Construction & Building Materials": [
        "cement products", "blocks", "tiles", "paints", "adhesives",
        "sanitaryware", "pipes", "fittings", "stone crushing", "aggregates",
        "infrastructure projects", "smart cities", "real estate", "RERA"
    ],
    "Leather & Footwear": [
        "tanning units", "leather garments", "leather accessories", "footwear",
        "leather exports", "FDDI", "leather cluster", "footwear design"
    ],
    "Wood & Furniture": [
        "furniture manufacturing", "modular furniture", "carpentry", "woodcraft",
        "Indian wooden furniture", "sustainable wood", "eco-friendly furniture"
    ],
    "Printing & Packaging": [
        "printing press", "commercial printing", "corrugated box", "label production", 
        "sticker production", "packaging innovations", "sustainable packaging"
    ],
    "Information Technology & Services": [
        "IT services", "ITES", "BPO", "KPO", "SaaS", "startups", "digital marketing",
        "Indian IT industry", "NASSCOM", "software exports", "IT parks", "tech hubs"
    ],
    "Logistics & Warehousing": [
        "logistics", "transporters", "last-mile delivery", "cold chain", "warehousing",
        "e-way bill", "GST transportation", "3PL", "4PL", "logistics parks"
    ],
    "Healthcare & Medical Devices": [
        "diagnostic labs", "medical devices", "disposable medical products",
        "Ayushman Bharat", "NDHM", "medical tourism", "health tech", "telemedicine"
    ],
    "Tourism & Hospitality": [
        "hotels", "lodges", "homestays", "travel agencies", "catering services",
        "ecotourism", "adventure tourism", "Incredible India", "domestic tourism"
    ],
    "Education & Skill Development": [
        "coaching centers", "edtech", "vocational training", "skill india",
        "NSDC", "NEP 2020", "education technology", "online learning"
    ],
    "Renewable Energy": [
        "solar power", "wind energy", "green hydrogen", "biomass", "renewable projects",
        "clean energy", "energy transition", "solar manufacturing", "KUSUM scheme"
    ],
    "Fintech & Banking": [
        "digital payments", "UPI", "mobile banking", "neo banks", "BFSI",
        "RBI", "NPCI", "financial inclusion", "microfinance", "digital lending"
    ],
    "E-commerce & Retail": [
        "online marketplace", "D2C brands", "quick commerce", "retail tech",
        "omnichannel retail", "ONDC", "e-commerce policy", "open network"
    ]
}

# Add India-specific business and policy terms
INDIA_SPECIFIC_TERMS = [
    "Make in India", "Startup India", "Digital India", "Atmanirbhar Bharat", 
    "PLI scheme", "GST", "RBI", "SEBI", "MSME", "SIDBI", "DGFT", "FDI policy",
    "budget", "economic survey", "five year plan", "NITI Aayog", 
    "Indian economy", "export promotion", "DPIIT", "SEZ", "industrial corridor",
    "ease of doing business", "India business", "Indian market", 
    "MSME sector", "PSU", "disinvestment", "production linked incentive",
    "India stack", "domestic manufacturing"
]

# Flatten the industry keywords for the scraper
NEWS_KEYWORDS = []

# Add India-specific terms
NEWS_KEYWORDS.extend(INDIA_SPECIFIC_TERMS)

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
    "sector development", "innovation", "export", "import", "trade",
    "India business", "Indian economy", "India market", "India exports",
    "India investment", "Indian industry", "India policy", "India growth"
]

NEWS_KEYWORDS.extend(COMMON_BUSINESS_KEYWORDS)

# Industry to image mapping for UI display
INDUSTRY_IMAGES = {
    "Textiles & Garments": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/readymade-garments.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/textile+industries.jpg"
    ],
    "Food & Agro Processing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/food+processing.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/fruit-vegetable-processing.jpg"
    ],
    "Automobile & Auto Components": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/auto_parts_industry_faces_total_collapse-min.jpg"
    ],
    "Chemicals & Pharmaceuticals": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Chemicals+%26+Pharmaceuticals.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Industrial+chemicals.webp"
    ],
    "Engineering & Capital Goods": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/capital-goods.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Industrial+equipment.png"
    ],
    "Electronics & Electricals": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Electrical+fittings+%26+cables.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Electrical+machinery.jpg"
    ],
    "Plastics & Rubber Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/7.+Plastics+%26+Rubber+Products.avif",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products+hoses.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products+tyres.jpg"
    ],
    "Handicrafts & Handlooms": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Handicrafts+%26+Handlooms.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/handloom.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Artisanal+crafts+(wood%2C+metal%2C+pottery).jpg"
    ],
    "Construction & Building Materials": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Construction+%26+Building+Materials.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Construction-Aggregate-Types.png",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Cement+products+(blocks%2C+tiles).avif"
    ],
    "Leather & Footwear": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.20.31+-+A+collage+of+four+images+depicting+different+stages+of+leather+and+footwear+production_+1)+A+traditional+leather+tanning+unit+with+large+drums+and+wor.webp"
    ],
    "Wood & Furniture": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.22.33+-+A+detailed+image+showcasing+wood+and+furniture+manufacturing.+The+scene+includes+modular+and+customized+furniture+pieces+being+crafted+in+a+profession.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.22.36+-+A+luxurious+furniture+showroom+featuring+premium+wooden+furniture.+The+scene+includes+elegant%2C+handcrafted+wooden+tables%2C+chairs%2C+cabinets%2C+and+sofas+.webp"
    ],
    "Printing & Packaging": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Printing+%26+Packaging+-+stickers.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Packaging-material-types-ftd.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Corrugated+box+manufacturing.webp"
    ],
    "Information Technology & Services": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Information-Technology-Services.png",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/internet-information-technology-businessman-hand-showing-concept-75784736.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Saas.jpg"
    ],
    "Logistics & Warehousing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Logistics+%26+Warehousing.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/produce-crates-in-cold-storage.jpeg.jpeg"
    ],
    "Healthcare & Medical Devices": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Healthcare+%26+Medical+Devices.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Disposable+medical+products.jpeg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Medical+device+assembly+unit.webp"
    ],
    "Tourism & Hospitality": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Tourism+%26+Hospitality.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Small+hotels%2C+lodges%2C+homestays.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Travel+agency.webp"
    ],
    "Education & Skill Development": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Education+%26+Skill+Development.png",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/vocational-training-centre-image.avif",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Edtech+startups.jpg"
    ],
    "Renewable Energy": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Solar+products+assembly.avif"
    ],
    "Fintech & Banking": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/digital-marketing-agency-in-chennai.png"
    ],
    "E-commerce & Retail": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/E-commerce+%26+Retail.jpg"
    ]
}
