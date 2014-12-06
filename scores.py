def getScores(username, password):

    from multiprocessing import Process, Lock, Value
    import requests
    from bs4 import BeautifulSoup

    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7'}
    credentials = {'username': username, 'password': password}

    login = requests.post('https://quickstart.collegeboard.org/posweb/login.jsp', params=credentials, headers=headers)



    if 'class="error"' in login.text:
        return -1

    session = login.cookies

    base = 'https://quickstart.collegeboard.org/posweb/questionInfoNewAction.do?testYear=2014&skillCd=%s&questionNbr=%i'

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


    data['M']['score'] = conversion[data['M']['raw'] + 2][1]
    data['CR']['score'] = conversion[data['CR']['raw'] + 2][0]
    data['W']['score'] = conversion[data['W']['raw'] + 2][2]
    return data

conversion = [
(20, 20, 20),
(21, 23, 20),
(22, 25, 22),
(24, 26, 24),
(26, 28, 26),
(28, 30, 28),
(30, 32, 30),
(31, 33, 32),
(32, 35, 33),
(33, 36, 34),
(35, 37, 35),
(36, 38, 36),
(37, 39, 37),
(38, 40, 38),
(39, 42, 39),
(40, 42, 40),
(41, 43, 41),
(42, 45, 42),
(43, 46, 43),
(44, 47, 44),
(45, 48, 45),
(46, 49, 47),
(46, 50, 48),
(47, 51, 48),
(48, 53, 49),
(49, 54, 51),
(50, 56, 53),
(51, 57, 54),
(51, 59, 55),
(52, 60, 56),
(53, 62, 57),
(54, 64, 59),
(55, 65, 61),
(56, 67, 62),
(57, 68, 63),
(58, 70, 65),
(59, 71, 67),
(60, 73, 69),
(61, 75, 70),
(62, 77, 71),
(64, 80, 76),
(65, 80, 80),
(66, 80, 80),
(67, 80, 80),
(70, 80, 80),
(71, 80, 80),
(73, 80, 80),
(75, 80, 80),
(78, 80, 80),
(80, 80, 80),
(80, 80, 80),
]
