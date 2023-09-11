import sys
import re
import numpy as np

# from numpy.radom import normal

DEBUG = True
COOP_STR = False
ADV_STR = False
MIN_ACTION = True
only_print_desired_actions = True

ROBOT_GRIPPER = 0
HUMAN_GRIPPER = 1

# Set this flag to true if it is a Prob human 
PROB_TERM = True
ADD_HUMAN_STOCHASTICITY = True


# Command: prism-games dl_model.prism spec.props -exportstrat strt.txt -exportstates states.txt

if DEBUG and COOP_STR:
    str_file_name = "manipulation_w_deadlock/coop_strt.txt"
    state_file_name = "manipulation_w_deadlock/states.txt"
elif DEBUG and ADV_STR:
    str_file_name = "manipulation_w_deadlock/adv_strt.txt"
    state_file_name = "manipulation_w_deadlock/states.txt"
elif DEBUG and MIN_ACTION:
    str_file_name = "manipulation_w_deadlock/min_action_strt.txt"
    state_file_name = "manipulation_w_deadlock/min_action_states.txt"
else:
    adv_file_name = "str.txt"
    state_file_name = "states.txt"

state_prism_to_real_map={}
state_real_to_prism_map={}
with open(state_file_name) as state_file:
    line = state_file.readline()
    while line:
        index = line.find(":")
        if index != -1:
            state_num = int(line[: index])
            state_name = line[index+1 : -1]
            state_prism_to_real_map[state_num] = state_name
            state_real_to_prism_map[state_name] = state_num
        else:
            print("# " + line[:-1])


        # nums = [int(s) for s in re.findall(r'\d+', line)]
        # if len(nums) == 3:#prism_index, dfa_index, mdp_index
        #     state_prism_to_real_map[nums[0]] = [nums[2], nums[1]]
        #     state_real_to_prism_map[nums[2]] = [nums[0]]
        line = state_file.readline()

    # print(state_prism_to_real_map)

adv_str = {}
with open(str_file_name) as adv_file:
    line = adv_file.readline()
    while line:
        line = line.strip()
        nums = line.split(":")
        # nums = nums.split(":")
        if len(nums) == 2:
            # prism_state_str = state_prism_to_real_map[int(nums[0])]
            # print(prism_state_str + " -> "+nums[1])
            # if MIN_ACTION:
            #     # split further
            #     min_act_nums = nums[0].split('),')
            #     adv_str[min_act_nums[0]+")"] = nums[1]

            # else:
            adv_str[nums[0]] = nums[1]
        line = adv_file.readline() 


# roll out the game
state = "(2,2,1,2,3)"
goalstate = '(4,4,1,2,3)'
TERM_LOC = '4'
done = False
rturn = True

while not done:
    strategy = adv_str.get(state, None)

    # update the state and chekc if you are done
    if strategy == 'null' or isinstance(strategy, type(None)) or state == goalstate:
        done = True
        break

    # sanity chekcing
    if not rturn:
        assert 'human' in strategy, "Error rolling out" 

    # add stochasticity to human action 
    if not rturn and ADD_HUMAN_STOCHASTICITY and 0.6 < np.random.normal():
        # roll a dice and 
        strategy = "humanchooseterm"
    
    print(f"{state} -> {strategy}")

    # The last two element are the row and columtn
    strategy_str = strategy.split("_")

    # parse the tuple of string so that it easier to update
    state_list = state.split(',')

    if "grasp" in strategy_str[0]:
        # update the
        tuple_idx = 3 + int(strategy_str[1])
        if "robot" in strategy_str[0]:
            state_list[tuple_idx] = str(ROBOT_GRIPPER)
        else:
            state_list[tuple_idx] = str(HUMAN_GRIPPER)
        
        # if it is the last object add the trailing bracket else no
        if tuple_idx == len(state_list) - 1:
            state_list[tuple_idx] += ")" 
            
    elif "motion" in strategy_str[0]:
        if "robot" in strategy_str[0]:
            state_list[0] =  "("+strategy_str[1]
        else:
            state_list[1] =  strategy_str[1]
    
    elif "place" in strategy_str[0]:
        if "robot" in strategy_str[0]:
            gripper_loc = state_list[0][1:]
            try:
                obj_idx = state_list.index('0')
                state_list[obj_idx] = gripper_loc
            except:
                obj_idx = state_list.index('0)')
                state_list[obj_idx] = gripper_loc + ")"

        else:
            human_hand_loc = state_list[1]
            try:
                obj_idx = state_list.index('1')
                state_list[obj_idx] = human_hand_loc
            except:
                obj_idx = state_list.index('1)')
                state_list[obj_idx] = human_hand_loc + ")"

    elif "selfloop" in strategy_str[0]:
        if "human" in strategy_str[0]:
            # if human has object in hand then return it loc 2. <- hardcoded in the abstraction file.
            if '1' in state_list:
                # find the obj index and update its location
                try:
                    obj_idx = state_list.index('1')
                    state_list[obj_idx] = '2'
                except:
                    obj_idx = state_list.index('1)')
                    state_list[obj_idx] = '2)'


    elif "chooseterm" in strategy_str[0]:
        if "robot" in strategy_str[0]:
            state_list[0] = "("+TERM_LOC
        else:
            state_list[1] = TERM_LOC

    # update turn
    state_list[2] = '0' if rturn else '1'

    state = ",".join(state_list)
    rturn = not rturn

