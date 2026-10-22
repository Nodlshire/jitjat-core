"""
JITJAT Substrate Schema Bootstrap & Invariant Initializer
Enforces WAL mode, synchronous=NORMAL, microsecond B-Tree covering indexes,
and deterministic micro-unit integer plasticity invariants.
"""
import os
import sqlite3
from pathlib import Path

def init_substrate_schema(db_path: str = "jitjat_cortex.db") -> None:
    """Initializes the high-performance memory-mapped WAL schema."""
    conn = sqlite3.connect(db_path, timeout=5.0)
    cur = conn.cursor()
    
    # 1. Concurrency, Memory-Mapping & WAL Hardening Pragmas
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = NORMAL;")
    cur.execute("PRAGMA mmap_size = 268435456;")  # 256MB mmap
    cur.execute("PRAGMA busy_timeout = 5000;")
    cur.execute("PRAGMA cache_size = -64000;")     # 64MB cache
    cur.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("PRAGMA foreign_keys = ON;")

    # 2. Cortical Hypergraph Nodes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jitjat_cortical_nodes (
        faculty_id TEXT PRIMARY KEY,
        domain TEXT NOT NULL,
        symbol_name TEXT NOT NULL,
        affordance_signature TEXT NOT NULL,
        blast_radius_json TEXT NOT NULL DEFAULT '{}',
        negative_invariants_json TEXT NOT NULL DEFAULT '[]',
        jit_capsule_hash TEXT NOT NULL,
        decay_epoch INTEGER NOT NULL DEFAULT 0,
        last_proven_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL DEFAULT 0,
        status TEXT CHECK(status IN ('ACTIVE', 'PROBATIONARY', 'QUARANTINED')) DEFAULT 'ACTIVE'
    );
    """)

    # 3. Hebbian Synaptic Edges (Deterministic Micro-Unit Integer Plasticity)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jitjat_synaptic_edges (
        source_id TEXT,
        target_id TEXT,
        edge_type TEXT NOT NULL,
        weight_micro INTEGER DEFAULT 1000000 CHECK(weight_micro >= 0 AND weight_micro <= 1000000),
        hebbian_weight INTEGER DEFAULT 1000000,
        PRIMARY KEY (source_id, target_id, edge_type),
        FOREIGN KEY (source_id) REFERENCES jitjat_cortical_nodes(faculty_id),
        FOREIGN KEY (target_id) REFERENCES jitjat_cortical_nodes(faculty_id)
    );
    """)

    # 4. Persona / Trait Cortex
    cur.execute("""
    CREATE TABLE IF NOT EXISTS willow_persona_cortex (
        trait_key TEXT PRIMARY KEY,
        value_json TEXT NOT NULL,
        last_updated INTEGER NOT NULL
    );
    """)

    # 5. Episodic Dialogue History
    cur.execute("""
    CREATE TABLE IF NOT EXISTS willow_dialogue_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp INTEGER NOT NULL
    );
    """)

    # 6. Composite Covering B-Tree Indexes for Pure Index-Only Scans
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cortex_domain_sym ON jitjat_cortical_nodes(domain, symbol_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cortex_domain_updated ON jitjat_cortical_nodes(domain, updated_at DESC);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_synapse_covering ON jitjat_synaptic_edges(source_id, weight_micro DESC, target_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_synapse_source ON jitjat_synaptic_edges(source_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_synapse_target ON jitjat_synaptic_edges(target_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_dialogue_time ON willow_dialogue_history(timestamp DESC);")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_substrate_schema()
    print("[✓] JITJAT Substrate schema successfully initialized.")
