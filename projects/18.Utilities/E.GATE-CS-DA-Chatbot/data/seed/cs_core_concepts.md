# GATE CS — Core Concepts Quick Reference

A dense, exam-oriented reference across the GATE CS & IT syllabus. Use it to
ground concept explanations and to recall key formulas and complexity bounds.

## Data Structures & Algorithms
- **Asymptotics:** O (upper), Ω (lower), Θ (tight). Master Theorem for
  `T(n)=aT(n/b)+f(n)`: compare `f(n)` with `n^{log_b a}`.
- **Sorting:** Merge/Heap sort `Θ(n log n)` worst case; Quicksort `Θ(n log n)`
  average, `Θ(n²)` worst; Counting/Radix `Θ(n)` for bounded keys. Only
  comparison sorts are `Ω(n log n)`.
- **Heaps:** build-heap `O(n)`; insert/extract `O(log n)`.
- **BST/AVL/Red-Black:** balanced trees give `O(log n)` search/insert/delete.
- **Hashing:** average `O(1)` lookup; collisions via chaining or open
  addressing; load factor α.
- **Graphs:** BFS/DFS `O(V+E)`. Dijkstra `O((V+E)log V)` with a heap (no
  negative edges). Bellman-Ford `O(VE)` handles negatives. Floyd-Warshall
  `O(V³)` all-pairs. MST: Kruskal `O(E log E)`, Prim `O(E log V)`.
- **Dynamic programming:** optimal substructure + overlapping subproblems
  (LCS, knapsack, matrix-chain, edit distance).
- **Greedy:** activity selection, Huffman coding, fractional knapsack.
- **NP-completeness:** SAT, 3-SAT, clique, vertex cover, Hamiltonian cycle,
  TSP (decision). Reductions are polynomial-time.

## Theory of Computation
- **Chomsky hierarchy:** Regular ⊂ CFL ⊂ CSL ⊂ Recursively Enumerable.
- Regular = DFA = NFA = regex; closed under union, intersection, complement.
- **Pumping lemma** proves a language is *not* regular / not context-free.
- CFL recognised by PDA; not closed under intersection/complement.
- **Decidability:** Halting problem is undecidable; `A_TM` undecidable.
  Rice's theorem: any non-trivial semantic property of TMs is undecidable.

## Compiler Design
- Phases: lexical → syntax → semantic → IR → optimisation → code gen.
- **Parsing:** LL(1) top-down (predictive); LR(0)/SLR/LALR/CLR bottom-up.
  FIRST/FOLLOW sets build LL(1) tables. Conflicts: shift-reduce, reduce-reduce.
- **SDT:** synthesised vs inherited attributes; S-attributed evaluated bottom-up.
- Live-variable analysis, register allocation via graph colouring.

## Operating Systems
- **Scheduling:** FCFS, SJF (optimal avg waiting, needs burst length), Round
  Robin (quantum), priority. Preemptive vs non-preemptive.
- **Synchronisation:** critical section, Peterson's solution, semaphores,
  mutex, monitors. Deadlock needs all 4: mutual exclusion, hold-and-wait, no
  preemption, circular wait. Banker's algorithm avoids deadlock.
- **Memory:** paging (no external frag), segmentation; TLB; page replacement
  (FIFO, LRU, Optimal; Belady's anomaly with FIFO). Effective access time with
  hit ratio.
- **Disk scheduling:** FCFS, SSTF, SCAN/LOOK, C-SCAN.

## DBMS
- **Normal forms:** 1NF→2NF (no partial dep)→3NF (no transitive dep)→BCNF
  (every determinant is a candidate key). Compute closure `X⁺` of attributes.
- **Transactions (ACID):** schedules — conflict-serializable (precedence graph
  acyclic), recoverable, cascadeless. 2PL ensures serializability;
  strict 2PL avoids cascading aborts.
- **Indexing:** B/B+ trees; dense vs sparse; hashing.
- **SQL & relational algebra:** σ (select), π (project), ⋈ (join), ÷ (division).

## Computer Networks
- **Models:** OSI (7 layers) vs TCP/IP. Encapsulation per layer.
- **Data link:** framing, CRC, sliding window (Go-Back-N, Selective Repeat),
  CSMA/CD (Ethernet), efficiency formulas.
- **Network:** IPv4 addressing, subnetting/CIDR, NAT; routing (distance vector
  vs link state — Dijkstra/OSPF).
- **Transport:** TCP (reliable, congestion control — slow start, AIMD) vs UDP;
  flow control via window.
- **Application:** DNS, HTTP, SMTP, DHCP.

## Digital Logic & Computer Organisation
- Boolean algebra, K-maps, SOP/POS, minimisation; combinational (MUX, decoder,
  adder) and sequential (flip-flops, registers, counters) circuits.
- Number systems & 2's-complement arithmetic; IEEE-754 floating point.
- **CO:** instruction cycle, addressing modes, pipelining (speedup = depth
  ideally; hazards: structural, data, control; forwarding, stalls). Cache
  (direct/associative/set-associative), AMAT = hit time + miss rate × penalty.

## General Aptitude (verbal + quantitative)
- Ratios, percentages, time-speed-distance, probability, permutations &
  combinations, data interpretation, reasoning, and English grammar/vocabulary.
