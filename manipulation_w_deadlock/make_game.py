from enum import Enum

CONCURRENT_GAME = False
NUM_LOCS = 5
ROBOT_GRIPPER = 0
HUMAN_GRIPPER = 1
TERM_LOC = NUM_LOCS-1
NUM_OBJS = 1

# The first |SMALL_OBJ| objects are small boxes and the rest a re normal (tall) objects
SMALL_OBJ = 1


IMPORTABLE = False
# HUMAN_TERM_PROB = 0.05  # Probaibility of human intervening
ROBOT_FAIL_PROB = 0.05  # 5% probaility of failing 
HUMAN_TERM_PROB = 0.05


class HumanIntProb(Enum):
    # Locs l2, l3, l4, l5 - Human Near region
    # human intervention probability for closer locs is constant and set to 50%
    # human intervention probability for farther locs is constants and set to 20%
    HUMAN_INT_L2 = 0.5
    HUMAN_INT_L3 = 0.5
    HUMAN_INT_L4 = 0.5
    HUMAN_INT_L5 = 0.5

    # Locs l6, l7, l8, - Human Far region
    HUMAN_INT_L6 = 0.2
    HUMAN_INT_L7 = 0.2
    HUMAN_INT_L8 = 0.2

class Transition:
    action=""
    prob_distr = [] # list of <new state, probability>

    def __init__(self, tpl_list):
        self.action=""
        self.prob_distr=tpl_list

class State:
    robot_loc=2
    human_loc=2
    robot_turn=False
    obj_locs=[]
    neighbors = []
    transitions = [] # list of transitions

    def __init__(self):
        self.robot_loc=2
        self.human_loc=2
        self.robot_turn=False
        self.obj_locs=[]
        self.neighbors=[]
        self.transitions=[]

    def toInt(self):
        r = 0
        power = 1
        for i in range(len(self.obj_locs)):
            r = r + self.obj_locs[i] * power
            power = power*NUM_LOCS
        r += self.robot_loc * power
        power *= NUM_LOCS
        r += self.human_loc * power
        power *= NUM_LOCS
        if self.robot_turn:
            r += power
        return r

    def toPrismStr(self, primed):
        if primed:
            rturn = 0
            if self.robot_turn:
                rturn = 1
            str = "(rloc'={}) & ".format(self.robot_loc)+"(hloc'={}) & ".format(self.human_loc)+"(rturn'={}) & ".format(rturn)
            for i in range(NUM_OBJS):
                str+="(o{}'={}) & ".format(i,self.obj_locs[i])
            return str[:-2]
        else:
            rturn = 0
            if self.robot_turn:
                rturn = 1
            str = "(rloc={}) & ".format(self.robot_loc)+"(hloc={}) & ".format(self.human_loc)+"(rturn={}) & ".format(rturn)
            for i in range(NUM_OBJS):
                str+="(o{}={}) & ".format(i,self.obj_locs[i])
            return str[:-2]

    def toTplStr(self, primed):
        t=0
        if self.robot_turn:
            t=1
        my_str="("+str(self.robot_loc)+","+str(self.human_loc)+","+str(t)
        for i in range(NUM_OBJS):
            my_str=my_str+","+str(self.obj_locs[i])
        my_str = my_str+")"
        return my_str



def genNeighbors(state):
    ret = []
    if state.robot_turn and state.robot_loc == TERM_LOC:
        s_prime=State()
        s_prime.robot_loc=state.robot_loc
        s_prime.human_loc=state.human_loc
        s_prime.obj_locs=state.obj_locs.copy()
        state.neighbors = [s_prime]
        state.transitions = [Transition([(s_prime,1.0)])]
        state.transitions[-1].action="robottermselfloop"
        s_prime.robot_turn = False
        ret.append(s_prime)
        return ret
    # if human in termnial state and object in human hand then return it
    elif not state.robot_turn and state.human_loc == TERM_LOC:
        s_prime=State()
        s_prime.robot_loc=state.robot_loc
        s_prime.human_loc=state.human_loc
        s_prime.obj_locs=state.obj_locs.copy()
        for i in range(len(s_prime.obj_locs)):
            if s_prime.obj_locs[i] == HUMAN_GRIPPER:
                s_prime.obj_locs[i] = 2
        state.neighbors = [s_prime]
        state.transitions = [Transition([(s_prime,1.0)])]
        state.transitions[-1].action="humantermselfloop"
        s_prime.robot_turn = True
        ret.append(s_prime)
        return ret

    # moving
    for i in range(2,NUM_LOCS): 
        # Skip the terminal transition if the human is holding an object
        if i == TERM_LOC and (not state.robot_turn) and any(ol == HUMAN_GRIPPER for ol in state.obj_locs):
            continue

        s_prime=State()
        already_there = False
        if state.robot_turn:
            if state.robot_loc == i:
                already_there = True
            s_prime.robot_loc=i
            s_prime.human_loc=state.human_loc
        else:
            if state.human_loc == i:
                already_there = True
            s_prime.robot_loc=state.robot_loc
            s_prime.human_loc=i
        
        s_prime.obj_locs = state.obj_locs.copy()
        s_prime.robot_turn = not state.robot_turn
        ret.append(s_prime)
        state.neighbors.append(s_prime)

        if state.robot_turn:
            if already_there:
                state.transitions.append(Transition([(s_prime, 1)]))
                state.transitions[-1].action="robotnoop"
            # add non-zero probaility of robot going to terinal state    
            else:
                # if it is already already going to temrinal state
                if i == TERM_LOC:
                    state.transitions.append(Transition([(s_prime, 1)]))
                else:
                    # if there is a small object in hand then add transition to terminal state
                    if (0 in s_prime.obj_locs and s_prime.obj_locs.index(0) < SMALL_OBJ):
                        s_prime2 = State()
                        s_prime2.robot_loc = TERM_LOC
                        s_prime2.human_loc = state.human_loc
                        s_prime2.obj_locs = state.obj_locs.copy()
                        s_prime2.robot_turn = not state.robot_turn
                        ret.append(s_prime2)
                        state.neighbours.append(s_prime2)
                        state.transitions.append(Transition([(s_prime, 1- ROBOT_FAIL_PROB), (s_prime2, ROBOT_FAIL_PROB)]))

                    # if hand is empty and moving to small box then add transition to terminal state
                    elif (0 not in s_prime.obj_locs and (i in s_prime.obj_locs and s_prime.obj_locs.index(i) < SMALL_OBJ)):
                        s_prime2 = State()
                        s_prime2.robot_loc = TERM_LOC
                        s_prime2.human_loc = state.human_loc
                        s_prime2.obj_locs = state.obj_locs.copy()
                        s_prime2.robot_turn = not state.robot_turn
                        ret.append(s_prime2)
                        state.neighbours.append(s_prime2)
                        state.transitions.append(Transition([(s_prime, 1- ROBOT_FAIL_PROB), (s_prime2, ROBOT_FAIL_PROB)]))
                    
                    else:
                        state.transitions.append(Transition([(s_prime, 1)]))
                state.transitions[-1].action="robotmotion"

                    
        else:
            # don't create two transitions to human term:
            if s_prime.human_loc==TERM_LOC:
                state.transitions.append(Transition([(s_prime, 1)]))
                state.transitions[-1].action="humanchooseterm"
            else:
                s_prime2=State()
                s_prime2.robot_loc=state.robot_loc
                s_prime2.human_loc=TERM_LOC
                s_prime2.obj_locs = state.obj_locs.copy()
                s_prime2.robot_turn = not state.robot_turn
                ret.append(s_prime2)
                state.neighbors.append(s_prime2)
                state.transitions.append(Transition([(s_prime,1 - HUMAN_TERM_PROB),(s_prime2, HUMAN_TERM_PROB)]))
                # state.transitions.append(Transition([(s_prime,1-HUMAN_TERM_PROB)]))
                if already_there:
                    state.transitions[-1].action="humannoop"
                else:
                    state.transitions[-1].action="humanmotion"
    
    # grasping and placing require empty/full hands
    grasped_index = -1
    if state.robot_turn:
        for i in range(NUM_OBJS):
            if state.obj_locs[i] == ROBOT_GRIPPER:
                grasped_index = i
    else:
        for i in range(NUM_OBJS):
            if state.obj_locs[i] == HUMAN_GRIPPER:
                grasped_index = i

    # grasping
    if grasped_index == -1:
        loc_of_interest = -1
        if state.robot_turn:
            loc_of_interest = state.robot_loc
        else:
            loc_of_interest = state.human_loc
        movable_obj_indices = []
        hand_free = True
        for i in range(NUM_OBJS):
            if state.obj_locs[i] == loc_of_interest:
                movable_obj_indices.append(i)
            if state.robot_turn and state.obj_locs[i] == ROBOT_GRIPPER:
                hand_free = False
            elif not state.robot_turn and state.obj_locs[i] == HUMAN_GRIPPER:
                hand_free = False

        if hand_free:       
            for i in movable_obj_indices:
                s_prime=State()
                s_prime.robot_loc=state.robot_loc
                s_prime.human_loc=state.human_loc
                s_prime.obj_locs = state.obj_locs.copy()
                if state.robot_turn:
                    s_prime.obj_locs[i] = ROBOT_GRIPPER
                else:
                    s_prime.obj_locs[i] = HUMAN_GRIPPER
                s_prime.robot_turn = not state.robot_turn
                ret.append(s_prime)
                state.neighbors.append(s_prime)
                if state.robot_turn:
                    s_prime2=State()
                    s_prime2.robot_loc=state.robot_loc
                    s_prime2.human_loc=state.human_loc
                    s_prime2.obj_locs = state.obj_locs.copy()
                    s_prime2.robot_turn = not state.robot_turn
                    ret.append(s_prime2)
                    state.neighbors.append(s_prime2)
                    state.transitions.append(Transition([(s_prime,0.9), (s_prime2,0.1)]))
                    state.transitions[-1].action="robotgrasp"
                else:
                    # state.transitions.append(Transition([(s_prime,1-HUMAN_TERM_PROB)]))
                    # state.transitions[-1].action="humangrasp"
                    s_prime2=State()
                    s_prime2.robot_loc=state.robot_loc
                    s_prime2.human_loc=TERM_LOC
                    s_prime2.obj_locs = state.obj_locs.copy()
                    s_prime2.robot_turn = not state.robot_turn
                    ret.append(s_prime2)
                    state.neighbors.append(s_prime2)
                    state.transitions.append(Transition([(s_prime,1 - HUMAN_TERM_PROB),(s_prime2, HUMAN_TERM_PROB)]))
                    state.transitions[-1].action="humangrasp"

    # placing   
    else:
        s_prime=State()
        s_prime.robot_loc=state.robot_loc
        s_prime.human_loc=state.human_loc
        s_prime.obj_locs = state.obj_locs.copy()
        if state.robot_turn:
            s_prime.obj_locs[grasped_index] = state.robot_loc
        else:
            s_prime.obj_locs[grasped_index] = state.human_loc
        s_prime.robot_turn = not state.robot_turn
        ret.append(s_prime)
        state.neighbors.append(s_prime)
        if state.robot_turn:
            state.transitions.append(Transition([(s_prime,1)]))
            state.transitions[-1].action="robotplace"
        else:
            s_prime2=State()
            s_prime2.robot_loc=state.robot_loc
            s_prime2.human_loc=TERM_LOC
            s_prime2.obj_locs = state.obj_locs.copy()
            s_prime2.robot_turn = not state.robot_turn
            ret.append(s_prime2)
            state.neighbors.append(s_prime2)
            state.transitions.append(Transition([(s_prime,1-HUMAN_TERM_PROB),(s_prime2,HUMAN_TERM_PROB)]))
            # state.transitions.append(Transition([(s_prime,1-HUMAN_TERM_PROB)]))
            state.transitions[-1].action="humanplace"

    # #At every human turn, there is a probability of human termination
    # if not state.robot_turn:
    #     s_prime=State()
    #     s_prime.robot_loc=state.robot_loc
    #     s_prime.human_loc=TERM_LOC
    #     s_prime.obj_locs = state.obj_locs.copy()
    #     s_prime.robot_turn = not state.robot_turn
    #     ret.append(s_prime)
    #     state.neighbors.append(s_prime)
    #     state.transitions.append(Transition([(s_prime,HUMAN_TERM_PROB)]))

    for n in ret:
        if state.robot_turn == n.robot_turn:
            print("ERROR, the turn didn't alternate=================================================================================")

    for n in state.neighbors:
        if state.robot_turn == n.robot_turn:
            print("ERROR, the turn didn't alternate=================================================================================")

    for t in state.transitions:
        for s_prime, prob in t.prob_distr:
            if state.robot_turn == s_prime.robot_turn:
                print("ERROR, the turn didn't alternate=================================================================================")
                print(len(state.transitions))

    return ret


def genGame(initial_state):
    s = initial_state

    visited_states = {s.toInt():s}
    curr_frontier = []
    all_states = []


    curr_frontier.append(s)

    while(len(curr_frontier) > 0):
        #remove state from frontier and add to visited states
        s = curr_frontier[-1]
        curr_frontier.pop()
        my_tpl = {s.toInt() : s}
        visited_states.update(my_tpl)
        all_states.append(s)
        #check all neighbors and add new ones to frontier
        neighbors = genNeighbors(s)
        for n in neighbors:
            if s.robot_turn == n.robot_turn:
                print("ERROR, the turn didn't alternate=================================================================================")

            if n.toInt() in visited_states:
                if visited_states[n.toInt()].robot_turn != n.robot_turn or visited_states[n.toInt()].human_loc != n.human_loc or visited_states[n.toInt()].robot_loc != n.robot_loc or visited_states[n.toInt()].obj_locs[0] != n.obj_locs[0]:
                    print("ERROR, the hash function doesn't work==================================================================================================")
                # pass
            else:
                curr_frontier.append(n)
    return all_states

def print_front_matter():
    if CONCURRENT_GAME:
        print("csg")
    else:
        print("smg")
    
    print("player r1")
    print("  robot, [robotnoop], [robotmotion], [robotplace], [robotgrasp], [robottermselfloop]")
    print("endplayer")

    print("player h1")
    print("  human, [humannoop], [humanmotion], [humanplace], [humangrasp], [humantermselfloop]")
    print("endplayer")

def print_global_vars():
    print("global rloc: [2..{}] init 2;".format(NUM_LOCS-1))
    print("global hloc: [2..{}] init 2;".format(NUM_LOCS-1))
    if not CONCURRENT_GAME:
        print("global rturn: [0..1] init 0;")
    for i in range(NUM_OBJS):
        print("global o{}: [0..{}] init 2;".format(i, TERM_LOC-1))

def print_robot_module(game, state_to_int_map):
    print("module robot")
    for s in game:
        if s.robot_turn:
            for t in s.transitions:
                string = ""
                for s_prime, prob in t.prob_distr:
                    string += " {}: {} +".format(prob, s_prime.toPrismStr(True))
                print("    [{}] ".format(t.action)+s.toPrismStr(False)+" -> "+string[:-2]+";")
    print("endmodule")


def print_human_module(game, state_to_int_map):
    print("module human")
    for s in game:
        if not s.robot_turn:
            for t in s.transitions:
                string = ""
                for s_prime, prob in t.prob_distr:
                    string += " {}: {} +".format(prob, s_prime.toPrismStr(True))
                print("    [{}] ".format(t.action)+s.toPrismStr(False)+" -> "+string[:-2]+";")
    print("endmodule")

def print_labels():
    print("label \"goalterm\" = (rloc={}) & (hloc={});".format(TERM_LOC,TERM_LOC))
    goal_string = ""
    for i in range(NUM_OBJS):
        goal_string += "(o{}={}) &".format(i, i+2)
    print("label \"goalcleaned\" = "+goal_string[:-2]+";")

def print_rewards():
    print("rewards")
    print("    true : 1;")
    print("endrewards")

def sat_goal(obj_locs):
    for i in range(NUM_OBJS):
        if obj_locs[i] != i+2:
            return False
    return True

def write_tra_file(game, state_to_int_map, og_state_to_int_map, int_to_state_map, num_choices, num_transitions, filename):
    with open(filename, "w") as f:
        f.write(str(len(state_to_int_map))+" "+str(num_choices)+ " "+str(num_transitions)+"\n")
        for s, i in state_to_int_map.items():
            for j in range(len(s.transitions)):
                t = s.transitions[j]
                for s_prime, p in t.prob_distr:
                    f.write(str(i) + " " + str(j) + " " + (str(og_state_to_int_map[s_prime.toInt()]) + " " + str(p) + " "+t.action+"\n"))

def write_sta_file(game, state_to_int_map, filename):
    with open(filename, "w") as f:
        my_str = ""
        for i in range(NUM_OBJS):
            my_str=my_str+",o"+str(i)
        f.write("(rloc,hloc,rturn"+my_str+")\n")
        for s, i in state_to_int_map.items():
            f.write(str(i)+":"+s.toTplStr(False)+"\n")

def write_lab_file(game, state_to_int_map, filename):
    with open(filename, "w") as f:
        f.write("0=\"init\" 1=\"deadlock\" 2=\"goalterm\" 3=\"goalcleaned\"\n")
        for s, i in state_to_int_map.items():
            my_str = ""
            if i == 0:
                my_str=my_str+" 0"
            if len(s.transitions) == 0:
                my_str=my_str+" 1"
            if s.robot_loc == TERM_LOC and s.human_loc == TERM_LOC:
                my_str=my_str+" 2"
            if sat_goal(s.obj_locs):
                my_str=my_str+" 3"
            if len(my_str) > 0:
                f.write(str(i)+":"+my_str+"\n")


def write_pla_file(game, state_to_int_map, filename):
    with open(filename, "w") as f:
        f.write(str(len(state_to_int_map))+"\n")
        for s, i in state_to_int_map.items():
            p = 1
            if not s.robot_turn:
                p = 2
            f.write(str(i)+":"+str(p)+"\n")

def write_rew_file(game, state_to_int_map, filename):
    with open(filename, "w") as f:
        f.write(str(len(state_to_int_map))+" "+str(len(state_to_int_map))+"\n")
        for s, i in state_to_int_map.items():
            f.write(str(i)+" 1\n")


initial_state=State()
initial_state.robot_loc = 2
initial_state.human_loc = 2
initial_state.obj_locs=[2]*NUM_OBJS
initial_state.robot_turn=False

game = genGame(initial_state)

state_to_int_map={initial_state.toInt():0}
real_state_to_int_map={initial_state:0}
int_to_state_map={0:initial_state}
counter = 1
num_prism_choices = 0
num_prism_transitions = 0
for s in game:
    if not (s.toInt() in state_to_int_map):
        tpl = {s.toInt():counter}
        state_to_int_map.update(tpl)
        real_state_to_int_map.update({s:counter})
        int_to_state_map.update({counter:s})
        counter+=1
        # for j in range(len(s.transitions)):
        #     num_prism_choices += 1
        #     t = s.transitions[j]
        #     for s_prime, p in t.prob_distr:
        #         num_prism_transitions+=1


if(IMPORTABLE):
    #TODO: why does this need to be here?????
    for s, i in real_state_to_int_map.items():
        for j in range(len(s.transitions)):
            num_prism_choices += 1
            t = s.transitions[j]
            for s_prime, p in t.prob_distr:
                num_prism_transitions+=1

    write_tra_file(game, real_state_to_int_map, state_to_int_map, int_to_state_map, num_prism_choices, num_prism_transitions, "model.tra")
    write_sta_file(game, real_state_to_int_map, "model.sta")
    write_lab_file(game, real_state_to_int_map, "model.lab")
    write_pla_file(game, real_state_to_int_map, "model.pla")
    write_rew_file(game, real_state_to_int_map, "model.rew")
else:
    print_front_matter()
    print_global_vars()
    print_robot_module(game, state_to_int_map)
    print_human_module(game, state_to_int_map)
    print_labels()
    print_rewards()
