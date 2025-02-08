import os
import math
import re
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve your Yelp API key from the environment variables
YELP_API_KEY = os.getenv("YELP_API_KEY")
if not YELP_API_KEY:
    raise ValueError("Missing YELP_API_KEY environment variable. Check your .env file.")

# Yelp API endpoints and headers
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_DETAILS_URL = 'https://api.yelp.com/v3/businesses/{}'
HEADERS = {'Authorization': f'Bearer {YELP_API_KEY}'}


def compute_distance(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance between two points on Earth (in miles)
    using the Haversine formula.
    """
    R = 3958.8  # Earth radius in miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def fetch_yelp_data(name, location_hint, max_photos=5):
    """
    Search for a business by name using Yelp Fusion API.
    The location_hint is used for the search; if unknown, we default to Bothell.
    Returns a tuple (business, photos) where business is the Yelp business object
    and photos is a list of image URLs.
    """
    params = {
        'term': name,
        'location': location_hint if location_hint != "Unknown" else "Bothell, WA",
        'limit': 1
    }
    response = requests.get(YELP_SEARCH_URL, headers=HEADERS, params=params)
    data = response.json()

    if not data.get('businesses'):
        print("No business found for:", name, location_hint)
        return None, []

    business = data['businesses'][0]

    # Retrieve detailed business info for additional photos.
    details_response = requests.get(YELP_DETAILS_URL.format(business['id']), headers=HEADERS)
    details = details_response.json()
    photos = details.get('photos', [])

    main_image = business.get('image_url')
    # If there are no photos in details, use the main image (only once)
    if not photos and main_image:
        photos = [main_image]
    # Otherwise, if the main image isn’t already in the photos list, add it at the beginning.
    elif main_image and main_image not in photos:
        photos.insert(0, main_image)

    return business, photos[:max_photos]


def fetch_image(url_or_path):
    """
    Fetch an image from a URL (http/https) or open from a local path.
    Returns a Pillow Image object.
    """
    if url_or_path.lower().startswith("http"):
        response = requests.get(url_or_path)
        response.raise_for_status()  # raise exception for bad responses
        img = Image.open(BytesIO(response.content))
        return img.convert("RGB")
    else:
        img = Image.open(url_or_path)
        return img.convert("RGB")


def create_restaurant_grid(restaurants, row_height=200, text_panel_width=300, img_width=200):
    """
    Create a composite PNG image where each restaurant gets one row.
      - Left panel shows restaurant name, city, and distance from Bothell.
      - Right area shows 5 images (resized to fit in cells). If fewer than 5 images
        are available, a placeholder is shown.
    """
    num_images_per_restaurant = 5
    num_restaurants = len(restaurants)
    final_width = text_panel_width + (img_width * num_images_per_restaurant)
    final_height = row_height * num_restaurants

    # Create a blank white canvas.
    final_img = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))

    # Prepare a font (try Arial; fallback to default if not available)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(final_img)

    for i, r in enumerate(restaurants):
        row_y = i * row_height

        # Draw the text panel
        text_x = 10
        text_y = row_y + 10
        text_lines = [
            f"Name: {r['name']}",
            f"City: {r['city']}",
            f"Distance: {r['distance_from_bothell']}"
        ]
        for line in text_lines:
            draw.text((text_x, text_y), line, fill=(0, 0, 0), font=font)
            text_y += 30

        # Prepare the list of images.
        # If the restaurant has fewer than 5 images, fill in with None.
        restaurant_images = r["images"][:]
        if len(restaurant_images) < num_images_per_restaurant:
            restaurant_images += [None] * (num_images_per_restaurant - len(restaurant_images))

        # Process images
        img_x_start = text_panel_width
        for j, img_url in enumerate(restaurant_images):
            if img_url is not None:
                try:
                    img = fetch_image(img_url)
                except Exception as e:
                    print(f"Warning: Could not load image '{img_url}': {e}")
                    img = Image.new("RGB", (img_width, row_height), color=(200, 200, 200))
            else:
                # Create a placeholder image for missing photos
                img = Image.new("RGB", (img_width, row_height), color=(220, 220, 220))
                placeholder_draw = ImageDraw.Draw(img)
                placeholder_text = "No Image"
                # Compute text width and height using getsize (or textbbox as a fallback)
                try:
                    text_width, text_height = font.getsize(placeholder_text)
                except AttributeError:
                    bbox = placeholder_draw.textbbox((0, 0), placeholder_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                placeholder_draw.text(
                    ((img_width - text_width) // 2, (row_height - text_height) // 2),
                    placeholder_text,
                    fill=(0, 0, 0),
                    font=font
                )

            # Resize the image while keeping its aspect ratio.
            w, h = img.size
            aspect_ratio = w / h
            new_height = row_height
            new_width = int(new_height * aspect_ratio)
            if new_width > img_width:
                new_width = img_width
                new_height = int(new_width / aspect_ratio)

            try:
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                resample_filter = Image.ANTIALIAS

            img = img.resize((new_width, new_height), resample_filter)
            cell_bg = Image.new("RGB", (img_width, row_height), color=(255, 255, 255))
            offset_x = (img_width - new_width) // 2
            offset_y = (row_height - new_height) // 2
            cell_bg.paste(img, (offset_x, offset_y))
            x_pos = img_x_start + (j * img_width)
            final_img.paste(cell_bg, (x_pos, row_y))

    return final_img


def parse_restaurant_input(line):
    """
    Given a minimal restaurant input string, return a dictionary
    with keys: 'name', 'city', 'distance_from_bothell', and 'images'.

    This version is more flexible. It:
      - Removes any leading numbering (e.g., "1. " or "2) ").
      - If the line contains a hyphen (" - ") or comma, splits on that.
      - Otherwise, assumes the last word is the city and the preceding words form the restaurant name.
    """
    # Remove leading numbering (e.g., "1. ", "2) ")
    line = re.sub(r'^\s*\d+[\.\)]\s*', '', line.strip())

    # Check for a hyphen or comma delimiter
    if " - " in line:
        parts = line.split(" - ")
        restaurant_name = parts[0].strip()
        # If the second part starts with "http", treat it as a URL
        if parts[1].strip().startswith("http"):
            location_hint = "Unknown"
        else:
            location_hint = parts[1].strip()
    elif "," in line:
        parts = line.split(",")
        restaurant_name = parts[0].strip()
        location_hint = parts[1].strip()
    else:
        # Assume the last word is the city and the rest is the restaurant name.
        tokens = line.split()
        if len(tokens) >= 2:
            restaurant_name = " ".join(tokens[:-1]).strip()
            location_hint = tokens[-1].strip()
        else:
            restaurant_name = line
            location_hint = "Bothell, WA"  # default fallback

    # Normalize location (e.g., "bellevue" -> "Bellevue")
    location_hint = location_hint.title()

    # Use the Yelp API to fetch business data and images.
    business, photos = fetch_yelp_data(restaurant_name, location_hint, max_photos=5)

    if business is not None:
        # Use the city returned by Yelp.
        city = business['location']['city']

        # Compute distance from Bothell (approximate coordinates)
        bothell_lat = 47.762
        bothell_lon = -122.205
        business_lat = business['coordinates']['latitude']
        business_lon = business['coordinates']['longitude']
        distance = f"{compute_distance(bothell_lat, bothell_lon, business_lat, business_lon):.1f} miles"
        images = photos
    else:
        # Fallback if Yelp search fails.
        city = location_hint
        distance = "Unknown"
        safe_name = "".join(c for c in restaurant_name if c.isalnum())
        images = [f"https://via.placeholder.com/300?text={safe_name}+{i+1}" for i in range(5)]

    return {
        "name": restaurant_name,
        "city": city,
        "distance_from_bothell": distance,
        "images": images
    }


if __name__ == "__main__":
    # Example minimal inputs (various formats)
    input_lines = [
        "1. Cactus bellevue",
        "2. The matador Redmond",
        "3. Tipsy Cow Woodinville",
        # Existing formats:
        "sura-korean-bbq-tofu-house-restaurant-LYNNWOOD",
        "Korea house restaurant - https://g.co/kgs/xG5zT8D",
        "Baekjeong KBBQ - http://www.baekjeongkbbq.com/locations-2/"
    ]

    # Process each input line to compute full restaurant data.
    restaurants = [parse_restaurant_input(line) for line in input_lines]

    # Create the composite image.
    final_image = create_restaurant_grid(restaurants)

    # Save the output image.
    output_filename = "restaurants_comparison.png"
    final_image.save(output_filename)
    print(f"Saved: {output_filename}")
