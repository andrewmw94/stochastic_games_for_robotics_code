import sys
import re


only_print_desired_actions = True

if(len(sys.argv) != 3):
    print("please run: python3 build_adversary adv.txt adv_states.txt")
    exit()


adv_file_name = sys.argv[1]
state_file_name = sys.argv[2]

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


with open(adv_file_name) as adv_file:
    line = adv_file.readline()
    while line:
        nums = line.split()
        if len(nums) == 2:
            prism_state_str = state_prism_to_real_map[int(nums[0])]
            print(prism_state_str + " -> "+nums[1])
        line = adv_file.readline()
        