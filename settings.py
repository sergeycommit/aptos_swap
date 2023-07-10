TOKEN_ADDRESSES = {
    'CAKE':"0x159df6b7689437016108a019fd5bef736bac692b6d4a1f10c941f6fbb9a74ca6::oft::CakeOFT",
    'BLT': "0xfbab9fb68bd2103925317b6a540baa20087b1e7a7a4eb90badee04abb6b5a16f::blt::Blt",
    'APT': "0x1::aptos_coin::AptosCoin",
    'USDT': "0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T",
    'WETH': "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::WETH",
    'USDC': "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC"
}

GAS_LIMIT = 1000

GAS_PRICE = 100

#   Можно поставить свою RPC
NODE_URL = "https://rpc.ankr.com/http/aptos/v1"

#   Можно поставить свой роутер
PANCAKESWAP_ROUTER = "0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::router::swap_exact_input"
ROUTER = PANCAKESWAP_ROUTER

#   Задержка между кошельками в секундах
WAIT_FROM = 5
WAIT_TO = 20
