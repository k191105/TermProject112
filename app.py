from cmu_graphics import *
import random
from graph import Graph
from shapes import drawCapsule

def onAppStart(app):
    app.width = 1000
    app.height = 600
    app.graph = Graph()
    app.R = 20
    app.mode = 'page_edit'
    app.buttons = returnButtons()

    # Drag Behaviour (some of this code is from CS academy, but most of it has been modified)
    app.draggingNode = False
    app.draggingEdge = False
    app.selectedNode = None
    app.lineStartLocation = None
    app.lineEndLocation = None

    app.otherSelectedNode = None
    app.surferIndex = None

    app.simulationRunning = False
    app.stepsPerSecond = 10
    app.visits = []
    app.totalVisits = 0
    app.locked = False
   

    app.computePageRankButton = {'Compute PageRank': {'id': 'compute_pagerank', 'label': 'Compute Pagerank', 'x': 40, 'y': 450, 'width': 120, 'height': 60, 'activated': False, 'fill': 'cyan'}}
    app.runSimButton = {'Run Simulation': {'id': 'run_sim', 'label': 'Run Simulation', 'x': 40, 'y': 520, 'width': 120, 'height': 60, 'activated': False, 'fill': 'cyan'}}
    app.stopSimButton = {'Stop Simulation': {'id': 'stop_sim', 'label': 'Stop Simulation', 'x': 40, 'y': 520, 'width': 120, 'height': 60, 'activated': False}}
    
def returnButtons():
    d = {
        'Edit Pages': {'id': 'page_edit', 'label': 'Edit Pages', 'x': 40, 'y': 50, 'width': 120, 'height': 40, 'activated': True, 'fill': None},
        'Edit Links': {'id': 'link_edit', 'label': 'Edit Links', 'x': 40, 'y': 100, 'width': 120, 'height': 40, 'activated': False, 'fill': None},
        'Eraser': {'id': 'eraser', 'label': '⌫', 'x': 40, 'y': 150, 'width': 30, 'height': 40, 'activated': False, 'fill': None},
        'Clear All': {'id': 'clear_all', 'label': 'Clear All', 'x': 80, 'y': 150, 'width': 80, 'height': 40, 'activated': False, 'fill': 'crimson'}
    }

    return d

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1-y2)**2)**0.5

def redrawAll(app):
    # Main drawing including control panels
    width = app.width

    startX, endX = (1/5)*width, (4/5)*width

    drawLine(startX, 0, startX, app.height)
    drawLine(endX, 0, endX, app.height)
    
    drawLabel("Network Design", 40, 30, font='Times New Roman', align='left', size=14, bold=True)
    # Draw Buttons
    for key in app.buttons:
        button = app.buttons[key]
        if button['fill'] == None:
            if app.simulationRunning:
                bfill='gainsboro'
            elif button['activated']:
                bfill ='lemonChiffon'    
            else:
                bfill='white'
            drawCapsule(button['x'], button['y'], button['width'], button['height'], border='black', fill=bfill)
        else:
            drawCapsule(button['x'], button['y'], button['width'], button['height'], border='black', fill=button['fill'] if not app.simulationRunning else 'gainsboro')
        drawLabel(button['label'], button['x'] + button['width']/2, button['y'] + button['height']/2, size=12)
    
    drawLine(40, 210, 160, 210)
    drawLabel("Simulation Settings", 40, 230, font='Times New Roman', align='left', size=14, bold=True)
    



    drawLine(40, 430, 160, 430)
    # Just compute PageRank
    computePageRank = app.computePageRankButton
    computePageRankButton = computePageRank['Compute PageRank']

    drawRect(computePageRankButton['x'], computePageRankButton['y'], computePageRankButton['width'], computePageRankButton['height'], border='black', fill='powderBlue' if not app.simulationRunning else 'gainsboro')
    drawLabel(computePageRankButton['label'], computePageRankButton['x'] + computePageRankButton['width']/2, computePageRankButton['y'] + computePageRankButton['height']/2, size=12, bold=True)

    runSim = app.runSimButton
    runSimButton = runSim['Run Simulation']

    runStopLabel = None
    buttonColor = None

    if app.simulationRunning == False:
        runStopLabel = 'Run Simulation'
        buttonColor = 'mediumSeaGreen'
    else:
        runStopLabel = 'Stop Simulation'
        buttonColor = 'crimson'

    drawRect(runSimButton['x'], runSimButton['y'], runSimButton['width'], runSimButton['height'], border='black', fill=buttonColor)
    drawLabel(runStopLabel, runSimButton['x'] + runSimButton['width']/2, runSimButton['y'] + runSimButton['height']/2, size=12, bold=True)


    # Drawing pre-existing edges
    drawDirectionalLinks(app)

    # Drawing nodes
    for i in range(len(app.graph.nodes)):
        circle = app.graph.nodes[i]
        circleX = circle[0]
        circleY = circle[1]
        radius = rounded(circle[2])
        nodefill = None
        if (app.selectedNode == i or app.otherSelectedNode == i):
            nodefill = 'green'
        elif app.surferIndex == i:
            nodefill = 'lemonChiffon'
        else:
            nodefill = 'white'
        drawCircle(circleX, circleY, radius, border = 'black', fill=nodefill)
        drawLabel(getLabel(i), circleX, circleY, size=12)
   
    #Drawing New edges (dotted):
    if app.draggingEdge and app.lineStartLocation != None and app.lineEndLocation != None:
        x0, y0 = app.lineStartLocation
        x1, y1 = app.lineEndLocation
        drawLine(x0, y0, x1, y1, dashes=app.draggingEdge, fill='blue', arrowEnd=True)

def drawDirectionalLinks(app):
    n = len(app.graph.nodes)
    if n > 0:
        for i in range(n):
            for j in range(n):
                if app.graph.adjacency_matrix[i][j] == 1:
                    currNode = app.graph.nodes[i]
                    nextNode = app.graph.nodes[j]
                    
                    x1, y1, r1 = currNode[0], currNode[1], rounded(currNode[2])
                    x2, y2, r2 = nextNode[0], nextNode[1], rounded(nextNode[2])

                    # TODO we want the arrows to start fomr edge of circle 1 and end at edge of circle 2. Can do some vector calc to achieve this:

                    # Find vector between nodes:
                    dx = x2 - x1
                    dy = y2 - y1
                    magnitude = (dy**2 + dx**2)**0.5

                    # Find unit vector:
                    ux, uy = dx/magnitude, dy/magnitude

                    # FIND COORDINATES
                    startX, startY = x1 + r1 * ux, y1 + r1 * uy
                    endX, endY = x2 - r2 * ux, y2 - r2 * uy
                    
                    drawLine(startX, startY, endX, endY, fill='blue', arrowEnd=True)

def getLabel(index):
    if index < 0:
        return ""
    else:
        # Recursively find the label
        last = chr((index % 26) + 65)
        return getLabel((index//26) - 1) + last   

def onMousePress(app, mouseX, mouseY):
    if app.simulationRunning:
        runSim = app.runSimButton
        runSimButton = runSim['Run Simulation']
        # only do something if we're clicking in the run/stop sim button:
        if (runSimButton['x'] <= mouseX <= runSimButton['x'] + runSimButton['width'] and runSimButton['y'] <= mouseY <= runSimButton['y'] + runSimButton['height']):
        # Logic here is courtesy of ChatGPT
            app.simulationRunning = not app.simulationRunning

            if app.simulationRunning:
                app.surferIndex = random.randint(0, len(app.graph.nodes) - 1)  
                app.visits = [0] * len(app.graph.nodes)
                app.totalSteps = 0
            return
        else:
            return
    # Control Panels mouse interaction
    for key in app.buttons:
        button = app.buttons[key]
        if (button['x'] <= mouseX <= button['x'] + button['width'] and
            button['y'] <= mouseY <= button['y'] + button['height']):
            
            app.mode = button['id']
            print(app.mode)

            if app.mode == 'clear_all':
                app.graph = Graph()
                app.mode == 'page_edit'
                return

            for other_key in app.buttons:
                other_button = app.buttons[other_key]
                other_button['activated'] = True if (other_key == key) else False
            return
    

    computePageRank = app.computePageRankButton
    computePageRankButton = computePageRank['Compute PageRank']

    # If click on computePageRank button, compute PageRank:
    if computePageRankButton['x'] <= mouseX <= computePageRankButton['x'] + computePageRankButton['width'] and computePageRankButton['y'] <= mouseY <= computePageRankButton['y'] + computePageRankButton['height']:
        app.graph.computePagerank()
    

    runSim = app.runSimButton
    runSimButton = runSim['Run Simulation']

    # if clicking in runsim button
    if (runSimButton['x'] <= mouseX <= runSimButton['x'] + runSimButton['width'] and runSimButton['y'] <= mouseY <= runSimButton['y'] + runSimButton['height']):
        # Logic here is courtesy of ChatGPT
        app.simulationRunning = not app.simulationRunning

        if app.simulationRunning:
            app.surferIndex = random.randint(0, len(app.graph.nodes) - 1)  
            app.visits = [0] * len(app.graph.nodes)
            app.totalSteps = 0
        return
    
    
    # Check if we're in the control area
    if not withinPlayArea(app, mouseX, mouseY):
        return
    
    i = findClickedNode(app, mouseX, mouseY)

    if app.mode == 'page_edit':
        if i != None:
            app.selectedNode = i
            app.draggingNode = True
            
        else:
            nodeInformation = [mouseX, mouseY]
            app.graph.addNode(nodeInformation)
    elif app.mode == 'link_edit':
        if i != None:
            app.draggingEdge = True
            app.selectedNode = i
            app.lineStartLocation = app.graph.nodes[i][:2]
            app.lineEndLocation = None

def onStep(app):
    if app.simulationRunning:
        app.totalSteps += 1
        if len(app.graph.nodes) > 0:
            currentNode = app.surferIndex
            nextNode = app.graph.takeRandomSurferStep(currentNode)

            # Add that we've visited this node once
            app.visits[nextNode] += 1

            # Change current surferIndex to be the next node given by takeRandomSurferStep
            app.surferIndex = nextNode
            
            totalVisits = sum(app.visits)
            
            if totalVisits == 0:
                pass
            
            numNodes = len(app.graph.nodes)

            for i in range(numNodes):
                # Change radius continuously
                app.graph.nodes[i][2] = app.R + ((app.visits[i]/totalVisits) * 100)

        
        if app.totalSteps >= 1000:
            app.simulationRunning = False

def withinPlayArea(app, x, y):
    #overall:
    width, height = app.width, app.height


    startX, endX = (1/5)*width, (4/5)*width
    startY, endY = (1/10)*height, (9/10)*height

    if startX <= x <= endX and startY <= y <= endY:
        return True
    else:
        return False
    
# get index of clicked node
def findClickedNode(app, mouseX, mouseY):
    for i in range(len(app.graph.nodes)):
        if distance(mouseX, mouseY, app.graph.nodes[i][0], app.graph.nodes[i][1]) <= app.graph.nodes[i][2]:
            return i
    return None

def isInNode(app, mouseX, mouseY):
    for i in range(len(app.graph.nodes)):
        if distance(mouseX, mouseY, app.graph.nodes[i][0], app.graph.nodes[i][1]) <= app.graph.nodes[i][2]:
            return True
    return False

def onMouseDrag(app, mouseX, mouseY):

    if app.mode == 'page_edit' and app.draggingNode == True:
        if app.selectedNode != None:
            # app.selectedNode give the index of the selected Node. Update its position with onMouseDrag

            r = app.graph.nodes[app.selectedNode][2] 
            
            if withinPlayArea(app, mouseX, mouseY):
                app.graph.nodes[app.selectedNode] = [mouseX, mouseY, r]


    elif app.mode == 'link_edit' and app.draggingEdge == True:
        if isInNode(app, mouseX, mouseY):
            app.otherSelectedNode = findClickedNode(app, mouseX, mouseY)
        else:
            app.otherSelectedNode = None

        app.lineEndLocation = (mouseX, mouseY)
    
    #TODO implement eraser
    elif app.mode == 'eraser':
        pass

def onMouseRelease(app, mouseX, mouseY):
    if app.mode == 'page_edit' and app.draggingNode:
        app.draggingNode = False
    elif app.mode == 'link_edit' and app.draggingEdge:

        # First check if the user has dragged into a valid node
        targetNodeIndex = findClickedNode(app, mouseX, mouseY)

        if targetNodeIndex != None and targetNodeIndex != app.selectedNode:
            print(app.graph.adjacency_matrix)
            app.graph.addEdge(app.graph.nodes[app.selectedNode], app.graph.nodes[targetNodeIndex])
            print(app.graph.adjacency_matrix)


        # Stop dragging the edge
        app.draggingEdge = False
        app.selectedNode = None
        app.otherSelectedNode = None
        app.lineStartLocation = None
        app.lineEndLocation = None

def onKeyPress(app, key):
    if app.selectedNode == None:
        return
    else:
        print(app.selectedNode)
        if key == 'd':
            app.graph.removeNode(app.selectedNode)
            app.selectedNode == None

def main():
    runApp()

main()

cmu_graphics.run()