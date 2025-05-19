import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plt.ion()  # Interactive mode ON

img = mpimg.imread("puzzle.jpg")  # Or any image you have
plt.imshow(img)
plt.title("Pop-up Test")
plt.pause(10)  # Keep window open for 10 seconds