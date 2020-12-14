import cv2
import numpy as np
from docscanner import utils
from scipy.spatial import distance as dist
import itertools
import pytesseract as pytesseract
import imutils
from .pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_text(self, img_cv):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        # print(pytesseract.image_to_string(img_rgb))

    def get_cv_frame(self):
        success, image = self.video.read()
        heightImg = 480
        widthImg = 640
        orig = image.copy()
        RESCALED_HEIGHT = 500.0
        ratio = image.shape[0] / RESCALED_HEIGHT
        rescaled_image = utils.resize(image, height=int(RESCALED_HEIGHT))

        # warped = transform.four_point_transform(orig, screenCnt * ratio)

        imgGray = cv2.cvtColor(rescaled_image, cv2.COLOR_BGR2GRAY)

        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)  # ADD GAUSSIAN BLUR
        imgThreshold = cv2.Canny(imgBlur, 0, 90)

        thres = utils.valTrackbars()  # GET TRACK BAR VALUES FOR THRESHOLDS
        # imgThreshold = cv2.Canny(imgDilated, 0, 90)  # APPLY CANNY BLUR
        kernel = np.ones((5, 5))

        # imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
        # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

        # print("STEP 1: Edge Detection")
        # cv2.imshow("Image", image)
        # cv2.imshow("Edged", imgThreshold)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # FIND ALL COUNTOURS
        imgContours = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
        # cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(imgThreshold.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = []

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break
        # show the contour (outline) of the piece of paper
        # print("STEP 2: Find contours of paper")
        # cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        # cv2.imshow("Outline", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #
        # apply the four point transform to obtain a top-down
        # view of the original image
        if screenCnt != []:
            warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
            # convert the warped image to grayscale, then threshold it
            # to give it that 'black and white' paper effect
            warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            T = threshold_local(warped, 11, offset=10, method="gaussian")
            warped = (warped > T).astype("uint8") * 255
            # show the original and scanned images
            # print("STEP 3: Apply perspective transform")
            # cv2.imshow("Original", imutils.resize(orig, height=650))
            # cv2.imshow("Scanned", imutils.resize(warped, height=650))
            # cv2.waitKey(0)
            final_img = imutils.resize(warped, height=650)
            self.get_text(final_img)
            return final_img
        else:
            # FIND THE BIGGEST COUNTOUR
            biggest, maxArea = utils.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
            if biggest.size != 0:
                biggest = utils.reorder(biggest)
                cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
                imgBigContour = utils.drawRectangle(imgBigContour, biggest, 2)
                cv2.imshow("big cont", imgBigContour)
                cv2.waitKey(0)

                pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
                pts2 = np.float32(
                    [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                imgWarpColored = cv2.warpPerspective(image, matrix, (widthImg, heightImg))

                # REMOVE 20 PIXELS FORM EACH SIDE
                imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
                imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))

                # APPLY ADAPTIVE THRESHOLD
                imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
                imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
                imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
                imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

                # Image Array for Display
                imageArray = ([image, imgGray, imgThreshold, imgContours],
                              [imgBigContour, imgWarpColored, imgWarpGray, imgAdaptiveThre])
                self.get_text(imgAdaptiveThre)
                return imgAdaptiveThre
            else:
                self.get_text(imgContours)
                return imgContours

        # # LABELS FOR DISPLAY
        # labels = [["Original", "Gray", "Threshold", "Contours"],
        #           ["Biggest Contour", "Warp Prespective", "Warp Gray", "Adaptive Threshold"]]

        # # SAVE IMAGE WHEN 's' key is pressed
        # if cv2.waitKey(1) & 0xFF == ord('s'):
        #     cv2.imwrite("Scanned/myImage" + str(count) + ".jpg", imgWarpColored)
        #     cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
        #                   (1100, 350), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(stackedImage, "Scan Saved",
        #                 (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
        #                 cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        #     cv2.imshow('Result', stackedImage)
        #     cv2.waitKey(300)
        #     count += 1

# MORPH = 9
#         # dilate helps to remove potential holes between edge segments
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
#         imgDilated = cv2.dilate(imgBlur, kernel)
#         #
#         CANNY = 84
# find edges and mark them in the output map using the Canny algorithm
# edged = cv2.Canny(imgDilated, 0, CANNY)
#
# IM_HEIGHT, IM_WIDTH, _ = image.shape
# approx_contours = []
#
# (cnts, hierarchy) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
#
# # loop over the contours
# for c in cnts:
#     # approximate the contour
#     approx = cv2.approxPolyDP(c, 80, True)
#     if self.is_valid_contour(approx, IM_WIDTH, IM_HEIGHT):
#         approx_contours.append(approx)
#         break
#
# # If we did not find any valid contours, just use the whole image
# if not approx_contours:
#     TOP_RIGHT = (IM_WIDTH, 0)
#     BOTTOM_RIGHT = (IM_WIDTH, IM_HEIGHT)
#     BOTTOM_LEFT = (0, IM_HEIGHT)
#     TOP_LEFT = (0, 0)
#     screenCnt = np.array([[TOP_RIGHT], [BOTTOM_RIGHT], [BOTTOM_LEFT], [TOP_LEFT]])
# else:
#     screenCnt = max(approx_contours, key=cv2.contourArea)
#
# screenCnt = screenCnt.reshape(4, 2)
#
# # apply perspective transformation
# warped = transform.four_point_transform(orig, screenCnt * ratio)
# gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
#
# sharpen = cv2.GaussianBlur(gray, (0, 0), 3)
# sharpen = cv2.addWeighted(gray, 2.5, sharpen, -0.5, 0)
#
# thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 15)

# return thresh
