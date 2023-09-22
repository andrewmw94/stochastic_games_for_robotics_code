import sys
import re

DEBUG = True
MIN_HUMAN_WIN = False

ABS_PATH = "/stochastic_games_for_robotics_code/icra24/tic_tac_toe/"

if DEBUG:
    # adv_file_name = "tic_tac_toe/adv.txt"
    # state_file_name = "tic_tac_toe/adv_states.txt"

    adv_file_name = ABS_PATH + "adv_strat.txt"
    state_file_name = ABS_PATH +  "adv_states.txt"
    adv_state_vals_file = ABS_PATH + "adv_state_vals.txt"

elif MIN_HUMAN_WIN:
    adv_file_name = ABS_PATH + "min_human_win_strat.txt"
    state_file_name = ABS_PATH +  "min_human_win_states.txt"
    adv_state_vals_file = ABS_PATH + "min_human_win_state_vals.txt"

else:
    # if(len(sys.argv) != 3):
    #     print("please run: python3 build_adversary adv.txt adv_states.txt")
    #     exit()
    
    adv_file_name = "str.txt"
    state_file_name = "states.txt"


    # adv_file_name = sys.argv[1]
    # state_file_name = sys.argv[2]

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

state_int_to_val = {}
line_count = 0
with open(adv_state_vals_file) as state_file:
    line = state_file.readline()
    while line:
        line = line.strip()
        state_int_to_val[line_count] = float(line)
        # keep reading until you terminate
        line = state_file.readline()
        line_count += 1


adv_str = {}
with open(adv_file_name) as adv_file:
    line = adv_file.readline()
    while line:
        line = line.strip()
        nums = line.split(":")
        # nums = nums.split(":")
        if len(nums) == 2:
            # prism_state_str = state_prism_to_real_map[int(nums[0])]
            # print(prism_state_str + " -> "+nums[1])
            adv_str[nums[0]] = nums[1]
        line = adv_file.readline() 


# roll out the game - Robot turn, and all cells are empty
curr_state = "(1,0,0,0,0,0,0,0,0,0)"
# get the initial state value
prism_state = state_real_to_prism_map[curr_state]
opt_state_val = state_int_to_val[prism_state]
done = False
rturn = True
i = 0 

while not done:
    strategy = adv_str.get(curr_state, None)

    # update the state and chekc if you are done
    if strategy == 'null' or isinstance(strategy, type(None)):
        done = True
        break

    # sanity chekcing
    if not rturn:
        assert 'human' in strategy, "Error rolling out" 

    print(f"{curr_state}; Current State Val: {opt_state_val}  ---> {strategy}")

    # The last two element are the row and columtn
    strategy_str = strategy.split("_")
    row_idx = strategy_str[-2]
    col_idx = strategy_str[-1]
    # manually introducing stovhasticity in the first robot move
    # robot stochasticity
    if i == 0 and rturn:
        row_idx = col_idx = 0
    
    # if i == 4 and rturn:
    #     row_idx = 2
    #     col_idx = 0

    # human stochasticity
    # if i == 1 and not rturn:clea
    #     row_idx = int(row_idx) + 1
    
    # # human stochasticity
    # if i == 2 and rturn:
    #     row_idx = 0
    #     col_idx = 0




    state_tuple_idx = 3 * int(row_idx) + (int(col_idx) + 1)

    # update turn
    state_list = curr_state.split(',') 
    state_list[0] = '(0' if rturn else '(1'
    state_list[state_tuple_idx] = '1' if rturn else '2'

    if ')' in state_list[-1]:
        nxt_state = ",".join(state_list)
    else:
        nxt_state = ",".join(state_list)
        nxt_state += ')'

    rturn = not rturn
    curr_state = nxt_state
    prism_state = state_real_to_prism_map[curr_state]
    opt_state_val = state_int_to_val[prism_state]

    # update counter
    i += 1

