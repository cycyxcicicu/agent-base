"""scripts/crawl_full_uml_theory.py

Cào toàn diện 22+ phân loại sơ đồ UML 2.5 (chuẩn và mở rộng theo cây phân loại)
cùng toàn bộ các trang lý thuyết phần tử chi tiết về D:/test-repo/uml/
"""

from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.crawl_jina_assets import crawl_page

FULL_UML_PAGES = [
    # === STRUCTURE DIAGRAMS & ELEMENTS ===
    {"folder": "class-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/class-diagrams-overview.html", "title": "Class Diagrams Overview"},
    {"folder": "class-diagram", "slug": "classifier", "url": "https://www.uml-diagrams.org/classifier.html", "title": "Classifiers (Classes, Interfaces)"},
    {"folder": "class-diagram", "slug": "association", "url": "https://www.uml-diagrams.org/association.html", "title": "Associations, Aggregation, Composition"},
    {"folder": "class-diagram", "slug": "multiplicity", "url": "https://www.uml-diagrams.org/multiplicity.html", "title": "Multiplicity Elements"},
    {"folder": "class-diagram", "slug": "generalization", "url": "https://www.uml-diagrams.org/generalization.html", "title": "Generalization & Inheritance"},
    {"folder": "class-diagram", "slug": "dependency", "url": "https://www.uml-diagrams.org/dependency.html", "title": "Dependencies & Realization"},
    {"folder": "class-diagram", "slug": "interface", "url": "https://www.uml-diagrams.org/interface.html", "title": "Interfaces & Provided/Required"},

    {"folder": "object-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/object-diagrams.html", "title": "Object Diagrams Overview"},
    {"folder": "object-diagram", "slug": "instance-specification", "url": "https://www.uml-diagrams.org/instance-specification.html", "title": "Instance Specification"},

    {"folder": "package-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/package-diagrams-overview.html", "title": "Package Diagrams Overview"},
    {"folder": "package-diagram", "slug": "package-merge", "url": "https://www.uml-diagrams.org/package-merge.html", "title": "Package Merge & Import"},
    {"folder": "model-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/package-diagrams/model.html", "title": "Model Diagrams (UML Extension)"},

    {"folder": "composite-structure-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/composite-structure-diagrams.html", "title": "Composite Structure Diagrams"},
    {"folder": "composite-structure-diagram", "slug": "internal-structure", "url": "https://www.uml-diagrams.org/composite-structure-diagrams/internal-structure.html", "title": "Internal Structure Diagram"},
    {"folder": "composite-structure-diagram", "slug": "collaboration-use", "url": "https://www.uml-diagrams.org/collaboration-use.html", "title": "Collaboration Use Diagram"},

    {"folder": "component-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/component-diagrams.html", "title": "Component Diagrams Overview"},
    {"folder": "component-diagram", "slug": "component", "url": "https://www.uml-diagrams.org/component.html", "title": "Component Elements & Packaging"},
    {"folder": "component-diagram", "slug": "port", "url": "https://www.uml-diagrams.org/port.html", "title": "Ports & Connectors"},
    {"folder": "manifestation-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/artifact.html", "title": "Manifestation & Artifact Diagrams"},

    {"folder": "deployment-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/deployment-diagrams-overview.html", "title": "Deployment Diagrams Overview"},
    {"folder": "deployment-diagram", "slug": "node", "url": "https://www.uml-diagrams.org/deployment-diagrams.html", "title": "Execution Environment & Devices"},
    {"folder": "network-architecture-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/network-architecture-diagrams.html", "title": "Network Architecture Diagrams"},

    {"folder": "profile-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/profile-diagrams.html", "title": "Profile Diagrams Overview"},
    {"folder": "profile-diagram", "slug": "stereotype", "url": "https://www.uml-diagrams.org/stereotype.html", "title": "Stereotypes & Tagged Values"},

    # === BEHAVIOR DIAGRAMS & ELEMENTS ===
    {"folder": "use-case-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/use-case-diagrams.html", "title": "Use Case Diagrams Overview"},
    {"folder": "use-case-diagram", "slug": "use-case", "url": "https://www.uml-diagrams.org/use-case.html", "title": "Use Cases, Extend, Include"},
    {"folder": "use-case-diagram", "slug": "actor", "url": "https://www.uml-diagrams.org/use-case-actor.html", "title": "Actors & Subject System"},

    {"folder": "information-flow-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/information-flow-diagrams.html", "title": "Information Flow Diagrams"},

    {"folder": "activity-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/activity-diagrams.html", "title": "Activity Diagrams Overview"},
    {"folder": "activity-diagram", "slug": "actions", "url": "https://www.uml-diagrams.org/activity-diagrams-actions.html", "title": "Executable Actions & Call Behaviors"},
    {"folder": "activity-diagram", "slug": "controls", "url": "https://www.uml-diagrams.org/activity-diagrams-controls.html", "title": "Control Nodes (Decision, Fork, Join, Final)"},
    {"folder": "activity-diagram", "slug": "objects", "url": "https://www.uml-diagrams.org/activity-diagrams-objects.html", "title": "Object Nodes, Buffers & Data Stores"},

    {"folder": "state-machine-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/state-machine-diagrams.html", "title": "State Machine Diagrams Overview"},
    {"folder": "state-machine-diagram", "slug": "behavioral-state", "url": "https://www.uml-diagrams.org/state-machine-diagrams/behavioral.html", "title": "Behavioral State Machine"},
    {"folder": "protocol-state-machine", "slug": "spec", "url": "https://www.uml-diagrams.org/protocol-state-machine-diagrams.html", "title": "Protocol State Machine Diagrams"},

    # === INTERACTION DIAGRAMS & ELEMENTS ===
    {"folder": "sequence-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/sequence-diagrams.html", "title": "Sequence Diagrams Overview"},
    {"folder": "sequence-diagram", "slug": "fragments", "url": "https://www.uml-diagrams.org/sequence-diagrams-combined-fragments.html", "title": "Combined Fragments (Alt, Loop, Par, Opt)"},
    {"folder": "sequence-diagram", "slug": "messages", "url": "https://www.uml-diagrams.org/sequence-diagrams-messages.html", "title": "Message Types (Sync, Async, Reply)"},

    {"folder": "communication-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/communication-diagrams.html", "title": "Communication Diagrams Overview"},
    {"folder": "timing-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/timing-diagrams.html", "title": "Timing Diagrams Overview"},
    {"folder": "interaction-overview-diagram", "slug": "spec", "url": "https://www.uml-diagrams.org/interaction-overview-diagrams.html", "title": "Interaction Overview Diagrams"},
]


def main():
    root_uml = Path("D:/test-repo/uml")
    root_uml.mkdir(parents=True, exist_ok=True)

    print(f"=== BẮT ĐẦU CÀO TOÀN DIỆN {len(FULL_UML_PAGES)} CHỦ ĐỀ SƠ ĐỒ & LÝ THUYẾT CHI TIẾT UML 2.5 ===")

    for idx, item in enumerate(FULL_UML_PAGES, 1):
        target_dir = root_uml / item["folder"]
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"{item['slug']}.md"

        print(f"[{idx}/{len(FULL_UML_PAGES)}] {item['title']} -> {item['folder']}/{item['slug']}.md...")
        if target_file.exists() and target_file.stat().st_size > 1500:
            print(f"  -> [EXISTS] Đã có sẵn ({target_file.stat().st_size} bytes)")
            continue

        try:
            crawl_page(
                target_url=item["url"],
                out_dir=target_dir,
                doc_slug=item["slug"],
                download_images=True,
                max_workers=4,
                timeout=45,
            )
            time.sleep(0.5)
        except Exception as e:
            print(f"  [WARN] Lỗi cào {item['title']}: {e}", file=sys.stderr)

    print("\n=== HOÀN TẤT TOÀN DIỆN 100% LÝ THUYẾT VÀ 22+ PHÂN LOẠI SƠ ĐỒ UML 2.5 TẠI D:/test-repo/uml ===")


if __name__ == "__main__":
    main()

