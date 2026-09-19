# Stack: Node.js / TypeScript

Lệnh dưới đây là mặc định phổ biến. Nếu `PROJECT.md` ghi lệnh khác thì theo `PROJECT.md`.

## Lệnh mặc định

| Việc | Lệnh |
|---|---|
| Cài phụ thuộc | `npm ci` (có lockfile) hoặc `npm install` |
| Chạy | `npm run dev` hoặc `npm start` (theo `package.json`) |
| Test | `npm test` |
| Lint | `npm run lint` |
| Build | `npm run build` |
| Kiểm tra kiểu (TypeScript) | `npx tsc --noEmit` |

Nếu dự án dùng `pnpm` hoặc `yarn`, thay lệnh tương ứng theo `PROJECT.md`.

## Cấu trúc thường dùng

`src/`, `tests/` (hoặc `__tests__/`), `package.json`, `tsconfig.json`.

## Quy ước code

- Đặt tên: `camelCase` cho hàm và biến, `PascalCase` cho lớp và kiểu.
- Với TypeScript: tránh `any`, bật `strict` nếu dự án đã bật.
- Theo ESLint và Prettier của dự án, không đổi cấu hình khi không được giao.

## File dùng chung (chỉ task được chỉ định mới sửa)

`package.json`, `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`, `tsconfig.json`, cấu hình ESLint và Prettier.

Thêm phụ thuộc mới làm đổi `package.json` và lockfile: chỉ một task duy nhất được làm việc này trong mỗi đợt song song.

## Không sửa tay

`node_modules/`, `dist/`, `build/`, `.next/`.

## Bẫy thường gặp trên Windows

- `node_modules` rất nặng: không đặt trong OneDrive, mỗi worktree sẽ có bản riêng.
- Đường dẫn dài trong `node_modules` có thể gây lỗi.
