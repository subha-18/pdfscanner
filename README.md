# pdfscanner

This Pdf scanner is made using ip webcam and few  image processing techniques. Technology Stack used: Python, openCV, numPy, PIL.
Features of pdf scanner:
1. Connected the phone camera with the laptop using python.
2. Used black and white conversion (if the image is normal and readable)
3. Used adaptive threshoding(if the image is unclear and not readable)
Additional features added:
1.DOCUMENT DETECTION using Canny Edge Detector, Gaussian Blur, Adaptive Thresholding (by finding the Largest contoured area and drawing it using drawCounter)
2.CROPPING the image by clicking 4 points using capturing mouse click method , Warp perspective, numpy type float32 to get the points to crop
