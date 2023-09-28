# Image Quality Index and Pixels Histogram Tool

This is a Python application for calculating the quality index of images using a combination of noise and intensity ratios.

## Prerequisites

Before running the application, make sure you have the following libraries installed:

- tkinter
- numpy
- pandas
- matplotlib
- opencv-python
- Pillow (PIL)

You can install these libraries using pip:

```bash
pip install tkinter numpy pandas matplotlib opencv-python Pillow
```

## Usage

1. Run the script using the following command:

```bash
python your_script_name.py
```

2. Click the "Select Images" button to choose one or more images for quality analysis.

3. Set the "Noise Percentile" and "Good/Bad QI Threshold" values as needed.

4. Click the "Calculate Quality" button to analyze the selected images.

## Output

- The application will display the selected image alongside its grayscale histogram.
- The results will be shown in the GUI, including the image name, quality index, and image quality ("Good" or "Bad").

## Contributing

Contributions to this project are welcome. You can fork the repository and submit a pull request to propose changes or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The application uses various Python libraries to perform image quality analysis.
```
