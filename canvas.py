from canvasapi import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import threading

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SIMPLE TO DO LIST")
        self.root.geometry(f"{300}x{300}")
        self.root.attributes('-topmost', True)

    def run(self):
        self.root.mainloop()

    def set_up_frames(self):
        self.home = tk.Frame(self.root)
        self.home.pack(fill = tk.BOTH, expand = True)
        
        self.button_frame = tk.Frame(self.home)
        self.button_frame.pack(pady=5)

        self.text_area_frame = tk.Frame(self.home)
        self.text_area_frame.pack(fill=tk.BOTH, expand=True)

        self.import_canvas_frame = tk.Frame(self.root)
    
    def text_area(self):
        self.text_box = tk.Text(self.home)
        self.custom_text_box = tk.Text(self.home)

    def place_text_boxes(self):
        self.text_area_frame.rowconfigure(0, weight=1)
        self.text_area_frame.rowconfigure(1, weight=1)
        self.text_area_frame.columnconfigure(0, weight=1)

        self.text_box.grid(in_ = self.text_area_frame, row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.custom_text_box.grid(in_ = self.text_area_frame, row=1, column=0, sticky="nsew", padx=10, pady=(10, 5))

    def save_button(self):
        self.save = tk.Button(self.button_frame, text = "Save Current List", width = 35, command = self.save_file)
    
    def import_from_saved_button(self):
        self.saved = tk.Button(self.button_frame, width = 35, text = "Import from Saved", command = self.get_save)

    def auto_import_button(self):
        auto_import = tk.Checkbutton(self.home, text = "Auto Import From Canvas Every Hour?", command = self.run_import)
        auto_import.grid(in_=self.button_frame, row=2, column=0, columnspan = 2, sticky="ew", padx=5)

    def canvas_button(self):
        self.submit = tk.Button(self.button_frame, width = 70, text = "Import from Canvas", command = self.canvas_button_command)

    def hide_button(self):
        self.hide = tk.Button(self.button_frame, command = self.hide_buttons, text = "Hide Buttons")

    def hide_buttons(self):
        self.submit.grid_remove()
        self.save.grid_remove()
        self.saved.grid_remove()

        self.hide.config(text="Show Buttons", command = self.show_buttons) 
        self.buttons_hidden = True

    def show_buttons(self):
        self.submit.grid()
        self.save.grid()
        self.saved.grid()

        self.hide.config(text="Hide Buttons", command = self.hide_buttons)

    def place_buttons(self):
        self.button_frame.columnconfigure(0, weight=1) 
        self.button_frame.columnconfigure(1, weight=1)

        self.submit.grid(in_=self.button_frame, row=0, column=0, columnspan=2, sticky="ew", padx = 5, pady = 10)
        self.save.grid(in_=self.button_frame, row=1, column=0, sticky="ew", padx=5)
        self.saved.grid(in_=self.button_frame, row=1, column=1, sticky="ew", padx=5)
        self.hide.grid(in_=self.button_frame, row=3, column=0, columnspan = 2, sticky="ew", padx=5)

    def canvas_button_command(self):
        self.home.pack_forget()

        for widget in self.import_canvas_frame.winfo_children():
            widget.destroy()

        self.set_get_buttons()

        submit_inputs = tk.Button(self.import_canvas_frame, text = "Import", padx = 70, command = self.get_inputs)
        submit_inputs.pack(padx=20, pady = 20)

        go_back = tk.Button(self.import_canvas_frame, text = "nevermind :(", command = self.go_back)
        go_back.pack(padx = 20, pady = 5)
    
    def make_buttons(self):
        self.canvas_button()
        self.save_button()
        self.import_from_saved_button()
        self.hide_button()

    
    def set_get_buttons(self):
        self.import_canvas_frame.pack(fill = tk.BOTH, expand = True)

        label_API_URL = tk.Label(self.import_canvas_frame, text = "Enter CANVAS URL:")
        label_API_URL.pack(padx = 20, pady = 10)
        self.enter_API_URL = tk.Entry(self.import_canvas_frame)
        self.enter_API_URL.pack()

        label_API_KEY = tk.Label(self.import_canvas_frame, text = "Enter CANVAS KEY:")
        label_API_KEY.pack(padx = 20, pady = 10)
        self.enter_API_KEY = tk.Entry(self.import_canvas_frame)
        self.enter_API_KEY.pack()

        label_USER_ID = tk.Label(self.import_canvas_frame, text = "Enter USER ID:")
        label_USER_ID.pack(padx = 20, pady = 10)
        self.enter_USER_ID = tk.Entry(self.import_canvas_frame)
        self.enter_USER_ID.pack()

    def go_back(self):
        self.import_canvas_frame.pack_forget()
        self.home.pack(fill = tk.BOTH, expand = True)

    def get_inputs(self):
        self.API_URL = self.enter_API_URL.get()
        self.API_KEY = self.enter_API_KEY.get()
        self.USER_ID = self.enter_USER_ID.get()

        self.import_canvas()

        if self.import_successful:
            self.go_back()
            self.auto_import_button()
            
    def run_import(self):
        thread = threading.Timer(10, self.loop_import)
        thread.start()

    def loop_import(self):
        self.text_box.delete("1.0", tk.END)
        self.import_canvas()

    def import_canvas(self):
        try:
            canvas = Canvas(self.API_URL, self.API_KEY)
            account = canvas.get_user(self.USER_ID)
            courses = account.get_courses()
            for course in courses:
                items = account.get_assignments(course)
                try:
                    if course.enrollment_term_id == 418:
                        self.text_box.insert("end", f'\ncourse: {course} \n')
                        self.text_box.insert("end", items[0])
                        """for item in items:
                            self.text_box.insert("end", item)
                            self.text_box.insert("end", "\n")"""
                except:
                    continue
            self.import_successful = True
        except:
            error = tk.Label(self.import_canvas_frame, text = "Error! Enter valid URL and Key.")
            error.pack()
            self.import_successful = False
        
    def save_file(self):
        canvas_file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if canvas_file_path:
            with open(canvas_file_path, "w") as file:
                file.write(self.text_box.get("1.0", tk.END))
        custom_file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if custom_file_path:
            with open(custom_file_path, "w") as file:
                file.write(self.custom_text_box.get("1.0", tk.END))
    
    def get_save(self):
        canvas_file_path = askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if canvas_file_path:
            with open(canvas_file_path, "r") as file:
                self.text_box.insert(tk.END, file.read())
        custom_file_path = askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if custom_file_path:
            with open(custom_file_path, "r") as file:
                self.text_box.insert(tk.END, file.read())

if __name__ == "__main__":
    win = Window()
    win.set_up_frames()
    win.make_buttons()
    win.place_buttons()
    win.text_area()
    win.place_text_boxes()
    win.run()

 
        