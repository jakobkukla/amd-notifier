import os
import sys
import time
import requests
import lxml.html

if ('GCM_SECRET' not in os.environ or 'GCM_ACCOUNT' not in os.environ):
    sys.exit("GCM_SECRET or GCM_ACCOUNT not set! Exiting...")

gcm_secret = os.environ.get('GCM_SECRET')
gcm_account = os.environ.get('GCM_ACCOUNT')

baseUrl = "https://store.digitalriver.com/store/defaults/de_DE/AddItemToRequisition/productID."

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
        "priority": "normal",
        "payload": "AAALLLAARM in der Feuerwache!"
    }

    requests.post(baseUrl, data=data)


def getErrorCode(productId):
    response = requests.get(baseUrl + productId, stream=True)
    response.raw.decode_content = True

    tree = lxml.html.parse(response.raw)
    error = tree.xpath("//*[@id=\"dr_ServerError\"]/span/p[3]")

    return int(error[0].text[-2] + error[0].text[-1])


def main():
    while True:
        for name, id in productIds.items():
            print(name + ": ", end='')

            if (getErrorCode(id) == 16):
                sendCloudMessage()
                print("CAT16 detected: Notification sent! Sleeping for 24h...")
                time.sleep(86400)

            print("CAT15")
            time.sleep(1)


main()
