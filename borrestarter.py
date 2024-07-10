import time
import subprocess
import requests
from web3 import Web3, HTTPProvider
from requests.auth import HTTPBasicAuth
from datetime import datetime

polygon_main = "https://your.polygonnode.com"
polygon_block_prev = 0

def restart_service(service_name):
    try:
        subprocess.run(['systemctl', 'restart', service_name], check=True)
        print(f"Service '{service_name}' restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart service '{service_name}': {e}")

def main(polygon_block_prev):
    service_name = "bor"
    while True:
        last_block_main = get_polygon_local(polygon_main)
        print("polygon_node_last: " + str(last_block_main))
        if last_block_main == polygon_block_prev:
            restart_service(service_name)
            print("Service restarted")
        else:
            print("Not necessary to restart")
        polygon_block_prev = last_block_main
        time.sleep(180)  # Sleep for 3 minutes (180 seconds)

def get_polygon_local(polygon_main):
    print("Hello")
    block_info = {
        "jsonrpc":"2.0",
        "method":"eth_getBlockByNumber",
        "params":["latest", True],
        "id": 1
        }
    response = requests.post(f"{polygon_main}", json=block_info)
    resp_data = response.json()
    last_block = int(resp_data["result"]["number"],16)
    print(last_block)
    return last_block

if __name__ == "__main__":
    main(polygon_block_prev)
