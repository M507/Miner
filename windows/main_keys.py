import psutil as psutil
import pytesseract
import subprocess
import os
import re
from PIL import Image
import win32gui
import win32ui
import numpy as np
import cv2
import pyautogui
import img_class
from random import randint
import win32api
import win32gui
import win32process
import wmi
import time


def enum_window_titles():
    def callback(handle, data):
        titles.append(win32gui.GetWindowText(handle))

    titles = []
    win32gui.EnumWindows(callback, None)
    return titles


def get_all_titles():
    titles = enum_window_titles()
    return [t for t in titles if len(t) > 1]


def get_setup_title(window_title="setup"):
    titles = get_all_titles()
    for title in titles:
        title_lower = title.lower()
        if window_title in title_lower:
            return title
    return None


def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        # if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        # print hwnd
        if found_pid == pid:
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def screenshot_by_pid(pid=None):
    if pid:
        hwnds = get_hwnds_for_pid(pid)
        print(hwnds)
        for hwnd in hwnds:
            print(hwnd)
            try:
                if hwnd:
                    win32gui.SetForegroundWindow(hwnd)
                    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
                    x, y = win32gui.ClientToScreen(hwnd, (x, y))
                    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
                    im = pyautogui.screenshot(region=(x, y, x1, y1))
                    if im is not None:
                        return im
                else:
                    print('Window not found!')
            except:
                print("Wrong handler 6733")
    else:
        print("No handler")
        im = pyautogui.screenshot()
        return im


def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        else:
            print('Window not found!')
    else:
        return None


def read_img(img_name):
    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Read image from which text needs to be extracted
    img = cv2.imread(img_name)

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()

    total_text = ""
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        total_text += pytesseract.image_to_string(cropped)

    return (total_text)


def create_another_version(return_list):
    img_name = return_list[0]
    img2 = Image.open(img_name)
    # Size of the image in pixels (size of orginal image)
    # (This is not mandatory)
    width, height = img2.size
    x = 0
    for i in range(x + 5, x + 25, 5):
        new_img_name = str(i) + '-' + img_name
        # Setting the points for cropped image
        left = 0
        top = i
        right = width
        bottom = height

        # crop
        im1 = img2.crop((left, top, right, bottom))

        # Shows the image in image viewer
        im1.save(new_img_name)
        return_list.append(new_img_name)
    return return_list


def create_imgs(img_name):
    # list_of_ImgOs = []
    img = cv2.imread(img_name)

    # Dimensions of the image
    sizeX = img.shape[1]
    sizeY = img.shape[0]
    nRows = 10
    mCols = 5

    print(img.shape)

    for nRows in range(10, 22, 1):
        for mCols in range(3, 8, 1):
            for i in range(0, nRows):
                for j in range(0, mCols):
                    roi = img[int(i * sizeY / nRows):int(i * sizeY / nRows + sizeY / nRows),
                          int(j * sizeX / mCols):int(j * sizeX / mCols + sizeX / mCols)]
                    image_name = f"imgs\\{img_name}_img_{nRows}_{mCols}_{i}_{j}.png"
                    cv2.imwrite(image_name, roi)

    # for starting_point_x in range(0,img.shape[0],5):
    #     for starting_point_y in range(0,img.shape[1],5):
    #         for r in range(starting_point_x,img.shape[0],x):
    #             for c in range(starting_point_y,img.shape[1],y):
    #                 point1 = [(starting_point_x+c),(starting_point_y+r)]
    #                 point2 = [c+y,r+x]
    #
    #                 #image_name = f"imgs\\img_{point1[0]}_{point1[1]}_{point2[0]}_{point2[1]}.png"
    #                 image_name = f"imgs\\img_{point1[0]}_{point1[1]}_{point2[0]}_{point2[1]}.png"
    #                 cv2.imwrite(image_name,img[r:r+x, c:c+y,:])
    #                 # Create an object and add it to the list.
    #                 #list_of_ImgOs.append(img_class.Img_Object(image_name, point1, point2, None))
    # #return list_of_ImgOs
    return None


def get_colors(img_name):
    """
    For a better efficiency.
    :return:
    """
    img = Image.open(img_name).convert("L")
    list_of_colors = Image.Image.getcolors(img)
    return list_of_colors


def execute_cmd(command):
    out = subprocess.Popen(command.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    return stdout


def go_to_image(image_name):
    try:
        if isinstance(image_name, str):
            try:
                pyautogui.click(image_name)
            except Exception as e:
                print("Error 97823 " + str(e))
        else:
            print("Error 62341")
    except Exception as e:
        print("Error 352264 " + str(e))


def isClickable(Img_Object):
    text = Img_Object.get_text()
    if "next" in text:
        Img_Object.set_priority_number(2)
    elif "i agree" in text:
        Img_Object.set_priority_number(3)
    elif "Ol accept t" in text:
        Img_Object.set_priority_number(3)
    elif "D1 accept t" in text:
        Img_Object.set_priority_number(3)
    elif "finish" in text:
        Img_Object.set_priority_number(1)
    else:
        return False
    return True


def remove_similar_images(Img_Object):
    pass


def isUnclickable(Img_Object):
    # Get the object's text
    text = Img_Object.get_text()
    if "not" in text:
        return True
    # Sometimes it reads "not" as "nat"
    if "nat" in text:
        return True
    if "pust" in text:
        return True
    if "hust" in text:
        return True
    if "cancel" in text:
        return True
    return False


# Shouldn't work
# def read_all_img(DIR):
#     pass
#     for filename in os.listdir(DIR):
#         filename = DIR + '\\' + filename
#                 # Read text
#         text =  read_img(filename)
#         # Clean the resulting text
#         text = re.sub(r'[^\x20-\x7F]+',' ', text).strip(' ').replace('\n','').replace('\t','').strip(' ')
#
#         # If short text then it's not important, just delete it.
#         if len(text) <= 1:
#             print("Passing a text")
#             continue
#
#         # Remove unwanted rectangle
#         if isUnclickable(Img_Object):
#             list_of_ImgOs.remove(Img_Object)
#
#         if isClickable(Img_Object) > 0:
#             pass
#             print(text)
#     # TODO: Add common places to click.. like I accept common place if "accept" was one of the words.
#     # Something
#
#     return list_of_ImgOs


def read_all_img_using_list_of_ImgOs(list_of_ImgOs):
    for Img_Object in list_of_ImgOs:
        # Get img name.
        filename = Img_Object.get_img_name()
        # Read text
        text = read_img(filename)
        # Clean the resulting text
        text = re.sub(r'[^\x20-\x7F]+', ' ', text).strip(' ').replace('\n', '').replace('\t', '').strip(' ')

        # If short text then it's not important, just delete it.
        if len(text) <= 1:
            list_of_ImgOs.remove(Img_Object)
            continue

        Img_Object.change_text(text)

        # Remove unwanted rectangle
        if isUnclickable(Img_Object):
            print(Img_Object.get_img_name() + " is not clickable. The text is " + Img_Object.get_text())
            list_of_ImgOs.remove(Img_Object)
            print("The above object got removed")

        if isClickable(Img_Object):
            pass
            print("isClickable: " + str(text))
    # TODO: Add common places to click.. like I accept common place if "accept" was one of the words.
    # Something

    return list_of_ImgOs


def remove_unusable_imgs(DIR):
    current_path = os.getcwd()
    for filename in os.listdir(DIR):
        filename = DIR + '\\' + filename
        if (len(get_colors(filename)) < 2):
            try:
                # Debug
                # command = "move "+ current_path + "\\"+ filename + " " + current_path + "\\old"

                command = "del " + current_path + "\\" + filename
                # print(command)
                os.system(command)
                # print(current_path + "\\"+ filename + " has been removed")
            except:
                print("Error 43312")
        else:
            pass
            # print(filename + " good to go")
    return None


def find_window_for_pid(pid):
    result = None

    def callback(hwnd, _):
        nonlocal result
        ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
        if cpid == pid:
            result = hwnd
            return False
        return True

    win32gui.EnumWindows(callback, None)
    return result


def get_setup_title_using_tasklist(window_title="setup"):
    l = execute_cmd("tasklist")
    lines = l.decode('utf-8').rstrip().split('\r\n')
    lines = [line for line in lines if len(line) > 0]
    for line in lines:
        line = str(line)
        if window_title in line:
            print(line)
            line = re.sub(' +', ' ', line)
            line = line.split(' ')
            pid = line[1]
            print(pid)


def get_setup_title_using_Win32_Process(window_title="setup"):
    procs = wmi.WMI().Win32_Process()
    for proc in procs:
        if window_title in proc.Name:
            return proc
    return None


def take_a_screenshot():
    proc = None
    setup_list = ["m_install", "setup", "install"]
    for window_name in setup_list:
        try:
            title = get_setup_title(window_name)
            if title is None:
                continue
            im = screenshot(title)
            return im
        except:
            pass

    # for window_name in setup_list:
    #     proc = get_setup_title_using_Win32_Process(window_name)
    #     if proc is not None:
    #         break
    # if proc is not None:
    #     im = screenshot_by_pid(proc.ProcessId)
    #     return im

    return None


def get_point_one(filename):
    filename = filename.split('_')
    return [int(filename[1]), int(filename[2])]


def get_point_two(filename):
    filename = filename.split('_')
    return [int(filename[3]), int(filename[4])]


def create_a_image_object_list(DIR):
    list_of_ImgOs = []
    for filename in os.listdir(DIR):
        filename = DIR + '\\' + filename
        point1 = point2 = 0
        # point1 = get_point_one(filename)
        # point2 = get_point_one(filename)
        list_of_ImgOs.append(img_class.Img_Object(filename, point1, point2, None))
    return list_of_ImgOs


def start_clicking_all_over_the_place(list_of_ImgOs):
    list_of_ImgOs = [x for x in list_of_ImgOs if x.priority_number > 0]
    list_of_ImgOs = sorted(list_of_ImgOs, key=lambda x: x.priority_number, reverse=True)
    for image_object in list_of_ImgOs:
        go_to_image(image_object.img_name)


def show_window(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            return True
    return False


def wc_l(DIR):
    print(str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])))


def clean_dirs():
    os.system("del imgs /q")
    os.system("mkdir imgs")
    os.system("mkdir dropbox")
    os.system("mkdir queue")
    os.system("mkdir screenshots")


def logic2():
    pass
    clean_dirs()
    # The dir where the images will be stored
    current_dir = "imgs"
    # The name of the current screenshot.
    current_screenshot = "current-tmp.png"
    # Take a screenshot
    im = take_a_screenshot()
    # Save the taken screenshot
    im.save(current_screenshot)
    # Add the current screenshot aka the first screenshot to current_screenshots_list list.
    current_screenshots_list = [current_screenshot]
    # Create a list of screenshots with different heights.
    current_screenshots_list = create_another_version(current_screenshots_list)
    for current_screenshot_img in current_screenshots_list:
        # Make small images
        create_imgs(current_screenshot_img)
    print("Printing the first len")
    wc_l(current_dir)
    # Remove all images that have less than 3 colors
    remove_unusable_imgs(current_dir)
    print("Printing the second len")
    wc_l(current_dir)
    # Create a list of img_obj elements
    list_of_ImgOs = create_a_image_object_list(current_dir)
    print("List created!")
    # Read images and change the element's values using objects from create_a_image_object_list(current_dir)
    list_of_ImgOs = read_all_img_using_list_of_ImgOs(list_of_ImgOs)
    # Read images using current_dir or DIR
    # list_of_ImgOs = read_all_img(current_dir)
    # Click
    start_clicking_all_over_the_place(list_of_ImgOs)


def check_if_it_exists(screenshot, small_image):
    small_image = "samples\\" + small_image
    img_rgb = cv2.imread(small_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(screenshot, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # The percentage of similarities
    # I set it to %100 by setting it to 1.
    threshold = 0.9
    loc = np.where(res >= threshold)
    if len(loc[0]) >= 1:
        return True
    else:
        return False


def get_all_files_that_starts_with(has_in_name):
    path = 'samples'
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and \
             has_in_name in i]
    return files


def generic_check(current_screenshot, name_of_the_check, repeated=False):
    tmp_list_of_images = get_all_files_that_starts_with(name_of_the_check)
    for tmp_image in tmp_list_of_images:
        try:
            if check_if_it_exists(current_screenshot, tmp_image):
                print("YES: " + name_of_the_check + " is found")

                if repeated:
                    # Return a list with the right one in the top of the list.
                    tmp_list_of_images2 = ["samples\\" + tmp_image]
                    for tmp_image2 in tmp_list_of_images:
                        if tmp_image is tmp_image2:
                            # Since we already added it
                            continue
                        tmp_list_of_images2.append("samples\\" + tmp_image2)
                    return tmp_list_of_images2
                else:
                    return "samples\\" + tmp_image
            else:
                print("No: " + name_of_the_check + " was not found")
                return None
        except:
            pass
    return None

def check_the_same_exactly(current_screenshot, past_current_screenshot):
    a = cv2.imread(current_screenshot)
    b = cv2.imread(past_current_screenshot)
    difference = cv2.subtract(a, b)    
    result = not np.any(difference)
    return result

def check_the_same(current_screenshot, past_current_screenshot):
    # Doesn't work
    small_image = past_current_screenshot
    screenshot = current_screenshot

    img_rgb = cv2.imread(small_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(screenshot, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # The percentage of similarities
    # I set it to %100 by setting it to 1.
    threshold = 0.9
    loc = np.where(res >= threshold)
    if len(loc[0]) >= 1:
        return True
    else:
        return False

def action(number):
    chosen_time = 0.1
    if number == 1:
        pyautogui.press('enter')
    if number == 2:
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('up')
        time.sleep(chosen_time)
        pyautogui.press('enter')
    if number == 3:
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('space')
        time.sleep(chosen_time)
        pyautogui.press('enter')
    if number == 4:
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('space')
        time.sleep(chosen_time)
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('enter')
    if number == 5:
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('space')
        time.sleep(chosen_time)
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('space')
        time.sleep(chosen_time)
        pyautogui.press('tab')
        time.sleep(chosen_time)
        pyautogui.press('enter')
    if number == 6:
        pass
    if number == 7:
        pass
    if number == 8:
        pass
    

def logic():
    # Take a screenshot
    clean_dirs()
    # The dir where the images will be stored
    current_dir = "imgs"
    value = str(randint(0, 10000))
    # The name of the current screenshot.
    current_screenshot = "screenshots\\" + value + "current-tmp.png"
    past_current_screenshot = "screenshots\\" + value + "-past-current-tmp.png"
    # Get the window in front so we can press enter
    time.sleep(5)
    try:
        im = take_a_screenshot()
    # pyautogui.press('enter')
    except Exception as e:
        print("Error 2 " + str(e))
        print("logic() broke")

    # static values
    overall_counter = 0
    action_counter = 1
    while True:
        print("action_counter is "+str(action_counter))
        try:
            # If it's not the first time
            if overall_counter != 0:
                im.save(past_current_screenshot)
            # Take a screenshot
            im = take_a_screenshot()
            # Save the taken screenshot
            im.save(current_screenshot)
        except Exception as e:
            print("Error 3 " + str(e))
            print("No window")
        
        try:
            print(current_screenshot)
            print(past_current_screenshot)
            if check_the_same_exactly(current_screenshot, past_current_screenshot):    
                action_counter += 1
            else:
                # Reset
                action_counter = 1
        except Exception as e:
            print("Error 5 " + str(e))
            print("No window")

        action(action_counter)
        overall_counter+=1
        if (overall_counter >= 100):
            overall_counter = 1


def main():
    while True:
        try:
            logic()
        except Exception as e:
            print("Error 1 " + str(e))
            print("logic() broke")


if __name__ == '__main__':
    os.chdir("C:\\Miner")
    main()
