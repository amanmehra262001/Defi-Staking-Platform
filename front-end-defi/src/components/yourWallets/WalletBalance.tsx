import { useEthers, useTokenBalance } from "@usedapp/core"
import { formatUnits } from "@ethersproject/units"
import { Token } from "../Main"
import { BalanceMsg } from "../../components/BalanceMsg"


export interface WalletBalanceProps {
    token: Token
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const tokenbalance = useTokenBalance(address, account)

    const formattedTokenBalance: number = tokenbalance ? parseFloat(formatUnits(tokenbalance, 18)) : 0
    // console.log(tokenbalance)
    return (<BalanceMsg
        label={`Your unstaked ${name} balance`}
        tokenImgSrc={image}
        amount={formattedTokenBalance} />)
}