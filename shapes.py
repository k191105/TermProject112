from cmu_graphics import *

def drawCapsule(x, y, width, height, border='black', fill=None):
    radius = height/2
    
    drawArc(x, y + radius, height, height, 90, 180, fill=fill, border=border)

    drawArc(x+width, y + radius, height, height, 270, 180, fill=fill, border=border)
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


    
def redrawAll(app):
    drawCapsule(100, 200, 100, 50)

runApp()

cmu_graphics.run()