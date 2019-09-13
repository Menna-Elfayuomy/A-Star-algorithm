# A Star algorithm on autonomous mobile robot <br/>
## Intro. 
That project is a part of my work in my Graduation project on a fully autonomous multi-agent robots. <br />
Main objective from the project is implementing a formation algorithm on the whole robots & developing different algorithms to reach approach of making each robot of them fully autonomous.<br /> 
That algorithms used to make each of them fully autonomous are:<br/>
- motion control algorithm 
- go to goal algorithm 
- localization algorithm using a perception data from an overhead camera 
- mapping representation 
- path planning algorithm           **that algorithm is the one included in that repo.**<br/> <br/>

## Description of the A Star algorithm provided
The A* (pronounced A-star) algorithm used in the autonomous systems to generate a free-from collision path for a robot starting from its current position to a desired goal point. <br/>  
My code depends on two main pieces of data which are the current location of the robot relative to a global reference position and the robot environment representation. Both of them are embedded togther and recieved as a one piece of data to be called ***the map.*** <br/> <br/>
The code follows the standard known approach of the A-star algorithm **except its __selection criteria__ to the successor nodes.** <br/>
The standard version selection criteria simply works as 
> if that node is signed/flagged as free and it hasn't been visited before the algorithm can consider it then go to calculate its cost and proceed further.

The issue with comes when my robot starts to move diagonally !!! <br/>
It gets stuck due its size __you can figure that in by watching the videos from the links__ <br/>
To overcome that i modified the selection criteria when it comes to searching a node that's considered in a diagonal direction relative to the current node. <br/>
The modified selection criteia then works as 

> if that node is signed/flagged as free and it hasn't been visited before 
> if that node is in axial direction relative to the current one the algorithm can consider it then go to calculate its cost and proceed further.
