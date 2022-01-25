import os

CHROME_OPTIONS = [
    '--no-sandbox',
    '--start-maximized',
    f'user-data-dir={os.path.abspath("User Data")}',
    'profile-directory=Binance'
]

CHROME_EXPERIMENTAL_OPTIONS = [
    ('excludeSwitches', ['enable-automation']),
    ('useAutomationExtension', False)
]

CHROME_USER_PROFILE_PREFERENCES = [
    ("credentials_enable_service", False),
    ("profile.password_manager_enabled", False)
]

# LOGIN_URL = 'https://accounts.binance.com/ru/login'
# LOGIN_URL = 'https://www.binance.com/ru/nft/mystery-box'
LOGIN_URL = 'https://www.binance.com/ru/nft/goods/sale/166902090169088000?isBlindBox=1&isOpen=false'
API_AUTH_URL = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/product-onsale'
# API_BUYING_URL = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create'  # For items
API_BUYING_URL = 'https://www.binance.com/bapi/nft/v1/private/nft/mystery-box/purchase'  # For mystery boxes
