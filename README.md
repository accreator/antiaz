The code is written in Python 3.6

Minimax vs Random
=================
* Set the depth for minimax in `agent.py` by modifying `MINIMAX_DEPTH`. The default depth is 9
* Run the following command

```
python agent.py
```

* The output consists of two numbers: the number of games won by Random, and the number of games won by Minimax

Resnet
======
* To generate the data for training, run the following in Python

```python
from data import DATA
data = DATA(9) #board size is 9x9
data.gen("trn", 800000) #800000 positions for training
data.gen("vld", 100000) #100000 positions for validation
data.gen("tst", 100000) #100000 positions for testing
```

* After generating the data, run the following command to train the resnet

```
python resnet.py
```

AlphaZero General
=================
* Go to directory `azgeneral`
* To train the model, run

```
python main.py
```

* To test the performance of the current best model with the random player, run 

```
python pit.py
```

* For testing, there are two configurable parameters in `pit.py`
	* Number of MCTS simulations per move, which can be set in line 23 (default: 24)
	* Number of games to play, which can be set in line 35 (default: 100)

* The output format is the same as AlphaZero General, i.e. in the last line of the output, there is a tuple (W, L, D), where W stands for the number of games won by AlphaZero General, L for lost and D for drawn.

* If you want to use the model trained by us, create a directory named `temp` in `azgeneral` and copy `model/best.pth.tar` to `azgeneral/temp/`