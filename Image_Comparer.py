import cv2 as cv
import time
from time import sleep
from pathlib import Path
import threading 
import numpy as np
import linecache

# Rgb values are flipped (B,G,R)

config_path = Path(__file__).with_name("config.txt")

print("Image Comparer")
print("")


choice = input("Type 'Start' to beginning Image Comparer or type 'Settings' to change various settings: ")
print("")
# Settings Menu
if choice in ["Settings" ,"settings"]:
        print("|Highlight Type|")
        print("Info: Changes how second image is highlighted to display areas of difference")
        print("")
        highlight_type = input("(Different) pixels or (Same) pixels: ")

        if highlight_type in ["Same", "same"]:
            highlight_type = "same \n"
        if highlight_type in ["Different", "different"]:
            highlight_type = "different \n"
        else:
            highlight_type = "same \n"

        time.sleep(1)

        print("")
        print("|Highlight Color|")
        print("Info: Changes color of highlighted pixels on the image")
        print("")
        color = input("(Grey), (Yellow), (Blue), (Green), (Black), (White): ")

        if color in ["Grey" ,"grey"]:
            color = "grey \n"
        if color in ["Yellow" ,"yellow"]:
            color = "yellow \n"
        if color in ["Blue" ,"blue"]:
            color = "blue \n"
        if color in ["Green" ,"green"]:
            color = "green \n"
        if color in ["Black", "black"]:
            color = "black \n"
        if color in ["White", "white"]:
            color = "white \n"

        
        time.sleep(1)
        print("Settings have been saved...")
        print("")

        # Reading config file
        with open(config_path, "r") as f:
            data = f.readlines()
            data[0] = highlight_type
            data[1] = color

        # Writing to config file
        with open(config_path, "w") as f:
            f.writelines(data)
       
        
        time.sleep(1)
        print("Start Program?")
        resume_program = input("Yes or No: ")
        if resume_program in ["No","no", "NO"]:
            quit()
        else:
            print("")

        

# If settings Menu is not selected
else:
    pass

# User input (Images)
image1_path = input("Drag and Drop First Image: ")

# Removes unnecessary text
image1_path = image1_path.strip('"')
image1_path = image1_path.strip("'")
image1_path = image1_path.strip("&")
image1_path = image1_path.strip(" '")


image2_path = input("Drag and Drop Second Image: ")

# Removes unnecessary text
image2_path = image2_path.strip('"')
image2_path = image2_path.strip("'")
image2_path = image2_path.strip("&")
image2_path = image2_path.strip(" '")

# Creates Array from selected images paths
image1 = cv.imread(str(image1_path))
image2 = cv.imread(str(image2_path))

    
# Image 1 Variables
image1_width = image1.shape[1]  # Max x value of first image 
image1_height = image1.shape[0] # Max y value of first image

image1_partial_list1 = []
image1_partial_list2 = []

image1_complete_list = []


# Image 2 Variables 
image2_width = image2.shape[1]  # Max x value of second image 
image2_height = image2.shape[0] # Max y value of second image


image2_partial_list1 = []
image2_partial_list2 = []

image2_complete_list = []


# Misc Varaibles 
same_factor = 0
run = True
text_only_mode = False
highlight_type = linecache.getline("config.txt", 1)
color = linecache.getline("config.txt", 2)


# Fixes Blank Spaces in input
highlight_type = highlight_type.strip()
color = color.strip()


def scanner_1():
    # Scans Image 1 even y values
    x = 0
    y = 0

   
    while y != image1_height:
        for x in range(image1_width):
            if x < image1_width:
                
                image1_partial_list1.append(image1[y, x])

            if x == image1_width -1:
                if y + 2 < image1_height:
                    x = 0 
                    y += 2

                else:
                    y += 1
                    x = 0
    

def scanner_2():
    # Scans Image 1 odd y values
    x = 0
    y = 1

    while y != image1_height:
        for x in range(image1_width):
            if x < image1_width:
                
                image1_partial_list2.append(image1[y, x])
                
            if x == image1_width -1 :
                if y + 2 < image1_height:
                    x = 0
                    y += 2
                        
                else:
                    y += 1
                    x = 0
    
    

def scanner_3():
    # Scans Image 2 even y values
    x = 0
    y = 0

    while y != image2_height:
        for x in range(image2_width):
            if x < image2_width:

                image2_partial_list1.append(image2[y, x])
               
            if x == image2_width -1:
                if y + 2 < image2_height:
                    x = 0
                    y += 2

                else:
                    y += 1
                    x = 0
   

def scanner_4():
    # Scans Image2 odd y values
    x = 0
    y = 1

    while y != image2_height:
        for x in range(image2_width):
            if x < image2_width:

                image2_partial_list2.append(image2[y, x])

            if x == image2_width -1:
                if y + 2 < image2_height:
                    x = 0
                    y += 2

                else:
                    y += 1
                    x = 0


def merger_1():
    # Joins list from thread 1 and 2 into single list
    count = 0
    x1 = 0
    x2 = 0

    for index in range(image1_height):
        if count % 2 == 0:
            for i in range(image1_width):
                image1_complete_list.append(image1_partial_list1[x1])
                x1 += 1
                
            count += 1

        else:
            for i in range(image1_width):
                image1_complete_list.append(image1_partial_list2[x2])
                x2 += 1
                
            count += 1
           

def merger_2():
    # Joins lists from threads 3 and 4 and joins into 1 list
    count = 0
    x3 = 0
    x4 = 0

    for index in range(image2_height):
        if count % 2 == 0:
            for i in range(image2_width):
                image2_complete_list.append(image2_partial_list1[x3])
                x3 += 1
                
            count += 1

        else:
            for i in range(image2_width):
                image2_complete_list.append(image2_partial_list2[x4])
                x4 += 1
                
            count += 1

    


def change_color(color, index):
    greyscale = round((int(image2_complete_list[index][0]) + int(image2_complete_list[index][1]) + int(image2_complete_list[index][2])) / 3)
    

    if color == "grey":
        image2_complete_list[index][0] = greyscale
        image2_complete_list[index][1] = greyscale
        image2_complete_list[index][2] = greyscale
    elif color == "yellow":
        image2_complete_list[index][0] = 0
        image2_complete_list[index][1] = greyscale
        image2_complete_list[index][2] = greyscale
    elif color == "blue":
        image2_complete_list[index][0] = greyscale
        image2_complete_list[index][1] = greyscale
        image2_complete_list[index][2] = 0
    elif color == "green":
        image2_complete_list[index][0] = 0
        image2_complete_list[index][1] = greyscale
        image2_complete_list[index][2] = 0
    elif color == "black":
        image2_complete_list[index][0] = 0
        image2_complete_list[index][1] = 0
        image2_complete_list[index][2] = 0
    elif color == "white":
        image2_complete_list[index][0] = 255
        image2_complete_list[index][1] = 255
        image2_complete_list[index][2] = 255
    else:
        image2_complete_list[index][0] = greyscale
        image2_complete_list[index][1] = greyscale
        image2_complete_list[index][2] = greyscale
    
    
def compare():
    print("Comparing Images...")
    # Compares complete list from both images 
    same_factor = 0

     # Only this outcome will display an image           
    if len(image1_complete_list) == len(image2_complete_list):
        for index in range(len(image2_complete_list)):
            if str(image2_complete_list[index][0:3]) == str(image1_complete_list[index][0:3]):
                same_factor += 1
                if highlight_type == "same":
                    change_color(color, index)
            else:
                if highlight_type == "different":
                    change_color(color, index)
                same_factor += 0

    if len(image1_complete_list) < len(image2_complete_list):
        for index in range(len(image1_complete_list)):
            if str(image1_complete_list[index][0:3]) == str(image2_complete_list[index][0:3]):
                same_factor += 1
            else:
                same_factor += 0

    if len(image1_complete_list) > len(image2_complete_list):
        for index in range(len(image2_complete_list)):
            if str(image1_complete_list[index][0:3]) == str(image2_complete_list[index][0:3]):
                same_factor += 1
            else:
                same_factor += 0

   
    return same_factor


def display_images(text_only_mode):
    if text_only_mode == False:
        print("Displaying Images...")
        

        display_different = np.concatenate((image1, image2), axis=1)
        display_same = np.concatenate((image1, image1), axis=1)

        # Checks if value of result is same as all the pixels in the 2nd image 
        if result == image2_width * image2_height:
            print("Press any key to close window")
            cv.imshow("Sameness Factor: "  + str(round((result / len(image2_complete_list)) * 100)) + "%" , display_same)
            cv.waitKey(0)
            
        else:
            print("Press any key to close window")
            cv.imshow("Sameness Factor: "  + str(round((result / len(image2_complete_list)) * 100)) + "%" , display_different)
            cv.waitKey(0)
        

    if text_only_mode == True:
        pass

        
    
def error_check():
    # Check if images are different in size and changes to text only mode to compensate
        if image1_height * image1_width != image2_height * image2_width:
            print("")
            print("Warning!")
            print("")
            print("Images selected are different sizes and cannot be displayed.")
            print("Continue in text only mode or Quit Program?: ")

            text_only_mode = input("Continue or Quit: ")
            if text_only_mode in ["Continue", "continue" ,"c" , "C"]:
                return True

            if text_only_mode in ["Quit", "quit" ,"q" ,"Q"]:
                #exits program
                quit()
            else:
                return True

        if image1_height * image1_width == image2_height * image2_width:
            return False
        print("")
        

if run  ==  True:
    if __name__ == "__main__":
        # Main Order of Events once program starts
        text_only_mode = error_check()
        


        start = time.time()
        print("")
        print("Scanning Images...")

        s1 = threading.Thread(target=scanner_1)
        s2 = threading.Thread(target=scanner_2)
        s3 = threading.Thread(target=scanner_3)
        s4 = threading.Thread(target=scanner_4)
        m1 = threading.Thread(target=merger_1)
        m2 = threading.Thread(target=merger_2)
        

        s1.start()
        s2.start()
        s3.start()
        s4.start()
        

        s1.join()
        s2.join()
        s3.join()
        s4.join()

        
        m1.start()
        m2.start()

        m1.join()
        m2.join()
        
    
        result = compare()
        print("Finished!")
        print("")

        end = time.time()
        difference = end - start

        time.sleep(1)

        print("Results:")
        print("Sameness Factor: " + str(round((result / len(image2_complete_list)) * 100)) + "%")
        print("Time Taken: " + str(round(difference, 2)) + " Seconds")
        
        time.sleep(1)

        print("")
        display_images(text_only_mode)

        
        
        print("")
        print("Exiting Program...")


'''
Acknowledgments:
https://opencv.org/
https://docs.python.org/3/library/time.html
https://pathlib.readthedocs.io/en/pep428/
https://docs.python.org/3/library/threading.html
https://numpy.org/
https://docs.python.org/3/library/linecache.html
'''