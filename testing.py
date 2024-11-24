from cmu_graphics import *

class Graph:
    def __init__(self):
        self.nodes = []
        self.adjacency_matrix = []
        self.transition_matrix = []

    def addNode(self, node):
        self.nodes.append(node)

        # Everytime this function is called, we should add a row and add a column to represent the extra node. 
        num_nodes = len(self.nodes)

        # Add a 0 to every row to represent the new node (adding a new column)
        for row in self.adjacency_matrix:
            row.append(0)
        
        # add a new row:
        newRow = [0] * num_nodes
        self.adjacency_matrix.append(newRow)
        

    def addEdge(self, node1, node2):
        print("Trying to add node", node1, 'and', node2)
        if node1 not in self.nodes or node2 not in self.nodes:
            print("one of the nodes aren't in self.nodes")
            return
        else:
            node1Index = self.nodes.index(node1)
            node2Index = self.nodes.index(node2)
            
            # Make sure no reflexivity
            if node1Index == node2Index:
                return
            
            self.adjacency_matrix[node1Index][node2Index] = 1

    # TODO RemoveNode Function
    # TODO RemoveEdge Function


def onAppStart(app):
    app.width = 1000
    app.height = 600
    app.graph = Graph()
    app.R = 15
    app.mode = 'page_edit'
    app.buttons = returnButtons()

    # Drag Behaviour (some of this code is from CS academy, but most of it has been modified)
    app.draggingNode = False
    app.draggingEdge = False
    app.selectedNode = None
    app.lineStartLocation = None
    app.lineEndLocation = None

    app.otherSelectedNode = None

def returnButtons():
    d = {
        'Edit Pages': {'id': 'page_edit', 'label': 'Edit Pages', 'x': 75, 'y': 60, 'width': 60, 'height': 25, 'activated': True},
        'Edit Links': {'id': 'link_edit', 'label': 'Edit Links', 'x': 75, 'y': 95, 'width': 60, 'height': 25, 'activated': False},
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
    # Draw Buttons
    for key in app.buttons:
        button = app.buttons[key]
        drawRect(button['x'], button['y'], button['width'], button['height'], border='black', fill='yellow' if button['activated'] else 'white')
        drawLabel(button['label'], button['x'] + button['width']/2, button['y'] + button['height']/2, size=9)


    # Drawing pre-existing edges
    n = len(app.graph.nodes)
    if n > 0:
        for i in range(n):
            for j in range(n):
                if app.graph.adjacency_matrix[i][j] == 1:
                    currNode = app.graph.nodes[i]
                    nextNode = app.graph.nodes[j]
                    drawLine(currNode[0], currNode[1], nextNode[0], nextNode[1])


    # Drawing nodes
    for i in range(len(app.graph.nodes)):
        circle = app.graph.nodes[i]
        circleX = circle[0]
        circleY = circle[1]
        drawCircle(circleX, circleY, app.R, border = 'black', fill='green' if (app.selectedNode == i or app.otherSelectedNode == i) else 'white')

    #Drawing New edges:
    if app.draggingEdge and app.lineStartLocation != None and app.lineEndLocation != None:
        x0, y0 = app.lineStartLocation
        x1, y1 = app.lineEndLocation
        drawLine(x0, y0, x1, y1, dashes=app.draggingEdge, fill='blue')

def onMousePress(app, mouseX, mouseY):
    # Control Panels mouse interaction
    for key in app.buttons:
        button = app.buttons[key]
        if (button['x'] <= mouseX <= button['x'] + button['width'] and
            button['y'] <= mouseY <= button['y'] + button['height']):
            
            app.mode = button['id']
            print(app.mode)

            for other_key in app.buttons:
                other_button = app.buttons[other_key]
                other_button['activated'] = True if (other_key == key) else False
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
            app.lineStartLocation = app.graph.nodes[i]
            app.lineEndLocation = None


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
        if distance(mouseX, mouseY, app.graph.nodes[i][0], app.graph.nodes[i][1]) <= app.R:
            return i
        
    return None


def isInNode(app, mouseX, mouseY):
    for i in range(len(app.graph.nodes)):
        if distance(mouseX, mouseY, app.graph.nodes[i][0], app.graph.nodes[i][1]) <= app.R:
            return True
        
    return False
def onMouseDrag(app, mouseX, mouseY):
    if app.mode == 'page_edit' and app.draggingNode == True:
        if app.selectedNode != None:
            #app.selectedNode give the index of the selected Node. Update it's position with onMouseDrag
            app.graph.nodes[app.selectedNode] = [mouseX, mouseY]
    elif app.mode == 'link_edit' and app.draggingEdge == True:
        if isInNode(app, mouseX, mouseY):
            app.otherSelectedNode = findClickedNode(app, mouseX, mouseY)
        else:
            app.otherSelectedNode = None


        app.lineEndLocation = (mouseX, mouseY)


def onMouseRelease(app, mouseX, mouseY):
    if app.mode == 'page_edit' and app.draggingNode:
        app.draggingNode = False
        app.selectedNode = None

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


def main():
    runApp()

main()

cmu_graphics.run()