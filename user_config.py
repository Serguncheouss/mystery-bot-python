###############
# CREDENTIALS #
###############

LOGIN = ''
PASSWORD = ''

###########
# REQUEST #
###########

REQUESTS_COUNT = 500  # Binance may be blocks almost all of them or ban you IP.
# SALE_TIME = 1639134000
# PURCHASE_INFO = {"number": 1, "productId": 164982370297592832}

################
# WAITING TIME #
################

LOGIN_BEFORE_TIME = 5  # 60 * 5 seconds (5 minutes)
PREPARE_REQUEST_BEFORE_TIME = 60  # 60 seconds (1 minute)
SALE_TIME = 1640084400000 / 1000  # Milliseconds (1/1,000 second)(UNIX time)

############
# TIMEOUTS #
############

DEFAULT_ELEMENT_WAITING_TIMEOUT = 200
DEFAULT_LOGIN_WAITING_TIMEOUT = 60 * 15  # 900 seconds

##############
# ORDER INFO #
##############

PURCHASE_INFO = {'number': 1, 'productId': 169335466973000704}
