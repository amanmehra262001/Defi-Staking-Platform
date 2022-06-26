// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    // Stake tokens
    // unstake
    // issue tokens
    // add allowed tokens
    // getETH value
    address[] public allowedToken;
    address[] public stakers;
    IERC20 public dappToken;
    mapping(address => mapping(address => uint256)) public stakingBalance;
    mapping(address => uint256) public UniqueTokenStaked;
    mapping(address => address) public tokenPriceFeedMapping;

    constructor(address _dappTokenAddress) public {
        dappToken = IERC20(_dappTokenAddress);
    }

    function stakeToken(uint256 _amount, address _token) public {
        // what tokenscan they stake
        // how much can they stake
        require(_amount > 0, "Amount need to be greater than 0");
        require(tokenIsAllowed(_token), "Token is currently not available.");
        // abi
        // address
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokenStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        if (UniqueTokenStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unstakeToken(address _token) public {
        // How much of this token does user have
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance can not be 0");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        UniqueTokenStaked[msg.sender] = UniqueTokenStaked[msg.sender] - 1;
    }

    function issue_token() public onlyOwner {
        for (
            uint256 stakersindex = 0;
            stakersindex < stakers.length;
            stakersindex++
        ) {
            address recipient = stakers[stakersindex];
            // send them a token reward
            // based on their total value locked
            uint256 userTotalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(UniqueTokenStaked[_user] > 0, "No Tokens Staked!");
        for (
            uint256 allowedTokenIndex = 0;
            allowedTokenIndex < allowedToken.length;
            allowedTokenIndex++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(_user, allowedToken[allowedTokenIndex]);
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        if (UniqueTokenStaked[_user] <= 0) {
            return 0;
        }
        // price of token * stakengBalance[_token][_User]
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return ((stakingBalance[_token][_user] * price) / 10**decimals);
    }

    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        // we also care about the decimals
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function setPriceFeedContract(address _token, address _pricefeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _pricefeed;
    }

    function updateUniqueTokenStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            UniqueTokenStaked[_user] = UniqueTokenStaked[_user] + 1;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedToken.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (
            uint256 allowedTokenIndex = 0;
            allowedTokenIndex < allowedToken.length;
            allowedTokenIndex++
        ) {
            if (allowedToken[allowedTokenIndex] == _token) {
                return true;
            }
        }
        return false;
    }
}
