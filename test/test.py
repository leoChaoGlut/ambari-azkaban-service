def ping(port):
    url = 'http://127.0.0.1:{0}/executor?action=ping'.format(port)
    while True:
        try:
            resp = requests.get(url)
            print(resp.text)
            if json.loads(resp.text)['status'] == 'alive':
                print('break')
                break
        except:
            print('e')
        time.sleep(1)


ping(12321)

import json
import requests
import time


def ping(port):
    url = 'http://127.0.0.1:{0}/status'.format(port)
    while True:
        try:
            resp = requests.get(url)
            print(resp.status_code)
            print(resp.text)
            print(requests.codes.ok)
            if resp.status_code == requests.codes.ok:
                break
        except:
            print('e')
        time.sleep(1)


ping(10200)

[download]
azkaban_web_tar_url = https: // ypsx - leo - sh.oss - cn - shanghai.aliyuncs.com / az - web.tar
azkaban_executor_tar_url = https: // ypsx - leo - sh.oss - cn - shanghai.aliyuncs.com / az - exec.tar
