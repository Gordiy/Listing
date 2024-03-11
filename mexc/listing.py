from sdk.build.lib.mexc_sdk import Spot


class Listing:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = Spot(api_key=api_key, api_secret=api_secret)
