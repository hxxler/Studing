import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processor App")

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.add_noise_button = tk.Button(master, text="Add Noise", command=self.add_noise)
        self.add_noise_button.pack()

        self.noise_level_label = tk.Label(master, text="Noise Level:")
        self.noise_level_label.pack()

        self.noise_level_scale = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.noise_level_scale.pack()

        self.remove_noise_button = tk.Button(master, text="Remove Noise", command=self.remove_noise)
        self.remove_noise_button.pack()

        self.threshold_label = tk.Label(master, text="Threshold Level:")
        self.threshold_label.pack()

        self.threshold_scale = tk.Scale(master, from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold_scale.pack()

        self.process_button = tk.Button(master, text="Process", command=self.process_image)
        self.process_button.pack()

        self.canvas = tk.Canvas(master)
        self.canvas.pack()

        self.original_image = None
        self.noisy_image = None
        self.filtered_image = None

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = cv2.imread(path)
            self.display_image(self.original_image)

    def display_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        self.canvas.image = photo
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    def add_noise(self):
        if self.original_image is not None:
            noise_level = self.noise_level_scale.get()
            noise = np.random.randint(0, 256, self.original_image.shape, dtype=np.uint8)
            noisy_image = cv2.addWeighted(self.original_image, 1 - noise_level / 100, noise, noise_level / 100, 0)
            self.noisy_image = noisy_image
            self.display_image(noisy_image)

    def remove_noise(self):
        if self.noisy_image is not None:
            threshold = self.threshold_scale.get()
            # Применение порогового фильтра
            filtered_image = self.noisy_image.copy()
            for i in range(1, filtered_image.shape[0] - 1):
                for j in range(1, filtered_image.shape[1] - 1):
                    neighbors = [
                      filtered_image[i - 1, j],  # Верхний сосед
                      filtered_image[i + 1, j],  # Нижний сосед
                      filtered_image[i, j - 1],  # Левый сосед
                      filtered_image[i, j + 1]   # Правый сосед
                      ]
                average_color = np.mean(neighbors, axis=0)
                if np.linalg.norm(filtered_image[i, j] - average_color) > threshold:
                    filtered_image[i, j] = average_color.astype(np.uint8)
        self.filtered_image = filtered_image
        self.display_image(filtered_image)


    def process_image(self):
        if self.original_image is not None and self.noisy_image is not None and self.filtered_image is not None:
            cv2.imshow("Original Image", self.original_image)
            cv2.imshow("Noisy Image", self.noisy_image)
            cv2.imshow("Filtered Image", self.filtered_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
