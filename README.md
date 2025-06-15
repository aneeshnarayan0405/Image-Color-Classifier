# Image Color Classifier

A Python application that analyzes images and identifies their dominant colors using K-means clustering.

## Features

- Identifies dominant colors in any image
- Provides color names and RGB values
- Visualizes original image with color swatches
- Handles various image formats (JPEG, PNG, WEBP)
- Adjustable number of colors to extract

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-color-classifier.git
   cd image-color-classifier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```bash
python color_classifier.py path/to/your/image.jpg
```

Optional arguments:
- `--k`: Number of dominant colors to extract (default: 3)

Example:
```bash
python color_classifier.py images/Test_Color.jpg --k 5
```

### As a Python Module

```python
from color_classifier import ImageColorClassifier

classifier = ImageColorClassifier(k=3)
color_name, rgb_value = classifier.analyze("path/to/image.jpg")
```

## Example Outputs

### Test_Image2.webp
![Test_Image2.webp analysis](images/Test_Image2_output.png)

Dominant colors:
1. Blue (RGB: [ 35  93 172])
2. Light Blue (RGB: [ 98 167 222])
3. White (RGB: [238 242 247])

### Test_Color.jpg
![Test_Color.jpg analysis](images/Test_Color_output.png)

Dominant colors:
1. Red (RGB: [237  28  36])
2. Blue (RGB: [  0 114 188])
3. Yellow (RGB: [255 242   0])

## Theory Behind the Implementation

The color classifier uses K-means clustering to identify dominant colors:

1. **Image Preprocessing**:
   - Converts image to RGB color space
   - Resizes while maintaining aspect ratio for faster processing

2. **Color Extraction**:
   - Reshapes image into a list of pixels
   - Uses K-means to cluster similar colors
   - Finds cluster centers (dominant colors)
   - Counts pixels in each cluster to determine dominance

3. **Color Naming**:
   - Compares each dominant color to a database of known colors
   - Uses Euclidean distance to find the closest named color

4. **Visualization**:
   - Displays original image alongside color swatches
   - Shows color names and RGB values

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
