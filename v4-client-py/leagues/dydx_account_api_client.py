from typing import Dict, List, Optional

class DydxAccountApiClient:
    def __init__(self, mnemonic: str):
        # Initialize the Dydx API client with the provided mnemonic
        # You can implement the initialization logic here
        self.mnemonic = mnemonic

    def get_subaccounts(self, address: str) -> List[Dict]:
        # Implement the logic to get subaccounts
        pass

    def get_subaccount(self, address: str, subaccount_number: int) -> Optional[Dict]:
        # Implement the logic to get a specific subaccount
        pass

    def get_asset_positions(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get asset positions
        pass

    def get_perpetual_positions(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get perpetual positions
        pass

    def get_transfers(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get transfers
        pass

    def get_orders(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get orders
        pass

    def get_fills(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get fills
        pass

    def get_funding(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get funding
        pass

    def get_historical_pnl(self, address: str, subaccount_number: int) -> List[Dict]:
        # Implement the logic to get historical pnl
        pass

