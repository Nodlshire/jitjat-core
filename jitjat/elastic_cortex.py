"""
JITJAT Core v2.0: Elastic Neuro-Symbolic Agent Memory, Wisdom Compaction & Compound Archetypes
License: Apache 2.0 (Open-Source Engine — Zero Proprietary ERP IP)
"""

import os
import json
import time
import sqlite3
import hashlib
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class FacultyManifest:
    faculty_id: str
    domain: str
    symbol_name: str
    category: str = "EXECUTION_KERNEL"  # UTILITY, EXECUTION_KERNEL, INVARIANT_GUARD
    initial_jat_ratio: int = 25
    affordance: str = ""
    wisdom_heuristics: List[str] = field(default_factory=list)
    negative_invariants: List[str] = field(default_factory=list)
    procedural_jit_payload: str = ""


class ElasticJitJatCortex:
    """
    In-Memory / WAL SQLite Hypergraph with Two-Way Elastic JAT/JIT Compaction,
    Wisdom Distillation, and Automatic Compound Archetype Discovery.
    """

    FLOORS = {"UTILITY": 5, "EXECUTION_KERNEL": 10, "INVARIANT_GUARD": 18}
    CEILINGS = {"UTILITY": 25, "EXECUTION_KERNEL": 35, "INVARIANT_GUARD": 40}

    def __init__(self, db_path: str = ":memory:", shm_dir: Optional[str] = None):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode = WAL;")
        base_shm = Path("/dev/shm") if Path("/dev/shm").exists() else Path(tempfile.gettempdir())
        self.shm_dir = Path(shm_dir) if shm_dir else (base_shm / "jitjat_oss_capsules")
        self.shm_dir.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS cortical_faculties (
                faculty_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                symbol_name TEXT NOT NULL,
                category TEXT NOT NULL,
                jat_ratio_percent INTEGER NOT NULL,
                maturity_stage TEXT NOT NULL,
                execution_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                hebbian_weight INTEGER DEFAULT 50000,
                wisdom_json TEXT NOT NULL,
                negative_invariants_json TEXT NOT NULL,
                jit_capsule_path TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_oss_domain_sym ON cortical_faculties(domain, symbol_name);

            CREATE TABLE IF NOT EXISTS compound_archetypes (
                archetype_id TEXT PRIMARY KEY,
                task_signature TEXT NOT NULL UNIQUE,
                faculty_ids_json TEXT NOT NULL,
                adaptation_rules_json TEXT NOT NULL,
                execution_count INTEGER DEFAULT 1
            );
        """)
        self.conn.commit()

    def register_faculty(self, manifest: FacultyManifest) -> Dict[str, Any]:
        capsule_path = self.shm_dir / f"{manifest.faculty_id}.jit.json"
        capsule_data = {
            "faculty_id": manifest.faculty_id,
            "procedural_payload": manifest.procedural_jit_payload,
            "affordance": manifest.affordance
        }
        capsule_path.write_text(json.dumps(capsule_data), encoding="utf-8")

        self.conn.execute("""
            INSERT OR REPLACE INTO cortical_faculties (
                faculty_id, domain, symbol_name, category, jat_ratio_percent, maturity_stage,
                wisdom_json, negative_invariants_json, jit_capsule_path
            ) VALUES (?, ?, ?, ?, ?, 'NOVICE_CONSCIOUS', ?, ?, ?)
        """, (
            manifest.faculty_id, manifest.domain, manifest.symbol_name, manifest.category,
            manifest.initial_jat_ratio, json.dumps(manifest.wisdom_heuristics),
            json.dumps(manifest.negative_invariants), str(capsule_path)
        ))
        self.conn.commit()
        return {"faculty_id": manifest.faculty_id, "jat_ratio": manifest.initial_jat_ratio}

    def evolve_faculty(
        self, faculty_id: str, succeeded: bool = True, learned_wisdom: Optional[str] = None, new_invariant: Optional[str] = None
    ) -> Dict[str, Any]:
        cur = self.conn.cursor()
        row = cur.execute("SELECT * FROM cortical_faculties WHERE faculty_id = ?", (faculty_id,)).fetchone()
        if not row:
            raise KeyError(f"Faculty {faculty_id} not registered")

        cat = row["category"]
        old_ratio = row["jat_ratio_percent"]
        exec_cnt = row["execution_count"] + (1 if succeeded else 0)
        fail_cnt = row["failure_count"] + (0 if succeeded else 1)

        floor = self.FLOORS.get(cat, 10)
        ceiling = self.CEILINGS.get(cat, 35)

        if not succeeded:
            new_ratio = min(ceiling, old_ratio + 5)
        else:
            reliability = exec_cnt / max(1, exec_cnt + fail_cnt * 3)
            drop = max(1, int((exec_cnt // 5) * reliability))
            new_ratio = max(floor, old_ratio - drop)

        stage = "MUSCLE_MEMORY_MASTER" if new_ratio <= 10 else ("VETERAN_REFLEX" if new_ratio <= 20 else "CONSOLIDATED")
        wisdom = json.loads(row["wisdom_json"])
        invariants = json.loads(row["negative_invariants_json"])

        if learned_wisdom and learned_wisdom not in wisdom:
            wisdom.append(learned_wisdom)
        if new_invariant and new_invariant not in invariants:
            invariants.append(new_invariant)

        weight_delta = 5000 if succeeded else -25000
        self.conn.execute("""
            UPDATE cortical_faculties
            SET jat_ratio_percent = ?, maturity_stage = ?, execution_count = ?, failure_count = ?,
                hebbian_weight = hebbian_weight + ?, wisdom_json = ?, negative_invariants_json = ?
            WHERE faculty_id = ?
        """, (new_ratio, stage, exec_cnt, fail_cnt, weight_delta, json.dumps(wisdom), json.dumps(invariants), faculty_id))
        self.conn.commit()
        return {"faculty_id": faculty_id, "old_ratio": old_ratio, "new_ratio": new_ratio, "stage": stage, "wisdom_count": len(wisdom)}

    def record_archetype(self, task_signature: str, faculty_ids: List[str], adaptation_rules: Optional[List[str]] = None) -> str:
        arch_id = "ARCH-" + hashlib.sha256(task_signature.encode()).hexdigest()[:8].upper()
        self.conn.execute("""
            INSERT INTO compound_archetypes (archetype_id, task_signature, faculty_ids_json, adaptation_rules_json, execution_count)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(task_signature) DO UPDATE SET execution_count = execution_count + 1
        """, (arch_id, task_signature, json.dumps(faculty_ids), json.dumps(adaptation_rules or [])))
        self.conn.commit()
        return arch_id

    def query_j_cortex(self, domain: str, symbol_name: str) -> Dict[str, Any]:
        t0 = time.perf_counter()
        rows = self.conn.execute("""
            SELECT faculty_id, jat_ratio_percent, maturity_stage, wisdom_json, negative_invariants_json, jit_capsule_path
            FROM cortical_faculties WHERE domain = ? AND symbol_name = ?
        """, (domain, symbol_name)).fetchall()
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {"results": [dict(r) for r in rows], "latency_ms": latency_ms}


if __name__ == "__main__":
    cortex = ElasticJitJatCortex()
    cortex.register_faculty(FacultyManifest(
        faculty_id="FAC-OSS-001",
        domain="Systems",
        symbol_name="ConcurrencyGuard",
        category="EXECUTION_KERNEL",
        initial_jat_ratio=25,
        wisdom_heuristics=["Prefer lock-free ring buffers on single-producer paths"],
        negative_invariants=["FORBIDDEN: Nested mutex acquisition without deterministic rank order"],
        procedural_jit_payload="def acquire_ordered(locks): return sorted(locks, key=lambda x: x.rank)"
    ))
    for i in range(15):
        state = cortex.evolve_faculty("FAC-OSS-001", succeeded=True, learned_wisdom=f"Validated lock rank cycle {i}")
    q = cortex.query_j_cortex("Systems", "ConcurrencyGuard")
    assert state["new_ratio"] == 10 and state["stage"] == "MUSCLE_MEMORY_MASTER"
    assert q["latency_ms"] < 2.5
    print(f"[PASS] jitjat-core v2.0 Elastic Compaction verified (25% -> {state['new_ratio']}% JAT in {q['latency_ms']:.3f}ms)")
