# Graph Report - Medic-Project  (2026-08-29)

## Corpus Check
- 26 files · ~5,153 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 154 nodes · 274 edges · 12 communities
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `adb34842`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- routes/sessions.py
- database.py
- devDependencies
- dependencies
- routes/clinical.py
- App.jsx
- FastAPI

## God Nodes (most connected - your core abstractions)
1. `process_new_session()` - 9 edges
2. `Base` - 8 edges
3. `User` - 8 edges
4. `owned_patient()` - 8 edges
5. `Patient` - 7 edges
6. `Session` - 7 edges
7. `login()` - 7 edges
8. `Appointment` - 6 edges
9. `ClinicalSession` - 6 edges
10. `create_session()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Appointment` --inherits--> `Base`  [EXTRACTED]
  app/models/clinical.py → app/models/__init__.py
- `ClinicalSession` --inherits--> `Base`  [EXTRACTED]
  app/models/clinical.py → app/models/__init__.py
- `Patient` --inherits--> `Base`  [EXTRACTED]
  app/models/clinical.py → app/models/__init__.py
- `Session` --inherits--> `Base`  [EXTRACTED]
  app/models/sessions.py → app/models/__init__.py
- `dashboard()` --uses--> `Patient`  [INFERRED]
  app/routes/clinical.py → app/models/clinical.py

## Import Cycles
- None detected.

## Communities (12 total, 0 thin omitted)

### Community 0 - "routes/sessions.py"
Cohesion: 0.12
Nodes (24): Session, create_session(), delete_session(), get_sessions(), AsyncSession, get, post, Returns a list of all clinical sessions ordered by date (newest first). (+16 more)

### Community 1 - "database.py"
Cohesion: 0.13
Nodes (21): get_db(), Base, User, login(), AsyncSession, post, get_current_user_profile(), AsyncSession (+13 more)

### Community 2 - "devDependencies"
Cohesion: 0.08
Nodes (23): autoprefixer, devDependencies, autoprefixer, postcss, tailwindcss, @types/react, @types/react-dom, vite (+15 more)

### Community 3 - "dependencies"
Cohesion: 0.13
Nodes (15): axios, clsx, framer-motion, dependencies, axios, clsx, framer-motion, lucide-react (+7 more)

### Community 4 - "routes/clinical.py"
Cohesion: 0.21
Nodes (23): Appointment, ClinicalSession, Patient, appointments(), copilot(), create_appointment(), create_patient(), create_session() (+15 more)

### Community 6 - "App.jsx"
Cohesion: 0.18
Nodes (10): age(), API, App(), Dashboard(), ini(), Patients(), Record(), SessionForm() (+2 more)

### Community 8 - "FastAPI"
Cohesion: 0.47
Nodes (5): init_db(), lifespan(), get, read_root(), FastAPI

## Knowledge Gaps
- **22 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dependencies` connect `dependencies` to `devDependencies`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `get_db()` connect `database.py` to `routes/sessions.py`, `routes/clinical.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `User` (e.g. with `login()` and `get_current_user_profile()`) actually correct?**
  _`User` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `routes/sessions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11954022988505747 - nodes in this community are weakly interconnected._
- **Should `database.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1330049261083744 - nodes in this community are weakly interconnected._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._