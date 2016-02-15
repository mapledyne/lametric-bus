from bs4 import BeautifulSoup
import requests
import time

oba_url = "http://pugetsound.onebusaway.org/where/sign/stop.action?id=1_"

stops = [["27", "27360", 100, ""], ["14", "11920", 100, ""]]


def _get(url):
    response = requests.get(url)

    return response.text


def bus(bus_stop):
    return _get(oba_url + bus_stop)


def buses():
    for one_stop in stops:
        web_body = bus(one_stop[1])
        soup = BeautifulSoup(web_body, 'html.parser')
        for one_bus in soup.findAll("td", class_="arrivalsStatusEntry"):
            timing = one_bus.string
            if timing == 'NOW':
                timing = '0'
            timing = int(timing)
            if timing < 1:
                continue
            if one_stop[2] > timing:
                one_stop[2] = timing

        for one_stop in stops:
            if one_stop[2] == 100:
                one_stop[3] = str(one_stop[0]) + ": --m"
            else:
                one_stop[3] = str(one_stop[0]) + ": " + str(one_stop[2]) + "m"
#            print one_stop[0] + ": " + str(timing) + "m"

def update_lametric():
    buses()
    print("Stops: " + str(stops))

    token = "ZDcyM2I0NTJjYTFjOGE3NzBlNTMwNjMyYjdjNzBiM2UxMGZiZGJkOWE0MmI5ODNkMTcwMDI4OWI1NzcyNzVkYQ=="

    headerset = {"Accept": "application/json",
                 "Cache-Control": "no-cache",
                 "X-Access-Token": token}

    frames = '{ "frames": [ { "index": 0, "text": "' + stops[0][3] + '", "icon": "a1372"}, { "index": 1, "text": "' + stops[1][3] + '", "icon": "a1372" } ] }'

    url = "https://developer.lametric.com/api/V1/dev/widget/update/com.lametric.e67bc58361aff696eced83d28d0aae32/1"

    requests.post(url, headers=headerset, data=frames)

if __name__ == '__main__':
    while True:
        update_lametric()
        time.sleep(60)
