import splashscreen_engine as splash

screen = splash.Screen()
screen.size(750,500)
# This Starts The Engine
screen.start()

# Background Video
video = splash.BackgroundVideo(
    screen,
    "ExampleVideos/SampleVid2.mp4",
    fps=30,
    loop=True
)

video.play()

# Loading Bar
bar = splash.LoadingBar(screen,add_xy=(0,100),height=50) # By default, position is (center) , add 100 units to y-axis and set height to 100
bar.set_video("Examplevideos/BarVid.mp4")
bar.place()

# Text `loading`
text = splash.Text(
    screen,
    "Loading...",
    "impact",
    20,
    # "down",
    add_xy=(0,100) # Place the bar downward and add 100 units to y-axis
    ,colour=(0,0,0)
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

import tkinter # Used as main screen for example.
main_screen = tkinter.Tk()

main_screen.geometry("750x500")

main_text = tkinter.Label(
    main_screen,
    text="Your Main Screen",
    font=("impact",40)
)

main_text.pack()

main_screen.mainloop()
