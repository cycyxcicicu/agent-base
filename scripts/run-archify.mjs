#!/usr/bin/env node
/**
 * scripts/run-archify.mjs
 * Trình khởi chạy Archify CLI linh hoạt & thông minh:
 * 1. Ưu tiên công cụ nhúng cục bộ trong dự án: `tools/archify/bin/archify.mjs`
 * 2. Nếu không có, đọc đường dẫn `quarantine_dir` từ file cấu hình duy nhất `skills.config.json`
 * 3. Nếu vẫn không thấy, thông báo rõ ràng cho lập trình viên cách cài đặt / chạy fetch-skills.py
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// 1. Kiểm tra bản nhúng cục bộ trong dự án
const localArchify = path.join(rootDir, 'tools', 'archify', 'bin', 'archify.mjs');
if (fs.existsSync(localArchify)) {
  const result = spawnSync(process.execPath, [localArchify, ...process.argv.slice(2)], {
    stdio: 'inherit',
    cwd: process.cwd()
  });
  process.exit(result.status ?? 0);
}

// 2. Đọc đường dẫn quarantine từ file cấu hình trung tâm (ưu tiên skills.config.local.json)
const localConfigFile = path.join(rootDir, 'skills.config.local.json');
const configFile = fs.existsSync(localConfigFile) ? localConfigFile : path.join(rootDir, 'skills.config.json');
let quarantineDir = process.env.SKILLS_QUARANTINE_DIR || '';

if (fs.existsSync(configFile)) {
  try {
    const raw = fs.readFileSync(configFile, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed.quarantine_dir) {
      quarantineDir = parsed.quarantine_dir;
    }
  } catch (err) {
    console.warn(`⚠️ Cảnh báo: Không thể phân tích ${path.basename(configFile)}: ${err.message}`);
  }
}

// Cho phép biến môi trường ghi đè tường minh (dành cho môi trường CI/CD hoặc container)
if (process.env.SKILLS_QUARANTINE_DIR) {
  quarantineDir = process.env.SKILLS_QUARANTINE_DIR;
}

// Mở rộng ký tự ~ trên macOS / Linux nếu có
if (quarantineDir.startsWith('~/') || quarantineDir === '~') {
  quarantineDir = path.join(os.homedir(), quarantineDir.slice(1));
}

// Kiểm tra nghiêm cấm ổ hệ thống OS (Windows: C:, macOS/Linux: root /System...)
if (quarantineDir) {
  const qTrim = quarantineDir.trim();
  if (process.platform === 'win32' && qTrim.toUpperCase().startsWith('C:')) {
    console.error('\n' + '='.repeat(80));
    console.error('⛔ LỖI AN TOÀN: File skills.config.json đang trỏ vào ổ C: (ổ hệ điều hành Windows).');
    console.error('Quy định nghiêm cấm cấu hình kho kỹ năng vào ổ C!');
    console.error('Vui lòng chạy: python scripts/setup-skills.py để cấu hình ổ dữ liệu hợp lệ (D:, E:...).');
    console.error('='.repeat(80) + '\n');
    process.exit(1);
  } else if (process.platform !== 'win32') {
    const forbidden = ['/System', '/usr', '/bin', '/etc', '/Library'];
    if (qTrim === '/' || forbidden.some(d => qTrim === d || qTrim.startsWith(d + '/'))) {
      console.error('\n' + '='.repeat(80));
      console.error(`⛔ LỖI AN TOÀN: File skills.config.json đang trỏ vào thư mục hệ thống (${qTrim}).`);
      console.error('Vui lòng chạy: python3 scripts/setup-skills.py để cấu hình thư mục người dùng (~/skills-quarantine) hoặc /Volumes/...');
      console.error('='.repeat(80) + '\n');
      process.exit(1);
    }
  }
}

// 3. Tìm Archify CLI trong thư mục quarantine nếu đã cấu hình
if (quarantineDir) {
  const candidates = [
    path.join(quarantineDir, 'archify', 'archify', 'bin', 'archify.mjs'),
    path.join(quarantineDir, 'archify', 'bin', 'archify.mjs')
  ];

  let targetBin = null;
  for (const cand of candidates) {
    if (fs.existsSync(cand)) {
      targetBin = cand;
      break;
    }
  }

  if (targetBin) {
    const result = spawnSync(process.execPath, [targetBin, ...process.argv.slice(2)], {
      stdio: 'inherit',
      cwd: process.cwd()
    });
    process.exit(result.status ?? 0);
  }
}

// 4. Báo lỗi thân thiện nếu không tìm thấy ở bất cứ đâu
console.error('\n' + '='.repeat(80));
console.error('❌ KHÔNG TÌM THẤY TRÌNH BIÊN DỊCH ARCHIFY CLI');
console.error('='.repeat(80));
console.error(`- Thư mục dự án: ${localArchify} (không có)`);
console.error(`- Thư mục quarantine: ${quarantineDir || '(chưa cấu hình)'} (không tìm thấy archify/bin/archify.mjs)`);
console.error('\n💡 HƯỚNG DẪN XỬ LÝ (CHỈ CẦN THIẾT LẬP 1 CHỖ DUY NHẤT):');
console.error('  1. Chạy lệnh: python scripts/setup-skills.py');
console.error('     (Hệ thống sẽ hỏi bạn muốn lưu kho kỹ năng ở đâu trên ổ dữ liệu D:, E:... và tải tự động)');
console.error('  2. Cấu hình được lưu tự động vào "skills.config.json" ở gốc dự án.');
console.error('='.repeat(80) + '\n');
process.exit(1);
