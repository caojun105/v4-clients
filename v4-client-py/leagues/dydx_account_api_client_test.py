# Example usage:
from dydx_account_api_client import DydxAccountApiClient
try:
    mnemonic = "your_mnemonic_here"
    dydx_api = DydxAccountApiClient(mnemonic)

    # Use the class methods to interact with the Dydx API
    subaccounts = dydx_api.get_subaccounts("example_address")
    subaccount = dydx_api.get_subaccount("example_address", 0)
    asset_positions = dydx_api.get_asset_positions("example_address", 0)
    perpetual_positions = dydx_api.get_perpetual_positions("example_address", 0)
    transfers = dydx_api.get_transfers("example_address", 0)
    orders = dydx_api.get_orders("example_address", 0)
    fills = dydx_api.get_fills("example_address", 0)
    funding = dydx_api.get_funding("example_address", 0)
    historical_pnl = dydx_api.get_historical_pnl("example_address", 0)

except Exception:
    print("An error occurred.")
