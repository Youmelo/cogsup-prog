import expyriment as exp

def draw_Hermann_grid(sq_size, space, n_rows, n_cols,sq_color, bg_color): 
    #sq_size: size = sq_size * width
    #space: space = space * width 
    exp_hermann = exp.design.Experiment(
        name = "Hermann Grid", 
        background_colour=bg_color)
    exp.control.initialize(exp_hermann)
    exp_hermann.screen.clear()

    #Parameters
    width, height = exp_hermann.screen.size
    r = width * sq_size
        #size
    rect_r = [r,r]
        #position!
    space = space * width
    d = r + space
    sum_h = space//2 + n_rows*d
    sum_w = space//2 + n_cols*d
        #check if parameters fit the screen
    if sum_h > height or sum_w > width:
        print("NO!! YOU REQUIRE TOO MUCH! Too many rows or columns, or size/space too large here")
        return 
        #position for 1st quadrant
    y = space//2 + r//2 # when row = 1
    for i in range(n_rows): 
        x = space//2 + r//2 # when col = 1
        for j in range(n_cols):
         # copy to 4 quadrants
            positions = [(x,y), (x,-y), (-x,y), (-x,-y)]
            nums = [0,1,2,3]        
            cube = [None]*4
            for num, position in zip(nums, positions):
                cube[num] = exp.stimuli.Rectangle(
                size = rect_r,
                colour= sq_color, 
                position = position)
                cube[num].present(clear=False, update=False)
            x = x + d #update x for next column
        y = y + d #update y for next row

    exp_hermann.screen.update()
    exp_hermann.keyboard.wait()

### RUN!!!
exp.control.set_develop_mode(True) 
draw_Hermann_grid(0.05, 0.01, 5, 5, (255,255,255), (0,0,0))


exp.control.end()


    

