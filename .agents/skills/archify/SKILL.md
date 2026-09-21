---
name: archify
description: Generate polished, interactive HTML and SVG architecture, workflow, sequence, data-flow, and state machine diagrams from typed JSON specifications.
triggers:
  - system map
  - architecture diagram
  - interactive diagram
  - data flow diagram
  - sequence diagram
---

# Archify (Interactive System Architecture Compiler)

> [!NOTE]
> **Bản chất thực thi**: Kỹ năng này cung cấp định dạng đặc tả typed JSON IR và hướng dẫn tạo biểu đồ kiến trúc HTML/SVG tự chứa trực tiếp (hoặc kết xuất qua `agent_core/design/svg_renderer.py`). Không đòi hỏi binary compiler bên ngoài.

Create self-contained, interactive HTML diagrams with inline SVG, zoom/pan controls, dark/light themes, and trace motion from compact typed JSON specifications.

## 1. Supported Diagram Types
1. **Architecture (`architecture`)**: High-level component topology, microservices, cloud infra, security zones, and communication channels.
2. **Workflow (`workflow`)**: Step-by-step human or agent processes, branching decisions, approval gates, and escalation paths.
3. **Sequence (`sequence`)**: Inter-service message flows, API calls, database queries, and async webhooks over time.
4. **Dataflow (`dataflow`)**: ETL/ELT pipelines, streaming transformations, caches, and storage sinks with lineage tracking.
5. **Lifecycle (`lifecycle`)**: State machines, lifecycle transitions, state invariants, and terminal conditions.

## 2. Specification Structure (JSON IR)
Draft the diagram specification using structured JSON:
```json
{
  "version": "2.0",
  "type": "architecture",
  "title": "Agent Base System Topology",
  "nodes": [
    {"id": "agent_core", "label": "Agent Core", "kind": "service", "status": "active"},
    {"id": "eval_engine", "label": "Eval & Redteam", "kind": "subsystem", "status": "active"},
    {"id": "storage", "label": "SQLite / Local FS", "kind": "database", "status": "storage"}
  ],
  "edges": [
    {"from": "agent_core", "to": "eval_engine", "label": "Dispatches tests", "style": "solid"},
    {"from": "eval_engine", "to": "storage", "label": "Persists proof logs", "style": "dashed"}
  ]
}
```

## 3. Quality Profile Guidelines
- **Showcase**: Maximum visual fidelity with semantic colors, clear iconography, distinct bounding boxes, and trace paths.
- **Standard**: Dense engineering diagrams optimized for rapid comprehension and technical reviews.
- Avoid crossed lines by grouping related subsystems into lanes or zones.
- Export as standalone `.html` with embedded CSS/SVG for offline viewing in any browser.
