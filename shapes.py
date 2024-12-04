from cmu_graphics import *

def drawCapsule(x, y, width, height, border='black', fill=None):
    radius = height/2
    
    drawArc(x, y + radius, height, height, 90, 180, fill=fill, border=border)

    drawArc(x+width, y + radius, height, height, 270, 180, fill=fill, border=border)


    drawRect(x, y, width, height, fill=fill)
    x = x - 1

    drawLine(x, y, x, y+height, fill='white' if fill == None else fill)

    x = x+2
    
    drawLine(x+width, y, x+width, y+height, fill='white'  if fill == None else fill)

    x = x - 3
    width += 4

    y += 1
    height -= 2

    drawLine(x, y, x+width, y)
    drawLine(x, y+height, x+width, y+height)


def drawSpeedBar(xStart, y, width, speeds=[0.5, 1, 1.5, 2, 4], selectedSpeed=None, appRunning=False):
    numSpeeds = len(speeds)
    drawLine(xStart, y, xStart + width, y)

    # Calculate the spacing between different speed options
    spacing = width/(numSpeeds - 1)


    lowerBound = min(speeds)
    upperBound = max(speeds)
    start_color = (240, 224, 195)
    end_color = (255, 0, 0)


    for i in range(numSpeeds):
        speed = speeds[i]

        # Get x for each speed option
        x = xStart + (i*spacing)

        # ChatGPT was used for the alignement and drawing that follows:

        # Select the chosen speed
        if speed == selectedSpeed:
            cFill = interpolate_color(speed, lowerBound, upperBound, start_color, end_color)
            r = 9
            if appRunning:
                cFill='gainsboro'
        else:
            cFill = 'white'
            r = 6

        drawCircle(x, y, r, fill=cFill, border='black')

        
        drawLabel(f'{speed}x', x, y + 20, align='center', size=9)
        


# ChatGPT wrote the entirety of this function 
def interpolate_color(speed, min_speed, max_speed, start_color, end_color):
    normalized = (speed - min_speed) / (max_speed - min_speed)

    normalized = max(0, min(1, normalized))
    
    r = int(start_color[0] + (end_color[0] - start_color[0]) * normalized)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * normalized)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * normalized)
    
    return rgb(r, g, b)



# For onMousePress: Need to be returning where the actual speeds are.
def returnSpeedBarPos(xStart, y, width, speeds=[0.5, 1, 1.5, 2, 4], selectedSpeed=None):
    numSpeeds = len(speeds)

    # Calculate the spacing between different speed options
    spacing = width/(numSpeeds - 1)

    speedCircles = []
    for i in range(numSpeeds):
        # Get x for each speed option
        x = xStart + (i*spacing)

        speedCircles.append([x, y, 6])
    
    return speedCircles


# def redrawAll(app):
#     speeds = [0.75, 1, 1.5, 2, 4]
#     drawSpeedBar(100, 200, 160, speeds, selectedSpeed=1)

# runApp()

    
# def redrawAll(app):
#     drawCapsule(100, 200, 100, 50)

# runApp()

# cmu_graphics.run()