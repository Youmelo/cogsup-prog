from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_j, K_f
import random

""" Constants """
KEYS = [K_j, K_f]

N_BLOCKS = 8
N_TRIALS_IN_BLOCK = 16
INSTRA_SelectColor = """
Hey! You gonna pick 4 colors for the experiment.
Here the colors you can choose:
1. Red
2. Blue
3. Green
4. Yellow
5. Orange
6. Purple
7. Black
8. Pink

Just press the number key for your color. You need 4 unrepeated colors.
"""
INSTR_START = """
In this task, you have to indicate whether the meaning of a word and the color of its font match.
Press J if they do, F if they don't.\n
Press SPACE to continue.
"""
INSTR_MID = """You have finished half of the experiment, well done! Your task will be the same.\nTake a break then press SPACE to move on to the second half."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = "You are correct!"
FEEDBACK_INCORRECT = "Sorry, that was incorrect."

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait()

def select_colors():
    intro = stimuli.TextScreen(text=INSTRA_SelectColor, text_justification=0, heading="First Step to the experiment")
    intro.present()
    selected_colors = {}
    color_options = {
        '1': ("Red", (255, 0, 0)),
        '2': ("Blue", (0, 0, 255)),
        '3': ("Green", (0, 255, 0)),
        '4': ("Yellow", (255, 255, 0)),
        '5': ("Orange", (255, 165, 0)),
        '6': ("Purple", (128, 0, 128)),
        '7': ("Black", (0, 0, 0)),
        '8': ("Pink", (255, 192, 203))
    }
    while len(selected_colors) < 4:
        key,rt = exp.keyboard.wait([ord(k) for k in color_options.keys()])
        key_char = chr(key)
        color_name, rgb = color_options[key_char]
        selected_colors[color_name] = rgb
    return selected_colors
def generate_stimuli_list(selected_colors):
    stims = {
        w: {c: stimuli.TextLine(w, text_colour=selected_colors[c])
            for c in selected_colors}
        for w in selected_colors
    }
    load([stims[w][c] for w in selected_colors for c in selected_colors])
    blocks = []
    for _ in range(N_BLOCKS):
        block_trials = []
        n_match = N_TRIALS_IN_BLOCK // 2
        n_mismatch = N_TRIALS_IN_BLOCK // 2
        for _ in range(n_match):
            w = random.choice(list(selected_colors))
            block_trials.append((w, w, "match"))
        for _ in range(n_mismatch):
            w = random.choice(list(selected_colors))
            c = random.choice([x for x in selected_colors if x != w])
            block_trials.append((w, c, "mismatch"))

        random.shuffle(block_trials)
        blocks.append(block_trials)
    return stims, blocks


""" Global settings """
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

""" Experiment """
def run_trial(block_id, trial_id, trial_type, word, color):
    stim = stims[word][color]
    present_for(fixation, t=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = key == K_j if trial_type == "match" else key == K_f
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)

control.start()
selected_colors = select_colors()
stims,blocks = generate_stimuli_list(selected_colors)
present_instructions(INSTR_START)

for block_id, block in enumerate(blocks, start=1):
    for trial_id, (word, color, trial_type) in enumerate(block, start=1):
        run_trial(block_id, trial_id, trial_type, word, color)

    if block_id != N_BLOCKS:
        present_instructions(INSTR_MID)

present_instructions(INSTR_END)

control.end()