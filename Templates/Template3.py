import splashscreen_engine as splash

screen = splash.Screen()
screen.size(750,500)

# This Starts The Engine
screen.start()
# Background Video
video = splash.BackgroundVideo(
    screen,
    "ExampleVideos/SampleVid3.mp4",
    fps=30,
    loop=True
)

video.play()

# Loading Bar
bar = splash.LoadingBar(screen,add_xy=(0,130)) # By default, position is (center) and add 100 units to y-axis
bar.place()

# Bar 2
bar2 = splash.LoadingBar(parent=screen,add_xy=(0,70),height=40) # By default, position is (center) and add 80 units to y-axis
bar2.set_video("ExampleVideos/SampleBarVid3.mp4")
bar2.place(colour=(0,0,0))


# Text `loading`
text = splash.Text(
    screen,
    "Loading...",
    "impact",
    20,
    "center",
    add_xy=(0,70), # Place the text on the bar2
    colour=(255,255,255)
)

text.show()

# Text2
text2 = splash.Text(
    screen,
    "Please Wait...",
    "impact",
    15,
    "down",
    add_xy=(0,-80) # Place the bar downward and subtract 80 units from y-axis
)

text2.show()

messages = [
    "Downloading Assets",
    "Updating Game",
    "Installing",
    "Please Wait"
]

# LOADING | you can add your `loading` processes here

a = 0
b = 0
current_message = 0
while not a >= 100:

    a += 0.3
    b += 1.5

    text.edit(text=f"{round(a,2)}%")

    text2.edit(text=f"{messages[current_message]}")

    bar.set_progress(b)
    bar2.set_progress(a)
    screen.wait(0.05)
    if b >= 100:
        if current_message == 3:
            continue
        bar2.set_progress(0)
        current_message+=1
        b = 0



text.edit(
    text="100%"
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