from cmu_graphics import *

def onAppStart(app):
    app.width = 600
    app.height = 400
    app.cx = app.width//2
    app.cy = 200
    app.r = 50
    app.dx = 10 # amount to change app.cx
    app.clicksInside = 0
    app.clicksOutside = 0
    app.dotsColor = 'blue'

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1-y2)**2)**0.5


def redrawAll(app):
    drawLabel('Click in Partial Dots', app.cx, 30, size=16)
    drawLabel('Press the left or right arrow', 200, 50, size=12)
    drawLabel('Click inside and outside the partial dots', 200, 70, size=12)
    drawLabel(f'Clicks inside: {app.clicksInside}', 200, 100, size=12)
    drawLabel(f'Clicks outside: {app.clicksOutside}', 200, 120, size=12)

    
    # Draw the dot:
    drawCircle(app.cx, app.cy, app.r, fill=app.dotsColor)
    # And if part of the dot extends beyond the right
    # edge, draw that same amount of dot on the left edge:
    if app.cx > app.width - app.r:
        pixelsBeyondRightEdge = (app.cx + app.r) - app.width
        cx = -app.r + pixelsBeyondRightEdge
        drawCircle(cx, app.cy, app.r, fill=app.dotsColor)

def onKeyPress(app, key):
    if key == 'right':
        app.cx += app.dx
        if app.cx >= app.width + app.r:
            app.cx = app.r
    elif key == 'left':
        app.cx -= app.dx
        if app.cx - app.r < 0:
            # The dot is partly off the left edge, so add
            # app.width to it, so that it instead sits partly
            # off the right edge:
            app.cx += app.width


def pointIsInEitherPartialDot(app, mouseX, mouseY):
    dot1X = app.cx
    
    if app.cx > app.width - app.r:
        pixelsBeyondRightEdge = (app.cx + app.r) - app.width
        dot2X = -app.r + pixelsBeyondRightEdge
    else:
        dot2X = dot1X
    
    if ((dot1X - app.r <= mouseX <=  dot1X + app.r) or (dot2X - app.r <= mouseX <=  dot2X + app.r)) and ((app.cy - app.r) <= mouseY <= (app.cy +app.r)):
        return True


def onMouseMove(app, mouseX, mouseY):
    if pointIsInEitherPartialDot(app, mouseX, mouseY):
        app.dotsColor = 'pink'
    else:
        app.dotsColor = 'blue'
        

def onMousePress(app, mouseX, mouseY):
    dot1X = app.cx
    
    if app.cx > app.width - app.r:
        pixelsBeyondRightEdge = (app.cx + app.r) - app.width
        dot2X = -app.r + pixelsBeyondRightEdge
    else:
        dot2X = dot1X
    
    
    if (distance(mouseX, mouseY, dot1X, app.cy) <= app.r) or (distance(mouseX, mouseY, dot2X, app.cy) <= app.r):
        app.clicksInside += 1
    else:
        app.clicksOutside += 1
    
def main():
    runApp()

main()
cmu_graphics.run()