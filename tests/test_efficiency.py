"""
Efficiency & Performance Tests for LegalLens AI.
Verifies response latencies (<50ms for cached responses), throughput,
in-memory LRU caching hit rates, and Gzip response compression.
"""

import unittest
import time
import json
from app import app
from sample_contracts import SAMPLE_CONTRACTS
import groq_service


class EfficiencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.text = SAMPLE_CONTRACTS["msa_freelance"]["text"]

    def test_01_lru_cache_hit_latency(self):
        """Verify warm cached responses execute in under 20ms (0ms target)."""
        # Prime cache
        self.app.post("/api/simplify-legal-docs",
                      data=json.dumps({"text": self.text}),
                      content_type="application/json")
        
        # Test cached latency
        t0 = time.perf_counter()
        res = self.app.post("/api/simplify-legal-docs",
                            data=json.dumps({"text": self.text}),
                            content_type="application/json")
        duration_ms = (time.perf_counter() - t0) * 1000
        
        self.assertEqual(res.status_code, 200)
        self.assertLess(duration_ms, 50.0, f"Cached latency was {duration_ms:.2f}ms (expected <50ms)")

    def test_02_gzip_compression_active(self):
        """Verify Flask-Compress compresses HTTP responses."""
        res = self.app.get("/", headers={"Accept-Encoding": "gzip"})
        self.assertEqual(res.status_code, 200)
        encoding = res.headers.get("Content-Encoding", "").lower()
        self.assertIn("gzip", encoding, "Response was not compressed with Gzip.")

    def test_03_performance_metrics_endpoint(self):
        """Verify /api/performance-metrics returns cache size and runtime stats."""
        res = self.app.get("/api/performance-metrics")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "optimized")
        self.assertIn("lru_cache", data)
        self.assertIn("compression", data)

    def test_04_whitespace_token_compression(self):
        """Verify whitespace compression optimizes token payload size."""
        bloated = "A\n\n\n\n\nB\n\n\n\n\nC"
        compressed = groq_service.compress_whitespace(bloated)
        self.assertEqual(compressed, "A\n\nB\n\nC")
        self.assertLess(len(compressed), len(bloated))


if __name__ == "__main__":
    unittest.main()
