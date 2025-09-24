import expyriment as exp

def draw_kanizsa_square(r_ratio, r_scale, c_scale): 
    #r_ratio: height = weight * r_ratio
    #r_scale: size of rectangle relative to screen width; 
    #c_scale: size of circles relative to screen width
    #Parameters
    width, height = exp_edge.screen.size
    circle_r = width*r_scale
    rect_x = width*c_scale
    rect_y = rect_x * r_ratio
    rect_r = [rect_x, rect_y]
    x = circle_r + rect_x//4
    y = circle_r + rect_y//4
    positions = [(x,y), (x,-y), (-x,y), (-x,-y)]
    nums = [0,1,2,3]        
    colors = [(0,0,0), (255,255,255), (0,0,0), (255,255,255)]
    circles = [None]*4      
    #Set Circles
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
    
    exp_edge.screen.update()

### Global settings
exp.control.set_develop_mode(True) 
exp_edge = exp.design.Experiment(name = "Display Edges", background_colour=(128,128,128)) #A class implementing a basic experiment
exp.control.initialize(exp_edge)

exp_edge.screen.clear()

### Stimuli and Design(trial & block struture)

draw_kanizsa_square(0.6, 0.05, 0.25) 

### Input
exp_edge.keyboard.wait()

exp.control.end()


    

