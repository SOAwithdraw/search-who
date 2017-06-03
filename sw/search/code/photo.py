import urllib2
import httplib
import urllib
import json


def Group(photos):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'a0b8976eaa1d49a8980e162b7d7741c1',
        #'Ocp-Apim-Subscription-Key': '0bb0d50d31034b4f8397ffacfb6e9185',
    }

    params = urllib.urlencode({})

    body = json.dumps({"faceIds": photos})
    print(body)

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        print('connect')
        conn.request("POST", "/face/v1.0/group?%s" % params, body, headers)
        print('requst')
        response = conn.getresponse()
        print('response')
        data = response.read()
        print('read')
        print(data)
        data = eval(data)
        conn.close()
    except Exception as e:
        print("error")
        return []

    return data


def Checkphoto(img):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'a0b8976eaa1d49a8980e162b7d7741c1',
        #'Ocp-Apim-Subscription-Key': '0bb0d50d31034b4f8397ffacfb6e9185',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender',
    })

    body = json.dumps({"url": img})
    print(body)

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        print('connect')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        print('requst')
        response = conn.getresponse()
        data = response.read()
        data = eval(data)
        conn.close()
    except Exception as e:
        print("Errer")

    context = []

    try:
        tryid = data[0]['faceId']
    except:
        return context

    for i in range(len(data)):
        context.append(data[i]["faceAttributes"])
        context[i]['id'] = data[i]['faceId']
        context[i]['siz'] = data[i]['faceRectangle']['width'] * data[i]['faceRectangle']['height']
        context[i]['url'] = img

    print "context:", context
    return context


def Cluster(photos):
    """Return 2 lists, one is [[14, 45, 47], [13, 24]], the other is ['http://isadb.jpg', 'htpp://bibjkbskd.jpg']"""
    # Checkphoto("http://upload.ahwang.cn/2015/1216/1450232258493.jpg")

    # id means api id, ind means returning ind
    # print photos
    fo = open("ids.txt", "w")
    tot = len(photos)
    ids = []
    for i in range(tot):
        ids.append([])
        if len(photos[i])>5:
            continue
        for j in photos[i]:
            if len(j) < 6 or j[:4] != 'http' or (j[-3:] != 'jpg' and j[-3:] != 'png'):
                continue
            content = Checkphoto(j)
            ids[i].extend(content)
            for k in content:
                fo.write(k['id'])
                fo.write('\n')
    fo.close()

    bagi_group = []
    mapf = {}
    for i in range(tot):
        for j in ids[i]:
            curid = j['id']
            bagi_group.append(curid)
            mapf[curid] = i

    bago_group = Group(bagi_group)
    print 'bago_group', bago_group

    fin = []
    mainphoto = []
    ctot = len(bago_group['groups'])
    for i in range(ctot):
        fin.append([])
        ma = 0
        curph = ''
        for j in bago_group['groups'][i]:
            curind = mapf[j]
            for k in ids[curind]:
                if k['id'] == j:
                    curwei = k['siz']
                    break
            if curwei > ma:
                ma = curwei
                curph = k['url']

            fin[i].append(curind)
        mainphoto.append(curph)

    print '\n'
    print fin
    print mainphoto

    return fin, mainphoto


def Try():

    fi = open("ids.txt", "r")
    bagi = fi.readlines()
    for i in range(len(bagi)):
        bagi[i] = bagi[i][:-1]
    fi.close()
    bago = Group(bagi)

if __name__ == '__main__':
    Try()
