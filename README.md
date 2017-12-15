
CS7NS1 (Scalable Computing) -- Assignment 2 #Cyclomatic-Complexity.
========================================
***Student ID:17310212 Name: Deepak Purohit***

To run. 

In GitHub, go to: Settings > Generate new token -> Enter password -> Generate token. Then copy the generated token 
In the working directory of the manager and the worker, open a text file and name it 'github-token.txt'. Paste the generated token into this text file. The manager and worker will use this token to access the GitHub API.
Run the manager: python manager.py [number of workers]
Once the Master's Flask server is running, run the run_elf.cmd script to start the workers: run_elf.cmd [number of workers] (Max number of workers that can run is 10)


