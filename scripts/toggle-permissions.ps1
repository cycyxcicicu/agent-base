<#
.SYNOPSIS
  Bật / tắt các quyền hạn chế (deny) của các Agent trong Kilo Code.
.EXAMPLE
  .\toggle-permissions.ps1 -Relax   # Comment các dòng cấm (deny) để Agent tự do phát triển phần mềm
  .\toggle-permissions.ps1 -Strict  # Mở lại các dòng cấm (deny) cho dự án yêu cầu bảo mật cao
#>
param(
    [switch]$Relax,
    [switch]$Strict
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyScript = Join-Path $scriptDir "toggle-permissions.py"

if ($Relax) {
    python $pyScript --relax
} else {
    # Mặc định là STRICT (bảo vệ): chỉ nới quyền khi truyền -Relax.
    python $pyScript --strict
}
