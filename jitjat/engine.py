"""
JITJAT Memory-Mapped Cognitive Substrate Engine
Provides sub-2.5ms deterministic state retrieval, cycle-safe associative graph traversal,
integer micro-unit synaptic plasticity, and episodic memory logging with zero cloud dependencies.
"""
import os
import time
import json
import sqlite3
import threading
from typing import Dict, List, Any, Optional, Tuple

MICRO_UNIT_MIN = 0
MICRO_UNIT_MAX = 1000000
MICRO_UNIT_ONE = 1000000
LTP_DELTA = 50000
LTD_DELTA = -100000

class JitJatEngine:
    def __init__(self, db_path: str = "jitjat_cortex.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._all_conns: List[sqlite3.Connection] = []
        self._lock = threading.Lock()
        self._ensure_connection()

    def _ensure_connection(self) -> sqlite3.Connection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=5.0)
            conn.row_factory = sqlite3.Row
            # Concurrency & WAL hardening pragmas
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            conn.execute("PRAGMA mmap_size = 268435456;")  # 256MB mmap
            conn.execute("PRAGMA busy_timeout = 5000;")
            conn.execute("PRAGMA cache_size = -64000;")     # 64MB cache
            conn.execute("PRAGMA temp_store = MEMORY;")
            conn.execute("PRAGMA foreign_keys = ON;")
            self._local.conn = conn
            with self._lock:
                self._all_conns.append(conn)
        return conn

    @property
    def _conn(self) -> sqlite3.Connection:
        return self._ensure_connection()

    @_conn.setter
    def _conn(self, val: Optional[sqlite3.Connection]):
        self._local.conn = val

    def upsert_cortical_node(self, faculty_id: str, domain: str, symbol_name: str,
                             affordance_signature: str, blast_radius: dict = None,
                             negative_invariants: list = None, capsule_hash: str = "genesis",
                             status: str = "ACTIVE", updated_at: Optional[int] = None) -> None:
        conn = self._ensure_connection()
        now = int(time.time()) if updated_at is None else int(updated_at)
        conn.execute("""
            INSERT INTO jitjat_cortical_nodes (
                faculty_id, domain, symbol_name, affordance_signature,
                blast_radius_json, negative_invariants_json, jit_capsule_hash,
                decay_epoch, last_proven_at, updated_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
            ON CONFLICT(faculty_id) DO UPDATE SET
                domain = excluded.domain,
                symbol_name = excluded.symbol_name,
                affordance_signature = excluded.affordance_signature,
                blast_radius_json = excluded.blast_radius_json,
                negative_invariants_json = excluded.negative_invariants_json,
                jit_capsule_hash = excluded.jit_capsule_hash,
                last_proven_at = excluded.last_proven_at,
                updated_at = excluded.updated_at,
                status = excluded.status;
        """, (
            faculty_id, domain, symbol_name, affordance_signature,
            json.dumps(blast_radius or {}), json.dumps(negative_invariants or []),
            capsule_hash, now, now, status
        ))
        conn.commit()

    def batch_insert_nodes(self, node_tuples: List[Tuple]) -> None:
        """Batch inserts cortical nodes in a single transaction."""
        conn = self._ensure_connection()
        conn.executemany("""
            INSERT OR REPLACE INTO jitjat_cortical_nodes (
                faculty_id, domain, symbol_name, affordance_signature,
                blast_radius_json, negative_invariants_json, jit_capsule_hash,
                decay_epoch, last_proven_at, updated_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, node_tuples)
        conn.commit()

    def add_synaptic_edge(self, source_id: str, target_id: str, edge_type: str = "ASSOCIATIVE",
                           weight: int = 1000000, weight_micro: Optional[int] = None) -> None:
        conn = self._ensure_connection()
        w = max(0, min(1000000, int(weight_micro if weight_micro is not None else weight)))
        conn.execute("""
            INSERT INTO jitjat_synaptic_edges (source_id, target_id, edge_type, weight_micro, hebbian_weight)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(source_id, target_id, edge_type) DO UPDATE SET
                weight_micro = excluded.weight_micro,
                hebbian_weight = excluded.hebbian_weight;
        """, (source_id, target_id, edge_type, w, w))
        conn.commit()

    def batch_insert_edges(self, edge_tuples: List[Tuple]) -> None:
        """Batch inserts synaptic edges in a single transaction."""
        conn = self._ensure_connection()
        conn.executemany("""
            INSERT OR REPLACE INTO jitjat_synaptic_edges (
                source_id, target_id, edge_type, weight_micro, hebbian_weight
            ) VALUES (?, ?, ?, ?, ?);
        """, edge_tuples)
        conn.commit()

    def update_synaptic_weight(self, source_id: str, target_id: str, delta: int,
                               edge_type: str = "ASSOCIATIVE") -> int:
        """Applies Hebbian plasticity with deterministic SQL integer clamping [0, 1000000]."""
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE jitjat_synaptic_edges
            SET weight_micro = MAX(0, MIN(1000000, weight_micro + ?)),
                hebbian_weight = MAX(0, MIN(1000000, weight_micro + ?))
            WHERE source_id = ? AND target_id = ? AND edge_type = ?
            RETURNING weight_micro;
        """, (int(delta), int(delta), source_id, target_id, edge_type))
        row = cur.fetchone()
        if row is not None:
            conn.commit()
            return int(row[0])
        # If edge does not exist, insert initial clamped weight
        init_w = max(0, min(1000000, 1000000 + int(delta)))
        cur.execute("""
            INSERT INTO jitjat_synaptic_edges (source_id, target_id, edge_type, weight_micro, hebbian_weight)
            VALUES (?, ?, ?, ?, ?);
        """, (source_id, target_id, edge_type, init_w, init_w))
        conn.commit()
        return init_w

    def apply_plasticity(self, source_id: str, target_id: str, delta: int,
                         edge_type: str = "ASSOCIATIVE") -> int:
        return self.update_synaptic_weight(source_id, target_id, delta, edge_type)

    def apply_ltp(self, source_id: str, target_id: str, edge_type: str = "ASSOCIATIVE") -> int:
        """Long-Term Potentiation (+50,000 micro-units)."""
        return self.update_synaptic_weight(source_id, target_id, LTP_DELTA, edge_type)

    def apply_ltd(self, source_id: str, target_id: str, edge_type: str = "ASSOCIATIVE") -> int:
        """Long-Term Depression (-100,000 micro-units)."""
        return self.update_synaptic_weight(source_id, target_id, LTD_DELTA, edge_type)

    def get_synaptic_weight(self, source_id: str, target_id: str, edge_type: str = "ASSOCIATIVE") -> Optional[int]:
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("SELECT weight_micro FROM jitjat_synaptic_edges WHERE source_id = ? AND target_id = ? AND edge_type = ?;",
                    (source_id, target_id, edge_type))
        row = cur.fetchone()
        return int(row[0]) if row else None

    def query_node(self, domain: str, symbol: str) -> Optional[Dict[str, Any]]:
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jitjat_cortical_nodes WHERE domain = ? AND symbol_name = ?;",
                    (domain, symbol))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_node_by_id(self, faculty_id: str) -> Optional[Dict[str, Any]]:
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jitjat_cortical_nodes WHERE faculty_id = ?;", (faculty_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def traverse_graph(self, domain: Optional[str] = None, symbol: Optional[str] = None,
                       max_depth: int = 2, max_hops: Optional[int] = None,
                       faculty_id: Optional[str] = None,
                       min_weight_micro: int = 200000) -> List[Dict[str, Any]]:
        """
        Cycle-Safe Recursive CTE Traversal.
        Tracks visited node paths: (',' || path || ',') NOT LIKE ('%,' || e.target_id || ',%')
        Enforces depth <= max_hops ceiling so cyclic topologies never loop infinitely.
        Prunes depressed edges where weight_micro < min_weight_micro.
        """
        conn = self._ensure_connection()
        cur = conn.cursor()
        hops = max_hops if max_hops is not None else max_depth

        if faculty_id:
            root_where = "faculty_id = ? AND status = 'ACTIVE'"
            root_params = [faculty_id]
        elif domain and symbol:
            root_where = "domain = ? AND symbol_name = ? AND status = 'ACTIVE'"
            root_params = [domain, symbol]
        elif domain:
            root_where = "domain = ? AND status = 'ACTIVE'"
            root_params = [domain]
        else:
            root_where = "status = 'ACTIVE'"
            root_params = []

        query = f"""
        WITH RECURSIVE Tree AS (
            SELECT 
                faculty_id, 
                domain, 
                symbol_name, 
                1 as depth,
                faculty_id as path
            FROM jitjat_cortical_nodes
            WHERE {root_where}
            UNION ALL
            SELECT 
                n.faculty_id, 
                n.domain, 
                n.symbol_name, 
                t.depth + 1 as depth,
                t.path || ',' || n.faculty_id as path
            FROM jitjat_synaptic_edges e
            JOIN Tree t ON e.source_id = t.faculty_id
            JOIN jitjat_cortical_nodes n ON e.target_id = n.faculty_id
            WHERE t.depth <= ?
              AND (',' || t.path || ',') NOT LIKE ('%,' || e.target_id || ',%')
              AND COALESCE(e.weight_micro, e.hebbian_weight, 1000000) >= ?
              AND n.status = 'ACTIVE'
        )
        SELECT faculty_id, domain, symbol_name, depth, path FROM Tree;
        """
        params = root_params + [hops, min_weight_micro]
        cur.execute(query, tuple(params))
        return [dict(r) for r in cur.fetchall()]

    def traverse_by_id(self, faculty_id: str, max_hops: int = 3) -> List[Dict[str, Any]]:
        return self.traverse_graph(faculty_id=faculty_id, max_hops=max_hops)

    def record_dialogue(self, role: str, message: str) -> int:
        conn = self._ensure_connection()
        now = int(time.time())
        cur = conn.cursor()
        cur.execute("INSERT INTO willow_dialogue_history (role, message, timestamp) VALUES (?, ?, ?);",
                    (role, message, now))
        conn.commit()
        return cur.lastrowid

    def get_recent_dialogue(self, limit: int = 6) -> List[Tuple[str, str]]:
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("SELECT role, message FROM willow_dialogue_history ORDER BY id DESC LIMIT ?;", (limit,))
        return list(reversed(cur.fetchall()))

    def get_stats(self) -> Dict[str, int]:
        conn = self._ensure_connection()
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM jitjat_cortical_nodes WHERE status = 'ACTIVE';")
        nodes = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM jitjat_synaptic_edges;")
        edges = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM willow_dialogue_history;")
        turns = cur.fetchone()[0]
        return {"nodes": nodes, "edges": edges, "dialogue_turns": turns}

    def close(self):
        with self._lock:
            for c in self._all_conns:
                try:
                    c.close()
                except Exception:
                    pass
            self._all_conns.clear()
        self._local.conn = None
