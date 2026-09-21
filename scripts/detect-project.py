#!/usr/bin/env python3
"""
scripts/detect-project.py
Scan repository and detect language, framework, database, and build tools.
Can auto-fill PROJECT.md.

Usage:
  python scripts/detect-project.py
  python scripts/detect-project.py --fill-project-md
"""

import sys
import re
import argparse
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def main():
    parser = argparse.ArgumentParser(description="Detect project tech stack and build tools.")
    parser.add_argument("--path", type=str, default="", help="Path to project root.")
    parser.add_argument("--fill-project-md", action="store_true", help="Auto-fill PROJECT.md with detected values.")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path(__file__).resolve().parent.parent
    print(f"=== Scanning repository at: {root} ===")

    detected_stacks = []
    detected_db = set()
    detected_broker = set()
    test_cmd = ""
    build_cmd = ""
    run_cmd = ""
    install_cmd = ""
    lint_cmd = ""
    stack_file = ""

    # 1. Java / Spring Boot
    is_pom = (root / 'pom.xml').exists()
    is_gradle = (root / 'build.gradle').exists() or (root / 'build.gradle.kts').exists()
    if is_pom or is_gradle:
        detected_stacks.append("Java (Maven)" if is_pom else "Java (Gradle)")
        stack_file = "java.md"
        if is_pom:
            install_cmd = "./mvnw dependency:go-offline" if sys.platform != 'win32' else r".\mvnw.cmd dependency:go-offline"
            build_cmd = "./mvnw clean package -DskipTests" if sys.platform != 'win32' else r".\mvnw.cmd clean package -DskipTests"
            run_cmd = "./mvnw spring-boot:run" if sys.platform != 'win32' else r".\mvnw.cmd spring-boot:run"
            test_cmd = "./mvnw test" if sys.platform != 'win32' else r".\mvnw.cmd test"
            lint_cmd = "./mvnw checkstyle:check" if sys.platform != 'win32' else r".\mvnw.cmd checkstyle:check"
        else:
            install_cmd = "./gradlew build --dry-run" if sys.platform != 'win32' else r".\gradlew.bat build --dry-run"
            build_cmd = "./gradlew build -x test" if sys.platform != 'win32' else r".\gradlew.bat build -x test"
            run_cmd = "./gradlew bootRun" if sys.platform != 'win32' else r".\gradlew.bat bootRun"
            test_cmd = "./gradlew test" if sys.platform != 'win32' else r".\gradlew.bat test"
            lint_cmd = "./gradlew spotlessApply" if sys.platform != 'win32' else r".\gradlew.bat spotlessApply"

    # 2. Node.js
    if (root / 'package.json').exists():
        detected_stacks.append("Node.js / TypeScript")
        if not stack_file:
            stack_file = "node.md"
            install_cmd = "npm install"
            build_cmd = "npm run build"
            run_cmd = "npm start"
            test_cmd = "npm test"
            lint_cmd = "npm run lint"

    # 3. Python
    if (root / 'requirements.txt').exists() or (root / 'pyproject.toml').exists() or (root / 'Pipfile').exists():
        detected_stacks.append("Python")
        if not stack_file:
            stack_file = "python.md"
            install_cmd = "pip install -r requirements.txt"
            build_cmd = "# python interpreted"
            run_cmd = "python src/main.py"
            test_cmd = "pytest"
            lint_cmd = "ruff check ."

    # 4. .NET (C#)
    sln_files = list(root.glob('*.sln'))
    csproj_files = list(root.glob('*/*.csproj')) + list(root.glob('*.csproj'))
    if sln_files or csproj_files:
        detected_stacks.append(".NET (C#)")
        if not stack_file:
            stack_file = "dotnet.md"
            install_cmd = "dotnet restore"
            build_cmd = "dotnet build"
            run_cmd = "dotnet run"
            test_cmd = "dotnet test"
            lint_cmd = "dotnet format"

    # 5. Check for Docker Compose / Infra
    compose_patterns = ['docker-compose*.yml', 'docker-compose*.yaml', 'infra/docker-compose*.yml', 'infra/docker-compose*.yaml']
    for pat in compose_patterns:
        for cf in root.glob(pat):
            try:
                content = cf.read_text(encoding='utf-8', errors='replace').lower()
                if 'postgres' in content:
                    detected_db.add("PostgreSQL")
                if 'mysql' in content or 'mariadb' in content:
                    detected_db.add("MySQL/MariaDB")
                if 'redis' in content:
                    detected_broker.add("Redis (Cache)")
                if 'rabbitmq' in content:
                    detected_broker.add("RabbitMQ")
                if 'mongo' in content:
                    detected_db.add("MongoDB")
                if 'kafka' in content:
                    detected_broker.add("Kafka")
            except Exception:
                pass

    stack_str = ", ".join(detected_stacks) if detected_stacks else "Generic / Unknown"
    stack_file_str = stack_file if stack_file else "_template.md"
    db_str = ", ".join(sorted(detected_db)) if detected_db else "None / Embedded"
    broker_str = ", ".join(sorted(detected_broker)) if detected_broker else "None"

    print(f"Detected Stack     : {stack_str}")
    print(f"Suggested Stack File: {stack_file_str}")
    print(f"Detected Databases : {db_str}")
    print(f"Detected Brokers   : {broker_str}")
    print(f"Suggested Test Cmd : {test_cmd}")
    print(f"Suggested Run Cmd  : {run_cmd}")

    if args.fill_project_md:
        proj_md = root / 'PROJECT.md'
        print(f"Updating {proj_md}...")
        proj_name = root.name
        new_content = f"""# PROJECT.md - thong tin rieng cua du an

| Muc | Gia tri |
|---|---|
| Ten du an | {proj_name} |
| Mo ta mot cau | Du an {proj_name} (tu dong nhan dien boi detect-project.py) |
| Stack | agents/stacks/{stack_file_str} |
| Nhanh chinh | main |
| Nhanh tich hop | develop |

## Lenh

| Viec | Lenh |
|---|---|
| Cai phu thuoc | {install_cmd} |
| Chay | {run_cmd} |
| Test | {test_cmd} |
| Lint / format | {lint_cmd} |
| Build | {build_cmd} |

## Pham vi va rang buoc

- Co so du lieu: {db_str}
- Message Queue / Cache: {broker_str}
- Tap tin dung chung (chi task duoc chi dinh moi sua): pom.xml, package.json, pyproject.toml, docker-compose*.yml
- File/thu muc cam sua tay: target/, build/, dist/, .venv/, bin/, obj/

## Ghi chu van hanh
- Docker Dev Services: xem infra/docker-compose.dev.yml
- Kiem tra merge: chay scripts/merge-gate.ps1 (hoac ./scripts/merge-gate.sh)
"""
        proj_md.write_text(new_content, encoding='utf-8')
        print(f"Successfully updated {proj_md}")


if __name__ == '__main__':
    main()
