import cv2
import numpy as np
import pytesseract as pytesseract
from docscanner.pyimagesearch import transform
from docscanner.pyimagesearch import imutils
from scipy.spatial import distance as dist
from matplotlib.patches import Polygon
import docscanner.polygon_interacter as poly_i
import matplotlib.pyplot as plt
import itertools
import math

from docscanner import utils


class VideoCamera(object):
    def __init__(self, interactive=False, MIN_QUAD_AREA_RATIO=0.25, MAX_QUAD_ANGLE_RANGE=40):

        self.video = cv2.VideoCapture(0)
        self.interactive = interactive
        self.MIN_QUAD_AREA_RATIO = MIN_QUAD_AREA_RATIO
        self.MAX_QUAD_ANGLE_RANGE = MAX_QUAD_ANGLE_RANGE

    def __del__(self):
        self.video.release()

    def filter_corners(self, corners, min_dist=20):
        """Filters corners that are within min_dist of others"""

        def predicate(representatives, corner):
            return all(dist.euclidean(representative, corner) >= min_dist
                       for representative in representatives)

        filtered_corners = []
        for c in corners:
            if predicate(filtered_corners, c):
                filtered_corners.append(c)
        return filtered_corners

    def angle_between_vectors_degrees(self, u, v):
        """Returns the angle between two vectors in degrees"""
        cos=np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        cos=np.clip(cos,-1,1)
        rad = np.arccos(cos)
        return np.degrees(rad)

    def get_angle(self, p1, p2, p3):
        """
        Returns the angle between the line segment from p2 to p1
        and the line segment from p2 to p3 in degrees
        """
        a = np.radians(np.array(p1))
        b = np.radians(np.array(p2))
        c = np.radians(np.array(p3))

        avec = a - b
        cvec = c - b


        return self.angle_between_vectors_degrees(avec, cvec)

    def angle_range(self, quad):
        """
        Returns the range between max and min interior angles of quadrilateral.
        The input quadrilateral must be a numpy array with vertices ordered clockwise
        starting with the top left vertex.
        """
        tl, tr, br, bl = quad
        ura = self.get_angle(tl[0], tr[0], br[0])
        ula = self.get_angle(bl[0], tl[0], tr[0])
        lra = self.get_angle(tr[0], br[0], bl[0])
        lla = self.get_angle(br[0], bl[0], tl[0])

        angles = [ura, ula, lra, lla]
        return np.ptp(angles)

    def get_corners(self, img):
        # cv2.imshow('get corners', img)
        # cv2.waitKey(0)
        #lsd = cv2.createLineSegmentDetector()
        lsd = cv2.ximgproc.createFastLineDetector()
        # print(lsd)
        lines = lsd.detect(img)
        #print(lines)
        result_img = lsd.drawSegments(img, lines)
        # cv2.imshow('draw segmn', result_img)
        # cv2.waitKey(0)
        # massages the output from LSD
        # LSD operates on edges. One "line" has 2 edges, and so we need to combine the edges back into lines
        # 1. separate out the lines into horizontal and vertical lines.
        # 2. Draw the horizontal lines back onto a canvas, but slightly thicker and longer.
        # 3. Run connected-components on the new canvas
        # 4. Get the bounding box for each component, and the bounding box is final line.
        # 5. The ends of each line is a corner
        # 6. Repeat for vertical lines
        # 7. Draw all the final lines onto another canvas. Where the lines overlap are also corners

        corners = []
        if lines is not None:
            # separate out the horizontal and vertical lines, and draw them back onto separate canvases
            lines = lines.squeeze().astype(np.int32).tolist()
            #print("Lines squeeze ", lines)
            horizontal_lines_canvas = np.zeros(img.shape, dtype=np.uint8)
            vertical_lines_canvas = np.zeros(img.shape, dtype=np.uint8)
            for line in lines:
                #print("line ", line)
                x1, y1, x2, y2 = line
                if abs(x2 - x1) > abs(y2 - y1):
                    (x1, y1), (x2, y2) = sorted(((x1, y1), (x2, y2)), key=lambda pt: pt[0])
                    cv2.line(horizontal_lines_canvas, (max(x1 - 5, 0), y1), (min(x2 + 5, img.shape[1] - 1), y2), 255, 2)
                else:
                    (x1, y1), (x2, y2) = sorted(((x1, y1), (x2, y2)), key=lambda pt: pt[1])
                    cv2.line(vertical_lines_canvas, (x1, max(y1 - 5, 0)), (x2, min(y2 + 5, img.shape[0] - 1)), 255, 2)

            lines = []

            # find the horizontal lines (connected-components -> bounding boxes -> final lines)
            contours = cv2.findContours(horizontal_lines_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[1]
            #print("contur", contours)
            #contours = sorted(contours, key=lambda c: cv2.arcLength(c, True), reverse=True)[:2]
            horizontal_lines_canvas = np.zeros(img.shape, dtype=np.uint8)
            for contour in contours:
                contour = contour.reshape((contour.shape[0], contour.shape[1]))
                min_x = np.amin(contour[:, 0], axis=0) + 2
                max_x = np.amax(contour[:, 0], axis=0) - 2
                left_y = int(np.average(contour[contour[:, 0] == min_x][:, 1]))
                right_y = int(np.average(contour[contour[:, 0] == max_x][:, 1]))
                lines.append((min_x, left_y, max_x, right_y))
                cv2.line(horizontal_lines_canvas, (min_x, left_y), (max_x, right_y), 1, 1)
                corners.append((min_x, left_y))
                corners.append((max_x, right_y))

            # find the vertical lines (connected-components -> bounding boxes -> final lines)
            contours = cv2.findContours(vertical_lines_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[1]
            #contours = sorted(contours, key=lambda c: cv2.arcLength(c, True), reverse=True)[:2]
            vertical_lines_canvas = np.zeros(img.shape, dtype=np.uint8)
            for contour in contours:
                contour = contour.reshape((contour.shape[0], contour.shape[1]))
                min_y = np.amin(contour[:, 1], axis=0) + 2
                max_y = np.amax(contour[:, 1], axis=0) - 2
                top_x = int(np.average(contour[contour[:, 1] == min_y][:, 0]))
                bottom_x = int(np.average(contour[contour[:, 1] == max_y][:, 0]))
                lines.append((top_x, min_y, bottom_x, max_y))
                cv2.line(vertical_lines_canvas, (top_x, min_y), (bottom_x, max_y), 1, 1)
                corners.append((top_x, min_y))
                corners.append((bottom_x, max_y))

            # find the corners
            corners_y, corners_x = np.where(horizontal_lines_canvas + vertical_lines_canvas == 2)
            corners += zip(corners_x, corners_y)

        # remove corners in close proximity
        corners = self.filter_corners(corners)

        return corners

    def is_valid_contour(self, cnt, IM_WIDTH, IM_HEIGHT):
        """Returns True if the contour satisfies all requirements set at instantitation"""

        return (len(cnt) == 4 and cv2.contourArea(cnt) > IM_WIDTH * IM_HEIGHT * self.MIN_QUAD_AREA_RATIO
                and self.angle_range(cnt) < self.MAX_QUAD_ANGLE_RANGE)

    def get_contour(self, rescaled_image):
        MORPH = 9
        CANNY = 84
        HOUGH = 25

        IM_HEIGHT, IM_WIDTH, _ = rescaled_image.shape

        # convert the image to grayscale and blur it slightly
        imgGray = cv2.cvtColor(rescaled_image, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)  # ADD GAUSSIAN BLUR

        # dilate helps to remove potential holes between edge segments
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
        imgDilated = cv2.dilate(imgBlur, kernel)
        # cv2.imshow('dilated', imgDilated)
        # cv2.waitKey(0)
        # find edges and mark them in the output map using the Canny algorithm
        edged = cv2.Canny(imgDilated, 0, CANNY)
        # cv2.imshow('canny', edged)
        # cv2.waitKey(0)
        test_corners = self.get_corners(edged)
        print("test_corners", test_corners)
        approx_contours = []

        if len(test_corners) >= 4:
            quads = []
            for quad in itertools.combinations(test_corners, 4):
                points = np.array(quad)
                points = transform.order_points(points)
                points = np.array([[p] for p in points], dtype="int32")
                quads.append(points)

                # get top five quadrilaterals by area
            quads = sorted(quads, key=cv2.contourArea, reverse=True)[:5]
            # sort candidate quadrilaterals by their angle range, which helps remove outliers
            quads = sorted(quads, key=self.angle_range)

            approx = quads[0]
            if self.is_valid_contour(approx, IM_WIDTH, IM_HEIGHT):
                approx_contours.append(approx)

            #for debugging: uncomment the code below to draw the corners and countour found
            #by get_corners() and overlay it on the image

            # cv2.drawContours(rescaled_image, [approx], -1, (20, 20, 255), 2)
            # plt.scatter(*zip(*test_corners))
            # plt.imshow(rescaled_image)
            # plt.show()

            #also attempt to find contours directly from the edged image, which occasionally
            #produces better results

        (cnts, hierarchy) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours
        for c in cnts:
            # approximate the contour
            approx = cv2.approxPolyDP(c, 80, True)
            if self.is_valid_contour(approx, IM_WIDTH, IM_HEIGHT):
                approx_contours.append(approx)
                break

        # If we did not find any valid contours, just use the whole image
        if not approx_contours:
            TOP_RIGHT = (IM_WIDTH, 0)
            BOTTOM_RIGHT = (IM_WIDTH, IM_HEIGHT)
            BOTTOM_LEFT = (0, IM_HEIGHT)
            TOP_LEFT = (0, 0)
            screenCnt = np.array([[TOP_RIGHT], [BOTTOM_RIGHT], [BOTTOM_LEFT], [TOP_LEFT]])

        else:
            screenCnt = max(approx_contours, key=cv2.contourArea)

        return screenCnt.reshape(4, 2)

    def interactive_get_contour(self, screenCnt, rescaled_image):
        poly = Polygon(screenCnt, animated=True, fill=False, color="yellow", linewidth=5)
        fig, ax = plt.subplots()
        ax.add_patch(poly)
        ax.set_title(('Drag the corners of the box to the corners of the document. \n'
                      'Close the window when finished.'))
        p = poly_i.PolygonInteractor(ax, poly)
        plt.imshow(rescaled_image)
        plt.show()

        new_points = p.get_poly_points()[:4]
        new_points = np.array([[p] for p in new_points], dtype="int32")
        return new_points.reshape(4, 2)

    def get_text(self, img_cv):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        print(pytesseract.image_to_string(img_rgb))

    def get_cv_frame(self):
        success, image = self.video.read()

        heightImg = 480
        widthImg = 640
        RESCALED_HEIGHT = 500.0
        ratio = image.shape[0] / RESCALED_HEIGHT
        orig = image.copy()
        rescaled_image = imutils.resize(image, height=int(RESCALED_HEIGHT))
        # cv2.imshow('rescaled', rescaled_image)
        # cv2.waitKey(0)
        # get the document contour
        screenCnt = self.get_contour(rescaled_image)

        if self.interactive:
            screenCnt = self.interactive_get_contour(screenCnt, rescaled_image)

        # apply perspective transformation
        warped = transform.four_point_transform(orig, screenCnt * ratio)

        # convert warped img to grayscale
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        # sharpen img
        sharpen = cv2.GaussianBlur(gray, (0, 0), 3)  # (0, 0), 3)
        # cv2.imshow('sharpen', sharpen)
        # cv2.waitKey(0)
        sharpen = cv2.addWeighted(gray, 2.5, sharpen, -0.5, 0)
        # cv2.imshow('sharpen', gray)
        # cv2.waitKey(0)

        # apply adaptive thrs to get black and white effect
        thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21,
                                       15)  # initially 21, 15
        self.get_text(thresh)
        # return the transformed img
        return thresh

        # thres = utils.valTrackbars()  # GET TRACK BAR VALUES FOR THRESHOLDS
        # imgThreshold = cv2.Canny(imgBlur, thres[0], thres[1])  # APPLY CANNY BLUR
        # kernel = np.ones((5, 5))
        # imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
        # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
        #
        # ## FIND ALL COUNTOURS
        # imgContours = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        # imgBigContour = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        # contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,
        #                                        cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
        # cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS
        #
        # # FIND THE BIGGEST COUNTOUR
        # biggest, maxArea = utils.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
        # if biggest.size != 0:
        #     biggest = utils.reorder(biggest)
        #     cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
        #     imgBigContour = utils.drawRectangle(imgBigContour, biggest, 2)
        #     pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
        #     pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
        #     matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #     imgWarpColored = cv2.warpPerspective(image, matrix, (widthImg, heightImg))
        #
        #     # REMOVE 20 PIXELS FORM EACH SIDE
        #     imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        #     imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))
        #
        #     # APPLY ADAPTIVE THRESHOLD
        #     imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        #     imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        #     imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        #     imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)
        #
        #     # Image Array for Display
        #     imageArray = ([image, imgGray, imgThreshold, imgContours],
        #                   [imgBigContour, imgWarpColored, imgWarpGray, imgAdaptiveThre])
        #
        #     return imgAdaptiveThre
        # else:
        #     return imgContours

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
