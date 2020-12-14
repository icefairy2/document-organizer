import cv2
import numpy as np

from docscanner import utils


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_cv_frame(self):
        success, image = self.video.read()
        heightImg = 480
        widthImg = 640

        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
        thres = [80, 200]  # GET TRACK BAR VALUES FOR THRESHOLDS
        imgThreshold = cv2.Canny(imgBlur, thres[0], thres[1])  # APPLY CANNY BLUR
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

        ## FIND ALL COUNTOURS
        imgContours = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS

        # FIND THE BIGGEST COUNTOUR
        biggest, maxArea = utils.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            biggest = utils.reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
            imgBigContour = utils.drawRectangle(imgBigContour, biggest, 2)
            pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
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

            return imgAdaptiveThre
        else:
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
