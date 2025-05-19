print(">>> progress_plot.py has been loaded!")  # Confirms module is imported

import matplotlib.pyplot as plt

class ProgressPlot:
    def __init__(self):
        print(">>> ProgressPlot initialized")  # Confirms class is created
        self.counter = 0
        self.fig, self.ax = plt.subplots()
        self.ax.set_axis_off()
        self.image_plot = None

    def show(self, image, title=""):
        print(f">>> Showing generation {self.counter}")  # Tracks each generation
        if self.image_plot is None:
            self.image_plot = self.ax.imshow(image)
        else:
            self.image_plot.set_data(image)

        self.ax.set_title(title)
        filename = f"progress_{self.counter:02d}.png"
        self.fig.savefig(filename, bbox_inches='tight')
        print(f"[✓] Saved {filename}")
        self.counter += 1

    def finish(self):
        print(">>> Final image saved. Plotting complete.")
