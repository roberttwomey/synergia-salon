import cv2 

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
while True:
    try:
        check, frame = webcam.read()
        image = cv2.resize(frame, (800, 600))
        #image = frame
        cv2.imshow("Capturing", image)
        cv2.imwrite(filename='capture.jpg', img=image)
        #print("Image saved!")
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
    
