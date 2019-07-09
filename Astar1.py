#!/usr/bin/env python
# robot 1

import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String
from std_msgs.msg import Int32
import numpy as np

# golbal variables
map = np.array(None)
g = None
id = None

# callback functions for ROS communication
def map_subscriber(Map):
    global map
    map =np.array([Map.data])
    map = map.reshape((7,7))

def rob_id (ID):
    global id
    id = ID.data

def goal_list(Goals):
    global g
    goals = np.array(Goals.data)
    g = [goals[1], goals[0]]

def Path_Pub(path):
    optimal_path = Int32MultiArray()
    optimal_path.data = path
    pub.publish(optimal_path)

    while not rospy.is_shutdown():
        rospy.sleep(1)

# A-Star functions
def distance(x1, y1, x2, y2):
    dist = np.sqrt(np.power((x1 - x2), 2) + np.power((y1 - y2), 2))
    return dist

def expand_array(node_x, node_y, hn, xTarget, yTarget, CLOSED, MAX_X, MAX_Y):
    node_x = node_x + 1
    node_y = node_y + 1
    xTarget = xTarget + 1
    yTarget = yTarget + 1
    CLOSED = np.array(CLOSED + 1)

    exp_array = np.array([])
    exp_count = 1
    c2 = CLOSED.shape[0]
    new_exp = np.zeros(5)

    for k in range(-1, 2):
        for j in range(-1, 2):
            if (k != j or k != 0):
                s_x = node_x + k
                s_y = node_y + j
                if ((s_x > 0 and s_x <= MAX_X) and (s_y > 0 and s_y <= MAX_Y)):
                    flag = 1
                    if (k == 1 and j == 1):
                        # check the curr.
                        for c1 in range(c2):
                            if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                flag = 0
                        # check the neigh.
                        s_x = s_x - 1
                        for c1 in range(c2):
                            if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                flag = 0
                        s_x = s_x + 1
                        s_y = s_y - 1
                        for c1 in range(c2):
                            if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                flag = 0
                        s_y = s_y + 1
                    else:
                        if (k == 1 and j == - 1):
                            # check the curr.
                            for c1 in range(c2):
                                if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                    flag = 0
                            # check the neigh.
                            s_y = s_y + 1
                            for c1 in range(c2):
                                if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                    flag = 0
                            s_y = s_y - 1
                            s_x = s_x - 1
                            for c1 in range(c2):
                                if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                    flag = 0
                            s_x = s_x + 1
                        else:
                            if (k == - 1 and j == 1):
                                # check the curr.
                                for c1 in range(c2):
                                    if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                        flag = 0
                                # check the neigh.
                                s_y = s_y - 1
                                for c1 in range(c2):
                                    if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                        flag = 0
                                s_y = s_y + 1
                                s_x = s_x + 1
                                for c1 in range(c2):
                                    if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                        flag = 0
                                s_x = s_x - 1
                            else:
                                if (k == - 1 and j == - 1):
                                    # check the curr.
                                    for c1 in range(c2):
                                        if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                            flag = 0
                                    # check the neigh.
                                    s_x = s_x + 1
                                    for c1 in range(c2):
                                        if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                            flag = 0
                                    s_x = s_x - 1
                                    s_y = s_y + 1
                                    for c1 in range(c2):
                                        if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                            flag = 0
                                    s_y = s_y - 1
                                else:
                                    for c1 in range(c2):
                                        if (s_x == CLOSED[c1, 0] and s_y == CLOSED[c1, 1]):
                                            flag = 0
                    if (flag == 1):
                        new_exp[0] = s_x - 1
                        new_exp[1] = s_y - 1
                        new_exp[2] = hn + distance(node_x, node_y, s_x, s_y)
                        new_exp[3] = distance(xTarget, yTarget, s_x, s_y)
                        new_exp[4] = new_exp[2] + new_exp[3]
                        if exp_count == 1:
                            exp_array = np.array([new_exp])
                        else:
                            exp_array = np.append([new_exp], exp_array, axis=0)
                        exp_count = exp_count + 1

    return exp_array

def node_index(OPEN, xval, yval):
    i = 0
    while (OPEN[i][1] != xval or OPEN[i][2] != yval):
        i = i + 1

    n_index = i
    return n_index

def insert_open(xval, yval, parent_xval, parent_yval, hn, gn, fn):

    new_row = np.zeros(8)
    new_row[0] = 1
    new_row[1] = xval
    new_row[2] = yval
    new_row[3] = parent_xval
    new_row[4] = parent_yval
    new_row[5] = hn
    new_row[6] = gn
    new_row[7] = fn

    return new_row

def min_fn(OPEN, OPEN_COUNT, xTarget, yTarget):
    flag = 0
    goal_index = 0
    temp_array = np.array([])

    for j in range(OPEN_COUNT):
        if OPEN[j][0] == 1:
            temp = np.append(OPEN[j][:], j)
            if temp_array.size == 0:
                temp_array = np.array([temp])
            else:
                temp_array = np.append(temp_array, [temp], axis=0)
            if (OPEN[j][1] == xTarget) and (OPEN[j][2] == yTarget):
                flag = 1
                goal_index = j

    if flag == 1:
        i_min = goal_index

    if len(temp_array) != 0:
        result = np.where(temp_array[:, 7] == np.amin(temp_array[:, 7]))
        temp_min = result[0]
        i_min = temp_array[temp_min[0], 8]
    else:
        i_min = -1

    return int(i_min)

##################################################################
rospy.init_node('Planning_1', anonymous=False)
pub = rospy.Publisher('Planning_Output1', Int32MultiArray)

while id != 1:
    rospy.Subscriber('robot_to_be_moved', Int32, rob_id)
while map.size == 1:
    rospy.Subscriber('rob1_map', Int32MultiArray, map_subscriber)
while g == None:
    rospy.Subscriber('next_goals_px', Int32MultiArray, goal_list)
###################################################################
# the main code
###################################################################
# Obstacle=-1,Target = 0,Robot=1,Space=2
#    formation data
rob_num = id
target = g

# DEFINE THE 2-D MAP ARRAY
MAP = np.array(map)

# variables scanned from the map
MAX_X, MAX_Y = [MAP.shape[0], MAP.shape[1]]
xval, yval = [(np.where(MAP == rob_num))[0], (np.where(MAP == rob_num))[1]]

xStart = xval
yStart = yval
xTarget = target[0]
yTarget = target[1]
###############################################################################################
# LISTS USED FOR ALGORITHM
###############################################################################################
# OPEN LIST STRUCTURE
# --------------------------------------------------------------------------
# IS ON LIST 1/0 |X val |Y val |Parent X val |Parent Y val |h(n) |g(n)|f(n)|
# --------------------------------------------------------------------------
OPEN = np.array([])
new_open = np.array([])
# CLOSED LIST STRUCTURE
# --------------
# X val | Y val |
# --------------
new_closed = np.ones(2)
# Put all obstacles on the Closed list
m = 1
for i in range(MAX_X):
    for j in range(MAX_Y):
        if (MAP[i, j] == - 1):
            new_closed[0] = i
            new_closed[1] = j
            if (m == 1):
                CLOSED = np.array([new_closed])
                m = m + 1
            else:
                CLOSED = np.append(CLOSED, [new_closed], axis=0)

CLOSED_COUNT = CLOSED.shape[0]
# set the starting node as the first node
xNode = xval
yNode = yval
OPEN_COUNT = 1
path_cost = 0
goal_distance = distance(xNode, yNode, xTarget, yTarget)
new_open = np.array(insert_open(xNode, yNode, xNode, yNode, path_cost, goal_distance, goal_distance))
OPEN = new_open
OPEN[0] = 0
new_closed = np.array([xNode[0], yNode[0]])
CLOSED = np.append(CLOSED, [new_closed], axis=0)
NoPath = 1
OPEN = np.array([OPEN])
count = 0
#############################################################################################
# START ALGORITHM
#############################################################################################
while ((xNode != xTarget or yNode != yTarget) and NoPath == 1):
    count = count + 1
    exp_array = np.array(expand_array(xNode, yNode, path_cost, xTarget, yTarget, CLOSED, MAX_X, MAX_Y))
    exp_count = exp_array.shape[0]

   # IS ON LIST 1/0 |X val |Y val |Parent X val |Parent Y val |h(n) |g(n)|f(n)|
    # --------------------------------------------------------------------------
    # EXPANDED ARRAY FORMAT
    # --------------------------------
    # |X val |Y val ||h(n) |g(n)|f(n)|
    # --------------------------------
    for i in range(exp_count):
        flag = 0
        for j in range(OPEN_COUNT):
            if (exp_array[i, 0] == OPEN[j, 1] and exp_array[i, 1] == OPEN[j, 2]):
                OPEN[j, 7] = min(OPEN[j, 7], exp_array[i, 4])
                if OPEN[j, 7] == exp_array[i, 4]:
                    # UPDATE PARENTS,gn,hn
                    OPEN[j, 3] = xNode
                    OPEN[j, 4] = yNode
                    OPEN[j, 5] = exp_array[i, 2]
                    OPEN[j, 6] = exp_array[i, 3]
                flag = 1
        if flag == 0:
            OPEN_COUNT = OPEN_COUNT + 1
            new_open = np.array(
                insert_open(exp_array[i, 0], exp_array[i, 1], xNode, yNode, exp_array[i, 2], exp_array[i, 3],
                            exp_array[i, 4]))
            OPEN = np.append(OPEN, [new_open], axis=0)
    ###################################################
    # END OF WHILE LOOP
    ###################################################
    # Find out the node with the smallest fn
    index_min_node = min_fn(OPEN, OPEN_COUNT, xTarget, yTarget)

    if (index_min_node != - 1):
        # Set xNode and yNode to the node with minimum fn
        xNode = OPEN[index_min_node, 1]
        yNode = OPEN[index_min_node, 2]
        path_cost = OPEN[index_min_node, 5]
        # Move the Node to list CLOSED
        CLOSED_COUNT = CLOSED_COUNT + 1
        new_closed = np.array([xNode, yNode])
        CLOSED = np.append(CLOSED, [new_closed], axis=0)
        OPEN[index_min_node, 0] = 0
    else:
        # No path exists to the Target!!
        NoPath = 0

i = (CLOSED.shape[0]) - 1
xval = CLOSED[i, 0]
yval = CLOSED[i, 1]
new_path = np.array([xval, yval])
Optimal_path = np.array([])
if Optimal_path.size == 0:
    Optimal_path = np.array([new_path])
else:
    Optimal_path = np.append(Optimal_path, [new_path], axis=0)

if ((xval == xTarget) and (yval == yTarget)):
    inode = 0
    parent_x = OPEN[node_index(OPEN, xval, yval), 3]
    parent_y = OPEN[node_index(OPEN, xval, yval), 4]
    while (parent_x != xStart or parent_y != yStart):
        new_path = np.array([parent_x, parent_y])
        Optimal_path = np.append(Optimal_path, [new_path], axis=0)
        inode = node_index(OPEN, parent_x, parent_y)
        parent_x = OPEN[inode, 3]
        parent_y = OPEN[inode, 4]

else:
    print("Sorry, No path exists to the Target!")

Optimal_path =np.array(Optimal_path.reshape(1,Optimal_path.size)[0])
Optimal_path =  Optimal_path.tolist()
print("Optimal path is")
print (Optimal_path)

Path_Pub(Optimal_path)

