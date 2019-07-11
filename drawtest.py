# !/usr/bin/python3
import tkinter as tk
# from threading import Thread


class VirtualLedStrip:
    def __init__(self, width, height, pixel_count):
        self.pixel_count = pixel_count

        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, bg='#fff',
                                width=width, height=height)

        pixel_size = int(width / pixel_count)
        self.pixels = [
            self.canvas.create_rectangle(
                pixel_size * i,
                0,
                pixel_size * (i + 1),
                pixel_size,
                outline="#000",
                fill="#fff"
            )
            for i in range(0, self.pixel_count)
        ]

        self.canvas.pack()

        super().__init__()

    def run(self):
        self.window.mainloop()

    def set_colors(self, colors):
        for i, pixel in enumerate(self.pixels):
            self.canvas.itemconfig(pixel, fill=colors[i])


# strip = VirtualLedStrip(1000, 10, 100)
# strip.start()
# print('hello')
