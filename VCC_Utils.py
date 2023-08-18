from screeninfo import get_monitors
import pygame
from pygame.locals import *
import os
import sys
import time as tme
from subprocess import Popen
import random

import VCC_ImageDisplay
from VCC_RecordData import *

pygame.init()

def time_str():
    return tme.strftime("%H_%M_%d_%m_%Y", tme.gmtime())

def render_waiting_screen(text_string=None, time_black=0.0):

    pygame.init()
    # pygame.font.init()
    h_str = str(get_monitors()[0])
    w, h = (h_str.split(',')[2], h_str.split(',')[3])
    hstr = int(float(h.split('=')[1]))
    wstr = int(float(w.split('=')[1]))
    display_x = int(float(wstr) / 2)
    display_y = int(float(hstr) / 2)
    display_x, display_y = (2 * display_x, 2 * display_y)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    window = pygame.display.set_mode((display_x, display_y), pygame.NOFRAME, 32)
    pygame.display.set_caption("VCC")

    if time_black > 0:
        window.fill((0., 0., 0.))
        timer_event = USEREVENT + 1
        pygame.time.set_timer(timer_event, int(time_black) * 1000)
        myfont = pygame.font.SysFont("arial", 60)
        if text_string:
            textsurface1 = myfont.render(text_string, False, (255, 255, 255))
            text_rect1   = textsurface1.get_rect(center=(display_x / 2, display_y / 2 - 100))
        window.blit(textsurface1, text_rect1)
    else:
        myfont = pygame.font.SysFont("arial", 30)
        press_string = "Please press the Space Bar to continue..."
        textsurface1 = myfont.render(press_string, False, (255, 255, 255))
        text_rect1 = textsurface1.get_rect(center=(display_x / 2, display_y / 2 + 100))
        if text_string:
            myfont = []
            myfont = pygame.font.SysFont("arial", 60)
            textsurface2 = myfont.render(text_string, False, (255, 255, 255))
            text_rect2 = textsurface2.get_rect(center=(display_x / 2, display_y / 2 - 100))
        window.fill((0, 0, 0))
        window.blit(textsurface1, text_rect1)
        if text_string:
            window.blit(textsurface2, text_rect2)

    pygame.display.update()
    busy = True
    while busy:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                busy = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                    busy = False
                    return False
                elif event.key == K_SPACE:
                    press_string1 = ""
                    textsurface_new = myfont.render(press_string1, False, (0, 0, 0))
                    window1 = pygame.display.set_mode((display_x, display_y), pygame.NOFRAME, 32)
                    window1.fill((0, 0, 0))
                    window1.blit(textsurface_new, text_rect1)
                    pygame.quit()
                    busy = False
                    return False

            if not (time_black > 0.):
                window.blit(textsurface1, text_rect1)
                if text_string:
                    window.blit(textsurface2, text_rect2)
            else:
                if event.type == timer_event:
                    pygame.quit()

                    return False
            if busy == False:
                break
            pygame.display.update()


def begin_VCC_video():
    print("Playing opening video")
    video_path = "/Videos/"
    os.startfile(video_path)
    # or
    #vid_cap = cv2.VideoCapture(video_path)
    # ret, frame = vid_cap.read()
    # while(1):
    #     ret, frame = vid_cap.read()
    #     cv2.imshow('frame', frame)


def begin_VCC_images(Imgclass, Trialnum, picnum):
    if not os.path.isdir("REC"):
        os.mkdir("REC")
    # Create a welcome screen
    render_waiting_screen("Welcome to Visions of Climate Change")
    render_waiting_screen("3", time_black=2.0)
    render_waiting_screen("2", time_black=2.0)
    render_waiting_screen("1", time_black=2.0)

    recorder = RecordData(250., 20., 60)   # First arg = Fs, second arg = participant age.
    render_waiting_screen(text_string=None, time_black=2.0)
    recorder.start_recording()

    for i in range(int(Trialnum)):

        recorder.add_trial(Imgclass)
        VCC_ImageDisplay.image_disp(Imgclass, picnum)
        tdata = recorder.add_trial(0.)









