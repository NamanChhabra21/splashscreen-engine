# splashscreen-engine
A module for making Splash Screens with videos, images, loading bars, text rendering, and threaded rendering support for your Applications.

## Sample Preview
![Preview](screenshot.png)

## Features

- Optional Title Bar
- Dynamic Window Resizing
- Fullscreen Support
- Background videos
- Background images
- Loading bars
- Text rendering
- Transparency support
- Threaded rendering
- Video looping
- Simple API

## Installation

```bash
pip install splashscreen-engine
```
OR
```bash
pip install splashscreen-engine==2.0.0
```

## Example

```python
import splashscreen_engine as splash

screen = splash.Screen()
screen.size(750,500)

# This Starts The Engine
screen.start()

# Background Video
video = splash.BackgroundVideo(
    screen,
    "exampleVid.mp4",
    fps=30,
    loop=True
)

video.play()

# Loading Bar
bar = splash.LoadingBar(screen,add_xy=(0,100)) # By default, position is `center` and add 100 units to y-axis
bar.place()

# Text `loading`
text = splash.Text(
    screen,
    "Loading...",
    "impact",
    20,
    "down",
    add_xy=(0,-80) # Place the text downward and subtract 80 units from y-axis
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
```

---

## Requirements
These Modules are automatically installed with : `pip install splashscreen-engine`
- pygame
- opencv-python
- numpy

---

# Functions

### Basic Window

```python
import splashscreen_engine as splash

screen = splash.Screen()

screen.size(750, 500)

screen.start()
```

#### Stop and Delete Screen

```python
screen.stop()

# Use:
screen.stop(quit_pygame=False)

# if you are using pygame in your own application.
```

#### Set Size for your window

```python
screen.size(750,500)

# Arguments:
# width, height, fullscreen

# OR

screen.size(fullscreen=True)
```

#### Set title for your window

```python
screen.title("Your Title")
```

#### Set Background color

```python
screen.set_bg_color((255,0,0)) # Red
```

#### Get Window Size

```python
width,height = screen.get_size()
```

---
### Window with Title bar (optional)
A title bar is the top bar of a window.
It usually contains:

- window title
- window icon # Coming Soon
- close button
- minimize button
- maximize button
- Note : Clicking on Maximize / Minimize button automatically resizes the screen

---
![Preview](screenshot2.png)
---
#### To create a Title Bar
```python
screen = splash.Screen(title_bar=True)
```
#### Functions for Title Bar
##### To Check if the user clicked on `X` button
```python
screen.is_quit()
```
##### To check if the user pressed `Esc` Key during fullscreen
```python
screen.is_escaped()
```
##### Note : These functions are only applicable when `title_bar = True` else it will raise an error.
---
### Wait Function

Instead of using `time.sleep()`,
you can use this function because it prevents
the `window not responding` issue.

```python
screen.wait(0.5) # Seconds
```

---

### Background Video

You can add a video as the background
of your splash screen using this function.

```python
video = splash.BackgroundVideo(
    screen,
    "exampleVid.mp4",
    fps=30,
    loop=True
)

# loop = True / False
# default(False)

# fps = int
# default(30)
```

#### Play video

```python
video.play()
```

#### Pause video

```python
video.pause()
```

#### Resume video

```python
video.resume()
```

#### Delete video

```python
video.delete()
```

#### Transparency

Make your video transparent.

Transparency Level:
`0 to 255`

Default:
`120`

```python
video.transparency(150)
```

#### Stop Transparency

```python
video.stop_transparency()
```

#### Stopping / Resuming Video Loops

```python
# Loop Video
video.loop = True

# Stop the Loop
video.stop_loop()

# OR
video.loop = False
```

#### To check whether the video is playing or stopped

```python
# Returns True if playing else False
video.playing()
```

---

### Background Image

You can add an image as the background
of your splash screen using this function.

```python
bg_img = splash.BackgroundImage(
    screen,
    "YourImage.png"
)

bg_img.set()
```

---

### Progress Bar

This function adds a progress bar.

```python
bar = splash.LoadingBar(
    screen,
    position="down",
    add_xy=(0,-50)
)

# Arguments:
# parent, width, height,
# position, add_xy

bar.place()

# Arguments:
# colour, loading_colour
```

#### Available Positions

```python
"center"
"right"
"left"
"up"
"down"
```



#### Hiding the Progress Bar

```python
bar.hide()
```

#### Setting Progress

```python
bar.set_progress(50)
```

---

### Text

Adds text on the screen.

```python
text = splash.Text(
    screen,
    "Loading...",
    "impact",
    20,
    position="center",
    add_xy=(0,0)
)

# Arguments:
# parent, text, font,
# size, position,
# add_xy, colour

text.show()
```

#### Available Positions

```python
"center"
"right"
"left"
"up"
"down"
```

#### Show and Hide text

```python
# Show text
text.show()

# Hide text
text.hide()
```

---

#### Edit The Text | Supports Dynamic Editing

This allows you to edit the text dynamically.

Example:
Changing:
`f"Loading {i}%"`
inside loops.

```python
text.edit(
    text = "New Loading Text Added",
    font = "IMPACT",
    new_size = 20,
    position = "center",
    add_xy = (0,0),
    colour = (0,255,0)
)
```
---
### `add_xy` Argument

`add_xy` allows you to move objects relative to their selected position.

Structure:

```python
add_xy = (x,y)
```

| Value | Meaning |
|---|---|
| Positive `x` | Move Right |
| Negative `x` | Move Left |
| Positive `y` | Move Down |
| Negative `y` | Move Up |

Example:

```python
text = splash.Text(
    screen,
    "Loading...",
    position="center",
    add_xy=(0,-100)
)
```

This places the text:
- Horizontally centered
- 100 pixels above the center

---

## Contributing & Feedback

Discuss approaches, suggest new features,
report bugs, or share improvements through GitHub
issues and discussions.

Mail:
chhabranaman21@gmail.com

---
