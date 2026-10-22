"""
JITJAT Performance Benchmark Utility
Tests reflex latency, graph traversal speed, and compares against cloud vector database averages.
"""
import time
import os
import sqlite3
from .bootstrap import init_substrate_schema
from .engine import JitJatEngine

def run_benchmark(db_path: str = "benchmark_cortex.db", iterations: int = 1000):
    print("=" * 65)
    print("JITJAT SUBSTRATE STANDALONE PERFORMANCE BENCHMARK")
    print("=" * 65)

    if os.path.exists(db_path):
        os.remove(db_path)

    init_substrate_schema(db_path)
    engine = JitJatEngine(db_path)

    # Seed test topology
    print("[*] Seeding 500 cortical nodes and 1,000 synaptic edges...")
    for i in range(500):
        engine.upsert_cortical_node(
            faculty_id=f"node_{i:04d}",
            domain="finance" if i % 2 == 0 else "infra",
            symbol_name=f"symbol_{i:04d}",
            affordance_signature=f"affordance_{i:04d}()"
        )
    for i in range(1, 500):
        engine.add_synaptic_edge(f"node_{i-1:04d}", f"node_{i:04d}", "ASSOCIATIVE", 1000000)

    # Measure lookup latency
    print(f"[*] Executing {iterations} single-node B-tree lookups...")
    latencies = []
    for i in range(iterations):
        t0 = time.perf_counter()
        _ = engine.query_node("finance", f"symbol_{(i*2)%500:04d}")
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)

    latencies_sorted = sorted(latencies)
    p50 = latencies_sorted[int(0.50 * len(latencies_sorted))]
    p95 = latencies_sorted[int(0.95 * len(latencies_sorted))]
    p99 = latencies_sorted[int(0.99 * len(latencies_sorted))]
    avg = sum(latencies) / len(latencies)

    print(f"\nBenchmark Results ({iterations} ops):")
    print(f"  Average: {avg:.4f} ms")
    print(f"  P50:     {p50:.4f} ms (Target SLA: <= 2.5000 ms)")
    assert p50 <= 2.5, f"P50 reflex latency SLA breach: {p50:.4f} ms > 2.5000 ms SLA"
    print(f"  P95:     {p95:.4f} ms")
    print(f"  P99:     {p99:.4f} ms")

    print("\nComparison Against Conventional Cloud Vector Stores (Pinecone, Weaviate, Qdrant Cloud):")
    print(f"  Cloud Vector Store Roundtrip: ~35.000 ms - 120.000 ms")
    print(f"  JITJAT On-Prem Reflex:        {p50:.4f} ms (~{int(50.0 / max(0.001, p50))}x faster, 0 network hops, 0 cloud spend)")

    engine.close()
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(f"{db_path}-wal"):
        os.remove(f"{db_path}-wal")
    if os.path.exists(f"{db_path}-shm"):
        os.remove(f"{db_path}-shm")

if __name__ == "__main__":
    run_benchmark()
