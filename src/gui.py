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


def launch_gui():
    root = tk.Tk()
    app = RPSGameApp(root)
    root.mainloop()
