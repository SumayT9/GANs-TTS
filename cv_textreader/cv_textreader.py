# # Import required packages
# import cv2
# import pytesseract

# # Mention the installed location of Tesseract-OCR in your system
# pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# # Read image from which text needs to be extracted
# img = cv2.imread("picture.jpg")

# # Preprocessing the image starts

# # Convert the image to gray scale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Performing OTSU threshold
# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# # Specify structure shape and kernel size.
# # Kernel size increases or decreases the area
# # of the rectangle to be detected.
# # A smaller value like (10, 10) will detect
# # each word instead of a sentence.
# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# # Appplying dilation on the threshold image
# dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# # Finding contours
# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
# 												cv2.CHAIN_APPROX_NONE)

# # Creating a copy of image
# im2 = img.copy()

# # A text file is created and flushed
# file = open("recognized.txt", "w+")
# file.write("")
# file.close()

# # Looping through the identified contours
# # Then rectangular part is cropped and passed on
# # to pytesseract for extracting text from it
# # Extracted text is then written into the text file
# for cnt in contours:
# 	x, y, w, h = cv2.boundingRect(cnt)

# 	# Drawing a rectangle on copied image
# 	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 	# Cropping the text block for giving input to OCR
# 	cropped = im2[y:y + h, x:x + w]

# 	# Open the file in append mode
# 	file = open("recognized.txt", "a")

# 	# Apply OCR on the cropped image
# 	text = pytesseract.image_to_string(cropped)

# 	# Appending the text into file
# 	file.write(text)
# 	file.write("\n")

# 	# Close the file
# 	file.close


import cv2
import sys
import os
import pytesseract
import page_dewarp

SCALE = 4
AREA_THRESHOLD = 0


def show_scaled(name, img):
    try:
        h, w = img.shape
    except ValueError:
        h, w, _ = img.shape
    cv2.imshow(name, cv2.resize(img, (w // SCALE, h // SCALE)))


def main():
    img = cv2.imread("data/gov_2.jpeg")
    # img = cv2.imread("test2.jpg")
    #img = img[10:-10, 10:-10]  # remove the border, it confuses contour detection
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) blocked for page_dewarp test
    # show_scaled("original", gray)

    # black and white, and inverted, because
    # white pixels are treated as objects in
    # contour detection
    '''thresholded = cv2.adaptiveThreshold(    #commented out for page_dewarp which already thresholds
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
        25,
        15
    )'''
    # show_scaled('thresholded', thresholded)
    # I use a kernel that is wide enough to connect characters
    # but not text blocks, and tall enough to connect lines.
    img_thresholded = page_dewarp.main(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 33))
    closing = cv2.morphologyEx(img_thresholded, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # show_scaled("closing", closing)

    for contour in contours:
        print('contour')
        convex_contour = cv2.convexHull(contour)
        area = cv2.contourArea(convex_contour)
        if area > AREA_THRESHOLD:
            cv2.drawContours(img_thresholded, [convex_contour], -1, (255, 0, 0), 3)
            x, y, w, h = cv2.boundingRect(contour)

            # 	# Drawing a rectangle on copied image
            rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 	# Cropping the text block for giving input to OCR
            cropped = img_thresholded[y:y + h, x:x + w]
            file = open("recognized.txt", "a")

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)

            # Appending the text into file
            file.write(text)
            file.write("\n")

            # Close the file
            file.close

        # show_scaled("contours", img)
    cv2.imwrite("contours.png", img_thresholded)


if __name__ == '__main__':
    main()
