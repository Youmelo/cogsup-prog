from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_LEFT, K_RIGHT, K_RETURN, K_1, K_2, K_l, K_r


""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

MOVE = 10; SIZE = 5; MAX_RADIUS = 150; MIN_RADIUS = 5
Instruction_1 = """Choose which eye to test First\nPress Key 'L' for left eye\nPress Key 'R' for right eye
                    """
Instruction_2 = """Only Open the eye you are testing.\n
                Keep your head still and focus on the cross.\n
                Press the LEFT or RIGHT arrow key to move the wcircle.\n
                Press '1' or '2'to decrease/ increase the size of the circle.\n
                Press 'Enter' when you can no longer see the circle.\n
                Press any key to start.
                """
"""Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c
def update_screen(fixation,circle):
    fixation.present(clear=True, update=False)
    circle.present(clear=False, update=True)

""" Experiment """
def run_trial(key_eye):
    key_record = ""
    radius = 75
    pos_now = (0,0)
    fix_pos = (0,0)
    key_eye = key_eye
    if key_eye == K_l:
        fix_pos = (300, 0)
        eye = 0
    if key_eye == K_r:
        fix_pos = (-300, 0)
        eye = 1
    intro_2 = stimuli.TextScreen("INSTRUCTION", Instruction_2)
    intro_2.present()
    exp.keyboard.wait()
    
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=fix_pos)
    fixation.preload()
    circle = make_circle(radius)
    
    fixation.present(True, False)
    circle.present(False, True)
    
    exp.add_data_variable_names(["eye(0-left,1-right)","key","radius","x_coord","y_coord"])
    
    while True:
        key = exp.keyboard.check()
        if key:
            if key == K_RETURN:
                break
                
            elif key == K_RIGHT:
                circle.move((MOVE, 0))
                update_screen(fixation, circle)
                pos_now = circle.position
                key_record = "Right"
                exp.data.add([eye,key_record,radius,pos_now[0], pos_now[1]])
            elif key == K_LEFT:
                circle.move((-MOVE, 0))
                update_screen(fixation, circle)
                pos_now = circle.position
                key_record = "Left"
                exp.data.add([eye,key_record,radius,pos_now[0], pos_now[1]])
            elif key == K_1:
                radius = max(MIN_RADIUS, radius - SIZE)
                circle = make_circle(radius, pos_now)
                update_screen(fixation, circle)
                key_record = "Smaller"
                exp.data.add([eye,key_record,radius,pos_now[0], pos_now[1]])
            elif key == K_2:
                radius = min(MAX_RADIUS, radius + SIZE)
                circle = make_circle(radius + SIZE, pos_now)
                update_screen(fixation, circle)
                key_record = "Larger"
                exp.data.add([eye,key_record,radius,pos_now[0], pos_now[1]])              
    
    exp.data.add([eye,"end",radius, pos_now[0], pos_now[1]])

control.start(subject_id=1)
intro_1 = stimuli.TextScreen("WELCOME TO BLIND SPOT TEST", Instruction_1)
intro_1.present()
key_eye,_ = exp.keyboard.wait(keys = [K_l, K_r])
run_trial(key_eye)
run_trial(K_l + K_r - key_eye) # run the other eye
    
control.end()