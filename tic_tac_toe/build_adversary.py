import sys
import re

DEBUG = False
only_print_desired_actions = True

if DEBUG:
    adv_file_name = "tic_tac_toe/adv.txt"
    state_file_name = "tic_tac_toe/adv_states.txt"
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
state = "(1,0,0,0,0,0,0,0,0,0)"
done = False
rturn = True

while not done:
    strategy = adv_str.get(state, None)

    # update the state and chekc if you are done
    if strategy == 'null' or isinstance(strategy, type(None)):
        done = True
        break

    # sanity chekcing
    if not rturn:
        assert 'human' in strategy, "Error rolling out" 

    print(f"{state} -> {strategy}")

    # The last two element are the row and columtn
    strategy_str = strategy.split("_")
    row_idx = strategy_str[-2]
    col_idx = strategy_str[-1]
    state_tuple_idx = 3 * int(row_idx) + (int(col_idx) + 1)

    # update turn
    state_list = state.split(',') 
    state_list[0] = '(0' if rturn else '(1'
    state_list[state_tuple_idx] = '1' if rturn else '2'

    state = ",".join(state_list)
    rturn = not rturn

