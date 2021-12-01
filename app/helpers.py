import json
import os
import requests

from datetime import datetime, timedelta


def get_account_stats(addr):
    os.environ["EXPLORER_API"] = "https://explorer.thetatoken.org:8443/api"
    uri = os.getenv("EXPLORER_API") + f"/account/{addr}"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)
    account = req.json()
    account["body"]["balance"]["theta"] = '{0:.4f}'.format(int(account["body"]["balance"]["thetawei"])/10**18)
    account["body"]["balance"]["tfuel"] = '{0:.4f}'.format(int(account["body"]["balance"]["tfuelwei"])/10**18)

    return account


def get_node_stake_by_acc(addr):
    os.environ["EXPLORER_API"] = "https://explorer.thetatoken.org:8443/api"
    uri = os.getenv("EXPLORER_API") + f"/accounttx/{addr}?type=10&type=11"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)
    txs = req.json()

    # note add and sub order not important
    node_stake_by_acc = {} 
    for tx in txs["body"]:
        # add type=10
        if tx["type"] == 10:
            try:
                node_stake_by_acc[tx["data"]["source"]["address"]] += int(int(tx["data"]["source"]["coins"]["tfuelwei"])/10**18)
            except KeyError:
                node_stake_by_acc[tx["data"]["source"]["address"]] = int(+int(tx["data"]["source"]["coins"]["tfuelwei"])/10**18)
        # sub type=11
        elif tx["type"] == 11:
            try:
                node_stake_by_acc[tx["data"]["source"]["address"]] -= int(int(tx["data"]["source"]["coins"]["tfuelwei"])/10**18)
            except KeyError:
                node_stake_by_acc[tx["data"]["source"]["address"]] = int(-int(tx["data"]["source"]["coins"]["tfuelwei"])/10**18)

    return node_stake_by_acc


def get_ok_status(statistics):
    current_utc = datetime.utcnow()

    for stat in statistics:
        if stat["created_at"][-3] == ":":
            stat["created_at"] = "".join(list(stat["created_at"][:-3]) + list(stat["created_at"][-2:]))

        # truncate milliseconds from RFC3339 datetime string
        if stat["created_at"][-5] == ".":
            stat["created_at"] = "".join(list(stat["created_at"][:-5]) + list(stat["created_at"][-1]))
        elif stat["created_at"][-4] == ".":
            stat["created_at"] = "".join(list(stat["created_at"][:-4]) + list(stat["created_at"][-1]))

        try:
            created_utc = datetime.strptime(stat["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            created_utc = datetime.strptime(stat["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        if current_utc.timestamp() - created_utc.timestamp() <= 60*10:
            stat["ok_status"] = 0
        elif current_utc.timestamp() - created_utc.timestamp() <= 60*60:
            stat["ok_status"] = 1
        elif current_utc.timestamp() - created_utc.timestamp() > 60*60:
            stat["ok_status"] = 2

    return statistics


def get_block_uptimes(addr, min):
    # get block stats
    uri = os.getenv("EDGESTATS_API_ADDR") + f"/stats/blocks/{min}"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)
    blocks = req.json()

    # get missed blocks
    uri = os.getenv("EDGESTATS_API_ADDR") + f"/stats/blocks/misses/{addr}/{min}"
    headers = {"x-api-key": os.getenv("EDGESTATS_API_KEY")}
    req = requests.request("GET", uri, json={}, headers=headers)
    misses = req.json()
    
    # get current time
    min_dt = datetime.strptime(min, "%Y-%m-%dT%H:%M:%SZ")

    # get 24hr blocks & misses
    blocks_24hr = []
    misses_24hr = []
    cutoff_24hr = (min_dt + timedelta(days=29)).isoformat()
    for block in blocks:
        if block["created_at"] > cutoff_24hr:
            blocks_24hr.append(block)
    for miss in misses:
        if miss["created_at"] > cutoff_24hr:
            misses_24hr.append(miss)

    # get 7day blocks & misses
    blocks_7day = []
    misses_7day = []
    cutoff_7day = (min_dt + timedelta(days=23)).isoformat()
    for block in blocks:
        if block["created_at"] > cutoff_7day:
            blocks_7day.append(block)
    for miss in misses:
        if miss["created_at"] > cutoff_7day:
            misses_7day.append(miss)

    # get uptime ratios
    ratios = {
        "24hr": '{0:.2f}'.format(100*(1.0 - (len(misses_24hr) / len(blocks_24hr)))),
        "7day": '{0:.2f}'.format(100*(1.0 - (len(misses_7day) / len(blocks_7day)))),
        "30day": '{0:.2f}'.format(100*(1.0 - (len(misses) / len(blocks)))),
    }

    # add aggs to object
    aggregates = {
        "blocks": {
            "24hr": len(blocks_24hr),
            "7day": len(blocks_7day),
            "30day": len(blocks),
            "list": blocks,
        },
        "misses": {
            "24hr": len(misses_24hr),
            "7day": len(misses_7day),
            "30day": len(misses),
            "list": misses,
        },
        "uptime": {
            "24hr": ratios["24hr"],
            "7day": ratios["7day"],
            "30day": ratios["30day"],
        },
    }

    return aggregates
