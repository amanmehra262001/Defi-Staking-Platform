import json
import os
import shutil
from brownie import config, DappToken, TokenFarm, network
from scripts.helpfullscripts import get_account, get_contract
from web3 import Web3
import yaml


KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_dapp_token(front_end=False):
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(dapp_token.address, {
                                  "from": account}, publish_source=config["networks"][network.show_active()].get("verify", False))
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply()-KEPT_BALANCE, {"from": account})
    tx.wait(1)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    if front_end:
        update_front_end()
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        tx = token_farm.addAllowedTokens(token.address, {"from": account})
        tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)
        return token_farm


def update_front_end():
    copy_folders_to_front_end("./build", "./front-end-defi/src/chain-info")
    with open("brownie-config.yaml", "r") as bc:
        config_dict = yaml.load(bc, Loader=yaml.FullLoader)
        with open("./front-end-defi/src/brownie-config.json", "w") as bcj:
            json.dump(config_dict, bcj)
    print("Front end Defi updated!")


def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    deploy_token_farm_and_dapp_token(front_end=True)