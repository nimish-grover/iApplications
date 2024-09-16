# app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from iTraining import app as Training
from iWater import app as Water
from iCore import app as Core
from iFinance import app as Finance
from iBot import app as Waterbot
from iLand import app as Land
from iCarbon import app as Carbon
from iSaksham import app as Saksham
from eSaksham import app as eSaksham
from eSaksham_1 import app as eSaksham_1

application = DispatcherMiddleware(Core, {
    '/iwater': Water,
    '/itraining': Training,
    '/ifinance': Finance,
    '/ibot': Waterbot,
    '/iland': Land,
    '/icarbon':Carbon,
    '/isaksham':Saksham,
    '/esaksham':eSaksham,
    '/esaksham_1':eSaksham_1
})

# application = iCore