CONCURRENT_GAME = False
GRID_SIZE = 25
TERM_LOC = GRID_SIZE*GRID_SIZE
NUM_HUMANS = 1

class Location:
    row=0
    col=0

    def __init__(self, r, c):
        self.row = r
        self.col = c

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class Transition:
    action=""
    prob_distr = [] # list of <new state, probability>

    def __init__(self, tpl_list):
        self.action=""
        self.prob_distr=tpl_list

class State:
    robot_loc=Location(0,0)
    human_loc=Location(GRID_SIZE-1, GRID_SIZE-1)
    robot_turn=False
    transitions = [] # list of transitions

    def __init__(self):
        self.robot_loc=Location(0,0)
        self.human_loc=Location(GRID_SIZE-1, GRID_SIZE-1)
        self.robot_turn=False
        self.transitions=[]

    def toInt(self):
        r = self.robot_loc.row
        power = GRID_SIZE
        r = r + self.robot_loc.col*power
        power = power*GRID_SIZE
        r = r + self.human_loc.row*power
        power = power*GRID_SIZE
        r = r + self.human_loc.col*power
        power = power*GRID_SIZE
        if self.robot_turn:
            r += power
        return r

    def toPrismStr(self, primed):
        if primed:
            rturn = 0
            if self.robot_turn:
                rturn = 1
            str = "(rlocrow'={}) & ".format(self.robot_loc.row) + "(rloccol'={}) & ".format(self.robot_loc.col) +"(hlocrow'={}) & ".format(self.human_loc.row) + "(hloccol'={}) & ".format(self.human_loc.col)+"(rturn'={}) & ".format(rturn)
            return str[:-2]
        else:
            rturn = 0
            if self.robot_turn:
                rturn = 1
            str = "(rlocrow={}) & ".format(self.robot_loc.row) + "(rloccol={}) & ".format(self.robot_loc.col) +"(hlocrow={}) & ".format(self.human_loc.row) + "(hloccol={}) & ".format(self.human_loc.col)+"(rturn={}) & ".format(rturn)
            return str[:-2]

def isValidLoc(loc, curr_loc, robot_turn):
    if robot_turn:
        if loc.row >= 0 and loc.row < GRID_SIZE:
            if loc.col >= 0 and loc.col < GRID_SIZE:
                return True
        return False
    else:
        if loc.row >= 0 and loc.row < GRID_SIZE:
            if loc.col >= 0 and loc.col < GRID_SIZE:
                if curr_loc.row >= curr_loc.col and curr_loc.col >= GRID_SIZE/2 and curr_loc.row == loc.row and curr_loc.col+1 == loc.col:
                    return True
                if curr_loc.row >= curr_loc.col and curr_loc.col >= GRID_SIZE/2 and curr_loc.row == loc.row and curr_loc.col+1 == loc.col:
                    return True
                if curr_loc.row >= curr_loc.col and curr_loc.col >= GRID_SIZE/2 and curr_loc.row == loc.row and curr_loc.col+1 == loc.col:
                    return True
                if curr_loc.row >= curr_loc.col and curr_loc.col >= GRID_SIZE/2 and curr_loc.row == loc.row and curr_loc.col+1 == loc.col:
                    return True
        return False

def genNeighbors(state):
    ret = []
    # if state.robot_turn and state.robot_loc == TERM_LOC:
    #     s_prime=State()
    #     s_prime.robot_loc=state.robot_loc.copy()
    #     s_prime.human_loc=state.human_loc.copy()
    #     state.transitions = [Transition([(s_prime,1.0)])]
    #     state.transitions[-1].action="robottermselfloop"
    #     s_prime.robot_turn = False
    #     ret.append(s_prime)
    #     return ret
    # elif not state.robot_turn and state.human_loc == TERM_LOC:
    #     s_prime=State()
    #     s_prime.robot_loc=state.robot_loc.copy()
    #     s_prime.human_loc=state.human_loc.copy()
    #     state.transitions = [Transition([(s_prime,1.0)])]
    #     state.transitions[-1].action="humantermselfloop"
    #     s_prime.robot_turn = True
    #     ret.append(s_prime)
    #     return ret

    #moving
    if state.robot_turn:
        #north
        newLoc = Location(state.robot_loc.row-1, state.robot_loc.col)
        if isValidLoc(newLoc, state.robot_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=newLoc
            s_prime.human_loc=Location(state.human_loc.row, state.human_loc.col)
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="robotmovenorth"
            s_prime.robot_turn = False
            ret.append(s_prime)
        #south
        newLoc = Location(state.robot_loc.row+1, state.robot_loc.col)
        if isValidLoc(newLoc, state.robot_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=newLoc
            s_prime.human_loc=Location(state.human_loc.row, state.human_loc.col)
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="robotmovesouth"
            s_prime.robot_turn = False
            ret.append(s_prime)
        #east
        newLoc = Location(state.robot_loc.row, state.robot_loc.col+1)
        if isValidLoc(newLoc, state.robot_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=newLoc
            s_prime.human_loc=Location(state.human_loc.row, state.human_loc.col)
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="robotmoveeast"
            s_prime.robot_turn = False
            ret.append(s_prime)
        #west
        newLoc = Location(state.robot_loc.row, state.robot_loc.col-1)
        if isValidLoc(newLoc, state.robot_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=newLoc
            s_prime.human_loc=Location(state.human_loc.row, state.human_loc.col)
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="robotmovewest"
            s_prime.robot_turn = False
            ret.append(s_prime)
    else:
        #north
        newLoc = Location(state.robot_loc.row-1, state.robot_loc.col)
        if isValidLoc(newLoc, state.human_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=Location(state.robot_loc.row, state.robot_loc.col)
            s_prime.human_loc=newLoc
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="humanmovenorth"
            s_prime.robot_turn = True
            ret.append(s_prime)
        #south
        newLoc = Location(state.robot_loc.row+1, state.robot_loc.col)
        if isValidLoc(newLoc, state.human_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=Location(state.robot_loc.row, state.robot_loc.col)
            s_prime.human_loc=newLoc
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="humanmovesouth"
            s_prime.robot_turn = True
            ret.append(s_prime)
        #east
        newLoc = Location(state.robot_loc.row, state.robot_loc.col+1)
        if isValidLoc(newLoc, state.human_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=Location(state.robot_loc.row, state.robot_loc.col)
            s_prime.human_loc=newLoc
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="humanmoveeast"
            s_prime.robot_turn = True
            ret.append(s_prime)
        #west
        newLoc = Location(state.robot_loc.row, state.robot_loc.col-1)
        if isValidLoc(newLoc, state.human_loc, state.robot_turn):
            s_prime=State()
            s_prime.robot_loc=Location(state.robot_loc.row, state.robot_loc.col)
            s_prime.human_loc=newLoc
            state.transitions.append(Transition([(s_prime,1.0)]))
            state.transitions[-1].action="humanmovewest"
            s_prime.robot_turn = True
            ret.append(s_prime)
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
                if visited_states[n.toInt()].robot_turn != n.robot_turn or visited_states[n.toInt()].human_loc != n.human_loc or visited_states[n.toInt()].robot_loc != n.robot_loc:
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
    print("  robot, [robotmovenorth], [robotmovesouth], [robotmoveeast], [robotmovewest]")
    print("endplayer")

    print("player h1")
    print("  human, [humanmovenorth], [humanmovesouth], [humanmoveeast], [humanmovewest]")
    print("endplayer")

def print_global_vars():
    print("global rlocrow: [0..{}] init 0;".format(GRID_SIZE-1))
    print("global rloccol: [0..{}] init 0;".format(GRID_SIZE-1))
    print("global hlocrow: [0..{}] init {};".format(GRID_SIZE-1, GRID_SIZE-1))
    print("global hloccol: [0..{}] init {};".format(GRID_SIZE-1, GRID_SIZE-1))
    if not CONCURRENT_GAME:
        print("global rturn: [0..1] init 0;")

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
    print("label \"collision\" = (rlocrow=hlocrow) & (rloccol=hloccol);")



initial_state=State()
initial_state.robot_loc = Location(0,0)
initial_state.human_loc = Location(GRID_SIZE-1,GRID_SIZE-1)
initial_state.robot_turn=False

game = genGame(initial_state)

state_to_int_map={initial_state.toInt():0}
counter = 1
for s in game:
    if not (s.toInt() in state_to_int_map):
        tpl = {s.toInt():counter}
        state_to_int_map.update(tpl)
        counter+=1

print_front_matter()
print_global_vars()
print_robot_module(game, state_to_int_map)
print_human_module(game, state_to_int_map)
print_labels()