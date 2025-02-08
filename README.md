# Restaurant Comparison Grid Generator

This project is a Python script that integrates with the Yelp Fusion API to fetch restaurant data and images, then generates a composite grid image displaying each restaurant’s details alongside up to 5 photos. The left panel of each row shows the restaurant's name, city, and its distance from Bothell, WA, while the right panel displays the images (or placeholders if images are missing).

## Features

- **Yelp API Integration:**  
  Searches for restaurants by name and location hint using the Yelp Fusion API, retrieving detailed business information along with photos.

- **Distance Calculation:**  
  Computes the great-circle distance (in miles) from Bothell, WA to the restaurant using the Haversine formula.

- **Flexible Input Parsing:**  
  Accepts multiple input formats, such as:
  - Numbered list entries (e.g., `1. Cactus bellevue`)
  - Hyphen-separated values (e.g., `Korea house restaurant - https://g.co/kgs/xG5zT8D`)
  - Comma-separated values (e.g., `Baekjeong KBBQ, Seattle`)

- **Composite Image Generation:**  
  Creates a PNG image grid where each row represents a restaurant with a text panel and an image panel. If fewer than 5 images are available, placeholders are shown.

## Requirements

- Python 3.6+
- [Requests](https://pypi.org/project/requests/)
- [Pillow](https://pypi.org/project/Pillow/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install the required packages using pip:

```bash
pip install requests pillow python-dotenv
```

## Setup

1. **Clone the Repository**

   Clone this repository to your local machine and navigate into the project directory:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Configure Your Yelp API Key**

   - Sign up for an API key at the [Yelp Developers](https://www.yelp.com/developers) website.
   - Create a `.env` file in the project root with the following content:

     ```dotenv
     YELP_API_KEY=your_yelp_api_key_here
     ```

## Usage

The script includes a sample `__main__` block with example restaurant inputs. To run the script, execute:

```bash
python <script_name>.py
```

After running, the script will generate a composite image named `restaurants_comparison.png` in the project directory.

## Code Overview

- **Environment Setup:**  
  Uses `python-dotenv` to load environment variables from a `.env` file, ensuring the Yelp API key is securely managed.

- **Yelp API Data Fetching:**  
  - `fetch_yelp_data(name, location_hint, max_photos=5)`: Searches for a business and retrieves its details and up to 5 photos.
  
- **Distance Calculation:**  
  - `compute_distance(lat1, lon1, lat2, lon2)`: Computes the great-circle distance between two coordinates using the Haversine formula.

- **Image Processing:**  
  - `fetch_image(url_or_path)`: Retrieves an image from a URL or local file path.
  - `create_restaurant_grid(restaurants, row_height=200, text_panel_width=300, img_width=200)`: Generates the composite grid image with a text panel and an image panel for each restaurant.

- **Input Parsing:**  
  - `parse_restaurant_input(line)`: Parses various restaurant input formats, extracting the restaurant name and location, then uses the Yelp API to fetch detailed data.

## Customization

- **Input Modification:**  
  Update the sample restaurant entries in the `__main__` block with your own data.
  
- **Layout Adjustments:**  
  Modify parameters like `row_height`, `text_panel_width`, and `img_width` in the `create_restaurant_grid` function to change the appearance of the final composite image.

## Troubleshooting

- **Missing Yelp API Key:**  
  Ensure that the `.env` file exists and contains a valid `YELP_API_KEY`.

- **No Business Found:**  
  Verify that the restaurant names and location hints are correct. The script will print a warning and use placeholders if a restaurant cannot be found.

- **Image Loading Issues:**  
  If images fail to load, the script will display a placeholder image. Check your network connection and ensure the image URLs are accessible.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **Yelp Fusion API:** For providing comprehensive restaurant data.
- **Pillow:** For advanced image processing capabilities.
- **python-dotenv:** For secure management of environment variables.
- **The Open Source Community:** For ongoing contributions to the libraries and tools used in this project.
