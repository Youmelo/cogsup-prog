import expyriment as exp

### Global settings
exp.control.set_develop_mode(True) 
exp_edge = exp.design.Experiment(name = "Display Edges") #A class implementing a basic experiment
exp.control.initialize(exp_edge)

### Stimuli and Design(trial & block struture)
#Parameters
width, height = exp_edge.screen.size  #Get the size of the screen
cube_r = width*0.05
x = width//2 - cube_r//2
y = height//2 - cube_r//2
cube_positions = [( x,  y), ( x, -y), (-x,  y), (-x, -y)] #Set the position of the rectangle to be in the center of the screen
cube_num = [0,1,2,3]
cubes = [None]*4
#Create stimuli
for num, position in zip(cube_num, cube_positions):
    cubes[num] = exp.stimuli.Rectangle(
        size=(cube_r,cube_r), 
        colour=(255, 0, 0), 
        position=position, 
        line_width=1) #Create a rectangle stimulus the size of the screen
#Present stimuli
for num in cube_num:
    cubes[num].present(clear=False, update=False) 

exp_edge.screen.update() #Update the screen

### Input
exp_edge.keyboard.wait()

exp.control.end()
