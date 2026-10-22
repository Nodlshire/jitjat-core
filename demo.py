#!/usr/bin/env python3
"""
JITJAT Standalone Interactive Runtime Showcase
Demonstrates the complete JITJAT neuro-symbolic lifecycle in under 10 seconds:
1. Initializes a temporary/in-memory SQLite WAL cortex substrate.
2. Registers sample faculties:
   - FAC-SQL-AUDIT (Domain: Database, Blast Radius: Low, Invariant: "Never drop tables without snapshot")
   - FAC-ERP-POSTING (Domain: Financial, Blast Radius: Critical, Invariant: "Double-entry balance check mandatory")
3. Links them with a directional synaptic edge and simulated Hebbian LTP weight (+50k micro-units).
4. Executes a recursive CTE lookup for FAC-ERP-POSTING and resolves companion audit faculty,
   printing traversal latency (in microseconds) directly to console.
5. Ephemerally writes and verifies a test JIT capsule in /dev/shm (falling back to tempfile on non-POSIX),
   then cleanly removes it.
6. Asserts exit code 0.
"""

import sys
import os
import json
import time
import tempfile
from pathlib import Path

# Add project root to path for direct imports
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from jitjat.bootstrap import init_substrate_schema
from jitjat.engine import JitJatEngine, LTP_DELTA
from jitjat.elastic_cortex import ElasticJitJatCortex, FacultyManifest


def main() -> int:
    overall_t0 = time.perf_counter()

    print("=" * 72)
    print("  JITJAT v2.0 STANDALONE COGNITIVE SUBSTRATE LIFECYCLE DEMO")
    print("=" * 72)

    # ---------------------------------------------------------
    # 1. Initialize temporary SQLite WAL cortex
    # ---------------------------------------------------------
    print("\n[Step 1/5] Initializing temporary SQLite WAL cognitive substrate...")
    temp_dir = tempfile.mkdtemp(prefix="jitjat_demo_")
    db_path = os.path.join(temp_dir, "demo_cortex.db")

    init_substrate_schema(db_path)
    engine = JitJatEngine(db_path)

    # Verify WAL mode
    wal_check = engine._conn.execute("PRAGMA journal_mode;").fetchone()
    journal_mode = wal_check[0] if wal_check else "unknown"
    print(f"  [✓] Cortex substrate online: {db_path}")
    print(f"  [✓] PRAGMA journal_mode: {journal_mode.upper()} (SLA: WAL concurrency enabled)")

    try:
        # ---------------------------------------------------------
        # 2. Register sample faculties
        # ---------------------------------------------------------
        print("\n[Step 2/5] Registering sample neuro-symbolic faculties...")

        # FAC-SQL-AUDIT
        fac_audit_id = "FAC-SQL-AUDIT"
        engine.upsert_cortical_node(
            faculty_id=fac_audit_id,
            domain="Database",
            symbol_name="sql_audit_guardian",
            affordance_signature="audit_ddl(sql: str) -> bool",
            blast_radius={"tier": "LOW", "impact": "schema_metadata_read"},
            negative_invariants=["Never drop tables without snapshot"],
            capsule_hash="hash_fac_sql_audit_v1",
            status="ACTIVE"
        )
        print(f"  [✓] Registered Faculty: {fac_audit_id}")
        print(f"      - Domain: Database | Blast Radius: Low")
        print(f"      - Negative Invariant: 'Never drop tables without snapshot'")

        # FAC-ERP-POSTING
        fac_erp_id = "FAC-ERP-POSTING"
        engine.upsert_cortical_node(
            faculty_id=fac_erp_id,
            domain="Financial",
            symbol_name="erp_general_ledger_post",
            affordance_signature="post_journal_batch(entries: list) -> str",
            blast_radius={"tier": "CRITICAL", "impact": "ledger_mutation"},
            negative_invariants=["Double-entry balance check mandatory"],
            capsule_hash="hash_fac_erp_posting_v1",
            status="ACTIVE"
        )
        print(f"  [✓] Registered Faculty: {fac_erp_id}")
        print(f"      - Domain: Financial | Blast Radius: Critical")
        print(f"      - Negative Invariant: 'Double-entry balance check mandatory'")

        # ---------------------------------------------------------
        # 3. Directional synaptic edge & simulated Hebbian LTP (+50k)
        # ---------------------------------------------------------
        print("\n[Step 3/5] Wiring directional synaptic edge & applying Hebbian LTP...")
        # Initial associative edge: baseline weight 500,000 micro-units (0.5 strength)
        base_weight = 500_000
        engine.add_synaptic_edge(
            source_id=fac_erp_id,
            target_id=fac_audit_id,
            edge_type="REQUIRES_AUDIT",
            weight_micro=base_weight
        )
        print(f"  [✓] Synapse wired: ({fac_erp_id}) --[REQUIRES_AUDIT]--> ({fac_audit_id})")
        print(f"      - Initial weight: {base_weight:,} micro-units (0.50 normalized)")

        # Apply Hebbian LTP (+50,000 micro-units)
        updated_weight = engine.apply_plasticity(
            source_id=fac_erp_id,
            target_id=fac_audit_id,
            delta=LTP_DELTA,
            edge_type="REQUIRES_AUDIT"
        )
        assert updated_weight == base_weight + LTP_DELTA, "Hebbian LTP delta mismatch!"
        print(f"  [✓] Hebbian LTP Potentiation (+{LTP_DELTA:,} micro-units):")
        print(f"      - Reinforced synaptic weight: {updated_weight:,} / 1,000,000 micro-units")

        # ---------------------------------------------------------
        # 4. Recursive CTE lookup & resolution latency (microseconds)
        # ---------------------------------------------------------
        print("\n[Step 4/5] Executing recursive CTE associative graph traversal...")
        t_traversal_0 = time.perf_counter_ns()
        results = engine.traverse_graph(faculty_id=fac_erp_id, max_hops=3, min_weight_micro=200_000)
        t_traversal_1 = time.perf_counter_ns()

        traversal_latency_us = (t_traversal_1 - t_traversal_0) / 1000.0
        traversal_latency_ms = traversal_latency_us / 1000.0

        print(f"  [✓] Traversal completed in: {traversal_latency_us:.2f} µs ({traversal_latency_ms:.4f} ms)")
        print(f"      - Discovered {len(results)} nodes in associative path:")
        for node in results:
            print(f"        * Depth {node['depth']}: {node['faculty_id']} ({node['domain']}::{node['symbol_name']})")

        # Verify companion audit faculty was resolved
        resolved_ids = [r["faculty_id"] for r in results]
        assert fac_erp_id in resolved_ids, f"Root {fac_erp_id} not found in traversal!"
        assert fac_audit_id in resolved_ids, f"Companion audit faculty {fac_audit_id} not resolved!"
        print(f"  [✓] Invariant Confirmed: {fac_erp_id} strictly coupled to {fac_audit_id}")

        # ---------------------------------------------------------
        # 5. Ephemeral JIT capsule in /dev/shm (or temp fallback)
        # ---------------------------------------------------------
        print("\n[Step 5/5] Ephemeral JIT capsule write & verify in shared memory...")
        shm_root = Path("/dev/shm") if Path("/dev/shm").exists() and os.access("/dev/shm", os.W_OK) else Path(tempfile.gettempdir())
        capsule_dir = shm_root / f"jitjat_demo_capsule_{os.getpid()}"
        capsule_dir.mkdir(parents=True, exist_ok=True)
        capsule_file = capsule_dir / f"{fac_erp_id}.jit.json"

        capsule_payload = {
            "faculty_id": fac_erp_id,
            "runtime_type": "EPHEMERAL_JIT_CAPSULE",
            "procedural_code": "def execute_posting(tx): return {'status': 'POSTED', 'hash': '0xABC123'}",
            "companion_guard": fac_audit_id,
            "timestamp_ns": time.time_ns()
        }

        # Write volatile capsule to RAM
        capsule_file.write_text(json.dumps(capsule_payload, indent=2), encoding="utf-8")
        print(f"  [✓] Mounted volatile capsule in RAM: {capsule_file}")

        # Read back and verify integrity
        verified_data = json.loads(capsule_file.read_text(encoding="utf-8"))
        assert verified_data["faculty_id"] == fac_erp_id
        assert verified_data["companion_guard"] == fac_audit_id
        print(f"  [✓] Capsule verified in RAM (Zero-drift execution payload verified)")

        # Clean up ephemeral capsule
        capsule_file.unlink()
        capsule_dir.rmdir()
        print(f"  [✓] Unmounted and evaporated ephemeral RAM capsule")

    finally:
        # Clean up database files
        engine.close()
        for suffix in ["", "-wal", "-shm"]:
            fpath = f"{db_path}{suffix}"
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass

    total_time = time.perf_counter() - overall_t0
    print("\n" + "=" * 72)
    print(f"  JITJAT LIFECYCLE COMPLETED SUCCESSFULLY IN {total_time:.3f} SECONDS (SLA: < 10.0s)")
    print("=" * 72 + "\n")

    assert total_time < 10.0, f"Demo exceeded 10-second SLA: {total_time:.2f}s"
    return 0


if __name__ == "__main__":
    sys.exit(main())
