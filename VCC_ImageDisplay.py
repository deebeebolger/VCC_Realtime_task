import pygame
import os
import random

pygame.init()

def fadeout(wides, heights, screen):
    fadout = pygame.Surface((wides, heights))
    fadout = fadout.convert()
    fadout.fill('black')
    for i in range(255):
        fadout.set_alpha(i)
        screen.blit(fadout,(0, 0))
        pygame.display.update()

def image_disp(iclass, inumber, disptime):
    pygame.init()

    currdir = '/Users/bolger/PycharmProjects/VCC_Realtime_task'
    pic_classlist = os.listdir('FAICC_Images')
    PicClass = [iclass for iclass in pic_classlist if
                "Images" in iclass]  # Ensure that we are only trying to open image directories.

    disp_size = pygame.display.get_desktop_sizes()  # Get display sizes
    print(f"The display screen size is: {disp_size[0]}")
    center_image = True
    screen_resolution = disp_size[0]
    screen_w, screen_h = screen_resolution
    random_secure = random.SystemRandom()

    if iclass == "randomize":
        print("Randomly selecting image class...")
        #class_choice = random_secure.choice(PicClass)  # Randomly select the inumber of images to present.
        #print(f"Randomly chosen image is {class_choice}.")

    elif "Images" in iclass:
        print(f"Image class already defined: {iclass}. ")
        class_choice = iclass

    figlist_pcurr = os.path.join("FAICC_Images", class_choice)
    figlist_curr  = os.listdir(figlist_pcurr)  # Get the current class images as a list.
    Figs = [truefig for truefig in figlist_curr if ".png" in truefig]  # Ensure that only image files are selected.
    figs_choice   = random_secure.sample(Figs, inumber)

    # Need to write the name of the ImageClass presented to file.
    file_savepath = os.path.join(currdir, "TrialData")
    if not os.path.exists(file_savepath):
        os.makedirs(file_savepath)

    fname = class_choice+"_images.txt"
    fname_path = os.path.join(file_savepath, fname)
    file_image = open(fname_path, "w")
    file_image.write(iclass+"\n")

    for icnt, currimg in enumerate(figs_choice):

        # write the name of image class and current image file to file.
        file_image.write(currimg+"\n")

        currpath = os.path.join(currdir, 'FAICC_Images', class_choice, currimg)
        image = pygame.image.load(currpath)

        window = pygame.display.set_mode((screen_w, screen_h))
        image_w, image_h = image.get_size()

        screen_aspect_ratio = screen_w / screen_h
        image_aspect_ratio = image_w / image_h

        if screen_aspect_ratio < image_aspect_ratio:  # Width is binding
            new_image_w = screen_w
            new_image_h = int(new_image_w / image_aspect_ratio)
            image = pygame.transform.scale(image, (new_image_w, new_image_h))
            image_x = 0
            image_y = (screen_h - new_image_h) // 2 if center_image else 0

        elif screen_aspect_ratio > image_aspect_ratio:  # Height is binding
            new_image_h = screen_h
            new_image_w = int(new_image_h * image_aspect_ratio)
            image = pygame.transform.scale(image, (new_image_w, new_image_h))
            image_x = (screen_w - new_image_w) // 2 if center_image else 0
            image_y = 0

        else:  # Images have the same aspect ratio
            image = pygame.transform.scale(image, (screen_w, screen_h))
            image_x = 0
            image_y = 0

        window.blit(image, (image_x, image_y))
        pygame.display.flip()

        start_tick = pygame.time.get_ticks()
        show_img = True

        while show_img == True:
            time_diff = (pygame.time.get_ticks() - start_tick) / 1000  # calculate the time interval in seconds
            # print(f'time passed {time_diff}secs')
            if time_diff >= disptime:
                fadeout(screen_w, screen_h, window)
                show_img = False

    # Need to put up a finish image/message here
    pygame.quit()
    file_image.close()
