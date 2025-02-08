# Restaurant Comparison Grid Generator

A Python script that leverages the Yelp Fusion API to search for restaurants, fetch their details and images, compute distances from Bothell, WA, and generate a composite image grid displaying each restaurant's information alongside up to 5 images.

## Features

- **Yelp API Integration**: Searches for restaurants and retrieves detailed business information and photos.
- **Distance Calculation**: Computes the great-circle distance from Bothell using the Haversine formula.
- **Image Processing**: Combines restaurant details and images into a single composite PNG image.
- **Flexible Input Parsing**: Supports various minimal input formats for restaurant names and locations.
- **Environment Variables**: Uses a `.env` file to securely store sensitive data (Yelp API key).

## Requirements

- Python 3.6+
- The following Python libraries:
  - [requests](https://pypi.org/project/requests/)
  - [Pillow (PIL)](https://pypi.org/project/Pillow/)
  - [python-dotenv](https://pypi.org/project/python-dotenv/)

### Installation

You can install the required packages using pip:

```bash
pip install requests pillow python-dotenv
