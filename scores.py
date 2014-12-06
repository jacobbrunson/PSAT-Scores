def getScores(username, password, config):

    from multiprocessing import Process, Lock, Value
    import requests
    from bs4 import BeautifulSoup

    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7'}
    credentials = {'username': username, 'password': password}

    login = requests.post(config['collegeboard']['login_url'], params=credentials, headers=headers)



    if 'class="error"' in login.text:
        return -1

    session = login.cookies

    base = config['collegeboard']['base_url']

    lock = Lock()
    scores = {'M': [38, Value('i', 0), Value('i', 0)], 'CR': [48, Value('i', 0), Value('i', 0)], 'W': [39, Value('i', 0), Value('i', 0)]}
    count = Value('i', 0)
    math = Value('i', 0)


    def worker(scores, s, i):
        result = BeautifulSoup(requests.get(base % (s, i), cookies=session, headers=headers).text).body.div.div
        if result is None:
            count.value = 9999
            return
        result = result.p.strong.text[22:]
        lock.acquire()
        if result == 'correctly':
            scores[s][1].value += 1
        elif result == 'incorrectly':
            scores[s][2].value += 1
            if s == 'M' and i >= 29 and i <= 38:
                math.value += 1
        count.value += 1
        lock.release()

    def go(scores, s, i):
        t = Process(target=worker, args=(scores, s, i))
        t.Daemon = True
        t.start()

    for s in scores:
        for i in xrange(1, scores[s][0] + 1):
            go(scores, s, i)

    while count.value < scores['M'][0] + scores['CR'][0] + scores['W'][0]:
        pass

    if count.value > 200:
        return -2

    data = {}
    for s in scores:
        data[s] = {
            'correct': scores[s][1].value,
            'incorrect': scores[s][2].value,
            'omitted': scores[s][0] - scores[s][1].value - scores[s][2].value,
            'total': scores[s][0]
        }
    data['M']['free'] = math.value

    data['M']['raw'] = int(round(data['M']['correct'] - (data['M']['incorrect'] - math.value) / 4.0))
    data['CR']['raw'] = int(round(data['CR']['correct'] - data['CR']['incorrect'] / 4.0))
    data['W']['raw'] = int(round(data['W']['correct'] - data['W']['incorrect'] / 4.0))


    data['M']['score'] = config['scoring']['conversion'][data['M']['raw'] - config['scoring']['conversion_index']][1]
    data['CR']['score'] = config['scoring']['conversion'][data['CR']['raw'] - config['scoring']['conversion_index']][0]
    data['W']['score'] = config['scoring']['conversion'][data['W']['raw'] - config['scoring']['conversion_index']][2]
    return data
