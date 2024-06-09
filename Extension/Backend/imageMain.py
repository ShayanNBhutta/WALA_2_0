import numpy as np
from scipy.stats import entropy
import requests
from PIL import Image
from io import BytesIO


def calculate_normalized_entropy_from_url(image_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print("Error fetching image from URL:", e)
        return -1

    # Read the image using PIL
    try:
        img = Image.open(BytesIO(response.content)).convert('L')
    except Exception as e:
        print("Error reading image:", e)
        return -1

    # Convert PIL image to numpy array
    img_array = np.array(img)

    # Flatten the image into a 1D array
    flat_img = img_array.flatten()

    # Calculate histogram
    hist, _ = np.histogram(flat_img, bins=256, range=[0, 256])

    # Normalize histogram to get probability distribution
    prob_dist = hist / np.sum(hist)

    # Calculate Shannon's entropy
    entropy_value = entropy(prob_dist, base=2)

    # Normalize entropy to the range [0, 1]
    normalized_entropy = entropy_value / np.log2(len(prob_dist))

    # Handle zero entropy
    if normalized_entropy == 0:
        normalized_entropy = 0.01

    print("Normalized Entropy:", normalized_entropy)

    return normalized_entropy
