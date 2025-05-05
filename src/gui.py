import tkinter as tk

class RPSGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("700x700")
        self.root.configure(bg="white")

def launch_gui():
    root = tk.Tk()
    app = RPSGameApp(root)
    root.mainloop()
