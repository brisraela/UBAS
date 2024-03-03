from tkinter import *
import cv2
import model
from PIL import Image, ImageTk
import customtkinter
import sys
import os


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




# Access the default camera
cap = cv2.VideoCapture(0)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Create a window object
app = customtkinter.CTk()
SHOW = False
# PLAY=False
DETECT = False


# Function to receive a WARNING or SAFE value and update the GUI
def update_warning(safe):
    if not safe:
        # Define the RGBA values for red with 50% transparency
        status.configure(text=" ⚠ WARNING ", bg_color="red")
    else:
        # Define the RGBA values for green with 50% transparency
        status.configure(text=" ✓ SAFE ", bg_color="green")


# Function to start/stop the camera feed
def toggle_camera_feed():
    global SHOW
    SHOW = not SHOW

    if SHOW:
        camera_button.configure(text="Hide Camera")
        detect_button.configure(state="normal")
    else:
        camera_button.configure(text="Show Camera")
        detect_button.configure(state="disabled")


# show_detected:
def show_detected():
    global DETECT
    DETECT = not DETECT

    if DETECT:
        detect_button.configure(text="Remove detect")
    else:
        detect_button.configure(text="Add detect")


def update_frame():
    # if PLAY:
    # Capture frame-by-frame
    ret, frame_basic = cap.read()
    SAFE, frame = model.analysis(frame_basic)

    rgb_frame = cv2.imread(resource_path('cameraOFF.png'))
    if SHOW:
        # cv2.imshow("live", frame)
        # Convert the frame from BGR to RGB
        rgb_frame = cv2.cvtColor(frame_basic, cv2.COLOR_BGR2RGB)
        # here v we exit from SHOW Cond
        if DETECT:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to an ImageTk format

    pil_image = Image.fromarray(rgb_frame)
    photo2 = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image, size=(600, 350))
    # photo = ImageTk.PhotoImage(image=image)
    # Update the label with the new image
    label_video.configure(image=photo2)
    label_video.image = photo2
    update_warning(SAFE)
    # if PLAY:
    app.after(10, update_frame)  # Schedule the next update_frame() call after 10 milliseconds


customFont = customtkinter.CTkFont("Courier", 20)

title = customtkinter.CTkLabel(master=app,
                               text="Unattended Baggage Alert System",
                               text_color="white",
                               font=(customFont, 36),
                               height=50,
                               corner_radius=12)

title.pack(side=TOP, anchor=N, padx=15, pady=15, fill=X)

# Create a label to display the SAFE/WARNING
status = customtkinter.CTkLabel(master=app,
                                text="none",
                                bg_color="black",
                                text_color="white",
                                font=(customFont, 24),
                                height=40,
                                corner_radius=12)

# Label for the camera feed
label_video = customtkinter.CTkLabel(app, text="")
label_video.pack(anchor=CENTER, padx=10, pady=10, fill=None)

status.pack(anchor=CENTER, padx=10, pady=10, fill=X)

# Create a button to toggle the camera feed
camera_button = customtkinter.CTkButton(app,
                                        text="Show Camera",
                                        font=(customFont, 20),
                                        fg_color="white",
                                        text_color="black",
                                        command=toggle_camera_feed)
camera_button.pack(side=LEFT, anchor=S, padx=10, pady=10, fill=BOTH, expand=YES)

detect_button = customtkinter.CTkButton(app,
                                        text="Add Detect",
                                        font=(customFont, 20),
                                        fg_color="white",
                                        text_color="black",
                                        command=show_detected,
                                        state=DISABLED)
detect_button.pack(side=RIGHT, anchor=S, padx=10, pady=10, fill=BOTH, expand=YES)

update_frame()

app.title("UBAS")
app.geometry('650x580')

# Start the tkinter main loop
app.mainloop()

# Release the capture
cap.release()
cv2.destroyAllWindows()