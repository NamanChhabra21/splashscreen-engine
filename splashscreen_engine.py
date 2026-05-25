import os
import threading
import time


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
s = '1'
os.environ['SDL_VIDEO_CENTERED'] = s

# Modules
import pygame
import cv2


deleted_by_user = False
program_stopped = False

def avoid_lag():
    global deleted_by_user
    if deleted_by_user:
        raise RuntimeError("Failed to update UI, the screen is deleted by either you or the user.")
    pygame.event.pump()



def draw_loading_bar(screen, bars):

    for bar in bars:
        if not isinstance(bar, LoadingBar):
            continue

        if bar.visible:
            screen_size = screen.get_size()
            if bar.position == "center":
                x = (screen_size[0]-bar.width)//2 + bar.add_xy[0] # Center + x , where x can be positive or negative
                y = (screen_size[1]-bar.height) // 2 + bar.add_xy[1]  # Center + y , where y can be positive or negative

            elif bar.position == "right":
                x = screen_size[0] - bar.width + bar.add_xy[0]
                y = (screen_size[1]-bar.height) // 2 + bar.add_xy[1]
            elif bar.position == "left":
                x =bar.add_xy[0]
                y = screen_size[1] // 2 + bar.add_xy[1]
            elif bar.position == "up":
                x = (screen_size[0]-bar.width)//2 + bar.add_xy[0]
                y = bar.height + bar.add_xy[1]
            elif bar.position == "down":
                x = (screen_size[0]-bar.width)//2 + bar.add_xy[0]
                y = screen_size[1]- bar.height + bar.add_xy[1]
            else:
                x,y=0,0

            # OUTER BAR
            pygame.draw.rect(
                screen,
                bar.colour,
                (
                    x,y,
                    int(bar.width),
                    int(bar.height)
                ),
                border_radius=10
            )

            # INNER LOADER
            pygame.draw.rect(
                screen,
                bar.loading_colour,
                (x,y,
                    int(
                        bar.width *
                        (bar.progress / 100)
                    ),
                    int(bar.height)
                ),
                border_radius=10
            )


def draw_text(screen, texts):
    for txt in texts:
        if not isinstance(txt, Text):
            continue

        if txt.visible:
            surface = txt.pg_font.render(txt.text, True, txt.colour)

            screen_size = screen.get_size()
            if txt.position == "center":
                x = screen_size[0]//2 + txt.add_xy[0] # Center + x , where x can be positive or negative
                y = screen_size[1] // 2 + txt.add_xy[1]  # Center + y , where y can be positive or negative
            elif txt.position == "right":
                x = screen_size[0] - surface.get_size()[0] + txt.add_xy[0]
                y = screen_size[1] // 2 + txt.add_xy[1]
            elif txt.position == "left":
                x = surface.get_size()[0] + txt.add_xy[0]
                y = screen_size[1] // 2 + txt.add_xy[1]
            elif txt.position == "up":
                x = screen_size[0]//2 + txt.add_xy[0]
                y = surface.get_size()[1] + txt.add_xy[1]
            elif txt.position == "down":
                x = screen_size[0]//2 + txt.add_xy[0]
                y = screen_size[1]-surface.get_size()[1] + txt.add_xy[1]
            else:
                x,y=0,0
            text_rect = surface.get_rect(center=(x,y))
            screen.blit(surface,text_rect)


one_time_warning = True # A variable used for printing warning inside the size() function | Ensuring doesn't repeat printing the same

class Screen:

    def __init__(self,title_bar=False):

        if not pygame.get_init():
            pygame.init()

        # Reset Quitting values
        global deleted_by_user,program_stopped
        deleted_by_user = False
        program_stopped = False

        # Default Height and Width
        self.height = 500
        self.width = 750

        # Fullscreen Variable
        self.fullscreen = False

        # Screen Info
        self.info = pygame.display.Info()

        # Caption
        self.caption = "Splash Screen"

        pygame.display.set_caption(self.caption)

        # Clock
        self.clock = pygame.time.Clock()

        # Running Variable
        self.running = False
        self.stopped = False

        # Screen
        self.screen = None

        # Background Color
        self.bgColor = (0, 0, 0)

        # BACKGROUND IMAGE
        self.current_background = None

        # FOREGROUND VIDEO
        self.foreground_video = None

        # Icon
        self.icon = None


        # GLOBAL UI
        self.ui_elements = []

        self.title_bar = title_bar
        self.is_escape = False







    def get_size(self):
        return self.width,self.height

    def start(self):


        self.running = True

        # CREATING SCREEN
        if self.fullscreen:
            # For Full Screen
            w, h = 0, 0
            self.is_escape = False # Reset Escape
        else:
            # For Normal Window
            w, h = self.width, self.height

        if not self.title_bar:
            # Creates window without title Bar
            self.screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
        else:
            # Creates window with title Bar
            self.screen = pygame.display.set_mode((w, h),pygame.RESIZABLE)


        self.screen.fill(self.bgColor)

        pygame.display.update()


        # BACKGROUND MAINLOOP
        def mainloop():
            global program_stopped

            if not self.screen:
                self.start()

            self.running = True



            while self.running and not self.stopped:

                # Updates window size every time you resize
                if self.title_bar:
                    size = pygame.display.get_window_size()
                    self.width,self.height = size[0],size[1]
                avoid_lag()

                if self.title_bar and self.fullscreen and not self.is_escape:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:

                            program_stopped = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.is_escape = True
                                break

                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            program_stopped = True



                # CLEAR SCREEN
                self.screen.fill(self.bgColor)

                # DRAW BACKGROUND IMAGE
                if self.current_background:
                    self.screen.blit(self.current_background.image,(0, 0))
                    draw_loading_bar(self.screen,self.current_background.ui_elements)
                    draw_text(self.screen,self.current_background.ui_elements)

                # DRAW FOREGROUND VIDEO
                if self.foreground_video:

                    # DRAW VIDEO FRAME
                    if self.foreground_video.frame:
                        self.screen.blit(self.foreground_video.frame,(0, 0))

                    # DRAW VIDEO UI
                    draw_loading_bar(self.screen,self.foreground_video.ui_elements)
                    draw_text(self.screen,self.foreground_video.ui_elements)

                # DRAW GLOBAL UI
                draw_loading_bar(self.screen,self.ui_elements)
                draw_text(self.screen,self.ui_elements)
                pygame.display.update()

                self.clock.tick(60)
            global deleted_by_user
            deleted_by_user = True
        threading.Thread(target=mainloop).start() # Starts Mainloop as background process

    def stop(self,quit_pygame = True):

        # Stops the Window
        self.running = False
        self.stopped = True

        # STOP VIDEO if playing
        if self.foreground_video:
            self.foreground_video.stop = True

        # Checks if user want to quit pygame or not
        if quit_pygame:
            pygame.quit()



    def size(self, width=750, height=500, fullscreen=False):


        # Check if width and height is integer and more than 0
        if (
                not isinstance(width, int)
                or
                not isinstance(height, int)
                or
                height < 1
                or
                width < 1
        ):
            raise TypeError(
                f"Width and Height must be positive integers. Got width = {width} and height = {height}."
            )

        global one_time_warning
        if self.running and one_time_warning:
            print(
                "\033[93m"
                "[WARNING]\n"
                "size() was called after start().\n\n"
                "This may cause screen flickering because\n"
                "the window needs to be recreated.\n\n"
                "For best results, call size() before start().\n\n"
                "This warning can be ignored if dynamic\n"
                "window resizing is intended."
                "\033[0m"
            )
        one_time_warning = False

        self.fullscreen = fullscreen

        if self.fullscreen:
            self.width,self.height = 0,0
        else:
            self.width,self.height = width,height
        if self.title_bar:
            screen_mode = pygame.RESIZABLE
        else:
            screen_mode = pygame.NOFRAME

        self.screen = pygame.display.set_mode((self.width,self.height),screen_mode)





    def title(self, text="Splash Screen"):

        self.caption = text.strip()

        pygame.display.set_caption(self.caption)

    @staticmethod
    def wait(seconds):

        if seconds <= 1:

            avoid_lag()

            time.sleep(seconds)

            return

        while seconds >= 0:

            avoid_lag()

            time.sleep(0.1)

            seconds -= 0.1

    def set_bg_color(self, color=(0, 0, 0)):

        self.bgColor = color

    def set_icon(self,path):
        if not self.title_bar:
            raise RuntimeError("Unable to set Icon, Title Bar is disabled.")
        self.icon = path
        icon_image = pygame.image.load(path).convert_alpha()
        pygame.display.set_icon(icon_image)



    def is_quit(self):
        if not self.title_bar:
            raise RuntimeError("`is_quit` only works if you enable Title Bar.")

        return program_stopped # True if quit else False
    def is_escaped(self):
        if not self.title_bar:
            raise RuntimeError("`is_escaped` only works if Title Bar is enabled.")
        escape = self.is_escape
        self.is_escape = False
        return escape # True if escape else False


class BackgroundVideo:

    def __init__(self, screen_object, path, fps=30,loop=False):

        # ONLY SCREEN ALLOWED
        if not isinstance(screen_object, Screen):

            raise RuntimeError(
                "You cannot merge backgrounds into other objects"
            )

        self.parent = screen_object

        self.path = path

        self.video = cv2.VideoCapture(self.path)

        self.stop = False

        self.is_playing = False

        self.loop_thread_video = None

        self.fps = fps

        # Transparency
        self.transparent = False
        self.transparent_level = 255

        # CURRENT FRAME
        self.frame = None

        # UI ELEMENTS
        self.ui_elements = []

        self.loop = loop

    def play(self):

        self.stop = False

        self.is_playing = True

        # SET FOREGROUND VIDEO
        self.parent.foreground_video = self

        if not self.video:
            return

        def thread_video():

            while self.parent.running and not self.stop:

                avoid_lag()

                # READ FRAME
                success, frame = self.video.read()

                # VIDEO FINISHED
                if not success:

                    # LOOP VIDEO
                    if self.loop:

                        self.video.set(
                            cv2.CAP_PROP_POS_FRAMES,
                            0
                        )

                        continue

                    # NORMAL VIDEO END
                    else:

                        self.is_playing = False

                        # REMOVE FRAME ONLY
                        self.frame = None

                        break

                # CONVERT COLORS
                frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                # FULLSCREEN
                if self.parent.fullscreen:

                    frame = cv2.resize(
                        frame,
                        (
                            self.parent.info.current_w,
                            self.parent.info.current_h
                        )
                    )

                # NORMAL WINDOW
                else:

                    frame = cv2.resize(
                        frame,
                        (
                            self.parent.width,
                            self.parent.height
                        )
                    )

                # CREATE SURFACE
                surface = pygame.surfarray.make_surface(
                    frame.swapaxes(0, 1)
                )

                # TRANSPARENCY
                if self.transparent:

                    surface.set_alpha(
                        self.transparent_level
                    )

                # STORE FRAME
                self.frame = surface

                self.parent.clock.tick(self.fps)

        self.loop_thread_video = threading.Thread(
            target=thread_video
        )

        self.loop_thread_video.start()

    def pause(self):

        self.stop = True

        self.is_playing = False

    def resume(self):

        self.stop = False

        self.play()

    def delete(self):

        self.pause()

        self.video.set(
            cv2.CAP_PROP_POS_FRAMES,
            0
        )

        self.frame = None

    def transparency(self, level=120):

        if level < 0:
            level = 0

        if level > 255:
            level = 255

        self.transparent = True

        self.transparent_level = level

    def stop_transparency(self):

        self.transparent = False

    def stop_loop(self):
        self.loop = False

    def playing(self):
        return self.playing


class BackgroundImage:

    def __init__(self, parent, path):

        # ONLY SCREEN ALLOWED
        if not isinstance(parent, Screen):

            raise RuntimeError(
                "You cannot merge backgrounds into other objects"
            )

        self.parent = parent

        self.path = path

        self.ui_elements = []

        image = pygame.image.load(self.path)

        # FULLSCREEN
        if self.parent.fullscreen:

            image = pygame.transform.scale(
                image,
                (
                    self.parent.info.current_w,
                    self.parent.info.current_h
                )
            )

        # NORMAL WINDOW
        else:

            image = pygame.transform.scale(
                image,
                (
                    self.parent.width,
                    self.parent.height
                )
            )

        self.image = image

    def set(self):

        self.parent.current_background = self


class LoadingBar:

    def __init__(self, parent, width=None, height=None,position="center",add_xy = (0,0)):

        check_valid_pos(position,"LoadingBar")
        self.position = position.lower()
        self.add_xy = add_xy  # adds / subtract the value of x-axis and y-axis from the chosen position

        self.parent = parent

        # AUTO REGISTER
        if hasattr(
                self.parent,
                "ui_elements"
        ):

            self.parent.ui_elements.append(
                self
            )

        self.screen_dimension = (
            pygame.display.get_window_size()
        )

        # RESPONSIVE WIDTH
        if width is None:

            width = (
                self.screen_dimension[0] * 0.6
            )

        # RESPONSIVE HEIGHT
        if height is None:

            height = (
                self.screen_dimension[1] * 0.015
            )

        self.width = width
        self.height = height
        self.colour = (255, 255, 255)

        self.loading_colour = (0, 255, 0)

        self.visible = False

        self.progress = 0

    def place(
            self,
            colour=(255, 255, 255),
            loading_colour=(0, 255, 0)
    ):

        self.colour = colour

        self.loading_colour = loading_colour

        self.visible = True

    def hide(self):

        self.visible = False

    def set_progress(self, value):

        # CLAMP
        if value < 0:
            value = 0

        if value > 100:
            value = 100

        self.progress = value

def check_valid_pos(string,object_type):
    available_position = ["right", "left", "down", "up", "center",None]
    if string not in available_position:
        available_position.pop() # Remove `None` for displaying Available positions
        raise RuntimeError(f"`{object_type}` object got unknown positional argument. Please choose from {available_position}")

class Text:

    def __init__(self,parent,text="Your Text Here",font=None,size=20,position="center",add_xy = (0,0),colour=(255, 255, 255)):

        check_valid_pos(position,"Text")
        self.position = position.lower()
        self.add_xy = add_xy  # adds / subtract the value of x-axis and y-axis from the chosen position


        self.parent = parent
        self.text = text
        self.font = font
        self.size = size
        self.position = position
        self.colour = colour
        # DEFAULT FONT
        self.pg_font = pygame.font.SysFont(self.font,self.size)
        self.visible = True



        # REGISTER
        if hasattr(self.parent, "ui_elements"):
            self.parent.ui_elements.append(self)

    def edit(self,text=None,font=None,new_size=None,position=None,add_xy=None,colour=None):

        if text is not None:
            self.text = text

        if font is not None:
            self.font = font
            # UPDATE FONT
            self.pg_font = pygame.font.SysFont(self.font, self.size)

        if new_size is not None:
            self.size = new_size

        if position is not None:
            self.position = position

        if add_xy is not None:
            self.add_xy = add_xy

        if colour is not None:
            self.colour = colour

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

class Documentation:
    def __init__(self):
        self.GithubReadMeLink = "https://github.com/NamanChhabra21/splashscreen-engine/blob/main/README.md"
        self.gmail = "chhabranaman21@gmail.com"
        self.ytChannel = "www.youtube.com/@GenZCoderZShorts"
        self.GithubLink = "https://github.com/NamanChhabra21"
        self.pypi = "https://pypi.org/project/splashscreen-engine/"
        self.issues = "https://github.com//NamanChhabra21//splashscreen-engine//issues"
        self.discussions = "https://github.com/NamanChhabra21/splashscreen-engine/discussions"

    def open(self):
        os.startfile(self.GithubReadMeLink)
    def contact(self):
        print(f"For Contact & Feedback :\n\
              Github : {self.GithubLink}\n\
              PyPI : {self.pypi}\n\
              YouTube : {self.ytChannel}\n\
              Issues : {self.issues}\n\
              Discussions : {self.discussions}\n\
              Mail : {self.gmail}")

