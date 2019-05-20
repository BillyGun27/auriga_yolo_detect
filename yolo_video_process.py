from yolo import YOLO
from timeit import default_timer as timer
from PIL import Image
import numpy as np
import cv2

def detect_video(yolo, video_path, output_path=""):
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps       = vid.get(cv2.CAP_PROP_FPS)
    video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output_path != "" else False
    if isOutput:
        print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
        if(video_path == 0 ):
            video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
            video_fps = 10.0 #20.0 ->normal 10.0 ->raspi min
        print(video_FourCC,video_fps)
        out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    while True:
        return_value, frame = vid.read()
        image = Image.fromarray(frame)
        #image , box , label  = yolo.detect_only_robot(image , "bottle")
        
        #imx = image.size[0]
        #top, left, bottom, right = box
        #xc = left + ( (right-left) //2)
        #yc = top + ( (bottom-top)  //2)
        #if( xc < (imx//3) ):
        #    posx = "left"
        #elif( (imx*2//3) < xc ):
        #    posx = "right"
        #else :
        #    posx = "center"
        
        #if label :
        #    print(label , box)
        #    print(posx)

        #if label:
        #    search_result = "Found" + label + " ,Pos : " + posx 
        #    color_result = (0, 255, 0)
        #else :
        #    search_result = "Not Found"
        #    color_result = (0, 0, 255)

        result = np.asarray(image)
        curr_time = timer()
        exec_time = curr_time - prev_time
        prev_time = curr_time
        accum_time = accum_time + exec_time
        curr_fps = curr_fps + 1
        if accum_time > 1:
            accum_time = accum_time - 1
            fps = "FPS: " + str(curr_fps)
            curr_fps = 0
        cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 0, 0), thickness=2)
        #cv2.putText(result, text=search_result, org=(3, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #            fontScale=0.50, color=color_result, thickness=2)
        height, width, channels = result.shape
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('result', width,height) 
        cv2.imshow("result", result)
        if isOutput:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()
    yolo.close_session() 


if __name__ == '__main__':
    detect_video(YOLO(), 0  ,"robot_cam.avi" )
