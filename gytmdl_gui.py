import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("GYTMDL GUI")

        self.label = tk.Label(master, text="Enter URL:")
        self.label.pack()

        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        self.progress = ttk.Progressbar(master, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack()

        self.start_button = tk.Button(master, text="Start Download", command=self.start_download)
        self.start_button.pack()

        # Bind the <Return> key event to start_download function
        self.master.bind("<Return>", self.start_download)

        # Close the window when the user clicks the close button
        master.protocol("WM_DELETE_WINDOW", self.close_window)

    def start_download(self, event=None):
        url = self.url_entry.get()
        if url:
            self.start_button.config(state="disabled")
            self.progress.start()
            threading.Thread(target=self.run_script, args=(url,)).start()

    def run_script(self, url):
        command = ["py", "-m", "gytmdl", url]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=startupinfo)
        while True:
            output = process.stdout.readline()
            if output.strip():
                print(output.strip())  # Display output in console (optional)
                # Update GUI or handle progress based on output
                # For example, you might check for specific strings in output to update progress bar
                if "100%" in output:
                    self.progress.stop()  # Stop the progress bar
                    break
                elif "File already exists" in output:
                    self.progress.stop()
                    self.start_button.config(state="normal")
                    self.show_error_message("File already exists!")
                    return
            else:
                break
        process.wait()
        self.progress.stop()
        self.start_button.config(state="normal")
        if process.returncode == 0:
            self.show_info_message("The download has finished!")

    def close_window(self):
        self.master.destroy()

    def show_error_message(self, message):
        error_window = tk.Tk()
        error_window.withdraw()  # Hide the error window
        messagebox.showerror("Error", message, parent=error_window)
        error_window.destroy()  # Destroy the error window after showing the message

    def show_info_message(self, message):
        messagebox.showinfo("Info", message)

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
