import splashscreen_engine as splash

screen = splash.Screen()
screen.size(750,500)

# This Starts The Engine
screen.start()

# Background Video
video = splash.BackgroundVideo(
    screen,
    "ExampleVideos/SampleVid4.mp4",
    fps=30,
    loop=True
)

video.play()

# Loading Bar
bar = splash.LoadingBar(screen,height=50,add_xy=(0,50)) # By default, position is (center) , add 50 units to y-axis and set height to 50
bar.set_video("ExampleVideos/SampleBarVid4.mp4")
bar.place()

# Text `loading`
text = splash.Text(
    screen,
    "Loading...",
    "forte",
    40,
    "center",
    add_xy=(0,100), # Place the bar `center` and add 100 units to y-axis,
    colour=(255,255,255)
)

text.show()

genZtext = splash.Text(
    screen,
    "GenZ CoderZ",
    "forte",
    100,
    "up",
    add_xy=(0,20), # Place the bar `up` and add 20 units to y-axis,
    colour=(255,255,255)
)
genZtext.show()


# LOADING | you can add your `loading` processes here

a = 0
b = 0
dots = 1

R = 0
G = 0
B = 0
while not a >= 100:

    a += 0.3
    b += 1
    bar.set_progress(a)

    # Loading dots Logic
    if b%10 == 0:
        text.edit(text=f"Loading{dots*"."}")
        dots+=1
        if dots > 3:
            dots=0
        b = 0

    # GenZ CoderZ text animation
    genZtext.edit(colour=(R,G,B))
    if R < 252:
        R += 3
    elif G < 252:
        G += 3
    elif B < 252:
        B += 3
    else:
        R,G,B = 0,0,0

    screen.wait(0.05)


screen.wait(3)

# Stop the splash screen after loading
screen.stop()


"""
if you are using pygame module in your own code,
use `screen.stop(quit_pygame=False)`
instead of `screen.stop()`
"""

# Main Screen Example

import tkinter
main_screen = tkinter.Tk()

main_screen.geometry("750x500")

main_text = tkinter.Label(
    main_screen,
    text="Your Main Screen",
    font=("impact",40)
)

main_text.pack()

main_screen.mainloop()
