import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
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

        self.image_label = tk.Label(self.camera_frame, bg="white")
        self.image_label.place(relx=0.5, rely=0.0, anchor="n")

        self.user_move_label = tk.Label(self.camera_frame, text="", bg="white", font=("Open Sauce Sans", 12))
        self.user_move_label.place(relx=0.5, rely=1.0, anchor="s")  # Bottom center

        # Right - Computer frame (fixed size)
        self.comp_frame = tk.Frame(self.canvas, bg="white", width=270, height=270)
        self.canvas.create_window(370, 20, anchor="nw", window=self.comp_frame)

        self.comp_image_label = tk.Label(self.comp_frame, bg="white")
        self.comp_image_label.place(relx=0.5, rely=0.0, anchor="n")  # Top 

        self.comp_move_label = tk.Label(self.comp_frame, text="", bg="white", font=("Open Sauce Sans", 12))
        self.comp_move_label.place(relx=0.5, rely=1.0, anchor="s")  # Bottom center

        # Load Computer Choice Images
        self.rock_photo = ImageTk.PhotoImage(Image.open("assets/rock.png").resize((200, 200), Image.LANCZOS))
        self.paper_photo = ImageTk.PhotoImage(Image.open("assets/paper.png").resize((200, 200), Image.LANCZOS))
        self.scissor_photo = ImageTk.PhotoImage(Image.open("assets/scissor.png").resize((200, 200), Image.LANCZOS))

        # --- Shoot Button ---
        self.shoot_button = customtkinter.CTkButton(
            master=root,
            text="SHOOT",
            command=self.capture_image,
            fg_color="black",
            hover_color="#333333",
            text_color="white",
            corner_radius=20,
            font=("Open Sauce Sans", 14),
            width=150,
            height=35
        )
        self.shoot_button.pack(pady=(0, 20))

        self.result_label = tk.Label(root, text="", font=("Open Sauce Sans", 14), bg="white")
        self.result_label.pack()

        self.update_camera()

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
    
    def round_corners(self, img, radius):
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
        img.putalpha(mask)
        return img
    
    def update_camera(self):
        ret, frame = self.video_stream.read()
        if ret:
            self.latest_frame = frame.copy()  # Save for gesture detection
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((300, (300 * 3) // 4), Image.LANCZOS)
            img = self.round_corners(img, radius=10)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
        self.root.after(10, self.update_camera)

    def capture_image(self):
        from processing import remove_background, greyscale, threshold, binarize
        from classifier import classify_gesture
        from game_logic import computer_choice, decide_winner

        try:
            ret, frame = self.video_stream.read()
            if ret:
                frame = cv2.flip(frame, 1)
                save_path = "images/input.jpg"
                cv2.imwrite(save_path, frame)

                no_bg_path = remove_background(save_path)
                gray_img = greyscale(no_bg_path)
                thresh_img = threshold(gray_img)
                bin_img = binarize(gray_img)
                
                user_move = classify_gesture(no_bg_path)
                comp_move = computer_choice()
                result = decide_winner(user_move, comp_move)

                # Set computer image
                if comp_move == "rock":
                    self.comp_image_label.configure(image=self.rock_photo)
                    self.comp_image_label.image = self.rock_photo
                elif comp_move == "paper":
                    self.comp_image_label.configure(image=self.paper_photo)
                    self.comp_image_label.image = self.paper_photo
                else:
                    self.comp_image_label.configure(image=self.scissor_photo)
                    self.comp_image_label.image = self.scissor_photo
                
                # Update text labels
                self.user_move_label.config(text=user_move.upper())
                self.comp_move_label.config(text=comp_move.upper())
                self.result_label.config(text=f"{result}")
                
            else:
                raise Exception("Failed to capture image from webcam")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quit_game(self):
        self.video_stream.release()
        self.root.quit()

def launch_gui():
    root = tk.Tk()
    app = RPSGameApp(root)
    root.mainloop()
