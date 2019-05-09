
# a node test.py

import CostumePy

CostumePy.listen("something", print)

while CostumePy.is_running():
    CostumePy.broadcast("control", True)


# A system launch
from multiprocessing import Process

from CostumePy import Launcher

l = Launcher()

l.add("test.py")
l.add("test2.py")

l.launch()
# which in turn
# for each node:
# launches each node in turn with os.system sys.executable filename.py &
# or sts = Popen([python, filename, arg1, arg2], shell=true)
# use sts.poll(), sys.terminate() or sys.kill()
# waits for communication setup
# sets up node
# then when it quits it sends shutdown commands to those processes
