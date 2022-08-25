from datetime import datetime, time, timezone

def regular_market_open() -> bool:
    open = datetime.utcnow().replace(hour = 13, minute = 30, second=00, tzinfo=timezone.utc).timestamp()
    close = datetime.utcnow().replace(hour = 20, minute = 00, second=00, tzinfo=timezone.utc).timestamp()
    now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    return ((now >= open) and (now <= close))

    #pre market = 0400 - 0930

def pre_market_open() -> bool:
    open = datetime.utcnow().replace(hour = 8, minute = 00, second=00, tzinfo=timezone.utc).timestamp()
    close = datetime.utcnow().replace(hour = 13, minute = 30, second=00, tzinfo=timezone.utc).timestamp()
    now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    return ((now >= open) and (now <= close))

    #post market = 1600 - 2000

def post_market_open() -> bool:
    open = datetime.utcnow().replace(hour = 20, minute = 00, second=00, tzinfo=timezone.utc).timestamp()
    close = datetime.utcnow().replace(hour = 00, minute = 00, second=00, tzinfo=timezone.utc).timestamp()
    now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    return ((now >= open) and (now <= close))
