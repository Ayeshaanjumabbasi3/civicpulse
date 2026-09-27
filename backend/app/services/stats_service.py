import json
class StatsService:
    def __init__(self,repo,redis_cache): self.repo=repo; self.redis_cache=redis_cache
    def get(self):
        cached=self.redis_cache.get('stats:global')
        if cached:return json.loads(cached),'HIT'
        data=self.repo.get_aggregates(); self.redis_cache.set('stats:global',json.dumps(data,default=lambda x:x.value),30); return data,'MISS'
