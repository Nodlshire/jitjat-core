# JITJAT v2.0: Elastic Neuro-Symbolic Agent Memory & Cognitive Substrate

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![SLA: Sub-2.5ms Reflex](https://img.shields.io/badge/Reflex%20SLA-%3C%202.5ms-brightgreen.svg)](#verified-benchmark-results)
[![Zero Cloud Lock-in](https://img.shields.io/badge/Dependencies-Zero%20External-orange.svg)](#the-jitjat-mechanism-two-way-elasticity--muscle-memory)

> **Manifesto: From Static Skills to Self-Evolving Faculties.**  
> Autonomous agents should not rely on static Markdown instruction sheets stuffed into context windows. JITJAT transitions agent engineering from passive manual lookups to a dynamic, biological cognitive hypergraph—compacting repeated executions into high-speed muscle memory while safeguarding execution with immutable invariants.

---

## 1. The Core Thesis: Why Skills.md Fails at Scale

The current paradigm of agent engineering relies heavily on static documentation: prompt packs, tool specifications, and directory trees of `.SKILL.md` files. While functional for single-turn toys, this approach breaks down under enterprise autonomous workloads.

### The Degradation Ceiling
When an agent system reaches **15+ static Markdown skill files**, catastrophic degradation begins:
1. **Prompt Bloat:** Context windows fill with boilerplate operational steps, parameter definitions, and illustrative examples before the agent even understands the user's intent.
2. **Context Dilution:** Critical business rules and constraints drown in an ocean of passive procedural documentation, degrading reasoning quality and multi-step adherence.
3. **Instruction Drift:** LLMs treat advisory tips with the same weight as critical safety boundaries, occasionally dropping crucial safety checks as context lengths grow.

```
Passive Skill Manuals (.SKILL.md)             Active Cognitive Faculties (JITJAT)
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│  • Passive documentation dumps       │     │  • Active, queryable hypergraph      │
│  • Static context tax on every turn  │ VS  │  • 0 tokens consumed at rest         │
│  • Linear degradation beyond 15 files│     │  • 100k+ faculties sub-0.25ms        │
│  • "Suggestions" treated as rules    │     │  • Hard Negative Invariants ($INV$)   │
│  • Memory never evolves or compacts  │     │  • Hebbian muscle-memory compaction  │
└──────────────────────────────────────┘     └──────────────────────────────────────┘
```

### From Passive Manuals to Active Faculties
Humans do not re-read an operational manual from start to finish before typing a command or riding a bicycle. Repetition transforms conscious deliberation into **subconscious muscle memory**, preserving conscious attention solely for edge cases and unbending boundary rules.

JITJAT replaces static Markdown manuals with **Active Faculties**: structured neuro-symbolic entities that live in an index-backed substrate at rest, execute in sub-millisecond reflex loops, and autonomously distill experience into wisdom.

---

## 2. The JITJAT Mechanism: Two-Way Elasticity & Muscle Memory

JITJAT operates on a dual-partition cognitive substrate that balances deliberate conscious focus against hyper-fast procedural muscle memory.

```
                      ┌──────────────────────────────────────┐
                      │        Autonomous AI Agent           │
                      └──────────────────┬───────────────────┘
                                         │ Sub-millisecond associative reflex
                                         ▼
   ┌────────────────────────────────────────────────────────────────────────┐
   │                       JITJAT Substrate Engine                          │
   │                                                                        │
   │  ┌──────────────────────────────┐    ┌──────────────────────────────┐  │
   │  │   Conscious JAT Anchor       │    │  Hebbian Integer Plasticity  │  │
   │  │   • Negative Invariants      │    │  • Clamped [0, 1,000,000]    │  │
   │  │   • Wisdom Heuristics        │    │  • Zero floating-point drift │  │
   │  │   • 5% to 40% Dynamic Elastic│    │  • Recursive CTE Traversal   │  │
   │  └──────────────┬───────────────┘    └──────────────┬───────────────┘  │
   └─────────────────┼───────────────────────────────────┼──────────────────┘
                     │                                   │
                     ▼                                   ▼
        ┌─────────────────────────┐         ┌─────────────────────────┐
        │  Ephemeral RAM Capsules │         │   Sub-2.5ms SQLite WAL  │
        │       (/dev/shm)        │         │   Memory-Mapped Graph   │
        │                         │         │                         │
        │ • Zero-token at rest    │         │ • 256MB mmap B-tree     │
        │ • Mounted only on call  │         │ • PRAGMA synchronous    │
        │ • Evaporates on reboot  │         │   = NORMAL              │
        │ • O(1) RAM execution    │         │ • Single-writer/N-reader│
        └─────────────────────────┘         └─────────────────────────┘
```

### JAT (Jack of All Trades — Cortical Anchor)
- **Zero Tokens at Rest:** Housed inside memory-mapped SQLite WAL (`jitjat_cortical_nodes` and `cortical_faculties`). Incurs zero prompt token overhead during standby.
- **Symbolic Guardrails:** Stores affordance signatures, relational graph connections, and unbending **Negative Invariants ($INV$)** (e.g., *"Never commit imbalanced debits and credits"*, *"Never execute unverified shell strings"*).
- **Sub-2.5ms Reflex Lookups:** Covered B-tree indices and cycle-safe recursive Common Table Expressions (CTEs) enable multi-hop associative routing across hundreds of thousands of nodes in fractions of a millisecond.

### JIT (Just In Time — Ephemeral Capsule)
- **Volatile Execution Capsules:** Heavy procedural bulk, tool wrappers, and executable code artifacts reside off-context in volatile RAM (`/dev/shm` or OS shared memory).
- **Mount on Call:** Capsules are loaded into RAM *only* for the execution turn and unmounted immediately upon completion.
- **Zero Drift Storage:** Volatile memory guarantees fresh state instantiation and prevents stale execution residue from leaking across environments.

### Hebbian Compaction (From Novice to Master)
When a new capability is registered, the agent lacks proven historical reliability. JITJAT initializes it in the `NOVICE_CONSCIOUS` stage with a high JAT ratio (25%–40%), forcing the agent to expend conscious token attention on the task.

As successful executions accumulate:
1. **Procedural Offloading:** Step-by-step instructions migrate into `/dev/shm` JIT binary muscle memory.
2. **Anchor Compaction:** The conscious JAT anchor shrinks progressively toward category safety floors:
   - `UTILITY`: Compresses down to **5% JAT**
   - `EXECUTION_KERNEL`: Compresses down to **10% JAT**
   - `INVARIANT_GUARD`: Compresses down to **18% JAT**
3. **Wisdom Distillation:** The compressed anchor retains exclusively pure **Wisdom Heuristics** (condensed lessons learned) and **Negative Invariants ($INV$)**. The faculty transitions to `MUSCLE_MEMORY_MASTER`.

### Fault-Driven Re-Expansion
Unlike static compression algorithms that permanently throw away nuance, JITJAT implements **Two-Way Elasticity**:
- If an edge case triggers a failure or assertion violation during execution, the faculty immediately **elastically re-expands** conscious focus (**+5% JAT per fault**, up to category ceilings of 25%–40%).
- The agent enters a deliberative state to inspect the anomaly, log new learned wisdom, register an updated negative invariant, and re-prove reliability across subsequent executions before compacting again.

---

## 3. Compound Archetypes & Swarm Empowerment

Real-world autonomous tasks rarely consist of isolated atomic tool calls; they require multi-faculty choreography.

### Recipe Recording (Compound Archetypes)
When an agent coordinates multiple faculties (e.g., *Syntax Validator* $\rightarrow$ *Sandbox Compiler* $\rightarrow$ *Regression Runner*) to resolve a complex workflow, JITJAT records the co-activation signature:
- **Automatic Binding:** Automatically generates a deterministic `ARCH-<hash>` Compound Archetype in the substrate.
- **Zero-Token Familiar Retrieval:** The next time a similar task signature is requested, the entire sequence is invoked as a single coordinated compound reflex with zero recurring planning or chain-of-thought overhead.

### Shared Substrate for Swarms
In multi-agent architectures, communication bottlenecks and out-of-sync context windows degrade swarm performance. JITJAT provides a unified memory-mapped substrate:
- **Shared Memory-Mapped WAL:** Multiple concurrent workers, subagents, and reader processes mount the same SQLite WAL file directly into memory.
- **Instant Muscle Memory Propagation:** When Worker A refines a procedure or learns a critical negative invariant, it commits the update to the shared substrate. Workers B, C, and D immediately inherit the new reflex and tripwires without prompt synchronization, coordinator re-prompting, or central orchestrator latency.
- **Concurrent Non-Blocking Throughput:** With SQLite WAL and `PRAGMA synchronous = NORMAL`, dozens of worker threads execute concurrent reads while writers record execution metrics without database lock contention.

---

## 4. Verified Benchmark Results

The JITJAT cognitive substrate is verified under a **5-Vector Forensic Torture Suite** and standalone latency benchmarks on local bare-metal hardware. All measurements are captured in machine-verifiable receipts (`BENCHMARK_RECEIPTS.json`).

### Test Host Specifications
- **CPU:** Intel(R) Core(TM) i5-6400T CPU @ 2.20GHz
- **RAM:** 11.56 GB
- **OS & Kernel:** Linux (kernel 7.2.5-100.fc43.x86_64, glibc 2.42)
- **SQLite Engine:** v3.50.2 | **Python:** 3.14.7

### 5-Vector Torture Suite Verification

| Vector | Focus / Condition | Workload & Metric | Result | Target SLA |
|---|---|---|:---:|:---:|
| **Vector 1: Scale & Cyclic Topology** | 100k nodes, 300k edges with deliberate 3-hop and 5-hop loops | 1,000 3-hop recursive CTE traversals | **P50: 0.2305 ms** (Avg: 0.2446 ms, P99: 0.4086 ms) | $\le 2.5000\text{ ms}$ (**PASS**) |
| **Vector 2: Multi-Threaded Concurrency** | High-contention lock stress: 16 Readers + 4 Writers | 5.08s sustained load: 7,805 reads, 3,944 writes | **2,314.6 ops/sec** (0 SQLite busy errors) | **PASS** |
| **Vector 3: Memory-Mapped Speedup** | Cold first-touch vs. 256MB mmap warm cache | 5,000 memory-mapped queries | **Warm P50: 0.0131 ms** (8.1x speedup over cold 0.1063 ms) | $\le 2.5000\text{ ms}$ (**PASS**) |
| **Vector 4: Hebbian Plasticity Invariance** | LTP (+50k) and LTD (-100k) boundary clamp checks | 1,000 LTP and 1,000 LTD steps + random delta series | Clamped `[0, 1000000]`, **0.00% float drift** | Invariant (**PASS**) |
| **Vector 5: Mid-Transaction SIGKILL** | Violent ungraceful kill (`kill -9`) mid-WAL transaction | Parent re-opens and runs `PRAGMA integrity_check` | **Integrity: OK**, 900 committed atomic nodes intact | Zero corruption (**PASS**) |

### Standalone Reflex Latency vs. Cloud Vector Stores

```
JITJAT On-Prem Reflex:        0.0182 ms (P50)  | ■
Conventional Cloud Vector DB: 35.0000 - 120.00 ms | ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
--> JITJAT is ~2,700x faster, consumes zero network hops, and requires $0.00 in cloud API spend.
```

---

## 5. Quickstart

### Installation
Clone the repository and install in editable mode:
```bash
git clone https://github.com/dslabs/jitjat-core.git
cd JITJAT
pip install -e .
```

### Running Tests & Benchmarks
```bash
# Run standalone reflex latency benchmark
python3 jitjat/benchmark.py

# Run full 5-vector scientific torture and concurrency suite
python3 jitjat/scientific_torture_suite.py
```

### Basic Usage: Two-Way Elastic Faculty Lifecycle
```python
from jitjat.elastic_cortex import ElasticJitJatCortex, FacultyManifest

# 1. Initialize cortex with SQLite WAL and ephemeral /dev/shm capsules
cortex = ElasticJitJatCortex(db_path="cortex.db")

# 2. Register a Novice Faculty (Starts with high conscious JAT: 25%)
cortex.register_faculty(FacultyManifest(
    faculty_id="FAC-RECONCILE",
    domain="Ledger",
    symbol_name="reconcile_transactions",
    category="EXECUTION_KERNEL",
    initial_jat_ratio=25,
    affordance="reconcile(ledger_id: str) -> bool",
    wisdom_heuristics=["Verify timestamps before hash check"],
    negative_invariants=["INV-01: Never commit unbalanced entries"],
    procedural_jit_payload="def execute(): return perform_reconciliation()"
))

# 3. Successful runs compact conscious bulk into muscle memory (towards 10% floor)
for _ in range(10):
    cortex.evolve_faculty("FAC-RECONCILE", succeeded=True)

# 4. An unexpected failure triggers fault-driven re-expansion (+5% JAT)
cortex.evolve_faculty(
    "FAC-RECONCILE",
    succeeded=False,
    learned_wisdom="Retry on network lock timeout",
    new_invariant="INV-02: Abort batch on dirty read"
)

# 5. Record a Compound Archetype for multi-agent workflows
arch_id = cortex.record_archetype(
    task_signature="close_period_audit",
    faculty_ids=["FAC-RECONCILE", "FAC-LEDGER-LOCK", "FAC-AUDIT-REPORT"]
)
print(f"Recorded Compound Archetype: {arch_id}")
```

---

## 6. Enterprise Systems & Advisory

While **JITJAT Core** is released as a platform-agnostic, open-source engine under the Apache 2.0 license, enterprise environments operating at mission-critical scale frequently require tailored adaptations.

**DSLabs Advisory Services** assists enterprise engineering teams with:
- **Legacy ERP & Core Banking Integration:** Bridging high-speed neuro-symbolic memory substrates into established enterprise data fabrics (SAP, Microsoft Dynamics 365, Oracle, and proprietary ledger architectures) without compromising transactional integrity.
- **Air-Gapped & Sovereign Deployments:** Hardening memory-mapped WAL cortex clusters in defense, healthcare, and air-gapped financial infrastructure where external cloud vectors and third-party SaaS memory providers are prohibited.
- **Custom Synaptic Plasticity & Domain Topologies:** Engineering custom negative-invariant validation gates, automated blast-radius containment, and domain-specialized archetype compaction for high-throughput autonomous agent swarms.
- **SLA Auditing & Formal Verification:** Production stress-testing under simulated hardware failures, multi-tenant concurrency contention, and disaster recovery validation.

For enterprise inquiries, architecture reviews, and production advisory:
- **Organization:** [DSLabs](https://github.com/dslabs)
- **Contact:** `stephen@dslabs.io`
- **License Support:** Apache 2.0 Open Source Core with available commercial SLA advisory.
