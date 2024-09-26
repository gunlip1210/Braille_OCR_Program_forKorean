import cv2
import math
from collections import Counter

# misc functions

def find_minimum_diff(top_low, standard):
  result = []
  white_flag = False
  temp = 0
  for idx, val in enumerate(top_low):
      if white_flag:
          if val < standard:
              white_flag = False
              result.append((idx + temp) // 2)
      else:
          if val >= standard:
              white_flag = True
              temp = idx
  for i in range(len(result) - 1):
      result[i] = result[i+1] - result[i]
  del result[-1]
  return min(result)
def find_set_coordinate(averageContours, error, direction):
  # direction = 0 -> find vertical line
  # direction = 1 -> find horizontal line
  averageContours.sort(key = lambda x: x[direction])
  # print(averageContours)
  result = []

  temp = [averageContours[0][direction]]
  for i in range(1, len(averageContours)):
      if averageContours[i][direction] - averageContours[i-1][direction] <= error:
          temp.append(averageContours[i][direction])
      else:
          result.append(round(sum(temp)/len(temp)))
          temp.clear()
          temp.append(averageContours[i][direction])
  result.append(round(sum(temp)/len(temp)))
  temp.clear()
  return result

def fill_emptyVerticalLine(set_column, error):
    def find_standard(set_column, error):
        diff_column = []
        for i in range(len(set_column)-1):
            diff_column.append(set_column[i+1] - set_column[i])
        diff_column.sort()
        diff_temp = [diff_column[0]]
        diff_result = []
        for i in range(1, len(diff_column)):
            if diff_column[i] - diff_column[i-1] <= error:
                diff_temp.append(diff_column[i])
            else:
                diff_result.append(sum(diff_temp)/len(diff_temp))
                diff_temp.clear()
                diff_temp.append(diff_column[i])
        diff_result.append(sum(diff_temp)/len(diff_temp))
        return diff_result[:2]
    
    def find_empty_ends(set_column, standard):
        empty_start = False
        empty_end = False
        if abs(standard[0] - set_column[1] + set_column[0]) > abs(standard[1] - set_column[1] + set_column[0]):
            empty_start = True
        if abs(standard[0] - set_column[-1] + set_column[-2]) > abs(standard[1] - set_column[-1] + set_column[-2]):
            empty_end = True
        return tuple([empty_start, empty_end])
    
    def fill_column(set_column, standard, empty_ends):
        result = []
        if empty_ends == (False, False):
            count = round((set_column[-1] - set_column[0] - standard[0]) / sum(standard))
            multiplier = (set_column[-1] - set_column[0] - standard[0]) / count / sum(standard)
            new_standard = (standard[0] * multiplier, standard[1] * multiplier)
            result.append(set_column[0])
            result.append(round(set_column[0] + new_standard[0]))
            for i in range(count):
                result.append(round(result[0] + sum(new_standard)*(i+1)))
                result.append(round(result[0] + sum(new_standard)*(i+1) + new_standard[0]))
        elif empty_ends == (True, False):
            count = round((set_column[-1] - set_column[0]) / sum(standard))
            multiplier = (set_column[-1] - set_column[0]) / count / sum(standard)
            new_standard = (standard[0] * multiplier, standard[1] * multiplier)
            result.append(round(set_column[0] - new_standard[0]))
            result.append(set_column[0])
            for i in range(count):
                result.append(round(result[1] + sum(new_standard)*(i) + new_standard[1]))
                result.append(round(result[1] + sum(new_standard)*(i+1)))
        elif empty_ends == (False, True):
            count = round((set_column[-1] - set_column[0]) / sum(standard))
            multiplier = (set_column[-1] - set_column[0]) / count / sum(standard)
            new_standard = (standard[0] * multiplier, standard[1] * multiplier)
            result.append(set_column[0])
            result.append(round(set_column[0] + new_standard[0]))
            for i in range(count):
                result.append(round(result[0] + sum(new_standard)*(i+1)))
                result.append(round(result[0] + sum(new_standard)*(i+1) + new_standard[0]))
        else:
            count = round((set_column[-1] - set_column[0] - standard[1]) / sum(standard))
            multiplier = (set_column[-1] - set_column[0] - standard[1]) / count / sum(standard)
            new_standard = (standard[0] * multiplier, standard[1] * multiplier)
            result.append(round(set_column[0] - new_standard[0]))
            result.append(set_column[0])
            for i in range(count+1):
                result.append(round(result[1] + sum(new_standard)*(i) + new_standard[1]))
                result.append(round(result[1] + sum(new_standard)*(i+1)))
        return result
            

    
    standard = find_standard(set_column, error)
    # print(standard)
    empty_ends = find_empty_ends(set_column, standard)
    # print(empty_ends)
    # print(set_column)
    set_column = fill_column(set_column, standard, empty_ends)
    # print(set_column)
    return set_column

def calcCircleCoordinates(x0, y0, r):
  # calculate the pixels that must be scruntized per braille dot, given (x,y) and radius
    braille = []
    circle_eq = lambda x: math.sqrt((r)**2 - (x - x0)**2)
    for i in range(x0 - r, x0 + r + 1):
        for j in range(y0 - int(circle_eq(i)), y0 + int(circle_eq(i)) + 1):
            braille.append((i, j))
    return braille
def calcBrailleGrid(x, y):
  # formatting braille grid for ease of calculation 
  #  1 2 
  #  3 4
  #  5 6
    braille = []
    if len(x)%2 or len(y)%3:
        raise ValueError('wrong line exist')
    for i in range(len(y)//3):
        for j in range(len(x)//2):
            braille.extend([[x[j*2+0], y[i*3+0]],[x[j*2+1], y[i*3+0]],
                           [x[j*2+0], y[i*3+1]],[x[j*2+1], y[i*3+1]],
                           [x[j*2+0], y[i*3+2]],[x[j*2+1], y[i*3+2]]])
    return braille
def ch2Braille(braille):
  # used to calculate single braille to unicode value
    unicode = 10240
    for i in range(6):
        unicode += braille[i%3][i//3]*2**i
    return chr(unicode)
def ch2Brailles(brailles):
  # used to calculate mutliple braille characters by calling function above
    braille = ""
    for i in brailles:
        braille += ch2Braille(i)
    return braille

# main functions (in order)
def findContours (img):
  # receieve image and read 
  assert img is not None, "file could not be read, check with os.path.exists()"
  
  # need this process (images need to be in this version)
  # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  # calculate using basic contouring
  ret, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
  
  # findContour(source image, contour retrieval mode, contour approximation method)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # finding the diameter 
  boundingBoxes = [list(cv2.boundingRect(i)) for i in contours]
  column = Counter([i[2] for i in boundingBoxes])
  mode = column.most_common(1)[0][0]
  diam = mode if mode > 1 else column.most_common(2)[1][0]

  
  # find average of the contours and number of contours in one "approximated simple" contour
  averageContours = []
  for i in range(len(contours)):
    sum_x = 0
    sum_y = 0
    for j in range(len(contours[i])):
      sum_x += list(contours[i][j][0])[0]
      sum_y += list(contours[i][j][0])[1]
    averageContours.append([int(sum_x/len(contours[i])), int(sum_y/len(contours[i]))])
    
  # TEST
  img_clone = img.copy()
  # for i in averageContours:
  #   cv2.circle(img_clone, i, 5, (255,0,0), 3)
  # cv2.imshow("image", img_clone)
  # cv2.waitKey()
  
  return averageContours, diam

#-------------------------------------------------------------------------------------------------------------------------
def findContours_dfs(img, standard):
  dx = (1, -1, 0, 0)
  dy = (0, 0, 1, -1)
  result = []
  temp = []
  def dfs(x, y):
    for i in range(4):
      temp_x = x + dx[i]
      temp_y = y + dy[i]
      if 0 <= temp_x < len(map[0]) and 0 <= temp_y < len(map) and map[temp_y][temp_x] > standard:
        map[temp_y][temp_x] = 0
        temp.append((temp_x, temp_y))
        dfs(temp_x, temp_y)
    return
  
  def calc_result(temp):
    sum_x = 0
    sum_y = 0
    for i in temp:
      sum_x += i[0]
      sum_y += i[1]
    return (round(sum_x / len(temp)), round(sum_y / len(temp)))
      
  map = []
  for i in img:
    map.append(list(i))
  for i in range(len(map)):
     for j in range(len(map[0])):
        if map[i][j] > standard:
           map[i][j] = 0
           temp.append((j, i))
           dfs(j, i)
           result.append(calc_result(temp))
           temp.clear()
  
  return result
  
   

def findBrailleGrid (img, averageContours):
  # more accurately calculate error 
  top_row = img[min(averageContours, key= lambda x:x[1])[1]]
  mindiff = find_minimum_diff(top_row, 50)
  error = mindiff * (1/4)
  
  setColumn = find_set_coordinate(averageContours, error, 0)
  setRow = find_set_coordinate(averageContours, error, 1)
  
  
  # print(setColumn)
  # print(error)
  # calculate the hypothetical values where braille dots do not exist 
  setColumn = fill_emptyVerticalLine(setColumn, error/3)
  
  
  # TEST
  coordsFullMatrix = []
  for i in setColumn:
    for j in setRow:
      coordsFullMatrix.append([i, j])
      
  
  img_clone = img.copy()
  img_clone = cv2.cvtColor(img_clone, cv2.COLOR_GRAY2BGR)
  
  for i in setRow:
    cv2.line(img_clone, (0, i), (80000, i), (255,255, 0), 1)
  for i in setColumn:
    cv2.line(img_clone, (i, 0), (i, 800), (255,255,0), 1)
  for i in averageContours:
    cv2.circle(img_clone, i, 1, (0, 0, 255), 2)
  # for i in coordsFullMatrix:
  #   cv2.circle(img_clone, i, 5, (255, 0, 255), 1)  
  cv2.imshow("image", img_clone)
  cv2.waitKey()
  
  # tidy the array into multidimensional array -> one index holds information of 6 dots 
  coordsPerGrid = calcBrailleGrid(setColumn, setRow)
  return coordsPerGrid 

def readBraille(img, diam, brailleGrid):
  # the function to actually read the braille
  radius = diam//2
  temp = []
  
  for i in brailleGrid:
    # use circleCoordinates to calculate relative pixels that we need to check 
    checkCoords = calcCircleCoordinates(*i, radius)
    temp.append(False)
    for j in checkCoords:
      # if a single pixel is not black, then it is considered a "filled" braille cell 
      if(img[j[1]][j[0]] > 100):
        temp[-1] = True
        break
  
  # append proper information 
  braille = []
  for i in range(len(brailleGrid) // 6):
    braille.append([[temp[i*6 + 0], temp[i*6 + 1]], [temp[i*6 + 2], temp[i*6 + 3]], [temp[i*6 + 4], temp[i*6 + 5]]])
  
  # convert to braille with function 
  result = ch2Brailles(braille)
  resultList = list(result)
  
  # remove excess or redundant spacing 
  idxToRemove = []
  prevSpace = False
  for i in range(len(result)):
    if(result[i] == '⠀'):
      if(prevSpace == False):
        prevSpace = True
      else:
        idxToRemove.append(i)
    else:
      prevSpace = False
  idxToRemove = sorted(idxToRemove, reverse=True)
  for i in idxToRemove:
    resultList.pop(i)
  
  result = "".join(resultList)
  return result

def main(img):
    # when column = contours, ac = averageContours, d = diameter
    ac, d = findContours(img)
    ac = findContours_dfs(img, 100)
    brailleGrid = findBrailleGrid(img, ac)
    string = readBraille(img, d, brailleGrid)
    return string