import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Entry, Text, Scrollbar
import os
from tkinter import Entry, DoubleVar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Required libraries
import cv2
import numpy as np
import pandas as pd
from itertools import chain

# Your image_index_cal function here...

def image_index_cal(filename, noise_percentile=60, qi_threshold=500, path=True):
    '''
    directory is the folder allow user upload image and store csv file
    '''
    
    img_arr = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    gray_array_filter = img_arr[img_arr > 1]

    # Compute the histogram of the grayscale array
    histogram, bins = np.histogram(gray_array_filter, bins=256, range=(0, 256))

    # Create the histogram plot
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_title("Grayscale Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")
    ax.bar(bins[:-1], histogram, width=1, color='gray')
    ax.set_xlim(0, 256)
    
    vec_1D = list(chain.from_iterable(img_arr))
    
    low = np.percentile(vec_1D, 1)
    #99% as saturation
    satu = np.percentile(vec_1D, 99)
    #62% as noise
    noise = np.percentile(vec_1D, noise_percentile)
    #Mean value of noise and saturation
    middle = np.mean([noise, satu])
    
    #Replace 0 with 1
    if low < 1:
        low = 1
    #Calculate intensity ratio    
    IR = (satu - low) / low * 100
        
    NM_pixels = len(list(x for x in vec_1D if noise <= x <= middle))
    MS_pixels = len(list(y for y in vec_1D if middle < y <= satu))
        
    TSR = MS_pixels / NM_pixels
        
    QI = IR*TSR
    
    if QI >= qi_threshold:
        img_quality = 'Good'
    else:
        img_quality = 'Bad'
        
    
    img_name = os.path.splitext(os.path.basename(filename))[0]

    predictions = []

    output = {
        'Image_name':img_name,
        'Quality_index':QI, 
        'Image_Quality':img_quality
    }
    
    predictions.append(output)

    df_name_qi = pd.DataFrame(output, columns =['Image_name', 'Quality_index', 'Image_Quality'], index=range(1))

    # Define the output file path
    if path:
        output_path = os.path.join(os.path.dirname(filename), 'predict', img_name + '_quality.csv')
    else:
        output_path = os.path.join(os.getcwd(), 'predict', img_name + '_quality.csv')

    # Check if the directory exists, if not, create it
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    out_csv = df_name_qi.to_csv(output_path, index=False)
    
    return out_csv, predictions, fig

def select_images():
    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=(("JPEG files", "*.jpeg"), ("PNG files", "*.png"), ("All files", "*.*")))
    if file_paths:
        image_paths_var.set(", ".join(file_paths))

def calculate_quality():
    image_paths = image_paths_var.get().split(", ")
    if not image_paths or image_paths == [""]:
        messagebox.showerror("Error", "Please select images first!")
        return

    results.delete(1.0, tk.END)  # Clear previous results
    
    noise_value = noise_percentile_var.get()
    threshold_value = threshold_var.get()
    
    for image_path in image_paths:
        _, predictions, histogram_fig = image_index_cal(image_path, noise_value, threshold_value, path=False)
        
        # Load and display the image
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # Resize the image to fit into the GUI
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=0, padx=10, pady=20)

        # Display the histogram next to the image
        canvas = FigureCanvasTkAgg(histogram_fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=20)

        # Display results in the GUI directly
        results.insert(tk.END, f"Image Name: {predictions[0]['Image_name']}\n")
        results.insert(tk.END, f"Quality Index: {predictions[0]['Quality_index']}\n")
        results.insert(tk.END, f"Image Quality: {predictions[0]['Image_Quality']}\n\n")

app = tk.Tk()
app.title("Image Quality Index Calculator")

# Variables
image_paths_var = tk.StringVar()
noise_percentile_var = DoubleVar(value=60)  # Default value of 30
threshold_var = DoubleVar(value=500)       # Default value of 500

# GUI Components
select_images_btn = Button(app, text="Select Images", command=select_images)
select_images_btn.grid(row=1, column=0, pady=20, columnspan=2)  # 

image_paths_label = Label(app, text="Selected Images:")
image_paths_label.grid(row=2, column=0, pady=10, sticky='w')  # Using grid

#image_paths_text = Text(app, height=5, width=50)
#image_paths_text.grid(row=3, column=0, pady=10, columnspan=2)
#image_paths_text.insert(tk.END, image_paths_var.get())
#image_paths_scroll = Scrollbar(app, command=image_paths_text.yview)
#image_paths_scroll.grid(row=3, column=2, sticky='ns')  # Adjusted for grid

# Entry for Noise Percentile
noise_percentile_label = Label(app, text="Noise Percentile:")
noise_percentile_label.grid(row=4, column=0, pady=5, sticky='w')
noise_percentile_entry = Entry(app, textvariable=noise_percentile_var)
noise_percentile_entry.grid(row=5, column=0, pady=5, sticky='w')

# Entry for Good/Bad QI Threshold
threshold_label = Label(app, text="Good/Bad QI Threshold:")
threshold_label.grid(row=4, column=1, pady=5, sticky='w')
threshold_entry = Entry(app, textvariable=threshold_var)
threshold_entry.grid(row=5, column=1, pady=5, sticky='w')

# Calculate Quality Button
calculate_btn = Button(app, text="Calculate Quality", command=calculate_quality)
calculate_btn.grid(row=6, column=0, pady=20, columnspan=2)

# Image Display Label
image_label = Label(app)
image_label.grid(row=0, column=0, padx=10, pady=20)  # Using grid layout for side-by-side display

# Results Label and Text Box
results_label = Label(app, text="Results:")
results_label.grid(row=7, column=0, pady=10, sticky='w')
results = Text(app, height=30, width=30)
results.grid(row=8, column=0, pady=10, columnspan=2)
results_scroll = Scrollbar(app, command=results.yview)
results_scroll.grid(row=8, column=2, sticky='ns')

app.mainloop()
