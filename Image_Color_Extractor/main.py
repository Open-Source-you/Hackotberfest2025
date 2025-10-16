"""
Image Color extractor using KMeans Clustering

Author: Madhan Kumar R
Date: 16 October 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import KMeans

# Place your image file in the same directory as this script
# and name it 'test.jpg' or change the filename below accordingly.
img = mpimg.imread('test.jpg')
print("Image exists")

image = mpimg.imread('test.jpg')
w, h, d = image.shape
pixels = image.reshape((w * h, d))
print("Image reshaped")
n_colors = 10
kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(pixels)
print("KMeans fitted")
palette = np.uint8(kmeans.cluster_centers_)

plt.imshow([palette])
plt.axis('off')
plt.show()
print("Palette displayed")
