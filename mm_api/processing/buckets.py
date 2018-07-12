from processing.redis_models import RedisDictModel


class Bucket(RedisDictModel):
  def __init__(self):
    pass


class HourlyBucket(Bucket):
  def __init__(self):
    pass


class DataStoreService(object):

  bucket_types = [
    HourlyBucket
  ]

  def generate_bucket_name(self, event):
    return event.data

  def update_buckets(self, event):
    for bucket_type in self.bucket_types:
      bucket = bucket_type(self.generate_bucket_name(event))
      self.update_metrics(event)

  def update_metrics(self, event):
    

    


