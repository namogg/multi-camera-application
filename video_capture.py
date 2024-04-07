import time
import threading
import cv2
import PIL.Image


"""TODO: add docstring"""


class VideoCapture:

    def __init__(self, video_source=0, width=400, height=400, fps=30):
        """TODO: add docstring"""

        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps

        self.running = False

    
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))              # convert float to int

        self.ret = False
        self.frame = None

        self.convert_color = cv2.COLOR_BGR2RGB

        self.convert_pillow = True

        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()
    
    def process(self):
        """TODO: add docstring"""
        
        while self.running:
            
            ret, frame = self.vid.read()
            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))

                if self.convert_pillow:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = PIL.Image.fromarray(frame)
                
                self.ret = ret
                self.frame = frame

            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                break

            # assign new frame
            self.ret = ret
            self.frame = frame
            # sleep for next frame
            time.sleep(1/self.fps)

    def get_frame(self):
        """TODO: add docstring"""

        return self.ret, self.frame

    # Release the video source when the object is destroyed
    def __del__(self):
        """TODO: add docstring"""

        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()