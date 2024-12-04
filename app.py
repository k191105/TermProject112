from cmu_graphics import *
import random
from graph import Graph
from shapes import drawCapsule, drawSpeedBar, returnSpeedBarPos
import numpy as np
import math

def onAppStart(app):
    resetApp(app)

def resetApp(app):
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
    app.surferTravel = []
    app.surferProgress = 0
    app.surferMoving = False
    app.surferOnEdge = None

    app.simulationRunning = False
    app.stepsPerSecond = 10
    app.visits = []
    app.totalVisits = 0
    app.totalSteps = 0
    app.locked = False

    app.computePageRankButton = {'Compute PageRank': {'id': 'compute_pagerank', 'label': 'Compute Pagerank', 'x': 50, 'y': 450, 'width': 100, 'height': 60, 'activated': False, 'fill': 'cyan'}}
    app.runSimButton = {'Run Simulation': {'id': 'run_sim', 'label': 'Run Simulation', 'x': 50, 'y': 520, 'width': 100, 'height': 60, 'activated': False, 'fill': 'cyan'}}
    app.stopSimButton = {'Stop Simulation': {'id': 'stop_sim', 'label': 'Stop Simulation', 'x': 50, 'y': 520, 'width': 100, 'height': 60, 'activated': False}}
    app.generateGraphButton = {'Generate Random Graph': {'id': 'generate_random', 'label': 'Generate Random Network', 'x': 40, 'y': 200, 'width': 120, 'height': 40, 'activated': False}}
    
    app.speedCirclesPos = []
    app.selectedSpeed = 1

def returnButtons():
    d = {
        'Edit Pages': {'id': 'page_edit', 'label': 'Edit Pages', 'x': 40, 'y': 40, 'width': 120, 'height': 40, 'activated': True, 'fill': None},
        'Edit Links': {'id': 'link_edit', 'label': 'Edit Links', 'x': 40, 'y': 90, 'width': 120, 'height': 40, 'activated': False, 'fill': None},
        'Eraser': {'id': 'eraser', 'label': '⌫', 'x': 40, 'y': 140, 'width': 15, 'height': 40, 'activated': False, 'fill': None},
        'Clear All': {'id': 'clear_all', 'label': 'Clear All', 'x': 100, 'y': 140, 'width': 60, 'height': 40, 'activated': False, 'fill': 'crimson'}
    }

    return d

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1-y2)**2)**0.5


############################################################
# Start Screen
############################################################

def start_redrawAll(app):

    # Background Image -- Can make this more sophisticated.
    imageWidth, imageHeight = getImageSize('welcomeImage.png')
    drawImage('welcomeImage.png', app.width/2, app.height/2, align='center', opacity = 60, width=imageWidth*(4/5), height=imageHeight*(4/5))

    drawLabel('Welcome!', app.width/2, app.height/2 - 50, size=24, bold=True)
    drawLabel(f'Welcome to PageRank Simulator', app.width/2, app.height/2, size=32, font='Monteserrat', bold=True)
    drawLabel('Press space to enter!', app.width/2, app.height/2 + 40, size=24)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('sim')

############################################################
# Simulation Screen
############################################################

def sim_redrawAll(app):
    # Main drawing including control panels
    width = app.width

    startX, endX = (1/5)*width, (4/5)*width



    if app.simulationRunning:
        drawRect(200, 0, 600, 600, fill='white')
        drawRect(0, 0, 200, 600, fill=rgb(249, 250, 250))
        drawRect(800, 0, 200, 600, fill=rgb(249, 250, 250))
        
    drawLine(startX, 0, startX, app.height)
    drawLine(endX, 0, endX, app.height)

    
    drawLabel("Network Design", 100, 20, font='Times New Roman', align='center', size=14, bold=True)
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

    # drawLine(20, 200, 180, 200)

    # Generate Random Graph Button
    generateRandomGraph = app.generateGraphButton
    generateRandomGraphButton = generateRandomGraph['Generate Random Graph']

    drawCapsule(generateRandomGraphButton['x'], generateRandomGraphButton['y'], generateRandomGraphButton['width'], generateRandomGraphButton['height'], border='black', fill='burlyWood' if not app.simulationRunning else 'gainsboro')
    drawLabel(generateRandomGraphButton['label'], generateRandomGraphButton['x'] + generateRandomGraphButton['width']/2, generateRandomGraphButton['y'] + generateRandomGraphButton['height']/2, size=11)


    drawLine(20, 260, 180, 260)
    drawLabel("Simulation Settings", 40, 280, font='Times New Roman', align='left', size=14, bold=True)
    
    # Speed BAR
    drawLabel("Speed:", 20, 300, align='left', size=12)
    drawSpeedBar(30, 320, 140, selectedSpeed=app.selectedSpeed, appRunning=app.simulationRunning)

    # drawLabel("Teleportation Probability:", 20, 360, align='left', size=12)

    # drawLabel("Change color on teleport?", 20, 380, align='left', size=12)

    drawLine(20, 430, 180, 430)

    if not app.simulationRunning:
        drawLabel("PageRank Simulator", 500, 30, size=21)
    elif app.simulationRunning:
        drawLabel("PageRank - Simulation Running", 500, 30, size=21)
        drawLabel(f"Steps taken: {app.totalSteps}", 500, 50, size=12)


    # Right Panel:

    drawCapsule(830, 20, 140, 30, border='black', fill='whiteSmoke')
    drawLabel("🔍 Page Rankings", 830, 35, align='left', font='Symbols', size=12)

    drawRanking(app)


    drawCapsule(840, 530, 120, 50, border='black', fill='salmon' if not app.simulationRunning else 'gainsboro')
    drawLabel("Reset Scores", 900, 555, align='center', font='Symbols', size=12)

    # Just compute PageRank
    computePageRank = app.computePageRankButton
    computePageRankButton = computePageRank['Compute PageRank']

    drawCapsule(computePageRankButton['x'], computePageRankButton['y'], computePageRankButton['width'], computePageRankButton['height'], border='black', fill='powderBlue' if not app.simulationRunning else 'gainsboro')
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

    drawCapsule(runSimButton['x'], runSimButton['y'], runSimButton['width'], runSimButton['height'], border='black', fill=buttonColor)
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
                    
                    if (i, j) == app.surferOnEdge:
                        eFill = 'gold'
                    else:
                        eFill = 'dodgerBlue'


                    drawLine(startX, startY, endX, endY, fill=eFill, arrowEnd=True)

                    # # Draw the surfer moving -- calculation aided by ChatGPT
                    # if app.surferMoving and (i, j) == app.currentEdge:
                    #     progressX = startX + (endX - startX) * app.surferProgress
                    #     progressY = startY + (endY - startY) * app.surferProgress
                    #     drawCircle(progressX, progressY, 8, fill='gold', border='black')

def getLabel(index):
    if index < 0:
        return ""
    else:
        # Recursively find the label
        last = chr((index % 26) + 65)
        return getLabel((index//26) - 1) + last   

def sim_onMousePress(app, mouseX, mouseY):

    # ------------------------------------------------------------------------------------------------------------------------------

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
    
    
    # ------------------------------------------------------------------------------------------------------------------------------


    # Control Panels mouse interaction
    for key in app.buttons:
        button = app.buttons[key]
        if (button['x'] <= mouseX <= button['x'] + button['width'] and
            button['y'] <= mouseY <= button['y'] + button['height']):
            
            app.mode = button['id']
            print(app.mode)

            if app.mode == 'clear_all':
                app.graph = Graph()
                app.mode = 'page_edit'
                app.visits = []
                app.totalVisits = 0
                app.surferIndex = None
                return

            for other_key in app.buttons:
                other_button = app.buttons[other_key]
                other_button['activated'] = True if (other_key == key) else False
            return
    
    # ------------------------------------------------------------------------------------------------------------------------------

    # Check if we're clicking in the generate random graph button:
    generateRandomGraph = app.generateGraphButton
    generateRandomGraphButton = generateRandomGraph['Generate Random Graph']

    if (generateRandomGraphButton['x'] <= mouseX <= generateRandomGraphButton['x'] + generateRandomGraphButton['width'] and 
        generateRandomGraphButton['y'] <= mouseY <= generateRandomGraphButton['y'] + generateRandomGraphButton['height']):
            app.totalVisits= 0
            app.visits = []
            app.surferIndex = None
            numNodes = random.randint(4, 12)

            generateEdgeProbability = random.uniform(0.15, 0.4)

            # Better version: Use beta distribution to return biased probability:
            # TODO NOT WORKING: FIXED
            randomNum = np.random.beta(2, 5)
            generateEdgeProbability = 0.1 + (0.7-0.1)*randomNum

            # Get play area bounds
            width, height = app.width, app.height
            startX, endX = (1/5)*width, (4/5)*width
            startY, endY = (1/8)*height, (7/8)*height

            playArea = [startX, endX, startY, endY]
            app.graph.generateRandomGraph(playArea, numNodes = numNodes, generateEdgeProbability = generateEdgeProbability)

    # ------------------------------------------------------------------------------------------------------------------------------

    # Need to check if we're changing the speed:
    circlePos = returnSpeedBarPos(30, 320, 140, selectedSpeed=app.selectedSpeed)

    for i in range(len(circlePos)):
        circle = circlePos[i]
        x, y, r = circle[0], circle[1], circle[2]
        if distance(mouseX, mouseY, x, y) <= r:
            # Select that circle
            app.selectedSpeed = [0.5, 1, 1.5, 2, 4][i]
            app.stepsPerSecond = 10*app.selectedSpeed

    # ------------------------------------------------------------------------------------------------------------------------------

    computePageRank = app.computePageRankButton
    computePageRankButton = computePageRank['Compute PageRank']

    # If click on computePageRank button, compute PageRank:
    if computePageRankButton['x'] <= mouseX <= computePageRankButton['x'] + computePageRankButton['width'] and computePageRankButton['y'] <= mouseY <= computePageRankButton['y'] + computePageRankButton['height']:
        app.graph.computePagerank()
    

    # ------------------------------------------------------------------------------------------------------------------------------


    runSim = app.runSimButton
    runSimButton = runSim['Run Simulation']

    # if clicking in runsim button
    if (runSimButton['x'] <= mouseX <= runSimButton['x'] + runSimButton['width'] and runSimButton['y'] <= mouseY <= runSimButton['y'] + runSimButton['height']):
        # Logic here is courtesy of ChatGPT
        app.simulationRunning = not app.simulationRunning

        if app.simulationRunning:
            try:
                app.surferIndex = random.randint(0, len(app.graph.nodes) - 1)  
                app.visits = [0] * len(app.graph.nodes)
                app.selectedNode = None
                app.totalSteps = 0
                app.surferMoving = False
            except:
                pass
        return
    

    # ------------------------------------------------------------------------------------------------------------------------------
    # CHeck if we're in the reset scores button
    if 840 <= mouseX <= 960 and 530 <= mouseY <= 580:
        resetVisits(app)
        for i in range(len(app.graph.nodes)):
            app.graph.nodes[i][2] = 20
            app.surferIndex = None
            

    # ------------------------------------------------------------------------------------------------------------------------------
    
    # Check we're not in the control area
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
            resetVisits(app)
    elif app.mode == 'link_edit':
        if i != None:
            app.draggingEdge = True
            app.selectedNode = i
            app.lineStartLocation = app.graph.nodes[i][:2]
            app.lineEndLocation = None

    # ------------------------------------------------------------------------------------------------------------------------------

def sim_onStep(app):
    if app.simulationRunning:
        app.totalSteps += 1

        if len(app.graph.nodes) > 0:
            currentNode = app.surferIndex
            nextNode = app.graph.takeRandomSurferStep(currentNode)

            # Add that we've visited this node once
            app.visits[nextNode] += 1

            app.surferOnEdge = (currentNode, nextNode)


            # Change current surferIndex to be the next node given by takeRandomSurferStep
            app.surferIndex = nextNode
            
            totalVisits = sum(app.visits)
            
            if totalVisits == 0:
                pass
            
            numNodes = len(app.graph.nodes)

            for i in range(numNodes):
                # Change radius continuously
                try:
                    app.graph.nodes[i][2] = app.R + ((app.visits[i]/totalVisits) * 100)
                except:
                    pass
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

def sim_onMouseDrag(app, mouseX, mouseY):

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

def sim_onMouseRelease(app, mouseX, mouseY):
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

def sim_onKeyPress(app, key):
    if key == 'r':
        resetApp(app)
        setActiveScreen('start')

    if app.selectedNode == None:
        return
    else:
        print(app.selectedNode)
        if key == 'd':
            app.graph.removeNode(app.selectedNode)
            resetVisits(app)
            app.selectedNode = None  

def drawRanking(app):
    numNodes = len(app.graph.nodes)

    if numNodes == 0:
        return

    startX, endX = (4/5) * app.width, app.width
    startY, endY = 70, 490


    if numNodes <= 1: 
        spacing = None
    else:
        spacing = (endY - startY)/(numNodes - 1)
        spacing = min(spacing, 50)
    
    standardLength = 50

    if len(app.visits) == 0:
        sortedNodeList = [getLabel(i) for i in range(numNodes)]
        sortedVisits = [0] * numNodes
    else:
        labelToScore = {getLabel(i): app.visits[i] for i in range(numNodes)}
        # Sorting method taken from StackOverflow: https://stackoverflow.com/questions/7340019/sort-values-and-return-list-of-keys-from-dict-python
        sortedNodeList = sorted(labelToScore, key=labelToScore.get, reverse=True)

        # This is faster than sorting the list straight up: this is O(N); sorting would be O(NlogN)
        sortedVisits = [labelToScore[label] for label in sortedNodeList]

    for i in range(len(sortedNodeList)):
        label = sortedNodeList[i]
        if len(sortedVisits) == 0:
            if spacing == None:
                y = startY
            else:
                y = startY + i*spacing
            
            drawCircle(832, y + 10, 15, fill=None, border='black')
            drawLabel(label, 832, y + 10)
            drawRect(startX + 60, y, standardLength, 20, fill='dodgerBlue')
        else:
            if spacing == None:
                y = startY
            else:
                y = startY + i*spacing
            numVisits = sortedVisits[i]
            totalVisits = sum(sortedVisits) if sum(sortedVisits) > 0 else 1
            lengthToAdd = math.log(numVisits + 1) / math.log(totalVisits + 1) * 50
            lengthToAddlabel = (numVisits/totalVisits)*50
            drawCircle(832, y + 10, 15, fill=None, border='black')
            drawLabel(label, 832, y + 10)
            drawRect(startX + 60, y, standardLength + lengthToAdd, 20, fill='dodgerBlue')
            drawLabel(f"{pythonRound(numVisits/totalVisits, 3)}", startX + 60 + (standardLength + lengthToAdd)/2, y + 10)

def resetVisits(app):
    app.visits = [0] * len(app.graph.nodes)

def main():
    runAppWithScreens(initialScreen='start')

main()

cmu_graphics.run()