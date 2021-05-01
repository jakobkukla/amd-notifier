import os
import sys
import time
from datetime import datetime
import requests
import lxml.html

if ('GCM_SECRET' not in os.environ or 'GCM_ACCOUNT' not in os.environ):
    sys.exit("GCM_SECRET or GCM_ACCOUNT not set! Exiting...")

gcm_secret = os.getenv('GCM_SECRET')
gcm_account = os.getenv('GCM_ACCOUNT')

try:
    timeout = float(os.getenv("AMD_TIMEOUT", 1))
except ValueError:
    timeout = 1

productIds = {
    '6700XT': '5496921400',
    '6800':   '5458374000',
    '6800XT': '5458374100',
    '6800XTM': '5496921500',
    '6900XT': '5458374200',
}


def sendCloudMessage():
    baseUrl = "https://llamalab.com/automate/cloud/message"

    data = {
        "secret": gcm_secret,
        "to": gcm_account,
        "priority": "high",
        "payload": "AAALLLAARM in der Feuerwache!"
    }

    requests.post(baseUrl, data=data)


def getErrorCode(productId):
    baseUrl = "https://store.digitalriver.com/store/defaults/de_DE/AddItemToRequisition/productID."

    response = requests.get(baseUrl + productId, stream=True)
    response.raw.decode_content = True

    tree = lxml.html.parse(response.raw)
    error = tree.xpath("//*[@id=\"dr_ServerError\"]/span/p[3]")

    return int(error[0].text[-2] + error[0].text[-1])


def main():
    while True:
        for name, id in productIds.items():
            dt = datetime.now().strftime("[%d/%m/%Y %H:%M:%S] ")
            print(dt + name + ": ", end='')

            if (getErrorCode(id) == 16):
                sendCloudMessage()
                print("CAT16 detected: Notification sent! Sleeping for 24h...")
                time.sleep(86400)

            print("CAT15")
            time.sleep(timeout)


main()
