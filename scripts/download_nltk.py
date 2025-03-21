#!/usr/bin/env python
"""
Script to download NLTK resources needed for the news scraper.
This script disables SSL verification by default to handle certificate issues.

Usage:
    python -m scripts.download_nltk [--verify-ssl]
"""

import os
import sys
import ssl
import nltk
import argparse

# List of required NLTK resources for newspaper3k
REQUIRED_NLTK_RESOURCES = [
    'punkt',
    'maxent_treebank_pos_tagger',
    'averaged_perceptron_tagger',
    'maxent_ne_chunker',
    'words',
    'stopwords'
]

def main():
    parser = argparse.ArgumentParser(description='Download NLTK resources for the news scraper')
    parser.add_argument('--verify-ssl', action='store_true', help='Enable SSL certificate verification')
    args = parser.parse_args()
    
    # Set NLTK data path
    nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
    os.environ['NLTK_DATA'] = nltk_data_dir
    
    # Create directory if it doesn't exist
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
        print(f"Created NLTK data directory at {nltk_data_dir}")
    
    # Disable SSL verification if requested
    if not args.verify_ssl:
        print("Disabling SSL certificate verification for NLTK downloads")
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except AttributeError:
            print("Failed to disable SSL verification")
    
    # Download resources
    print("Downloading NLTK resources...")
    for resource in REQUIRED_NLTK_RESOURCES:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, download_dir=nltk_data_dir)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Error downloading {resource}: {e}")
    
    print("\nDownload complete.")
    print(f"NLTK data directory: {nltk_data_dir}")
    print(f"Resources downloaded: {', '.join(REQUIRED_NLTK_RESOURCES)}")

if __name__ == "__main__":
    main()