from threading import Lock
from time import perf_counter


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self.requests_total = 0
        self.request_seconds_total = 0.0
        self.triage_seconds_total = 0.0
        self.triage_total = 0
        self.fallback_total = 0
        self.cache_lookups = 0
        self.cache_hits = 0

    def record_cache(self, hit: bool) -> None:
        with self._lock:
            self.cache_lookups += 1
            if hit:
                self.cache_hits += 1

    def record_request(self, started: float) -> None:
        with self._lock:
            self.requests_total += 1
            self.request_seconds_total += perf_counter() - started

    def record_triage(self, latency_ms: int, fallback: bool) -> None:
        with self._lock:
            self.triage_total += 1
            self.triage_seconds_total += latency_ms / 1000
            if fallback:
                self.fallback_total += 1

    def prometheus(self) -> str:
        with self._lock:
            return "\n".join(
                [
                    "# TYPE civicpulse_requests_total counter",
                    f"civicpulse_requests_total {self.requests_total}",
                    "# TYPE civicpulse_request_seconds_total counter",
                    f"civicpulse_request_seconds_total {self.request_seconds_total:.6f}",
                    "# TYPE civicpulse_triage_total counter",
                    f"civicpulse_triage_total {self.triage_total}",
                    "# TYPE civicpulse_triage_seconds_total counter",
                    f"civicpulse_triage_seconds_total {self.triage_seconds_total:.6f}",
                    "# TYPE civicpulse_triage_fallback_total counter",
                    f"civicpulse_triage_fallback_total {self.fallback_total}",
                    "# TYPE civicpulse_triage_cache_lookups_total counter",
                    f"civicpulse_triage_cache_lookups_total {self.cache_lookups}",
                    "# TYPE civicpulse_triage_cache_hits_total counter",
                    f"civicpulse_triage_cache_hits_total {self.cache_hits}",
                    "# TYPE civicpulse_triage_cache_hit_ratio gauge",
                    f"civicpulse_triage_cache_hit_ratio {(self.cache_hits / self.cache_lookups) if self.cache_lookups else 0:.6f}",
                    "",
                ]
            )


metrics = Metrics()
