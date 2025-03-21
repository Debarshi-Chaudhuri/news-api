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
    "Plastics & Rubber Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/7.+Plastics+%26+Rubber+Products.avif"
    ],
    "Adhesives": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/adhesives..webp"
    ],
    "Artisanal Crafts": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Artisanal+crafts+(wood%2C+metal%2C+pottery)+1.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Artisanal+crafts+(wood%2C+metal%2C+pottery).jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Artisanal+crafts+(wood%2C+metal%2C+pottery)2.webp"
    ],
    "Auto Parts": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/auto_parts_industry_faces_total_collapse-min.jpg"
    ],
    "BPO Services": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/bpo-service.png"
    ],
    "Capital Goods": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/capital-goods.webp"
    ],
    "Casting": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/casting.jpeg"
    ],
    "Cement Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Cement+products+(blocks%2C+tiles).avif"
    ],
    "Chemicals & Pharmaceuticals": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Chemicals+%26+Pharmaceuticals.jpg"
    ],
    "Coaching Centers": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Coaching+centers.avif"
    ],
    "Construction & Building Materials": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Construction+%26+Building+Materials.jpg"
    ],
    "Construction Aggregates": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Construction-Aggregate-Types.png"
    ],
    "Corrugated Box Manufacturing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Corrugated+box+manufacturing.webp"
    ],
    "Cosmetics & Personal Care": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Cosmetics+%26+personal+care+products.webp"
    ],
    "Leather & Footwear": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.20.31+-+A+collage+of+four+images+depicting+different+stages+of+leather+and+footwear+production_+1)+A+traditional+leather+tanning+unit+with+large+drums+and+wor.webp"
    ],
    "Wood & Furniture Manufacturing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.22.33+-+A+detailed+image+showcasing+wood+and+furniture+manufacturing.+The+scene+includes+modular+and+customized+furniture+pieces+being+crafted+in+a+profession.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/DALL%C2%B7E+2025-03-21+15.22.36+-+A+luxurious+furniture+showroom+featuring+premium+wooden+furniture.+The+scene+includes+elegant%2C+handcrafted+wooden+tables%2C+chairs%2C+cabinets%2C+and+sofas+.webp"
    ],
    "Diagnostic Labs": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Diagnostic+labs.avif"
    ],
    "Digital Marketing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/digital-marketing-agency-in-chennai.png",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/digital-marketing-agency-popular-services-1024x791.webp"
    ],
    "Disposable Medical Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Disposable+medical+products.jpeg"
    ],
    "Dyes and Intermediates": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Dyes+and+intermediates.jpeg"
    ],
    "Edtech Startups": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Edtech+startups.jpg"
    ],
    "Education & Skill Development": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Education+%26+Skill+Development.png"
    ],
    "Electrical Fittings & Cables": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Electrical+fittings+%26+cables.jpg"
    ],
    "Electrical Machinery": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Electrical+machinery.jpg"
    ],
    "Embroidered Clothes": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Embroidered+clothes.jpg-org.jpg"
    ],
    "Ethnic Products for Export": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Ethnic+products+for+export.jpeg"
    ],
    "Food & Catering Services": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Food+%26+catering+services.jpg"
    ],
    "Food Processing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/food+processing.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/fruit-vegetable-processing.jpg"
    ],
    "Handicrafts & Handlooms": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Handicrafts+%26+Handlooms.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/handloom.jpg"
    ],
    "Healthcare & Medical Devices": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Healthcare+%26+Medical+Devices.webp"
    ],
    "Home Décor & Gift Articles": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Home+de%CC%81cor%2C+gift+articles.jpg"
    ],
    "Industrial Chemicals": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Industrial+chemicals.webp"
    ],
    "Industrial Equipment": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Industrial+equipment.png"
    ],
    "Information Technology Services": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Information-Technology-Services.png",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/internet-information-technology-businessman-hand-showing-concept-75784736.webp"
    ],
    "Label & Sticker Production": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Label+%26+sticker+production.webp"
    ],
    "Limestone & Lodges": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/limestone-lodges.jpg"
    ],
    "Logistics & Warehousing": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Logistics+%26+Warehousing.webp"
    ],
    "Medical Device Assembly": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Medical+device+assembly+unit.webp"
    ],
    "Oil Mill": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/oil+mill.jpg"
    ],
    "Packaging Materials": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Packaging-material-types-ftd.jpg"
    ],
    "Paints & Adhesives": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Paints%2C+adhesives..webp"
    ],
    "Personal Care Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/personal-care-product-manufacturer.jpg"
    ],
    "Printing & Packaging": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Printing+%26+Packaging+-+stickers.webp"
    ],
    "Cold Storage": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/produce-crates-in-cold-storage.jpeg.jpeg"
    ],
    "Readymade Garments": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/readymade-garments.webp"
    ],
    "Rice & Flour Mill": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/rice-flour-mill.jpg"
    ],
    "Rubber Products": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products++belts.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products+hoses.webp",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products+tyres.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Rubber-based+products.jpg"
    ],
    "SaaS": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Saas.jpg"
    ],
    "Sanitaryware & Fittings": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Sanitaryware%2C+pipes+%26+fittings.jpg",
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/sanitaryware.jpg"
    ],
    "Sheet Metal Fabrication": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/sheet-metal-fabrication.jpg"
    ],
    "Small Hotels & Homestays": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Small+hotels%2C+lodges%2C+homestays.jpg"
    ],
    "Small Pharma Units": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/small+pharma+units.avif"
    ],
    "Solar Products Assembly": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Solar+products+assembly.avif"
    ],
    "Stone Crushing & Aggregates": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Stone+crushing+%26+aggregates.jpg"
    ],
    "Textile Industries": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/textile+industries.jpg"
    ],
    "Tourism & Hospitality": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Tourism+%26+Hospitality.jpg"
    ],
    "Travel Agency": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Travel+agency.webp"
    ],
    "Tyre Retreading": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Tyre+retreading.jpeg"
    ],
    "Vocational Training": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/vocational-training-centre-image.avif"
    ],
    "Welding": [
        "https://pice-prod-public.s3.ap-south-1.amazonaws.com/app/hackathon/Welding.webp"
    ]
}
