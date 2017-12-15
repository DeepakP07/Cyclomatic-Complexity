import requests
from collections import deque
from flask import Flask
from flask_restful import Resource, Api, request
import sys
import time

app = Flask(__name__)
api = Api(app)

new_t = time.clock()
new_t1 = time.clock()

job_queue = deque()
JOB_QUEUE_LOCK = Lock()
CC = 0
CC_COUNT = 0
CC_LOCK = Lock()
worker_cc = 0
total_commits = 0
avg_cc = 0
job_queue_length = 0
recv_count = 0
num_workers = sys.argv[1]

class master(Resource):
 """

    def get(self):
        global JOB_QUEUE
        global JOB_QUEUE_LOCK
        with JOB_QUEUE_LOCK:
            try:
                return {'sha': JOB_QUEUE.popleft()}

            except IndexError:
                return '', 204"""
     def get(self):
        global job_queue
        global new_t

        if job_queue:
            if job_queue_length-1 == len(job_queue):    # record intial time when first url is taken by a worker
                new_t = time.clock()
            return job_queue.popleft()
        else:
            return "finished"   # when all urls are complete

  """
    new_cc = float(request.form['cc'])
     with CC_LOCK:
     CC += new_cc
     CC_COUNT += 1
     if CC_COUNT == TOTAL_COMMITS:
        shutdown_server()
        return '', 503

     return '', 204

  """
    def put(self):
        global total_cc
        global recv_count
        global new_t
        global new_t1
        global ave_cc

        worker_cc = int(request.form['cc'])
        total_cc += worker_cc           # append to total CC of commits

        print("RECEIVED: " + str(worker_cc))
        recv_count += 1

        if recv_count == int(num_workers):
            kill_manager()
        return '', 204


def kill_manager():

    func = request.environ.get('werkzeug.server.shutdown')
    # shut down the server
    if func is None:
        raise RuntimeError('Server not ru')
    func()

def get_urls(github_url):

    tree_urls = []

    payload_headers = get_params_headers()

    resp = requests.get(github_url,   params=payload_headers[0], headers=payload_headers[1])    # get the commit page of the github url

    for item in resp.json():
        tree_urls.append(item['commit']['tree']['url']) # parse out all tree URLs from the commit page and append to a list

    return tree_urls


def get_job_queue(tree_urls):

    global job_queue
    global job_queue_length

    payload_headers = get_params_headers()

    for blob_url in tree_urls:
        resp = requests.get(blob_url,   params=payload_headers[0], headers=payload_headers[1])  # get data at each tree url

        tree = resp.json()['tree']

        for item in tree:
            file_url = item['url']
            filename = item['path']

            filename_url = file_url + '|' + filename
            job_queue.append(filename_url)      # append the two to the blob list - these will be sent to the flask server

    job_queue_length = len(job_queue)   # record the length of the list


def get_headers_params():
    with open('github-token.txt', 'r') as tmp_file:
        token = tmp_file.read()

    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    return (payload, headers)


def main():

    print ("Master started...")
    github_url = 'https://api.github.com/repos/DeepakP07/MultiClient-Chat-server/commits'  # commit url of this project on github

    print("Getting Tree URL list...")
    tree_urls = get_tree_urls(github_url)      # get the list of tree URLs from the project's commits
    print("Tree URL list received...")

    print("Gettng blob URL's...")
    get_blob_url_list(tree_urls)    # get blob URLs of each tree
    print("Blob URL's received...")

    app.run(host='localhost', port=2020, debug=False)       # start the flask server
    t_new = time.clock()               # record the end time after server has shut down

    ave_cc = total_cc / job_queue_length        # get average CC for all commits
    print("\nAverage CC: " + str(ave_cc))
    print("Total CC: " + str(total_cc) + "\n")

    total = new_t- new_t1
    print("overall time taken was: " + str(total) + " seconds")

    time_str = "num_workers=" + str(num_workers) + ", time=" + str(total) + "sec\n"

    with open("TimeTaken.txt", 'a+') as time_file:
        time_file.write(time_str)


api.add_resource(master, '/')

if __name__ == "__main__":
    main()
