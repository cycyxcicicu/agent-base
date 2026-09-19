# Stack: .NET (C#)

Lệnh dưới đây là mặc định phổ biến. Nếu `PROJECT.md` ghi lệnh khác thì theo `PROJECT.md`.

## Lệnh mặc định

| Việc | Lệnh |
|---|---|
| Khôi phục phụ thuộc | `dotnet restore` |
| Build | `dotnet build` |
| Chạy | `dotnet run --project <đường dẫn dự án>` |
| Test | `dotnet test` |
| Format | `dotnet format` (nếu dự án dùng) |

## Cấu trúc thường dùng

`src/<Project>/`, `tests/<Project>.Tests/`, file `.sln`, `.csproj`.

## Quy ước code

- Đặt tên: `PascalCase` cho lớp, phương thức, thuộc tính; `camelCase` cho biến cục bộ và tham số; `_camelCase` cho trường private (nếu dự án theo quy ước này).
- Bật nullable reference types nếu dự án đã bật, không tắt để cho qua cảnh báo.
- Theo `.editorconfig` của dự án.

## File dùng chung (chỉ task được chỉ định mới sửa)

`*.sln`, `*.csproj`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `nuget.config`.

## Không sửa tay

`bin/`, `obj/`, file sinh tự động (`*.g.cs`, `*.Designer.cs`), migration đã áp dụng.

## Cơ sở dữ liệu

Migration đã áp dụng lên môi trường thật không được sửa: tạo migration mới. Task đụng migration phải có "Kịch bản hoàn tác" trong card.

## Bẫy thường gặp trên Windows

- `bin/` và `obj/` do mỗi worktree sinh riêng, không commit.
- Đường dẫn dài và khoảng trắng: dùng dấu nháy khi gọi lệnh.
