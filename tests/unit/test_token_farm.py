
from brownie import network, exceptions
from scripts.helpfullscripts import INITIAL_VALUE, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.deploy import deploy_token_farm_and_dapp_token
import pytest


def test_set_price_feed_contract():
    # Assert
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    token_farm.setPriceFeedContract(dapp_token.address, get_contract(
        "eth_usd_price_feed"), {"from": account})
    # Assert
    assert (token_farm.tokenPriceFeedMapping(
        dapp_token.address) == get_contract("eth_usd_price_feed"))
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token.address, get_contract(
            "eth_usd_price_feed"), {"from": non_owner})


def test_stake_tokens(amount_staked):
    # Assert
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeToken(amount_staked, dapp_token.address, {"from": account})

    # Assert
    assert((token_farm.stakingBalance(
        dapp_token.address, account.address)) == amount_staked)
    assert token_farm.UniqueTokenStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    # ASSERT
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing.......")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)

    # ACT
    token_farm.issue_token({"from": account})

    # ASSERT
    assert(dapp_token.balanceOf(account.address)
           == starting_balance + INITIAL_VALUE)
