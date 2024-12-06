import math

def optimizeNodeLayout(nodes, playArea=[200, 800, 60, 600], k=1000000, scalingFactor=0.08):

    # Use coulomb's law. Idea is to model each node as a proton and each edge as a spring. Then can use Coulomb's law to calculate repuslive force and can use Hooke's law to calculate tension on edges.
    # See Fruchterman-Reingold Algorithm

    """
    - for each node, pair it with another node
    - calculate the distance between the nodes (use distance formula)
    - every other node will exert some force on this node
    - calculate the force every other node is exerting on this node and sum
    - do this for all nodes
    - now we have forces on every node
    - adjust every node's position according to the position (how?)
        - F = ma
        - We get some force in x direction, some force in y direction. We can take mass to be constant. 
        - Force applied gives acceleration in some direction. (for instance, node A might have x accelaration +0.4.)
        - Give it one second to accelarate? So its x position will change by +0.4 

    - repeat whole process 100 times or until temperature small enough (Fruchterman-Reingold Algorithm)
    
    """

    numNodes = len(nodes)
    # List for net forces on each node, matches the nodes in the list:
    
    for _ in range(1000):
        netForces = [[0, 0] for i in range(numNodes)]
        for i in range(numNodes):
            for j in range(numNodes):
                if i == j:
                    continue
                nodeI = nodes[i]
                nodeJ = nodes[j]

                nodeIx, nodeIy, nodeIr = nodeI[0], nodeI[1], nodeI[2]
                nodeJx, nodeJy, nodeJr = nodeJ[0], nodeJ[1], nodeJ[2]
                

                rSquared = ((nodeIx - nodeJx)**2 + (nodeIy - nodeJy)**2) + 0.0001

                # Calculate coulomb repulsion force with k = 10**3 (actual k is for protons and far too strong)
                f = k/rSquared

                # Get compoments of force
                # Can find angle between the nodes using arctan:
                alpha = math.atan2((nodeIy - nodeJy),(nodeIx - nodeJx))

                # This angle alpha is the same as the angle in the triangle formed by F, Fx, and Fy. 
                fx = math.cos(alpha)*f
                fy = math.sin(alpha)*f

                # Change the net forces on i
                netForces[i][0] += fx
                netForces[i][1] += fy

        # # Problem was that layout was becoming very boxy. Solution idea to add a gravitational force like a spring binding all nodes to center of page
        for i in range(numNodes):
            nodeIx, nodeIy, nodeIr = nodes[i][0], nodes[i][1], nodes[i][2]

            distance = math.sqrt((500 - nodeIx)**2 + (300 - nodeIy)**2) + 0.001  

            # Using Hooke's Law: F = kx
            f_gravity =  (0.01 * (distance))

            # Same calculations as before
            alpha = math.atan2(300 - nodeIy, 500 - nodeIx)
            fx = math.cos(alpha) * f_gravity
            fy = math.sin(alpha) * f_gravity
            
            netForces[i][0] += fx
            netForces[i][1] += fy

        # Now we have net forces on all the nodes
        # Adjust every node's position based on the net force acting upon them
        for i in range(numNodes):
            fx, fy = netForces[i][0], netForces[i][1]

            # fx is actually huge so we should make it smaller
            dx, dy = scalingFactor*fx, scalingFactor*fy

            nodes[i][0] += dx
            nodes[i][1] += dy

            # Make sure new positions are within playarea. Logic here was helped by chatgpt
            startX, endX, startY, endY = playArea
            nodes[i][0] = min(max(nodes[i][0], startX + 40), endX - 40)
            nodes[i][1] = min(max(nodes[i][1], startY + 20), endY - 60)


        scalingFactor *= 0.9
    return nodes
