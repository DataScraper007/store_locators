import gzip
import os
from datetime import datetime
import json

import pymysql
import scrapy
from scrapy.cmdline import execute

from store_locators.items import StoreLocatorsItem


class TMobileSpider(scrapy.Spider):
    name = "t_mobile"

    def __init__(self):
        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'actowiz',
            'db': 'store_locators'
        }
        super().__init__()
        self.cookies = None
        self.headers = None
        self.datetime = datetime.now().strftime('%Y%m%d')
        self.page_save = fr"C:\Users\Admin\PycharmProjects\page_save\store_locators\{self.datetime}\{TMobileSpider.name}"

        self.conn = pymysql.connect(**db_params)
        self.cur = self.conn.cursor()

    def start_requests(self):
        self.cur.execute("SELECT short_name, lat, `long`, state FROM lat_long")
        self.cookies = {
            'TFPIDS': '90095dee-37b4-4484-8c4b-f4359526c6e4',
            'TFPID': '90095dee-37b4-4484-8c4b-f4359526c6e4',
            'visid_incap_2810275': 'Nd2kau6fS8GEPyzmqI4PJZcs6GYAAAAAQUIPAAAAAACZ21p+TTOT9QVfW2PNjk0s',
            'kndctr_1358406C534BC94D0A490D4D_AdobeOrg_identity': 'CiYxNDc1ODE4MTgzMzk4MDgwNTQ5MTMyMzkyNTExNTUwMDA5Njc2NFITCO3ouNefMhABGAEqBElORDEwAPAB7ei4158y',
            'AMCV_1358406C534BC94D0A490D4D%40AdobeOrg': 'MCMID|14758181833980805491323925115500096764',
            '_ga': 'GA1.1.1766813937.1726491801',
            'AWSALB': 'xoJ8CZ+zuBAN8MGYaGYu8XsY+233H4cBDjFRADNaMw3q+PPc+kSASxktn4plnJQW9c7QtQ3UAjm7Y2cHu7o5BfHuuyAj5PFvxLTmWUI1Cz+fMsepnIvYYHHMUs5Y',
            'AWSALBCORS': 'xoJ8CZ+zuBAN8MGYaGYu8XsY+233H4cBDjFRADNaMw3q+PPc+kSASxktn4plnJQW9c7QtQ3UAjm7Y2cHu7o5BfHuuyAj5PFvxLTmWUI1Cz+fMsepnIvYYHHMUs5Y',
            'search_visitorId': '0de8de36-9f8a-4658-b9a6-4ed8a3883443',
            'QuantumMetricUserID': 'ef618e945ae75bb8409a4a4ecc3a95ae',
            'LPVID': 'lmMDYxMGJkZjVjNTk4MmQy',
            '_gcl_au': '1.1.798496218.1726491959',
            '_fbp': 'fb.1.1726491959565.705948091570307811',
            '_abck': '660433ED9B5CC6397FE745A5BE54A182~-1~YAAQhidzaF4f6tiRAQAA5IAq/gza8u5OvwzL7UQT0K/yfLLE7QFROj+qSXMO4tyJTyL0NVvpz/H5ilX8jecipakb2YJK6sdtvbXbCY4chQwzpEYXeNZAMcX6sEyT9gl6g2k7FQ3NuzOM+lTwsG7fXKAKUbhGTwHuhD/vUZVrj6tdGgEkdmHa+Lgt70BM8hLYH9aV9eEVlLhzHFvgew5e4PP4VX3rL4xgzC+0BCCOVMftHZqGtCFQX6vQofHqmh6qIX/7/dghGT+uQFD0bJ1uzwO4t0hOiuAGHKPzEqsRH8Cu+v+11EZkMkdJC93zExYQLLoNZOh0i0Geg8tcOLK7l4Zbwv/Nb23KQYVAe385TUERw9caNhmmwsbWZSHp6UExkKJExCxt6PXUm9EQD8chK1eLdgSEvz5UYFCvruQgJZOJ9ibio7fz1WGlCSGg~-1~-1~-1',
            'bm_mi': 'C17186FC4B8F8EA4E8EE816976716636~YAAQhidzaGlu6tiRAQAAbngw/hk7LjZH7zjIyhTS2iv3kiT3ru+h/oQmnZibXnuucKR/7oBf2b9dq+r9EEJWjrCVuP2TrhR9yELhrR7K9NmMTNS0ECU0ZDdw26l+yeYmACyXVkr/AYVm/YhvOvwtgxRqa3pCiyaLo2fZ6qAUJdUzxw0sNnIHiuh4/oDCMXz0fTReFVODSClM0XUJj/+5167xL2g9IVKu+bRA2uZ0AR9+YWJRR+HTF30l5AyVStUmXHM75hFnVzhRisQ20vUxxwV+CBln1TicE+gT8d/rpNk1JjpM/hyK5pW4RdTeblY=~1',
            'kndctr_1358406C534BC94D0A490D4D_AdobeOrg_cluster': 'ind1',
            'mbox': 'session%2314758181833980805491323925115500096764%2DddduJw%231726548335',
            'mboxEdgeCluster': '41',
            'ac': 't!0~s!0~m!0~b!0~h!0~n!0~l!0',
            'a_token': 'eyJraWQiOiI0NDY3MzUxNy04MTc4LTJjYTMtOWU3MC1mZTZiYjg4YjU2OTIiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJqWWZQdWNkYURmMjRVYkdLNkJ1NkFZN1N4VW5OY2I3SiIsInJ0Ijoie1wic2VnbWVudGF0aW9uSWRcIjpcIlRJVEFOXCJ9IiwiZGVhbGVyQ29kZSI6IiIsImlzcyI6Imh0dHBzOi8vYXBpLnQtbW9iaWxlLmNvbS9vYXV0aDIvdjYiLCJtYXN0ZXJEZWFsZXJDb2RlIjoiIiwiYXV0aFRpbWUiOiIxNzI2NTQ2NDc2MDE3Iiwic3RvcmVJZCI6IiIsImF1ZCI6ImpZZlB1Y2RhRGYyNFViR0s2QnU2QVk3U3hVbk5jYjdKIiwidXNuIjoiNmNlNmE4YTItZDUwZS0xNTg4LThiZTYtMDI4NDUyYzk3MGI3Iiwic2VuZGVySWQiOiIiLCJuYmYiOjE3MjY1NDY0NzYsInNjb3BlIjoiIiwiZXhwIjoxNzI3MTUxMjc2LCJhcHBsaWNhdGlvbklkIjoiVE1PIiwiaWF0IjoxNzI2NTQ2NDc2LCJqdGkiOiJjN2Y3MjA0MS02NGNlLTE3MTAtOGI5Yi0zOGYyNDhlMjVhMzQiLCJjaGFubmVsSWQiOiIifQ.nYc9OLz9x6UVxeFv7gousvOL0yn0sAA8m5MzRuXvznuCiDTJuKESkAYTI3TVjvr-M-iIACK2iZRBDq7i10oiCt4shUsQ3gMY37mqTURi9aaWS7R5Cpe-aiq9nbHAzGImSKmsuH--Q3iPItRkEiurjBTjTIL0Q7AQ2OoNVTYXZ46rbEycFTpuc62Ap9kXI3SvCtPgi8VH8drnxd0LRNNP7ToHNqiy4Y7EW2NUp8BrHTqJ1J6dq0yaAECz48bjxy_kzPtiW0WU6NtEQmnhQYoWat3SGGcZVbHInWnxanT0lp2m-YYCqp3MSTUFnkempn-7OInfrxz4fxXzn303xNBJqg',
            'tmobglobalshareddata': '%7B%22creditProfileId%22%3A%22gncukmjsivcuclkfimydilkbguzumljxg5degljrgizdsrjzgm2ekmrwgq%3D%22%2C%22profileId%22%3A%22my3wmzrtgbrtollfmu3toljug43tgljzmqygillcmrrginlfme2wkmjrmu%3D%22%2C%22profileAccountId%22%3A%22inatcqseiu2telkgiq3taljvivauiljtgi3dilkfgy4tsrbvgfbuenrugu%3D%22%7D',
            'GEOTMO': 'PRD-TMO-HAP-EAST-2',
            'ak_bmsc': '9A7759BA54E403948052499B533BAB6F~000000000000000000000000000000~YAAQhidzaOlu6tiRAQAA6X4w/hmsIGSSHdmhMykghA4hhQTiqKTnKd0AqWGAombW5nKryrMztRitQ4LWC2r5pf2z8Iez6hbMw8yJdWUh07unXpB2gK8vRAFiRxkolNWUodC6qpYqAmS1armEkNzd8u4hjSDeK1MiOPjD3LZ8fyzJdBOcAaKV2lJzZLU7mzsShRFWiLtV8MWdypmLOdA7INKfb7CZIMg2Bv4vovfoAZ3h0S1T1UtR9h+eY1tbmgO7GQxNpeMmfaqdQD4pGc5UbzKZt/JW4IHk+uQnL1SR2epmO0R9lPOtRMRtyGX/EZ+2W1yruDcRgrabc4mdunhgEwE5oLgUCjakEyACMhUB1VB838JdmvR9XNejAhN+MvgZoKryWSkJkqwyXuHKprbtUcThm84UsjMcNxWv2/C5sc30YGEQu2UMQ0d+j28sT6jwC7FsyfaHbGPbItTBsGTfI7E/SrQ+nzemUZq8M35TPrc=',
            'invc': '["i-9300db9f-de74-4133-e25e-4c711de33ff9",null,null]',
            'QuantumMetricSessionID': '6fdfeb3d2df8e7a09785bbbe497b4d12',
            'QuantumMetricReplay': 'https://tmobile.quantummetric.com/#/replay/cookie:6fdfeb3d2df8e7a09785bbbe497b4d12?ts=1726503280-1726589680',
            'KPI_EV': '1',
            '_uetsid': '5cf4b78074ab11ef871f3fccc364e345',
            '_uetvid': '5cf4d06074ab11ef886d0593a435d51b',
            '_scid': 'pGpZDniIopa9vmsViFw0nrR_FYdz9ohg',
            '_scid_r': 'pGpZDniIopa9vmsViFw0nrR_FYdz9ohg',
            '_clck': 'sunw9n%7C2%7Cfp9%7C0%7C1721',
            '_ScCbts': '%5B%22561%3Bchrome.2%3A2%3A5%22%5D',
            '_clsk': '1nw7mhe%7C1726546483089%7C1%7C0%7Cx.clarity.ms%2Fcollect',
            '_sctr': '1%7C1726511400000',
            'LPSID-62258097': 'Mrp9atpHRryfRt7o9chAsQ',
            'QSI_HistorySession': 'https%3A%2F%2Fwww.t-mobile.com%2F~1726546487952',
            'bm_sz': 'BDF41DE57332A1401ACD81C278A4454A~YAAQhidzaP126tiRAQAAahAx/hmExAzoc05Yr//A0sWwkBLzgl+2VV3em7dmhYBS5J4+yQaaTyuP5ZB0ZIW64DkeqqW1/R7m5bXEuVR+Y9t9H7cHsg19GqbmxewQx9IsroWGaG6pO+nAMM/L0J89lCvDwab/3GTGguwoWgHqRz3ObERNku3g2Qpm14fldxjfBs6Xef7kXupDZkhHannTuCXB0BhN1H+J+RHSvrWbVygpBuvrvk3I4kXJHWNSGgUjCPDk5W9OqzMapurOz1rAk8dlpfSoIlWYQIv8RlPTWgMNsQBit66M4EhETiAPzy55G46/ZYoMyl4GcrFPv+gALcUckRL9jY+DTtEUeAiw17gXNedbdymOndooPzfs3xM81wzDPmTyGJqTXzpyqeuFpq8FFp8SQZIQej/S62iUtJBYdptxcA==~4535617~4273987',
            'ADRUM_BT': 'R:93|i:2915084|g:f5183be5-1cdc-4cf5-91df-038445f7f097104790|e:0|n:tmo-prod_c41114b8-4495-49d5-b8b6-beebf9de79fa',
            '_ga_NEXYYTFQFY': 'GS1.1.1726546501.3.1.1726546516.45.0.0',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Sep+17+2024+09%3A45%3A16+GMT%2B0530+(India+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=b6a810e9-c721-442a-b7db-e8d44f236645&interactionCount=1&landingPath=NotLandingPage&groups=CX%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2Cgpc%3A1&AwaitingReconsent=false',
            'pv_pageName': 'TMO%20%7C%20Store%20%3A%20Search%20%3A%20City%20-%20Great%20Falls%2C%20MT',
            '_ga_SK38WR4SG9': 'GS1.1.1726546478.2.1.1726546525.13.0.0',
            'bm_sv': '1B9796357CB98FFBC9DAD915DBEFD384~YAAQhidzaAx96tiRAQAAUG4x/hn6JNwAEu6ZLDynbhb+3yVIriHeSFiudAtp+jhFXo/39kpMYKnOSgMJ3ZrI6UNOeSQv+2Qs+oQ7D+1B6l6wVWoaQxNpMlnB5KQx+fN4H8dN9vzLmxJiuMvJE5UcsB1a3ohx2sM+TlQg3/QtqnfGKRl2ZvKLSB0R3c3/wZG4sI2PvgAPoy4fpmxAoMSnxabZN5FPX+mGhlefAEFf76IskjS+EmDhCjNIv1xl/dFbft92~1',
            'KPI_TA_Visit': '%7B%22g%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22kf%22%3A%22tft.tft2.tfu.tfu2.ppvfl.ppvfl2.ppv_lfpv1.ppv_lfpv2%22%2C%22pp%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22ppv%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22ppi%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22ptf%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22ptfi%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22pbz%22%3A%7B%22t%22%3A26%2C%22p%22%3A2%7D%2C%22pd%22%3A%7B%22t%22%3A19%2C%22p%22%3A1%7D%2C%22pdc%22%3A%7B%22t%22%3A19%2C%22p%22%3A1%7D%2C%22ppv_lf%22%3A%7B%22t%22%3A19%2C%22p%22%3A1%7D%7D',
        }
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            # 'cookie': 'QuantumMetricReplay=https://tmobile.quantummetric.com/#/replay/cookie:f3c8b4519cfc54015aeeb21e736299a3?ts=1726448609-1726535009; _abck=660433ED9B5CC6397FE745A5BE54A182~-1~YAAQX/3UF1UmYMGRAQAAjSvu+gy6yZz5lOC4wqB8fminuc0fMZtw70Egt/43vyTEARklnGWI8hQRHtRmBCF78bUkniKtjTrVNY16s24TA5p8Y3fEgPhopmjS4s8gU4EwAIS9Nie8KUg0/5iPqXDDV/Yumj8l1F2XbgdGNiR8xpa4MBGuB2/ObwuI0pZfidrAZSJjpec/qwsqxJqs+RSX004xElCHfOTyLhXpjn9wdZ8aFPy1uvbL3aJUBcko+Td4LsU8+3eZXQgvg/aVPKY2lxVkTsf2YOvbqP2pKIcV3og+jPJCWR+u3NjJstbC6Dp2j1l0EJ9jZB/iGpygC8kyudOn1wZ6L8joOeoIfTAvQDp+4irenQyEKYEMFQpPLJZL5n1ArFSCjdM9OgLe+K/DEVlwzNZfSxGt1KL01K3MWQ==~-1~-1~-1; bm_mi=67335EC611D5FD6FE52977261CC7F38D~YAAQX/3UF4kmYMGRAQAAIDHu+hkGq+WcR5hKBiersEMYqFWFnPCGAUjUmR1KkSuXbe+u8lTOd1RKF9Zyfdm+sGjSWCFLSU5/bQgw/XlOu9B6i1dXSocJv7tH8nxFBjrbGoTopF8ai6HDXMIN+j2YjW5ax/YeZh5+MFY76BP2ENwcVP/3DtIGkIbDXwL9ijBxfkhoB9iDKl7QjlK+dyGEutf1WYR0Drg9kScUBV33bKqIUNSLuJ3do9uCAMli44xF6ytUPBmjUPUAlaZzT1ZabfrY0Mwc/1+LEk3azU9ioxTjRxcgGVuvGJbJxyFo5mVM/FGs4oEnff+kkkhh64jD5XB4AlMxLQBicc6B9plXdlxK2+fj5DYMevmrnZeJPUR2ABY+xBMJaYBCtwA9GWhRY+GENfS0/JJnEuvouyTITfy5CxUiemEXG7NBVPKz4GrKWCrBWer7ST87GtfXlmtbYKiX6b95~1; TFPIDS=90095dee-37b4-4484-8c4b-f4359526c6e4; TFPID=90095dee-37b4-4484-8c4b-f4359526c6e4; visid_incap_2810275=Nd2kau6fS8GEPyzmqI4PJZcs6GYAAAAAQUIPAAAAAACZ21p+TTOT9QVfW2PNjk0s; incap_ses_8074_2810275=nJsYI4iIpGapoGPHYpwMcJcs6GYAAAAAwdVLQOSSEvFT+PQ/j8JVxQ==; GEOTMO=PRD-TMO-HAP-EAST-2; kndctr_1358406C534BC94D0A490D4D_AdobeOrg_cluster=ind1; kndctr_1358406C534BC94D0A490D4D_AdobeOrg_identity=CiYxNDc1ODE4MTgzMzk4MDgwNTQ5MTMyMzkyNTExNTUwMDA5Njc2NFITCO3ouNefMhABGAEqBElORDEwAPAB7ei4158y; AMCV_1358406C534BC94D0A490D4D%40AdobeOrg=MCMID|14758181833980805491323925115500096764; _ga=GA1.1.1766813937.1726491801; AWSALB=xoJ8CZ+zuBAN8MGYaGYu8XsY+233H4cBDjFRADNaMw3q+PPc+kSASxktn4plnJQW9c7QtQ3UAjm7Y2cHu7o5BfHuuyAj5PFvxLTmWUI1Cz+fMsepnIvYYHHMUs5Y; AWSALBCORS=xoJ8CZ+zuBAN8MGYaGYu8XsY+233H4cBDjFRADNaMw3q+PPc+kSASxktn4plnJQW9c7QtQ3UAjm7Y2cHu7o5BfHuuyAj5PFvxLTmWUI1Cz+fMsepnIvYYHHMUs5Y; search_visitorId=0de8de36-9f8a-4658-b9a6-4ed8a3883443; JSESSIONID=node043n654omabas1mx2ddh2kia3n453666.node0; ak_bmsc=C4ABFA2577AB7F08666C03652B254200~000000000000000000000000000000~YAAQX/3UF64nYMGRAQAA7UXu+hkLJplFb2kaw/ESDyvWTKo7cd5ZxFzJmkrGvXS3G0D5kGWgTwMSp7qIdIxJQj8u+tJFK00ulCrjcrO5J+w78/H+DoTQFUT+1N+j730oqbWDT68N6gkUgbEm/MkOJHV/2Igm36oBkdUEtOrEb6nDxPXxwwh1WXMdztw77CdPQPSMiFE8pcC6EM9fGKiuxhczsQnJcegByV3fbjdwlO33hvlLNrWxgGhwa1aNou8+48T5KTqxBUJ5NqPX1xgl6I9bVIfvF9hdiDnhD5+t1x5HA8QwL/HbMmWGhX0TW/wXlODE0c7pg3jU/l3BaY6UjVDRafrqX8NGnDuiZdAm861cCgmDUNpy1w7WAyyrdoODjnIgY22qHD/o/qvqLTHyScNgsSJVK4bWxVwjyYRtC66oft5MezvntGmxhZLOejP0whncYBS6kg+E/D1JCpTZ1Cfcva9jRXSdebmeroyRKgxmB8tX8aV+52lWONW1K6Y0lZMDxgLbmX12jxZ58cfZEdJ02Wrzib9ZeWstYSMLE7BIZK9hqoI9kWEkEEiBq+p25MsLUrIqWu7cqZEotdxJgTBxKdykXcRKBs098A7ASe5/y4QUNKtuFD7k; QuantumMetricSessionID=f3c8b4519cfc54015aeeb21e736299a3; QuantumMetricUserID=ef618e945ae75bb8409a4a4ecc3a95ae; LPVID=lmMDYxMGJkZjVjNTk4MmQy; LPSID-62258097=s_eh0EnQSOyhWm6C9aBL5Q; bm_sz=BEDB2200D5236D2553B90C5020414A51~YAAQr5YRYNbFWNuRAQAAEozw+hlGqsddrqlQuuPKrnIGxb36UqAJ3yGhFjdeyXnPBEnZlWCyMog5uuwkyb8WlUWYu1VDYD6r8NXQ6GrcHz5752l0XPPhcn2qQkoA1hEnwMh7viyS8vf2UPoGCbYYwfIkYRTG0nk8wFrOvw3rd3/NrOpQvSSIbj8bWcuYmfOd+JTj0Qxm/KeRYDmC73dxWZxDAe0p/4Aol8xGH+IQfCuucTwqG6C1sy38FmvIzpOHV1lmGMW92VoHvdyOreOikYJsjNvx7dHSfIVZHGitGrQjwz45HOesFwypjIlh4QvgYu6ZphV6aBWBWtMjPdzFlkv7JpSZLcJCjYyNqaVWH4BkbK6kfs2EXY/8rmYOHTeQpi08TDOJhk0JNAN/KlXcpddPfUIz8cTebqethP9M~3420726~3354935; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+16+2024+18%3A35%3A55+GMT%2B0530+(India+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=b6a810e9-c721-442a-b7db-e8d44f236645&interactionCount=1&landingPath=NotLandingPage&groups=CX%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2Cgpc%3A1&AwaitingReconsent=false; pv_pageName=TMO%20%7C%20Store%20%3A%20Search%20%3A%20City%20-%20Great%20Falls%2C%20MT; _gcl_au=1.1.798496218.1726491959; _fbp=fb.1.1726491959565.705948091570307811; KPI_EV=1; _ga_NEXYYTFQFY=GS1.1.1726491801.1.1.1726491974.39.0.0; _ga_SK38WR4SG9=GS1.1.1726491801.1.1.1726492356.60.0.0; bm_sv=EE39B211447DD0F8B56D2C1EC149E275~YAAQX/3UFzqFYMGRAQAAC/f2+hnW/22tU0++uol66KfVFxw/oTyhnvrXjFHb5Ch2yyLYQ3WNr1PjHM2yLHlYoSu/Sw3kGCV8PD6dmlws72khbSXuBSlqnSN5+1aKpifqz8eFQRPFTOQl5yKAeMhWJzYAQy5rhTed887wF0gCTIgfz+V1D1UXmB7VyAQlF28NaeDfWiYZ/duu3R1aQ5vmlQ5e/2Q211tO+jJ3HiIz2A5h89GeOjPN3M5JxmM3qQGB5Una~1; KPI_TA_Visit=%7B%22g%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22kf%22%3A%22tft.tft2.ppvfl.ppvfl2.ppv_lfpv1.ppv_lfpv2%22%2C%22pp%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22ppv%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22ppi%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22pd%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22pdc%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22ptf%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22ptfi%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22pbz%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%2C%22ppv_lf%22%3A%7B%22t%22%3A296%2C%22p%22%3A1%7D%7D',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.t-mobile.com/stores/locator/?q=&loc=Montana,%20United%20States&lat=47.072515&lon=-109.172599&bsort=recommended&showall=false',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-csrftoken': 'null',
        }

        locations = self.cur.fetchall()
        for location in locations:
            state, lat, long, loc = location
            print("=============================", state)
            yield scrapy.Request(
                # url=f"https://www.t-mobile.com/stores/api/get-nearby-business/?q=&loc={location['loc']}&lat={location['lat']}&lon={location['lon']}",
                url=f"https://www.t-mobile.com/stores/api/get-nearby-business/?q=&loc={loc}&lat={lat}&lon={long}",
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
                cb_kwargs={"current_page": 1, "lat": lat, "long": long, "state": state, 'loc': loc}
            )

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text)
        file_path = self.page_save + '\\' + kwargs['state'] + ".html.gz"

        if not os.path.exists(self.page_save):
            os.makedirs(self.page_save)
        with gzip.open(file_path, 'wb') as file:
            file.write(response.body)

        product_data = json_data.get('business_list', {}).get('object_list', {})

        item = StoreLocatorsItem()
        if product_data:
            for data in product_data:
                item['state'] = data['locale']['region']['state']
                if item['state'] == kwargs['state']:
                    item['store_id'] = data['external_store_code']
                    item['name'] = data['display_name']
                    item['latitude'] = data['lat']
                    item['longitude'] = data['lon']
                    item['street'] = " ".join(data['address_text_lines'][:-1])
                    item['city'] = data['locale']['name']
                    item['zip_code'] = data['address_postcode']
                    item['country'] = 'USA'
                    item['county'] = ''
                    item['phone'] = data['contact_context']['business_phone_raw']
                    item['open_hours'] = " | ".join(data['all_opening_hours']['schemaHrs'])
                    item['url'] = "https://www.t-mobile.com" + data['business_link'] if data['business_link'] else ''
                    item['provider'] = "T-Mobile"
                    item['category'] = "Computer And Electronics Stores"
                    item['updated_date'] = datetime.today().strftime('%d-%m-%Y')
                    item['status'] = 'Open' if data['all_opening_hours']['isOpen'] == True else 'Closed'
                    item['direction_url'] = data['get_directions_link']
                    yield item

            total_pages = json_data['business_list']['paginator']['num_pages']
            next_page = kwargs['current_page'] + 1 if total_pages >= (kwargs['current_page'] + 1) else None

            if next_page:
                yield scrapy.Request(
                    # url=f"https://www.t-mobile.com/stores/api/get-nearby-business/?q=&loc={location['loc']}&lat={location['lat']}&lon={location['lon']}&page={next_page}",
                    url=f"https://www.t-mobile.com/stores/api/get-nearby-business/?q=&lat={kwargs['lat']}&lon={kwargs['long']}&page={next_page}",
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    cb_kwargs={"current_page": next_page, "lat": kwargs['lat'], "long": kwargs['long'],
                               "state": kwargs['state'], 'loc': kwargs['loc']}
                )


if __name__ == '__main__':
    execute(f'scrapy crawl {TMobileSpider.name}'.split())
