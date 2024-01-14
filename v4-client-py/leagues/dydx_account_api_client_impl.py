from v4_client_py.clients import IndexerClient, Subaccount
from v4_client_py.clients.constants import Network
import os
import sys
from typing import Dict, List, Optional


client = IndexerClient(
    config=Network.mainnet().indexer_config,
)

class PerpetualPositionFields:
    status = 'status'
    side = 'side'
    size = 'size'
    maxSize = 'maxSize'
    entryPrice = 'entryPrice'
    createdAt = 'createdAt'
    createdAtHeight = 'createdAtHeight'
    closedAt = 'closedAt'
    sumOpen = 'sumOpen'
    sumClose = 'sumClose'
    netFunding = 'netFunding'
    realizedPnl = 'realizedPnl'
    unrealizedPnl = 'unrealizedPnl'

class AssetPositionFields:
    size = 'size'
    side = 'side'
    assetId = 'assetId'

class DydxAccountApiClientImpl:
    def __init__(self):
        # Initialize the Dydx API client with the provided mnemonic
        # You can implement the initialization logic here
        self.client = IndexerClient(config=Network.mainnet().indexer_config)

    ## 总的入口，可以获得所有信息
    def get_subaccounts(self, address: str) -> List[Dict]:
        try:
            subaccounts_response = self.client.account.get_subaccounts(address)
            return subaccounts_response.data["subaccounts"]
        except Exception as e:
            print(f"Failed to get subaccounts: {e}")
            return []

    def get_subaccount(self, address: str, subaccount_number: int) -> Optional[Dict]:
        try:
            subaccount_response = self.client.account.get_subaccount(address, subaccount_number)
            return subaccount_response.data["subaccount"]
        except Exception as e:
            print(f"Failed to get subaccount: {e}")
            return None

    def get_asset_positions(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            asset_positions_response = self.client.account.get_subaccount_asset_positions(address, subaccount_number)
            return asset_positions_response.data["positions"]
        except Exception as e:
            print(f"Failed to get asset positions: {e}")
            return []

    def get_perpetual_positions(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            perpetual_positions_response = self.client.account.get_subaccount_perpetual_positions(address, subaccount_number)
            return perpetual_positions_response.data["positions"]
        except Exception as e:
            print(f"Failed to get perpetual positions: {e}")
            return []

    def get_transfers(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            transfers_response = self.client.account.get_subaccount_transfers(address, subaccount_number)
            return transfers_response.data["transfers"]
        except Exception as e:
            print(f"Failed to get transfers: {e}")
            return []

    def get_orders(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            orders_response = self.client.account.get_subaccount_orders(address, subaccount_number)
            return orders_response.data
        except Exception as e:
            print(f"Failed to get orders: {e}")
            return []

    def get_fills(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            fills_response = self.client.account.get_subaccount_fills(address, subaccount_number)
            return fills_response.data["fills"]
        except Exception as e:
            print(f"Failed to get fills: {e}")
            return []

    def get_funding(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            funding_response = self.client.account.get_subaccount_funding(address, subaccount_number)
            return funding_response.data["fundingPayments"]
        except Exception as e:
            print(f"Failed to get funding: {e}")
            return []

    def get_historical_pnl(self, address: str, subaccount_number: int) -> List[Dict]:
        try:
            historical_pnl_response = self.client.account.get_subaccount_historical_pnls(address, subaccount_number)
            return historical_pnl_response.data["historicalPnl"]
        except Exception as e:
            print(f"Failed to get historical pnl: {e}")
            return []

class DydxSubaccount:
    def __init__(self, subaccount_data: Dict):
        self.address = subaccount_data.get('address', '')
        self.subaccount_number = subaccount_data.get('subaccountNumber', 0)
        self.equity = subaccount_data.get('equity', '0')
        self.free_collateral = subaccount_data.get('freeCollateral', '0')
        self.open_perpetual_positions = self._parse_positions(subaccount_data.get('openPerpetualPositions', {}), PerpetualPositionFields)
        self.asset_positions = self._parse_positions(subaccount_data.get('assetPositions', {}), AssetPositionFields)
        self.margin_enabled = subaccount_data.get('marginEnabled', False)

    def get_perpetual_positions(self) -> Dict:
        return self._parse_positions(self.open_perpetual_positions, PerpetualPositionFields)

    def get_asset_positions(self) -> Dict:
        return self._parse_positions(self.asset_positions, AssetPositionFields)

    def _parse_positions(self, positions_data: Dict, field_class) -> Dict:
        parsed_positions = {}
        required_fields = [getattr(field_class, field) for field in dir(field_class) if not callable(getattr(field_class, field)) and not field.startswith("__")]

        for symbol, position_data in positions_data.items():
            missing_fields = [field for field in required_fields if field not in position_data]
            if missing_fields:
                raise ValueError(f"Missing fields {missing_fields} in position data for {field_class.__name__} with key '{symbol}'")

            parsed_positions[symbol] = {
                field: position_data[field] for field in required_fields
            }

        return parsed_positions


# # Example usage:
try:
    address = 'dydx135fhnvd8ca0wjuwzzhyn7pzrz33tpuytjvh7g9'
    mnemonic = "your_mnemonic_here"
    dydx_api = DydxAccountApiClientImpl()

    # Use the class methods to interact with the Dydx API
    example_address = 'dydx135fhnvd8ca0wjuwzzhyn7pzrz33tpuytjvh7g9'
    subaccounts = dydx_api.get_subaccounts(example_address)
#     #print(subaccounts)
#     subaccount = dydx_api.get_subaccount(example_address, 0)
#     #print(subaccounts)
#     asset_positions = dydx_api.get_asset_positions(example_address, 0)
#     print(asset_positions)
#     perpetual_positions = dydx_api.get_perpetual_positions(example_address, 0)
#     transfers = dydx_api.get_transfers(example_address, 0)
#     orders = dydx_api.get_orders(example_address, 0)
#     fills = dydx_api.get_fills(example_address, 0)
#     funding = dydx_api.get_funding(example_address, 0)
#     historical_pnl = dydx_api.get_historical_pnl(example_address, 0)

except Exception as e:
    print(f"Failed to get historical pnl: {e}")


dydx_subaccounts = [DydxSubaccount(subaccount_data) for subaccount_data in subaccounts]

# Accessing fields
for subaccount in dydx_subaccounts:
    try:
        print(f"Subaccount Open Perpetual Positions: {subaccount.get_perpetual_positions()}")
    except ValueError as e:
        print(f"Error: {e}")
    try:
        print(f"Subaccount Asset Positions: {subaccount.get_asset_positions()}")
    except ValueError as e:
        print(f"Error: {e}")

