import tkinter as tk
from PIL import Image, ImageTk
import customtkinter
import cv2
from tkinter import messagebox

class RPSGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("700x530")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        #initialize the web cam
        self.video_stream = cv2.VideoCapture(0)
        if not self.video_stream.isOpened():
            messagebox.showerror("Error", "Cannot open the webcam!")
            exit()

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

        self.user_move_label = tk.Label(self.camera_frame, text="test", bg="white", font=("Open Sauce Sans", 12))
        self.user_move_label.place(relx=0.5, rely=1.0, anchor="s")  # Bottom center

        # Right - Computer frame (fixed size)
        self.comp_frame = tk.Frame(self.canvas, bg="white", width=270, height=270)
        self.canvas.create_window(370, 20, anchor="nw", window=self.comp_frame)

        self.comp_move_label = tk.Label(self.comp_frame, text="test", bg="white", font=("Open Sauce Sans", 12))
        self.comp_move_label.place(relx=0.5, rely=1.0, anchor="s")  # Bottom center

        # --- Shoot Button ---
        self.shoot_button = customtkinter.CTkButton(
            master=root,
            text="SHOOT",
            fg_color="black",
            hover_color="#333333",
            text_color="white",
            corner_radius=20,
            font=("Open Sauce Sans", 14),
            width=150,
            height=35
        )
        self.shoot_button.pack(pady=(0, 20))

        self.result_label = tk.Label(root, text="Result", font=("Open Sauce Sans", 14), bg="white")
        self.result_label.pack()

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
