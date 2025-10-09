from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_LEFT, K_RIGHT
import random
""" Global settings """
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)
intro = "In this experiment, you will see a series of color words\nYour task is to indicate\nwhether the color of the word matches the word itself\nPress ←  key if they match\n Press → if they mismatch"
COLORS = {
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0),
    "Orange": (255, 165, 0),
}
def make_color_block(n_trials):
    block_trials=[]
    for _ in range(n_trials):
        is_match = random.choice([True, False])
        word = random.choice(list(COLORS.keys()))
        if is_match:
            color = COLORS[word]
        else:
            color = COLORS[random.choice([c for c in COLORS.keys() if c != word])]

        stim = stimuli.TextLine(word, position=(0,0), text_colour=color, text_size=30)
        block_trials.append((is_match, word, color, stim))
    return block_trials

def load(stims): 
    for stim in stims:
        stim.preload()

def run_trial():
    key_record = ""
    for block in range(2):
        num_trial = 0
        trials = make_color_block(5)
        load([t[3]for t in trials]) 
        fixation = stimuli.FixCross(size=(50, 50), line_width=10, position=(0,0), colour=C_BLACK)
        fixation.preload()
        for ismatch, word, color, stim in trials:
            fixation.present()
            exp.clock.wait(500)
            num_trial += 1
            accuracy = None
            stim.present()
            t0 = exp.clock.time
            key,_ = exp.keyboard.wait(keys=[K_LEFT, K_RIGHT])
            t1 = exp.clock.time
            
            print(key)
            print(key == K_LEFT)
            RT = t1 - t0
            if key == K_LEFT:
                key_record = "Left"
                accuracy = ismatch

            elif key == K_RIGHT:
                key_record = "Right"
                accuracy = not ismatch

            if (accuracy):
                stimuli.TextLine(text="Correct!Press any key to continue",position=(0,0),text_colour=(0,255,0)).present()
                exp.keyboard.wait()
            else:
                stimuli.TextLine(text="Incorrect!Press any key to continue",position=(0,0),text_colour=(255,0,0)).present()
                exp.keyboard.wait()
            exp.data.add([block, num_trial, ismatch, word, color, key_record, RT, accuracy])
   
exp.add_data_variable_names(["block","trial","match","word","color","Response", "RT","Accuracy"])
control.start(subject_id=1)

intro_1 = stimuli.TextScreen("WELCOME TO TEST", intro)
intro_1.present()
exp.keyboard.wait()

run_trial()    
control.end()