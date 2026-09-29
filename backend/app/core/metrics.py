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
        self.request_histogram = {
            bucket: 0 for bucket in (0.01, 0.05, 0.1, 0.5, 1.0, 5.0, float("inf"))
        }
        self.triage_histogram = {
            bucket: 0 for bucket in (0.01, 0.1, 0.5, 1.0, 5.0, 10.0, float("inf"))
        }

    def record_cache(self, hit: bool) -> None:
        with self._lock:
            self.cache_lookups += 1
            if hit:
                self.cache_hits += 1

    @staticmethod
    def _observe(histogram, value: float) -> None:
        for bucket in histogram:
            if value <= bucket:
                histogram[bucket] += 1

    def record_request(self, started: float) -> None:
        with self._lock:
            self.requests_total += 1
            elapsed = perf_counter() - started
            self.request_seconds_total += elapsed
            self._observe(self.request_histogram, elapsed)

    def record_triage(self, latency_ms: int, fallback: bool) -> None:
        with self._lock:
            self.triage_total += 1
            elapsed = latency_ms / 1000
            self.triage_seconds_total += elapsed
            self._observe(self.triage_histogram, elapsed)
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
                    *[
                        f'civicpulse_request_latency_seconds_bucket{{le="{("+Inf" if b == float("inf") else b)}"}} {v}'
                        for b, v in self.request_histogram.items()
                    ],
                    f"civicpulse_request_latency_seconds_count {self.requests_total}",
                    f"civicpulse_request_latency_seconds_sum {self.request_seconds_total:.6f}",
                    "# TYPE civicpulse_triage_total counter",
                    f"civicpulse_triage_total {self.triage_total}",
                    "# TYPE civicpulse_triage_seconds_total counter",
                    f"civicpulse_triage_seconds_total {self.triage_seconds_total:.6f}",
                    *[
                        f'civicpulse_triage_latency_seconds_bucket{{le="{("+Inf" if b == float("inf") else b)}"}} {v}'
                        for b, v in self.triage_histogram.items()
                    ],
                    f"civicpulse_triage_latency_seconds_count {self.triage_total}",
                    f"civicpulse_triage_latency_seconds_sum {self.triage_seconds_total:.6f}",
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
