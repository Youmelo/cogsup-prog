import expyriment as exp

### Global settings
exp.control.set_develop_mode(True) 
exp_edge = exp.design.Experiment(name = "Display Edges", background_colour=(128,128,128)) #A class implementing a basic experiment
exp.control.initialize(exp_edge)

exp_edge.screen.clear()
### Stimuli and Design(trial & block struture)
#Parameters
width, height = exp_edge.screen.size  #Get the size of the screen
circle_r = width*0.05
x = circle_r + width//16
y = circle_r + width//16
rect_r = [width//4, width//4]
positions = [( x,  y), ( x, -y), (-x,  y), (-x, -y)] #Set the position of the rectangle to be in the center of the screen
nums = [0,1,2,3]
colors = [(0,0,0), (255,255,255), (0,0,0), (255,255,255)]
circles = [None]*4

#Set stimuli-circles
for num, position, colors in zip(nums, positions, colors):
    circles[num] = exp.stimuli.Circle(
        radius=circle_r, 
        colour=colors, 
        position=position) 
#Set rectangle
rectangle = exp.stimuli.Rectangle(
    size = rect_r,
    colour =(128,128,128))

#Present stimuli
for num in nums:
    circles[num].present(clear=False, update=False) 
    
rectangle.present(clear=False, update=False)

exp_edge.screen.update() #Update the screen

### Input
exp_edge.keyboard.wait()

exp.control.end()
