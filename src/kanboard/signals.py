import datetime

def set_backlogged_at(sender, instance, **kwargs):
    if instance.id: return None
    instance.backlogged_at = datetime.datetime.now()
