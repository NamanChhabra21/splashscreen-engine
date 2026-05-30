import splashscreen_engine as splash

screen = splash.Screen()
screen.size(750,500)

# This Starts The Engine
screen.start()

# Background Video
video = splash.BackgroundVideo(
    screen,
    "ExampleVideos/exampleVid.mp4",
    fps=30,
    loop=True
)

video.play()

# Loading Bar
bar = splash.LoadingBar(screen,add_xy=(0,100)) # By default, position is (center) and add 100 units to y-axis
bar.place()

# Text `loading`
text = splash.Text(
    screen,
    "Loading...",
    "impact",
    20,
    "down",
    add_xy=(0,-80) # Place the bar downward and subtract 80 units from y-axis
)

text.show()

# LOADING | you can add your `loading` processes here

a = 0

while not a >= 100:

    a += 0.3

    text.edit(
        text=f"loading : {round(a,2)}%"
    )

    bar.set_progress(a)

    screen.wait(0.05)

text.edit(
    text="loaded : 100%"
)

screen.wait(3)

# Stop the splash screen after loading
screen.stop()


"""
if you are using pygame module in your own code,
use `screen.stop(quit_pygame=False)`
instead of `screen.stop()`
"""

# Main Screen Example

import tkinter # pip install tkinter -- used as main screen for example.
main_screen = tkinter.Tk()

main_screen.geometry("750x500")

main_text = tkinter.Label(
    main_screen,
    text="Your Main Screen",
    font=("impact",40)
)

main_text.pack()

main_screen.mainloop()
