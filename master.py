import requests
from collections import deque
from flask import Flask
import sys
import time

app = Flask(__name__)
api = Api(app)

t0 = time.clock()
t1 = time.clock()

job_queue = deque()
worker_cc = 0           # CC received from a worker
total_commits = 0            # total CC of all worker_cc's
avg_cc = 0              # average CC for all commits
job_queue_length = 0
recv_count = 0
num_workers = sys.argv[1]

class Manager(Resource):

    def get(self):
        global job_queue
        global t0

        if job_queue:
            if job_queue_length-1 == len(job_queue):    # record intial time when first url is taken by a worker
                t0 = time.clock()
            return job_queue.popleft()
        else:
            return "finished"   # when all urls are complete
