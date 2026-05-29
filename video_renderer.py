import cv2
import pygame

class Vid:

    def __init__(self,video_path):

        self.path = video_path
        self.ret = None
        self.frame = None
        self.video = cv2.VideoCapture(video_path)

    def next_frame(self,width,height):

        # Reading Next Frame
        self.ret,self.frame =self.video.read()

        # Check if next frame exists
        if not self.ret:
            return None
        # Resizing the Frame
        self.frame = cv2.resize(self.frame,(width,height))

        # Converting BGR to RGB ( pygame supports RGB )
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

        # Swapping dimensions for pygame
        self.frame = self.frame.swapaxes(0,1)

        # Make pygame Surface
        surface = pygame.surfarray.make_surface(self.frame)

        # Return pygame Surface
        return surface

    def reset_frames(self):
        self.video.set(cv2.CAP_PROP_POS_FRAMES,0)

