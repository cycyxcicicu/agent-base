"""
Tracer-Bullet Vertical Slicing & Dependency DAG Frontier Resolver.
Học hỏi từ: pocock-skills (to-tickets, frontier dependency, vertical slicing).
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set, Optional, Any


@dataclass
class Ticket:
    ticket_id: str
    title: str
    status: str  # TODO, IN_PROGRESS, DONE, BLOCKED
    blocked_by: List[str] = field(default_factory=list)
    has_ui: bool = False
    has_api: bool = False
    has_db: bool = False
    has_test: bool = False
    file_path: Optional[str] = None


class TicketParser:
    """Phân tích các phiếu công việc Tracer-Bullet Markdown."""

    @classmethod
    def parse_markdown(cls, content: str, file_path: Optional[str] = None) -> Optional[Ticket]:
        lines = content.splitlines()
        ticket_id = ""
        title = ""
        status = "TODO"
        blocked_by: List[str] = []

        # Bóc tách tiêu đề # T-01: ...
        for line in lines:
            if line.startswith("# "):
                m = re.match(r"#\s+([A-Za-z0-9_.-]+)\s*:\s*(.*)", line)
                if m:
                    ticket_id = m.group(1).strip()
                    title = m.group(2).strip()
                else:
                    title = line.replace("#", "").strip()
                break

        # Bóc tách metadata status & blocked_by
        for line in lines:
            if "Trạng thái" in line or "Status" in line:
                for st in ["DONE", "IN_PROGRESS", "BLOCKED", "TODO"]:
                    if st in line.upper():
                        status = st
                        break
            if "Bị chặn bởi" in line or "blocked_by" in line.lower():
                # Tìm các mã ticket dạng T-01, T-02
                matches = re.findall(r"\b[A-Za-z0-9_.-]+-\d+(?:\.\d+)?\b", line)
                blocked_by.extend([m for m in matches if m != ticket_id])

        # Kiểm tra vertical slices
        has_ui = bool(re.search(r"(?i)\b(UI|Giao diện|Frontend|Component)\b", content))
        has_api = bool(re.search(r"(?i)\b(API|Route|Endpoint|Controller|Backend)\b", content))
        has_db = bool(re.search(r"(?i)\b(DB|Database|Migration|Schema|Bảng|Model)\b", content))
        has_test = bool(re.search(r"(?i)\b(Test|Kiểm thử|Unit test|E2E)\b", content))

        if not ticket_id:
            ticket_id = Path(file_path).stem if file_path else "UNKNOWN"

        return Ticket(
            ticket_id=ticket_id,
            title=title or ticket_id,
            status=status,
            blocked_by=list(set(blocked_by)),
            has_ui=has_ui,
            has_api=has_api,
            has_db=has_db,
            has_test=has_test,
            file_path=file_path
        )


class DependencyGraph:
    """Đồ thị phụ thuộc tác vụ và cơ chế tìm đường biên khả thi (Frontier)."""

    def __init__(self, tickets: List[Ticket]):
        self.tickets: Dict[str, Ticket] = {t.ticket_id: t for t in tickets}

    def validate_dependencies(self) -> List[str]:
        """
        Kiểm tra tính toàn vẹn của đồ thị:
        Phát hiện các ticket phụ thuộc vào ticket ID không tồn tại trong danh mục.
        """
        missing_errors = []
        for t_id, ticket in self.tickets.items():
            for dep in ticket.blocked_by:
                if dep not in self.tickets:
                    missing_errors.append(f"Ticket '{t_id}' phụ thuộc vào ticket không tồn tại '{dep}'")
        return missing_errors

    def get_frontier(self, strict: bool = True) -> List[Ticket]:
        """
        Tìm các ticket ở đường biên (Frontier):
        Là các ticket chưa xong (TODO / IN_PROGRESS) mà TẤT CẢ các ticket trong blocked_by đều đã DONE!
        Cho phép nhiều Agent nhận việc song song mà tuyệt đối không dẫm chân hoặc chờ nhau.
        Nếu strict=True, tự động gọi validate_dependencies() và báo lỗi nếu có ticket phụ thuộc ID không tồn tại.
        """
        if strict:
            missing = self.validate_dependencies()
            if missing:
                raise ValueError("Đồ thị phụ thuộc chứa ticket ID không tồn tại:\n" + "\n".join(missing))

        frontier: List[Ticket] = []

        done_ids = {t_id for t_id, t in self.tickets.items() if t.status == "DONE"}

        for t_id, ticket in self.tickets.items():
            if ticket.status in ["DONE"]:
                continue
            # Kiểm tra xem toàn bộ các điều kiện phụ thuộc đã hoàn thành chưa
            dependencies_met = all(dep in done_ids for dep in ticket.blocked_by)
            if dependencies_met:
                frontier.append(ticket)

        return frontier

    def detect_cycles(self) -> Optional[List[str]]:
        """
        Phát hiện chu trình phụ thuộc vòng (Circular Dependency) bằng thuật toán DFS.
        Nếu phát hiện cycle, trả về đường dẫn chu trình (ví dụ: ['T-01', 'T-02', 'T-01']).
        Nếu là DAG hợp lệ, trả về None.
        """
        visited = set()
        rec_stack = []

        def dfs(node: str) -> Optional[List[str]]:
            visited.add(node)
            rec_stack.append(node)

            ticket = self.tickets.get(node)
            if ticket:
                for dep in ticket.blocked_by:
                    if dep not in self.tickets:
                        continue
                    if dep not in visited:
                        cycle = dfs(dep)
                        if cycle:
                            return cycle
                    elif dep in rec_stack:
                        # Tìm thấy chu trình vòng
                        idx = rec_stack.index(dep)
                        return rec_stack[idx:] + [dep]

            rec_stack.pop()
            return None

        for node in self.tickets:
            if node not in visited:
                cycle = dfs(node)
                if cycle:
                    return cycle
        return None

    def topological_sort(self) -> List[str]:
        """
        Sắp xếp tô-pô các ticket theo thứ tự thực thi hợp lệ (Kahn's Algorithm).
        Ném ra ValueError nếu tồn tại chu trình vòng (Deadlock).
        """
        cycle = self.detect_cycles()
        if cycle:
            raise ValueError(f"Phát hiện chu trình phụ thuộc vòng (Circular Deadlock): {' -> '.join(cycle)}")

        # Tính toán in-degree (số lượng dependencies mà ticket này phụ thuộc vào)
        # Ở đây A.blocked_by = [B] nghĩa là B phải xong trước A (B -> A)
        in_degree = {t_id: 0 for t_id in self.tickets}
        adj = {t_id: [] for t_id in self.tickets}

        for t_id, ticket in self.tickets.items():
            for dep in ticket.blocked_by:
                if dep in self.tickets:
                    adj[dep].append(t_id)
                    in_degree[t_id] += 1

        queue = [t_id for t_id, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order

    def calculate_critical_path(self) -> List[str]:
        """
        Tính toán Đường Găng (Critical Path): Chuỗi phụ thuộc dài nhất trong DAG.
        Xác định thời gian tối thiểu và các mấu chốt quyết định tiến độ dự án.
        """
        order = self.topological_sort()
        # dist[u] = độ dài đường đi dài nhất kết thúc tại u
        dist = {t_id: 1 for t_id in self.tickets}
        prev = {t_id: None for t_id in self.tickets}

        for u in order:
            ticket = self.tickets.get(u)
            if ticket:
                for dep in ticket.blocked_by:
                    if dep in dist and dist[dep] + 1 > dist[u]:
                        dist[u] = dist[dep] + 1
                        prev[u] = dep

        # Tìm node có dist lớn nhất
        if not dist:
            return []
        max_node = max(dist, key=dist.get)

        path = []
        curr = max_node
        while curr:
            path.append(curr)
            curr = prev[curr]

        return path[::-1]

    def validate_vertical_slice(self, ticket: Ticket) -> Dict[str, Any]:
        """Xác thực chuẩn Tracer-Bullet: Phải cắt dọc đầy đủ lát cắt."""
        layers = {
            "UI": ticket.has_ui,
            "API": ticket.has_api,
            "DB": ticket.has_db,
            "Test": ticket.has_test
        }
        is_complete = sum(layers.values()) >= 3
        return {
            "ticket_id": ticket.ticket_id,
            "is_complete_slice": is_complete,
            "layers": layers
        }

