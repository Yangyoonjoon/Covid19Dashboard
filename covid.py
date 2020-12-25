import requests
import xml.etree.cElementTree as et

def getCovid(_date=''):
    URL = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?'
    KEY = 'serviceKey=xoKtSVwxXEsusOjSE9aQ3TMrUhJy%2Fpo%2BtpIFlsDiuJanSUhYHFhILYD%2Fd%2FSzxNyelVbGE1OhFWcfqTHIN2f4fQ%3D%3D'
    PAGE = '&pageNo=1'
    ROW = '&numOfRows=10'
    START = f'&startCreateDt={_date}'
    END = f'&endCreateDt={_date}'

    MSG = URL + KEY + PAGE + ROW + START + END

    try:
        response = requests.get(MSG)
    except Exception as e:
        print(e)
        return []
    else:
        # byte -> str : decode
        # str -> byte : encode

        _data = response.content

        return xmlParcer(_data.decode('utf-8'), 'item')


def xmlParcer(xmlstr, _tag=''):
    lst = []
    root = et.fromstring(xmlstr)
    for tag in root.iter(tag=_tag):
        temp = []
        for k, subtag in enumerate(tag.iter()):
            if tag!=subtag and k!=5 and k!=6 and k!=13 and k!=14 and k!=15:
                # 날짜 파싱
                if k == 1:
                    idx = subtag.text.find(' ')
                    temp.append(subtag.text[:idx])
                else:
                    if subtag.text == '-':
                        temp.append(0)
                    else:
                        temp.append(subtag.text)
        lst.append(temp)

    #print(lst)

    return lst
    