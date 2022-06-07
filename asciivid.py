import numpy as np
import cv2
import tkinter
## whitedensity = "#@B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. "
density = ".'`^,:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*&@#MW"

# function getASCIIFromPixel maps the values of intensity of pixel [0,255] to a range of the density list.
# It then finds the ASCII character to replace the pixel with and returns the character.
def getASCIIFromPixel(x):
    return density[int(np.interp(x,[0,255],[0,len(density)]))]

# Since the function is to be used on a nparray, the function is vectorized to getASCIIFromPixelVectorised
getASCIIFromPixelVectorised = np.vectorize(getASCIIFromPixel)



# function turnASCII takes the capture as an input -- has to be an image as an array-like -- 
# converts it to grayscale, resizes it to be smaller and then gets the ascii values for it using getASCIIFromPixelVectorised
# converts it to a string and returns that string
def turnASCII(cap):
    grayscale = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.resize(grayscale, (0,0), fx = 0.3, fy = 0.1)
    ASCIIArray = getASCIIFromPixelVectorised(grayscale)
    ASCIIString = ""
    for char in ASCIIArray:
        ASCIIString+="".join(char)
        ASCIIString+="\n"
    return ASCIIString



# Since tkinter doesn't inherintly support loops because of its mainloop, a recursive function to update the frames is written
# fucntion update takes the current frame every 5 ms and calls the turnASCII function and updates a label to have that ASCII value.
# at the end it calls the after function which calls the update method again after 5 ms in the tkinter mainloop.
def update():
    global label
    ret,frame = cap.read()
    label['text'] = turnASCII(frame)
    win.after(5, update)

    
# cap = cv2.imread("image.jpg")
cap = cv2.VideoCapture(0)
win = tkinter.Tk()
label=tkinter.Label(win, text='', font=('Courier 5'),fg="white",bg="black")
label.pack()
update()
win.mainloop()
cap.release()
