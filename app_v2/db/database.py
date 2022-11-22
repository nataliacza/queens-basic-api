from deta import Deta

from config import settings

deta = Deta(settings.deta_project_key)
users_db = deta.Base("users")
categories_db = deta.Base("categories")
cities_db = deta.Base("cities")
queens_db = deta.Base("queens")
