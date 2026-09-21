#!/usr/bin/env node
/**
 * Ticket Dependency & Frontier Validator (Adapted from pocock-skills / to-tickets)
 * Checks DAG integrity, detects cycles, validates blockers, and identifies agent frontier.
 */

const fs = require('fs');
const path = require('path');

function parseFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;

  const rawLines = match[1].split(/\r?\n/);
  const data = {};
  for (const line of rawLines) {
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let val = line.slice(colonIdx + 1).trim();

    if (val.startsWith('[') && val.endsWith(']')) {
      const inner = val.slice(1, -1).trim();
      data[key] = inner ? inner.split(',').map(s => s.trim().replace(/^["']|["']$/g, '')) : [];
    } else {
      data[key] = val.replace(/^["']|["']$/g, '');
    }
  }
  return data;
}

function run() {
  const targetDir = process.argv[2] || __dirname;
  console.log(`\n🔍 Quét và kiểm định đồ thị phụ thuộc Tickets tại: ${targetDir}\n`);

  const files = fs.readdirSync(targetDir).filter(f => f.endsWith('.md') && f !== 'README.md');
  const tickets = new Map();

  for (const file of files) {
    const fullPath = path.join(targetDir, file);
    const fm = parseFrontmatter(fullPath);
    if (fm && fm.id) {
      tickets.set(fm.id, {
        file,
        id: fm.id,
        title: fm.title || 'Untitled',
        status: fm.status || 'unknown',
        blocked_by: fm.blocked_by || []
      });
    }
  }

  console.log(`📋 Đã phát hiện ${tickets.size} tickets hợp lệ có frontmatter.\n`);

  // 1. Kiểm tra Missing Blockers
  let hasError = false;
  for (const [id, ticket] of tickets.entries()) {
    for (const blocker of ticket.blocked_by) {
      if (!tickets.has(blocker)) {
        console.error(`❌ [LỖI LIÊN KẾT] Ticket ${id} phụ thuộc vào '${blocker}' nhưng không tìm thấy ticket này!`);
        hasError = true;
      }
    }
  }

  // 2. Kiểm tra chu trình phụ thuộc (Cycle Detection)
  const visited = new Set();
  const recursionStack = new Set();

  function hasCycle(nodeId, path = []) {
    visited.add(nodeId);
    recursionStack.add(nodeId);
    path.push(nodeId);

    const ticket = tickets.get(nodeId);
    if (ticket && ticket.blocked_by) {
      for (const blocker of ticket.blocked_by) {
        if (!visited.has(blocker)) {
          if (hasCycle(blocker, [...path])) return true;
        } else if (recursionStack.has(blocker)) {
          console.error(`❌ [CHU TRÌNH PHỤ THUỘC PHÁT HIỆN]: ${path.join(' -> ')} -> ${blocker}`);
          return true;
        }
      }
    }

    recursionStack.delete(nodeId);
    return false;
  }

  for (const id of tickets.keys()) {
    if (!visited.has(id)) {
      if (hasCycle(id)) hasError = true;
    }
  }

  // 3. Xác định Frontier (Các ticket sẵn sàng làm việc ngay)
  const frontier = [];
  for (const [id, ticket] of tickets.entries()) {
    if (ticket.status === 'done') continue;

    const allBlockersDone = ticket.blocked_by.every(blockerId => {
      const b = tickets.get(blockerId);
      return b && b.status === 'done';
    });

    if (allBlockersDone) {
      frontier.push(ticket);
    }
  }

  // Hiển thị bảng tổng hợp trạng thái
  console.log('| ID | Tiêu đề | Trạng thái | Phụ thuộc (Blocked by) | Sẵn sàng (Frontier)? |');
  console.log('|---|---|---|---|---|');
  for (const [id, t] of tickets.entries()) {
    const isFrontier = frontier.some(f => f.id === id);
    const blockersStr = t.blocked_by.length > 0 ? t.blocked_by.join(', ') : 'None';
    console.log(`| ${t.id} | ${t.title} | ${t.status} | ${blockersStr} | ${isFrontier ? '🟢 CÓ THỂ LÀM NGAY' : '⏳ Đang chờ/Đã xong'} |`);
  }

  console.log('\n--- KẾT QUẢ PHÂN TÍCH FRONTIER ---');
  if (frontier.length > 0) {
    console.log(`🎯 Các ticket nằm trên FRONTIER sẵn sàng phân công cho Agent:`);
    for (const f of frontier) {
      console.log(`   👉 [${f.id}] ${f.title} (File: ${f.file})`);
    }
  } else {
    console.log('🏁 Không có ticket nào khả dụng trên Frontier.');
  }

  if (hasError) {
    console.error('\n💥 Kiểm định thất bại: Phát hiện lỗi cấu trúc đồ thị phụ thuộc.');
    process.exit(1);
  } else {
    console.log('\n✅ Kiểm định đồ thị phụ thuộc HOÀN TOÀN HỢP LỆ (DAG hợp lệ, 0 chu trình).');
  }
}

run();
