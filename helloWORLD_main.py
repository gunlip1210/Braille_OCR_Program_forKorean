# init
import glob
import os

import cv2
import numpy
import read_braille
from pathlib import Path
import braille2hangul_new as braille2hangul

try:
    from google.colab.patches import cv2_imshow
    exeAtColab = True
    print("This program is not for google colab")
    exit()
except:
   exeAtColab = False

# class
class openCV():
    def cut(image):
        # cut a single image by user mouse input
        line_tmp = [(0, 0), (0, 0)]
        lines = []
        flags = {"lButton": False}

        def calc_tangent(line):
            # calculate tanget between two points
            if line[0][0] == line[1][0]:
                return "inf"
            else:
                return (line[1][1]-line[0][1]) / (line[1][0]-line[0][0])
            
        def check_tangent(line):  
            # return True: vertical, False: horizontal
            tmp = calc_tangent(line)
            if tmp == "inf" or abs(tmp) >= 1:
                return True
            else:
                return False

        def calc_intersection(line1, line2):
            # calculate coordinate of two line intersecting points 
            a1 = calc_tangent(line1)
            a2 = calc_tangent(line2)
            # if a1 == "inf" and a2 == "inf":
            #     if line2[0][0] == 0:
            #         return (line1[0][0], line2[0][1])
            #     else:
            #         return (line1[0][0], line2[1][1])
            #     raise ValueError("parallel")
            if a1 == "inf":
                b2 = -a2*line2[0][0] + line2[0][1]
                return (line1[0][0], round(a2*line1[0][0] + b2))
            elif a2 == "inf":
                b1 = -a1*line1[0][0] + line1[0][1]
                return (line2[0][0], round(a1*line2[0][0] + b1))
            else:
                b1 = -a1*line1[0][0] + line1[0][1]
                b2 = -a2*line2[0][0] + line2[0][1]
                x = (b2 - b1) / (a1 - a2)
                return (round(x), round(a1*x + b1))
        
        def draw_line(image, sideline=False):
            # draw line on image
            if check_tangent(line_tmp):  # vertical line
                start_point = calc_intersection(line_tmp, [(0, 0), (image.shape[1], 0)])
                end_point = calc_intersection(line_tmp, [(0, image.shape[0]), image.shape[1::-1]])
                cv2.line(image, start_point, end_point, (0, 0, 255), 1)
                if sideline:
                    #cv2.line(image, (start_point[0]-10, start_point[1]), (end_point[0]-10, end_point[1]), (100, 100, 255), 1)
                    cv2.line(image, (start_point[0]-25, start_point[1]), (end_point[0]-25, end_point[1]), (100, 100, 255), 1)
                    #cv2.line(image, (start_point[0]+10, start_point[1]), (end_point[0]+10, end_point[1]), (100, 100, 255), 1)
                    cv2.line(image, (start_point[0]+25, start_point[1]), (end_point[0]+25, end_point[1]), (100, 100, 255), 1)
            else:  # horizontal line
                start_point = calc_intersection(line_tmp, [(0, 0), (0, image.shape[0])])
                end_point = calc_intersection(line_tmp, [(image.shape[1], 0), image.shape[1::-1]])
                cv2.line(image, start_point, end_point, (0, 0, 255), 1)
                if sideline:
                    #cv2.line(image, (start_point[0], start_point[1]-10), (end_point[0], end_point[1]-10), (100, 100, 255), 1)
                    cv2.line(image, (start_point[0], start_point[1]-25), (end_point[0], end_point[1]-25), (100, 100, 255), 1)
                    #cv2.line(image, (start_point[0], start_point[1]+!0), (end_point[0], end_point[1]+10), (100, 100, 255), 1)
                    cv2.line(image, (start_point[0], start_point[1]+25), (end_point[0], end_point[1]+25), (100, 100, 255), 1)
            return (start_point, end_point)
            
        def sort_lines():
            # sort lines clockwise from 12 o'clock
            flags = [check_tangent(l) for l in lines]
            horizontal_line = []
            vertical_line = []
            for idx, flag in enumerate(flags):
                if flag:
                    vertical_line.append(lines[idx])
                else:
                    horizontal_line.append(lines[idx])
            if (horizontal_line[0][0][1] + horizontal_line[0][1][1]) < (horizontal_line[1][0][1] + horizontal_line[1][1][1]):
                horizontal_line.reverse()
            if (vertical_line[0][0][0] + vertical_line[0][1][0]) > (vertical_line[1][0][0] + vertical_line[1][1][0]):
                vertical_line.reverse()
            for i in range(4):
                if i%2 == 0:
                    lines[i] = horizontal_line.pop()
                else:
                    lines[i] = vertical_line.pop()

        def affin_transform():
            # edit a image by affin transform
            intersection_points = []
            for i in range(4):
                intersection_points.append(calc_intersection(lines[i], lines[i-1]))
            width = max(abs(intersection_points[0][0]-intersection_points[1][0]), abs(intersection_points[2][0]-intersection_points[3][0]))
            height = max(abs(intersection_points[1][1]-intersection_points[2][1]), abs(intersection_points[3][1]-intersection_points[0][1]))
            intersection_points = numpy.array(intersection_points, dtype=numpy.float32)
            cut_points = numpy.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype=numpy.float32)
            transform_mtrx = cv2.getPerspectiveTransform(intersection_points, cut_points)
            image_origin[0] = cv2.warpPerspective(image_origin[0], transform_mtrx, (width, height))
            
        def onMouse(event, x, y, flag, param):
            # Callback function of 'setMouseCallback()' function
            if flag == cv2. EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
                if len(lines) == 0:
                    image_draw[0] = image_origin[0].copy()
                image_draw_tmp = image_draw[0].copy()
                line_tmp[1] = (x, y)
                cv2.circle(image_draw_tmp, line_tmp[0], 2, (0, 0, 255))
                draw_line(image_draw_tmp, sideline = True)
                cv2.imshow("CUT", image_draw_tmp)
            elif event == cv2.EVENT_LBUTTONDOWN:
                flags["lButton"] = True
                line_tmp[0] = (x, y)
            elif event == cv2.EVENT_RBUTTONDOWN and flags["lButton"]:
                flags["lButton"] = False
                tmp = draw_line(image_draw[0])
                lines.append(tmp)
                if len(lines) == 4:
                    sort_lines()
                    affin_transform()
                    lines.clear()
                    cv2.imshow("CUT", image_origin[0])

        # edit_cutting
        image_origin = [image.copy()]
        image_draw = [0]
        cv2.namedWindow("CUT")
        cv2.moveWindow("CUT", 0, 0)
        cv2.setMouseCallback("CUT", onMouse)
        cv2.imshow("CUT", image_origin[0])
        while True:
            tmp = cv2.waitKey(0)
            if tmp == 13:
                break
            elif tmp == 27:
                exit()
        return image_origin[0]
        
    def edit_cutting(self):
        # call 'cut()' method about 'self.images'
        for idx, image in enumerate(self.images):
            self.images[idx] = openCV.cut(image.copy())

    def read_brailles(self):
        self.strings = []
        for image in self.images:
            self.strings.append(read_braille.main(image))
        print("\n".join(self.strings))

    def hangul(self):
        self.hanguls = []
        for b in self.strings:
            self.hanguls.append(braille2hangul.ch2hangul(b))
    
    def print_result(self):
        for i in range(len(self.strings)):
            print("-> ", self.hanguls[i], sep='', end="\n\n")
        
    def __init__(self, dirPath, filenameExtension=".jpg"):
        # assign dirPath at self.dirPath without filename extension
        if '*' in dirPath:
            self.dirPath = dirPath[:dirPath.rindex('*')]
        else:
            self.dirPath = dirPath
        self.dirPath = self.dirPath.rstrip('/')

        # assign image file names at self.imagesNames with filename extension
        try:
            self.imageNames = [imagePath[imagePath.replace('\\', '/').rindex('/') + 1:] for imagePath in glob.glob(self.dirPath + "/*" + filenameExtension)]
        except:
            raise ValueError("Invalid directory path")
        if len(self.imageNames) == 0:
            raise ValueError("Empty directory")

        # read images at self.images list
        self.images = [cv2.imread(self.dirPath + '/' + imageName) for imageName in self.imageNames]

    def show(self, print_image_name=False):
        # print image
        for i in range(len(self.imageNames)):
            if print_image_name:
                print('<' + self.imageNames[i] + ">  at '" + self.dirPath + "'")
            if exeAtColab:
                cv2_imshow(self.images[i])
            else:
                cv2.imshow('<' + self.imageNames[i] + ">  at '" + self.dirPath + "'", self.images[i])
                while True:
                    tmp = cv2.waitKey(0)
                    if tmp == 13:
                        break
                    elif tmp == 27:
                        exit()
                cv2.destroyWindow('<' + self.imageNames[i] + ">  at '" + self.dirPath + "'")

    def save(self, saveAtNewDir=True, newDirPath=None, fileNamePrefix='', fileNamePostfix=''):
        if saveAtNewDir:
            if newDirPath is None:
                newDirPath = self.dirPath + "_result"
            mkdir(newDirPath)
        else:
            newDirPath = self.dirPath
        for i in range(len(self.imageNames)):
            cv2.imwrite(newDirPath + '/' + fileNamePrefix + self.imageNames[i][:self.imageNames[i].rindex('.')]
                        + fileNamePostfix + self.imageNames[i][self.imageNames[i].rindex('.'):], self.images[i])

    def ch2gray(self):
        self.images = [cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in self.images]

    def ch2binary(self, thresh):
        images_tmp = []
        for image in self.images:
            ret, image_binary = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
            images_tmp.append(image_binary)
        self.images = images_tmp

    def ch2binary_TOZERO(self, thresh):
        images_tmp = []
        for image in self.images:
            ret, image_binary = cv2.threshold(image, thresh, 255, cv2.THRESH_TOZERO)
            images_tmp.append(image_binary)
        self.images = images_tmp

    def ch2binary_mean(self, blockSize, C):
        self.images = [cv2.multiply(cv2.adaptiveThreshold(image, 1, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C), image) for image in self.images]

    def ch2binary_gaussian(self, blockSize, C):
        self.images = [cv2.adaptiveThreshold(image, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C) for image in self.images]

    def resize(self, size):
        images_tmp = []
        for image in self.images:
            tmpSize = image.shape
            tmpSize = tmpSize[0:2]
            times = size / max(tmpSize)
            if times > 1:
                images_tmp.append(cv2.resize(image, dsize=(0, 0), fx=times, fy=times, interpolation=cv2.INTER_LANCZOS4))
            elif times < 1:
                images_tmp.append(cv2.resize(image, dsize=(0, 0), fx=times, fy=times, interpolation=cv2.INTER_AREA))
            else:
                images_tmp.append(image)
        self.images = images_tmp

    def resize_absolute(self, Xsize, Ysize):
        self.images = [cv2.resize(image, dsize=(Xsize, Ysize), interpolation=cv2.INTER_LINEAR) for image in self.images]

    def resize_relative(self, times):
        if times > 1:
            self.images = [cv2.resize(image, dsize=(0, 0), fx=times, fy=times, interpolation=cv2.INTER_LANCZOS4) for image in self.images]
        elif times < 1:
            self.images = [cv2.resize(image, dsize=(0, 0), fx=times, fy=times, interpolation=cv2.INTER_AREA) for image in self.images]


# function
def mkdir(mkdirPath):
    # if mkdirPath is not exist, make mkdirPath directory
    try:
        if not os.path.exists(mkdirPath):
            os.makedirs(mkdirPath)
    except:
        raise OSError("Failed to make a new directory")

def rmfile(rmfilePath):
    # if rmfile is exist, remove rmfilePath file
    try:
        if os.path.isfile(rmfilePath):
            os.remove(rmfilePath)
    except:
        raise OSError("Failed to remove file")

def rmdir(rmdirPath, rmOption_force=False):
    # if rmdir is exist and is empty, remove rmdirPath directory
    try:
        if os.path.isdir(rmdirPath):
            os.rmdir(rmdirPath)
    except:
        raise OSError("Failed to remove directory")


# main
def main(DIR_PATH = None):
    # 이미지 저장된 폴더 경로
    if DIR_PATH == None:
        temp = os.path.abspath(__file__).replace('\\', '/')
        DIR_PATH = temp[:temp.rindex('/')] + "/images_sample"
    # CHANGE DIRECTORY PATH
    images = openCV(DIR_PATH)

#    images.resize(1000)
    images.resize(1000)
    images.edit_cutting()
    
    images.ch2gray()
    images.ch2binary_mean(35, -15)
    images.resize_relative(0.5)
    images.ch2binary_TOZERO(200)
    images.resize_relative(2)
    images.resize_relative(0.5)
    images.ch2binary(208)
    images.resize_relative(3)

    # for checking image
    # images.show()

    images.read_brailles()
    images.hangul()
    images.print_result()
    print("잘못된 점자가 있다면 다음 링크에 접속하여 알려주세요!")
    print("https://forms.gle/mujnsSb8JxSwyThD8")
    # images.edit_cutting()
    # images.save()
    # images.show()

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            print("Can not read braille. Try again!")
            cv2.destroyAllWindows()
            continue
        break