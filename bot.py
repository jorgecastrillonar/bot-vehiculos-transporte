#########################################################

from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    
#########################################################


#########################################################

if __name__ == '__main__':
    bot.polling(timeout=20)
    
#########################################################