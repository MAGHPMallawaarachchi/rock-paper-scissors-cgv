import tkinter as tk
from PIL import Image, ImageTk

class RPSGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("700x700")
        self.root.configure(bg="white")

        # --- Top bar ---
        self.top_frame = tk.Frame(root, bg="white")
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Left title
        self.title_frame = tk.Frame(self.top_frame, bg="white")
        self.title_frame.pack(side="left")

        self.title_label = tk.Label(self.title_frame, text="ROCK PAPER SCISSORS", font=("Open Sauce Sans", 20), bg="white")
        self.title_label.pack(side="left", padx=(0, 10))

        arrow_img = Image.open("assets/arrow.png").resize((30, 20), Image.LANCZOS)
        self.icon_image = ImageTk.PhotoImage(arrow_img)
        self.icon_label = tk.Label(self.title_frame, image=self.icon_image, bg="white")
        self.icon_label.pack(side="left")

        # Right group info
        self.right_frame = tk.Frame(self.top_frame, bg="white")
        self.right_frame.pack(side="right")

        self.group_label = tk.Label(self.right_frame, text="GROUP C", font=("Open Sauce Sans", 12), bg="white")
        self.group_label.pack(side="left", padx=(0, 5))

        shape_img = Image.open("assets/shape.png").resize((30, 30), Image.LANCZOS)
        self.shape_image = ImageTk.PhotoImage(shape_img)
        self.shape_label = tk.Label(self.right_frame, image=self.shape_image, bg="white")
        self.shape_label.pack(side="left")

        # --- Camera + Computer Move Canvas ---
        self.canvas = tk.Canvas(root, width=662, height=332, bg="white", highlightthickness=0)
        self.canvas.pack(pady=(10, 10))

        self.rounded_rect(self.canvas, 1, 1, 661, 321, radius=15, fill="white", outline="#D3D3D3", width=1)
        self.canvas.create_line(341, 10, 341, 312, fill="#D3D3D3", width=1)

        # Left - User camera frame (fixed size)
        self.camera_frame = tk.Frame(self.canvas, bg="white", width=270, height=270)
        self.canvas.create_window(20, 20, anchor="nw", window=self.camera_frame)

        # Right - Computer frame (fixed size)
        self.comp_frame = tk.Frame(self.canvas, bg="white", width=270, height=270)
        self.canvas.create_window(370, 20, anchor="nw", window=self.comp_frame)

    def rounded_rect(self, canvas, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

def launch_gui():
    root = tk.Tk()
    app = RPSGameApp(root)
    root.mainloop()
