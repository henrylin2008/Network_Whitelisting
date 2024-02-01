# This Script is for IT Networking team;
# Objective: Pulling dynamic IPs from vendors on daily basis and store the result in local server (172.20.6.12:8080),
#            then firewalls (PAN) grant traffic on these whitelisted IPs (to JIRA server)
# Creator: Henry Lin

import json, requests
import schedule, time

def github_ips():
    try:
        r = requests.get('https://api.github.com/meta')
        json_response = r.json()

        f = open("ips/github_ips.txt", "w")
        for item in json_response['hooks']:
            print(item, file=f)

        for item in json_response['api']:
            print(item, file=f)

        f.close()
    except:
        print("Unable to query Github")

def okta_ips():
    try:
        r = requests.get('https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json')
        json_response = r.json()

        f = open("ips/okta_ips.txt", "w")

        for i in json_response['us_cell_7']['ip_ranges']:
            print(i, file=f)

        f.close()
    except:
        print("Unable to query Okta")

def mailx_ips():
    try:
        r = requests.get('https://autobox.infra.wish.com/api/netbox/mailx-inventory')
        json_response = r.json()

        f = open("ips/mailx_ips.txt", "w")
        for item in json_response['results']:
            print(item, file=f)

        f.close()
    except:
        print("Unable to query autobox")



#schedule.every(1).minutes.do(github_ips)
#schedule.every(1).minutes.do(okta_ips)

#schedule.every().day.at("00:30").do(github_ips)
#schedule.every().day.at("00:30").do(okta_ips)
#schedule.every(5).minutes.do(mailx_ips)

#while True:
#    schedule.run_pending()
#    time.sleep(1)

if __name__ == '__main__':
    schedule.every().day.at("00:30").do(github_ips)
    schedule.every().day.at("00:30").do(okta_ips)
    schedule.every(5).minutes.do(mailx_ips)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except:
            pass
