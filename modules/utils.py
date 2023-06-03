import time
import weakref

from colorama import Fore

from dateutil import parser
from datetime import datetime
from dateutil.relativedelta import relativedelta

class InstanceCache:
    def __init__(self, ttl):
        self.ttl = ttl
        self.cache = {}
        
    def get(self, cls, args):
        now = time.time()

        # Remove expired entries from the cache
        self.cache = {k: v for k, v in self.cache.items() if v[1] > now}

        # If a cached instance exists and hasn't expired, return it
        if args in self.cache:
            return self.cache[args][0]()

        # Otherwise, return None
        return None
        
    def add(self, instance, args):
        now = time.time()
        expiration = now + self.ttl

        # Store a weak reference to the instance in the cache
        self.cache[args] = (weakref.ref(instance), expiration)
        
def get_time() -> str:
    now_utc = datetime.utcnow()
    current_time = now_utc.strftime("%H:%M:%S") 
    return current_time

def get_date() -> str:
    now_utc = datetime.utcnow()
    current_date = now_utc.strftime("%d/%m/%Y")
    return current_date

def get_access_extension(current_expiration_date: str, extension_type: str, extension_length: str):
    expiration = parser.parse(current_expiration_date)
    if(extension_type == 'Y'):
        expiration = expiration + relativedelta(years = extension_length)
    elif(extension_type == 'M'):
        expiration = expiration + relativedelta(months = extension_length)
    elif(extension_type == 'W'):
        expiration = expiration + relativedelta(weeks = extension_length)
    elif(extension_type == 'D'):
        expiration = expiration + relativedelta(days = extension_length)
    return str(expiration)

def log(level: str, message: str):
    date = get_date()
    datetime = get_time()

    write_message = "{: <12} {: <10} {: <8} {: <10}".format(date, datetime, level.upper(), message)

    try:
        with open("indicator_manager.log", "a", encoding = "utf-8") as log_text_file:
            print(Fore.BLUE + f"\nLog → {write_message}")
            log_text_file.write(write_message + "\n")

    except Exception as error:
        print(Fore.RED + "\n\n\n" + traceback.format_exc() + "\n\n\n")
    