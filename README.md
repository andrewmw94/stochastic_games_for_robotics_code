# Install the Dockerfile

### Prerequisite
- docker

### Build
```bash
docker build -t IMAGE_NAME .
```

e.g. `docker build -t prism .`

Note: the dot looks for a Dockerfile in the current repository.Then spin an instance of the container by using the following command

## Run

```bash
docker run -it --rm --name <docker_container_name> <docker_image_name>

```

To create a persistent container, run the following command (no `rm` tag)

```bash
docker run -it --name <docker_container_name> <docker_image_name>

```

The combined command looks like this

```bash
docker run -it -v $PWD:/stochastic_games_robotics_code --name sg_hri_faster_code faster_sg_hri_icra24_code
```

Here `$PWD` is the local directory you want to volume bind to `/stochastic_games_robotics_code` Directory inside the container. 

If you are more used to GUI and would like to edit or attach a container instance to the VSCode ([Link](https://code.visualstudio.com/docs/devcontainers/containers)) then follow the instructions below:


### Attaching the remote container to VScode


1. Make sure you have the right VS code extensions installed
	* install docker extension
	* install python extension
	* install remote container extension
	* Now click on the `Remote Explore` tab on the left and attach VScode to a container.
2. This will launch a new vs code attached to the container and prompt you to a location to attach to. The default is root, and you can just press enter. Congrats, you have attached your container to VSCode.


## Run PRISM and PRIMS-Games

In docker, to run `prism`,
```bash
cd /prism/prism/bin && ./prism
```

OR to run `prism GUI`

```bash
cd /prism/prism/bin && ./xprism
```

 To run `prism-games`

```bash
cd /prism-games/prism/bin && ./prism
```

OR to run `prism-games GUI`

```bash
cd /prism-games/prism/bin && ./xprism
```

## Check PRISM and PRISM-games Installation

To check if everything worked, you can try the following inside the container (the second one will only work if PPL was successfully installed):

```bash
cd /prism-games/prism
make PPL_DIR=/usr/local/lib
make test testppl
```

The test should ultimately display: "Testing result: PASS"

# Running the code

Change the working Dir

```bash
cd stochastic_games_for_robotics_code
```

Then, `cd` to the folder you want to edit, e.g., ```cleaning_room```.

edit ```make_game.py``` to the scenario you want, e.g., ```num_blocks = 3``` and ``` num_locations = 7```

```
python3 make_game.py > model.prism
~/prism-games/prism/bin/prism model.prism spec.props
```

## Running with an imported model
```
~/Development/prism-games/prism/bin/prism -importtrans model.tra -importstates model.sta -importplayers model.pla -importlabels model.lab -importstaterewards model.rew -smg -explicit -javamaxmem 1g spec.props
```


### Memory issues

If you get the followin error `java.lang.OutOfMemory` then use this command to provide more memory to JAVA. On Unix, Linux or Mac OS X platforms, this can done by using the `-javamaxmem`switch, passed either to the command-line script prism or the GUI launcher xprism. For example:

```bash
/prism-games/prism/bin/prism -javamaxmem 10g model.prism spec.props
```

Note: Make sure you are in the same folder as the `model.prism` file created above. For more troubleshooting and memory related issues check this [Link](https://www.prismmodelchecker.org/manual/ConfiguringPRISM/OtherOptions)


## Directories

* cleaning_room_human_prob_term = Model where at each state there is non-zero probability of human terminating. 
* cleaning_room_human_unlimited = Model where the ratio of robot to human action is fixed. (There is no bound on human actions)
* tic tac toe = The classic game with trembling hand (for stochasticity)


All the other repositories are experimental

Driving = Borrowed from chen et al. See README in that directory.
Gridworld = Testing scenarios to determin the cause of bottleneck in PRISM  



