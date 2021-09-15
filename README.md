# Running the code
cd to the folder you want to edit, e.g., ```cleaning_room```

edit ```make_game.py``` to the scenario you want, e.g., ```num_blocks = 3``` and ``` num_locations = 7```

```
python3 make_game.py > model.prism
~/prism-games/prism/bin/prism model.prism spec.props
```

# Running with an imported model
```
~/Development/prism-games/prism/bin/prism -importtrans model.tra -importstates model.sta -importplayers model.pla -importlabels model.lab -importstaterewards model.rew -smg -explicit -javamaxmem 1g spec.props
```