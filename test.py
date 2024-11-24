from cmu_graphics import *

def onAppStart(app):
    app.circles = []
    app.R = 5
    app.selectedCircle = None

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1-y2)**2)**0.5

def redrawAll(app):
    for i in range(len(app.circles)):
        circle = app.circles[i]
        circleX = circle[0]
        circleY = circle[1]
        color = 'white' if app.selectedCircle != i else 'black'
        drawCircle(circleX, circleY, app.R, border = 'black', fill=color)

    for i in range(len(app.circles) - 1):
        currCircle = app.circles[i]
        nextCircle = app.circles[i+1]
        drawLine(currCircle[0], currCircle[1], nextCircle[0], nextCircle[1])

def onKeyPress(app, key):
    if app.selectedCircle == None:
        return
    else:
        if key == 'd':
            app.circles.pop(app.selectedCircle)
            app.selectedCircle == None

def onMousePress(app, mouseX, mouseY):
    for i in range(len(app.circles)):
        if distance(mouseX, mouseY, app.circles[i][0], app.circles[i][1]) <= app.R:
            app.selectedCircle = i
            return
    
    circleInformation = [mouseX, mouseY]
    app.circles.append(circleInformation)
    
def main():
    runApp()

main()

cmu_graphics.run()