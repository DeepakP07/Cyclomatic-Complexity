import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import requests
from time import gmtime, strftime
import os.path
from re import match
import time



class elf():
    total_commits = 0
    master_url = 'http://localhost:2020/'

    config_cyclo = Config(
            exclude='',
            ignore='venv',
            order=SCORE,
            no_assert=True,
            show_closures=False,
            min='A',
            max='F',
    )

    def __init__(self):
        self.url = requests.get(self.manager_url).json()   # get the first url

    def get__params_headers(self):
        with open('github-token.txt', 'r') as tmp_file:
            token = tmp_file.read()

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        return (payload, headers)


    def check_pyfile(self, filename):
        return True if match('.*\.py', filename) is not None else False

    def calc_CC(self, blob_url):

        url = blob_url.split('|')[0]
        filename = blob_url.split('|')[1]

        payload_headers = self.get__params_headers()

        flag = self.check_python_file(filename)      # check if file is a python file
        if flag == True:

            resp = requests.get(url,   params=payload_headers[0], headers=payload_headers[1])       # get the data from the file

            c_time = time.clock()
            c_time = str(c_time)
            c_time = c_time.split('.')[1]
            sha = url.split('/blobs/')[1]       # give the temp file a unique name (sha + current processor time)

            file_path = sha + c_time  + '.py'

            with open(file_path, 'w') as tmp_file:      # temporarily write out the file's data
                tmp_file.write(resp.text)
            tmp_file.close()


            CC_file_get = open(file_path, 'r')      # read in the file's data
            results = CCHarvester(file_path, self.cc_config).gobble(CC_file_get)        # calculate the CC of the temp file
            CC_file_get.close()
            os.remove(file_path)        # delete the temp file

            file_cc = 0

            for i in results:
                file_cc += int(i.complexity)        # append CC of all parts of the file to a total CC for the file

            print("Complexity of file: " + str(file_cc))

            return file_cc
        else:
            return 0        # if file is not a python file

    def receive_work(self):

        file_cc = self.calc_CC(self.url)      # this is called on first url
        self.total_cc += file_cc

        self.url = requests.get(self.manager_url).json()
        while self.url != "finished":          
            file_cc = self.calc_CC(self.url)
            self.total_cc += file_cc
            self.url = requests.get(self.manager_url).json()      


        print("Finished...")
        print("Total CC: " + str(self.total_cc))
        requests.put(self.manager_url, data={'cc': self.total_cc})    

def main():

    print("Worker is ready to receive...")
    worker = elf()
    worker.receive_work()

if __name__ == "__main__":
    main()
