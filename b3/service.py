import datetime
from decimal import Decimal

from b3.repository import get_file
import re

def get_valid_tickers(tickers):
    tickers = tickers.split(',')
    tickers = filter(lambda ticker: re.fullmatch('[A-Z]{4}[0-9]{1,2}', ticker), tickers)
    tickers = set(tickers)
    return list(tickers)


def get_stocks_prices(tickers, dates):
    lines = get_file(dates[0].year)
    data = []

    for line in lines:
        if line[:2] != '01':
            continue

        if line[12:24].strip() not in tickers:
            continue

        if datetime.datetime.strptime(line[2:10], '%Y%m%d').date() not in dates:
            continue

        data.append(parse_object(line))

    return data

def parse_object(line):
    return {
        "TIPREG": int(line[0:2]),
        "DATA": datetime.datetime.strptime(line[2:10], '%Y%m%d').date(),
        "CODBDI": int(line[10:12]),
        "CODNEG": line[12:24].strip(),
        "TPMERC": int(line[24:27]),
        "NOMRES": line[27:39].strip(),
        "ESPECI": line[39:49].strip(),
        "PRAZOT": int(line[49:52]) if line[49:52].strip() != '' else None,
        "MODREF": line[52:56].strip(),
        "PREABE": Decimal(line[56:69]) / 100,
        "PREMAX": Decimal(line[69:82]) / 100,
        "PREMIN": Decimal(line[82:95]) / 100,
        "PREMED": Decimal(line[95:108]) / 100,
        "PREULT": Decimal(line[108:121]) / 100,
        "PREOFC": Decimal(line[121:134]) / 100,
        "PREOFV": Decimal(line[134:147]) / 100,
        "TOTNEG": int(line[147:152]),
        "QUATOT": int(line[152:170]),
        "VOLTOT": Decimal(line[170:188]) / 100,
        "PREEXE": Decimal(line[188:201]) / 100,
        "INDOPC": int(line[201:202]),
        "DATVEN": datetime.datetime.strptime(line[202:210], "%Y%m%d").date(),
        "FATCOT": int(line[210:217]),
        "PTOEXE": Decimal(line[217:230]) / 1000000,
        "CODISI": line[230:242].strip(),
        "DISMES": int(line[242:245])
    }