import tkinter as tk


class Render:
    def __init__(self, width=500, height=500):
        self.master = tk.Tk()
        self.width = width
        self.height = height
        self.button = tk.Button(self.master, text="Stop", command=self.stop_simulation)
        self.button.pack()
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="gray")
        self.master.title("Collider")
        self.canvas.pack()
        self.simulate = True

    def stop_simulation(self):
        self.simulate = False

    def draw_disk(self, cx, cy, r):
        cx *= self.width
        cy *= self.height
        r *= self.width
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="blue")

    def update_and_clear(self):
        self.update()
        self.clear()

    def clear(self):
        self.canvas.delete("all")

    def update(self):
        self.canvas.update()
        self.canvas.update_idletasks()
