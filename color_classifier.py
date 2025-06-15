import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
import argparse
import os

class ImageColorClassifier:
    def __init__(self, k=3):
        self.k = k  # Number of dominant colors to extract
        
        # Extended color database
        self.color_db = {
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203),
            'brown': (165, 42, 42),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'lime': (0, 255, 0),
            'maroon': (128, 0, 0),
            'olive': (128, 128, 0),
            'navy': (0, 0, 128),
            'teal': (0, 128, 128),
            'silver': (192, 192, 192),
            'gold': (255, 215, 0),
            'violet': (238, 130, 238),
            'indigo': (75, 0, 130),
            'coral': (255, 127, 80),
            'salmon': (250, 128, 114),
            'turquoise': (64, 224, 208)
        }

    def preprocess_image(self, image_path):
        """Load and preprocess the image"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to load image - may be corrupt or wrong format")
        
        # Convert from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image to speed up processing while maintaining aspect ratio
        height, width = image.shape[:2]
        max_dim = 500
        scale = max_dim / max(height, width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), 
                         interpolation=cv2.INTER_AREA)
        
        return image

    def get_dominant_colors(self, image):
        """Extract dominant colors using K-means clustering"""
        # Reshape the image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=self.k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the cluster centers (dominant colors)
        colors = kmeans.cluster_centers_
        
        # Count the number of pixels in each cluster
        counts = Counter(kmeans.labels_)
        
        # Sort colors by frequency
        sorted_colors = sorted(zip(colors, counts.values()), 
                             key=lambda x: x[1], reverse=True)
        
        return [color for color, count in sorted_colors]

    def closest_color_name(self, rgb_color):
        """Find the closest color name for an RGB value"""
        min_distance = float('inf')
        closest_name = "Unknown"
        
        for name, rgb in self.color_db.items():
            distance = sum((rgb[i] - rgb_color[i]) ** 2 for i in range(3))
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        return closest_name

    def display_results(self, image, dominant_colors):
        """Display the original image and dominant colors"""
        plt.figure(figsize=(15, 5))
        
        # Show original image
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.axis('off')
        plt.title("Original Image")
        
        # Show dominant colors
        plt.subplot(1, 2, 2)
        for i, color in enumerate(dominant_colors):
            plt.subplot(1, len(dominant_colors), i+1)
            plt.imshow([[color.astype(int)]])
            plt.axis('off')
            color_name = self.closest_color_name(color)
            plt.title(f"{color_name}\nRGB: {color.astype(int)}")
        
        plt.tight_layout()
        plt.show()

    def analyze(self, image_path):
        """Main function to analyze an image"""
        try:
            # Load and preprocess the image
            image = self.preprocess_image(image_path)
            
            # Get dominant colors
            dominant_colors = self.get_dominant_colors(image)
            
            # Display results
            self.display_results(image, dominant_colors)
            
            # Return the most dominant color
            most_dominant = dominant_colors[0]
            color_name = self.closest_color_name(most_dominant)
            return color_name, most_dominant.astype(int)
        
        except Exception as e:
            print(f"Error processing image: {e}")
            return None, None


def main():
    parser = argparse.ArgumentParser(description='Image Color Classifier')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--k', type=int, default=3, 
                      help='Number of dominant colors to extract (default: 3)')
    args = parser.parse_args()

    classifier = ImageColorClassifier(k=args.k)
    color_name, rgb_value = classifier.analyze(args.image_path)

    if color_name:
        print(f"\nMost dominant color: {color_name}")
        print(f"RGB value: {rgb_value}")

if __name__ == "__main__":
    main()
