import asyncio
import logging
from v4_client_py.chain.aerial.wallet import LocalWallet
from v4_client_py.clients.dydx_subaccount import Subaccount

from v4_client_py.clients.dydx_validator_client import ValidatorClient
from v4_client_py.clients.constants import BECH32_PREFIX, Network

from tests.constants import DYDX_TEST_MNEMONIC

import asyncio
import logging
import os
import sys
from random import randrange

from v4_client_py.chain.aerial.wallet import LocalWallet
from v4_client_py.clients import CompositeClient, Subaccount
from v4_client_py.clients.constants import BECH32_PREFIX, Network

from v4_client_py.clients.helpers.chain_helpers import (
    ORDER_FLAGS_LONG_TERM,
    OrderType,
    OrderSide,
    OrderTimeInForce,
    OrderExecution,
)

from tests.constants import MAX_CLIENT_ID
from mnemonic_parser import MnemonicManager, MnemonicManagerSingleton

# Set the mnemonic as a variable in your shell


mnemonic_manager = MnemonicManagerSingleton().get_mnemonic_manager()
try:
    address_to_query = 'dydx1az8je6f07lv7rkhuq5hd8cac9e9uw3r38yncdl'
    mnemonic = mnemonic_manager.get_mnemonic(address_to_query)
    # print(f"MNEMONIC for {address_to_query}: {mnemonic}")
except KeyError as e:
    print(e)

c678_addr = 'dydx1xcts7yg9cuyxcxqgjes4fyw4723e8kfam05xf6'

# if MNEMONIC is None:
#     print("MNEMONIC not provided.")
#     sys.exit(1)

# define objects to be used with the SDK
wallet = LocalWallet.from_mnemonic(mnemonic, BECH32_PREFIX)
network = Network.mainnet()
client = CompositeClient(
    network,
)
subaccount = Subaccount(wallet, 0)



async def main() -> None:
    transfer_amount = 1/1000000
    try:
        tx = client.transfer_to_subaccount(
            subaccount=subaccount,
            recipient_address=c678_addr,
            recipient_subaccount_number=0,
            amount= transfer_amount,
        )
        print('**Transfer Tx**')
        print(tx)
    except Exception as e:
        print(e)

    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())

