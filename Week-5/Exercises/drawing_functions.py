from expyriment import design, control, stimuli
import random
FPS = 60 # frames per second
MSPF = 1000/FPS # milliseconds per framea(more robust than using 16.67as it's accurate and easy to modify)
def to_frames(t):
    return t / MSPF #(frames in given time t)

def to_time(frames):
    return frames * MSPF #(time in given frames)

def load(stims): 
    for stim in stims:
        stim.preload()

def timed_draw(stims):
    t0 = exp.clock.time
   
    for i, stim in enumerate(stims):
        stim.present(clear=(i == 0), update=(len(stims)-1 == i))
    
    t1 = exp.clock.time
    return t1-t0
    # return the time it took to draw

def present_for(stims, num_frames):# num_frames = 60 = 1000ms
    if num_frames == 0: #if num_frames = 0, no need to present anything
        return
    dt = timed_draw(stims)
    if dt > 0:
        t = to_time(num_frames) # convert frames to time
        exp.clock.wait(t-dt)    


""" Test functions 
exp = design.Experiment()

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
load([fixation])

n = 20
positions = [(random.randint(-300, 300), random.randint(-300, 300)) for _ in range(n)]
squares = [stimuli.Rectangle(size=(50, 50), position = pos) for pos in positions]
load(squares)

durations = []

t0 = exp.clock.time
for square in squares:
    if not square.is_preloaded:
        print("Preloading function not implemneted correctly.")
    stims = [fixation, square] 
    present_for(stims, 12)
    t1 = exp.clock.time
    durations.append(t1-t0)
    t0 = t1

print(durations)

control.end()
"""