if %1%==1 goto worker1
if %1%==2 goto worker2
if %1%==3 goto worker3

:worker1
    start cmd /c python worker.py
    goto finished
:worker2
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished

:worker3
    start cmd /c python worker.py
    start cmd /c python worker.py
    start cmd /c python worker.py
    goto finished
:finished
