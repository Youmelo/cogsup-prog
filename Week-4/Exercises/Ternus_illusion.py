from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE  
import random

def load_stimuli(stims):
    for stim in stims:
        stim.preload()

def make_circle( pos, c_rad=50, c_color=(0, 0, 0)):
    return [stimuli.Circle(radius=c_rad, position=pos, colour=c_color)]

def add_tags(t_rad, t_color, pos):
    return [stimuli.Circle(radius = t_rad, position = pos, colour=t_color)]

def present_for(stims, t=250):
    """ Present stimulis at once for a given time."""
    t0 = exp.clock.time
    for i, stim in enumerate(stims):
        stim.present(clear=(i == 0), update=(len(stims)-1 == i))
    t1 = exp.clock.time
    exp.clock.wait(t-(t1-t0))

def move_position(positions, move_distance):
    return [(x + move_distance, y) for x, y in positions]

def create_positions(n, scale, y, move_distance, circle_distance,c_rad):
    positions_c1f1 = [(random.randint(-scale, scale)-c_rad, y) for _ in range(n)]  
    positions_c2f1 = move_position(positions_c1f1, circle_distance)
    positions_c1f2 = move_position(positions_c1f1, move_distance)
    positions_c2f2 = move_position(positions_c2f1, move_distance)
    return {"c1f1":positions_c1f1, "c2f1":positions_c2f1, "c1f2":positions_c1f2, "c2f2":positions_c2f2}

""" Test functions """
exp = design.Experiment(background_colour=(255,255,255))
control.set_develop_mode()
control.initialize(exp)

block_conditions = [{'block_id': 1, 'has_tags': False, 'isi': 100},  {'block_id': 2, 'has_tags': False, 'isi': 400},  {'block_id': 3, 'has_tags': True,  'isi': 100}]
scale = 30 # scale for random position
c_rad = 50
t_rad = 15
n = 5 # number of trials per block
y = 0 
move_distance = 100
circle_distance = 150
t1_color = (200, 0, 0)
t2_color = (0, 0, 200)
# Create Stimulus
pos_blocks = [create_positions(n, scale, y, move_distance, circle_distance,c_rad) for _ in range(3)]
for i, block in enumerate(block_conditions):
    if exp.keyboard.check(K_SPACE): # inside the loop 
         break
    current_trial_positions = pos_blocks[i]
    
    for trial in range(n):
        random_move = -1
        move_distance = random_move * move_distance
        keys = ["c1f1", "c2f1", "c1f2", "c2f2"]
        circle_stims = [make_circle(pos=current_trial_positions[key][trial], c_rad=c_rad) for key in keys]
        c1f1, c2f1, c1f2, c2f2 = circle_stims
        frame1_stims = c1f1 + c2f1
        frame2_stims = c1f2 + c2f2
        if block['has_tags']:
            colors = [t1_color, t2_color, t1_color, t2_color]
            tags = [add_tags(t_rad, colors[i], current_trial_positions[key][trial]) for i, key in enumerate(keys)]
            t1f1, t2f1, t1f2, t2f2 = tags
            frame1_stims = frame1_stims + t1f1 + t2f1
            frame2_stims = frame2_stims + t1f2 + t2f2  
        else:
            tags = []

        #Load stimuli
        load_stimuli(frame1_stims)
        load_stimuli(frame2_stims)

        #Run experiment
        present_for(frame1_stims, t=200)     
        exp.screen.clear() 
        exp.screen.update()
        exp.clock.wait(block['isi'])   

        present_for(frame2_stims, t=200)
        exp.screen.clear()
        exp.screen.update()
        exp.clock.wait(block['isi'])

control.end()

