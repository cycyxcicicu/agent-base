---
description: "Xây và giữ CI/CD, môi trường chạy, đóng gói và quy trình deploy. Không deploy lên môi trường thật khi chưa được người dùng duyệt. Không sửa code ứng dụng."
mode: all
model: 9router/claude-sonet-5-9router
permission:
  edit:
    "*": deny
    "docs/notes/inbox/**": allow
    "docs\\notes\\inbox\\**": allow
    ".github/**": allow
    ".github\\**": allow
    "infra/**": allow
    "infra\\**": allow
    "deploy/**": allow
    "deploy\\**": allow
    "Dockerfile*": allow
    "docker-compose*": allow
    "docs/runbooks/**": allow
    "docs\\runbooks\\**": allow
    "tasks/**": allow
    "tasks\\**": allow
    ".env*": deny
  bash:
    "*": allow
    "npm publish*": ask
    "docker push*": ask
    "twine upload*": ask
    "terraform apply*": ask
    "kubectl apply*": ask
    "kubectl delete*": ask
    "docker system prune*": ask
    "git checkout .": ask
    "git restore .": ask
    "*drop table*": ask
    "*drop database*": ask
    "*truncate*": ask
    "terraform destroy*": ask
    "helm install*": ask
    "helm upgrade*": ask
    "helm uninstall*": ask
    "npm unpublish*": ask
    "yarn publish*": ask
    "pnpm publish*": ask
    "cargo publish*": ask
    "dotnet nuget push*": ask
    "aws s3 rm*": ask
    "aws s3 sync*": ask
    "gcloud * delete*": ask
    "az * delete*": ask
    "git add*": ask
    "git.exe add*": ask
    "*git add*": ask
    "*git.exe add*": ask
    "git -C * add*": ask
    "git --* add*": ask
    "git -* add*": ask
    "git commit*": ask
    "git.exe commit*": ask
    "*git commit*": ask
    "*git.exe commit*": ask
    "git -C * commit*": ask
    "git --* commit*": ask
    "git -* commit*": ask
    "git push*": ask
    "git.exe push*": ask
    "*git push*": ask
    "*git.exe push*": ask
    "git -C * push*": ask
    "git --* push*": ask
    "git -* push*": ask
    "git reset*": deny
    "git stash drop*": deny
    "git stash clear*": deny
    "git tag -d*": deny
    "git tag -f*": deny
    "git tag --delete*": deny
    "git clean*": deny
    "git init*": deny
    "git clone*": deny
    "git branch -D*": deny
    "git branch --delete*": deny
    "git worktree prune*": deny
    "git worktree lock*": deny
    "git worktree unlock*": deny
    "git remote add*": deny
    "git remote remove*": deny
    "git remote set-url*": deny
    "git remote rename*": deny
    "git config *": deny
    "*install-hooks*": deny
    "git -C * reset*": deny
    "git -C * clean*": deny
    "git -C * config*": deny
    "git --* reset*": deny
    "git --* clean*": deny
    "git --* config*": deny
    "git -* reset*": deny
    "*&&*git reset*": deny
    "*;*git reset*": deny
    "*|*git reset*": deny
    "git push --force*": deny
    "git push -f*": deny
    "git reset --hard*": deny
    "command git *": deny
    "/usr/bin/git *": deny
    "\"git\" *": deny
    "'git' *": deny
    "*git reset*": deny
    "*git.exe reset*": deny
    "*git*stash drop*": deny
    "*git*stash clear*": deny
    "*git*tag -d*": deny
    "*git*tag -f*": deny
    "*git*tag --delete*": deny
    "*git clean*": deny
    "*git.exe clean*": deny
    "*git init*": deny
    "*git.exe init*": deny
    "*git clone*": deny
    "*git.exe clone*": deny
    "*git*branch -D*": deny
    "*git*branch --delete*": deny
    "*git*worktree prune*": deny
    "*git*worktree lock*": deny
    "*git*worktree unlock*": deny
    "*git*remote add*": deny
    "*git*remote remove*": deny
    "*git*remote set-url*": deny
    "*git*remote rename*": deny
    "*git config *": deny
    "*git.exe config *": deny
    "*$(*git*)*": deny
    "*`*git*`*": deny
    "*git*--no-verify*": deny
    "*\ngit reset*": deny
    "git add -A*": deny
    "git add --all*": deny
    "git add .": deny
    "git add . *": deny
    "git add -f*": deny
    "git add --force*": deny
    "git add*--force*": deny
    "git add* -f *": deny
    "git commit*--amend*": deny
    "git commit*--no-verify*": deny
    "git commit -n*": deny
    "git commit*--author*": deny
    "git commit*--reset-author*": deny
    "git commit*--no-gpg-sign*": deny
    "git push*--force*": deny
    "git push* -f": deny
    "git push* -f *": deny
    "git push*--delete*": deny
    "git push* -d *": deny
    "git push* -d": deny
    "git push*--mirror*": deny
    "git push*--all*": deny
    "git push*--tags*": deny
    "git push*--prune*": deny
    "git push*--no-verify*": deny
    "git push* :*": deny
    "git push*:main*": deny
    "git push*:master*": deny
    "git push*:develop*": deny
    "git push*:release/*": deny
    "git push*refs/heads/main*": deny
    "git push*refs/heads/master*": deny
    "git push*refs/heads/develop*": deny
    "git push* main": deny
    "git push* main *": deny
    "git push* master": deny
    "git push* master *": deny
    "git push* develop": deny
    "git push* develop *": deny
    "git push* release/*": deny
    "*git add -A*": deny
    "*git add --all*": deny
    "*git add .": deny
    "*git add . *": deny
    "*git add -f*": deny
    "*git add --force*": deny
    "*git add*--force*": deny
    "*git add* -f *": deny
    "*git commit*--amend*": deny
    "*git commit*--no-verify*": deny
    "*git commit -n*": deny
    "*git commit*--author*": deny
    "*git commit*--reset-author*": deny
    "*git commit*--no-gpg-sign*": deny
    "*git push*--force*": deny
    "*git push* -f": deny
    "*git push* -f *": deny
    "*git push*--delete*": deny
    "*git push* -d *": deny
    "*git push* -d": deny
    "*git push*--mirror*": deny
    "*git push*--all*": deny
    "*git push*--tags*": deny
    "*git push*--prune*": deny
    "*git push*--no-verify*": deny
    "*git push* :*": deny
    "*git push*:main*": deny
    "*git push*:master*": deny
    "*git push*:develop*": deny
    "*git push*:release/*": deny
    "*git push*refs/heads/main*": deny
    "*git push*refs/heads/master*": deny
    "*git push*refs/heads/develop*": deny
    "*git push* main": deny
    "*git push* main *": deny
    "*git push* master": deny
    "*git push* master *": deny
    "*git push* develop": deny
    "*git push* develop *": deny
    "*git push* release/*": deny
    "git -c alias.*": deny
    "*git -c alias.*": deny
    "git.exe -c alias.*": deny
    "*git.exe -c alias.*": deny
    "git -c core.hooksPath*": deny
    "*git -c core.hooksPath*": deny
    "git.exe -c core.hooksPath*": deny
    "*git.exe -c core.hooksPath*": deny
    "git -c core.hookspath*": deny
    "*git -c core.hookspath*": deny
    "git.exe -c core.hookspath*": deny
    "*git.exe -c core.hookspath*": deny
    "git -c core.sshCommand*": deny
    "*git -c core.sshCommand*": deny
    "git.exe -c core.sshCommand*": deny
    "*git.exe -c core.sshCommand*": deny
    "git -c core.sshcommand*": deny
    "*git -c core.sshcommand*": deny
    "git.exe -c core.sshcommand*": deny
    "*git.exe -c core.sshcommand*": deny
    "git -c core.editor*": deny
    "*git -c core.editor*": deny
    "git.exe -c core.editor*": deny
    "*git.exe -c core.editor*": deny
    "git -c core.pager*": deny
    "*git -c core.pager*": deny
    "git.exe -c core.pager*": deny
    "*git.exe -c core.pager*": deny
    "git -c core.fsmonitor*": deny
    "*git -c core.fsmonitor*": deny
    "git.exe -c core.fsmonitor*": deny
    "*git.exe -c core.fsmonitor*": deny
    "git -c core.askPass*": deny
    "*git -c core.askPass*": deny
    "git.exe -c core.askPass*": deny
    "*git.exe -c core.askPass*": deny
    "git -c core.askpass*": deny
    "*git -c core.askpass*": deny
    "git.exe -c core.askpass*": deny
    "*git.exe -c core.askpass*": deny
    "git -c credential.*": deny
    "*git -c credential.*": deny
    "git.exe -c credential.*": deny
    "*git.exe -c credential.*": deny
    "git -c include.*": deny
    "*git -c include.*": deny
    "git.exe -c include.*": deny
    "*git.exe -c include.*": deny
    "git -c includeIf.*": deny
    "*git -c includeIf.*": deny
    "git.exe -c includeIf.*": deny
    "*git.exe -c includeIf.*": deny
    "git -c includeif.*": deny
    "*git -c includeif.*": deny
    "git.exe -c includeif.*": deny
    "*git.exe -c includeif.*": deny
    "git -c url.*": deny
    "*git -c url.*": deny
    "git.exe -c url.*": deny
    "*git.exe -c url.*": deny
    "git -c protocol.*": deny
    "*git -c protocol.*": deny
    "git.exe -c protocol.*": deny
    "*git.exe -c protocol.*": deny
    "git -c http.*": deny
    "*git -c http.*": deny
    "git.exe -c http.*": deny
    "*git.exe -c http.*": deny
    "git -c user.*": deny
    "*git -c user.*": deny
    "git.exe -c user.*": deny
    "*git.exe -c user.*": deny
    "git -c author.*": deny
    "*git -c author.*": deny
    "git.exe -c author.*": deny
    "*git.exe -c author.*": deny
    "git -c committer.*": deny
    "*git -c committer.*": deny
    "git.exe -c committer.*": deny
    "*git.exe -c committer.*": deny
    "git -c commit.gpgSign*": deny
    "*git -c commit.gpgSign*": deny
    "git.exe -c commit.gpgSign*": deny
    "*git.exe -c commit.gpgSign*": deny
    "git -c commit.gpgsign*": deny
    "*git -c commit.gpgsign*": deny
    "git.exe -c commit.gpgsign*": deny
    "*git.exe -c commit.gpgsign*": deny
    "git -c gpg.*": deny
    "*git -c gpg.*": deny
    "git.exe -c gpg.*": deny
    "*git.exe -c gpg.*": deny
    "git -c diff.external*": deny
    "*git -c diff.external*": deny
    "git.exe -c diff.external*": deny
    "*git.exe -c diff.external*": deny
    "git -c sequence.editor*": deny
    "*git -c sequence.editor*": deny
    "git.exe -c sequence.editor*": deny
    "*git.exe -c sequence.editor*": deny
    "git -c pager.*": deny
    "*git -c pager.*": deny
    "git.exe -c pager.*": deny
    "*git.exe -c pager.*": deny
    "git --config-env*": deny
    "*git --config-env*": deny
    "& git*": deny
    "& \"git\"*": deny
    "& 'git'*": deny
    "& *git.exe*": deny
    "*; & git*": deny
    "*; & \"git\"*": deny
    "*; & 'git'*": deny
    "*; & *git.exe*": deny
    "*| & git*": deny
    "*| & \"git\"*": deny
    "*| & 'git'*": deny
    "*| & *git.exe*": deny
    "*|| & git*": deny
    "*|| & \"git\"*": deny
    "*|| & 'git'*": deny
    "*|| & *git.exe*": deny
    "*&& & git*": deny
    "*&& & \"git\"*": deny
    "*&& & 'git'*": deny
    "*&& & *git.exe*": deny
    "*( & git*": deny
    "*( & \"git\"*": deny
    "*( & 'git'*": deny
    "*( & *git.exe*": deny
    "*{ & git*": deny
    "*{ & \"git\"*": deny
    "*{ & 'git'*": deny
    "*{ & *git.exe*": deny
    "*\n& git*": deny
    "*\n& \"git\"*": deny
    "*\n& 'git'*": deny
    "*\n& *git.exe*": deny
    "git filter-branch*": deny
    "git.exe filter-branch*": deny
    "*git filter-branch*": deny
    "*git.exe filter-branch*": deny
    "git filter-repo*": deny
    "git.exe filter-repo*": deny
    "*git filter-repo*": deny
    "*git.exe filter-repo*": deny
    "git update-ref*": deny
    "git.exe update-ref*": deny
    "*git update-ref*": deny
    "*git.exe update-ref*": deny
    "git reflog expire*": deny
    "git.exe reflog expire*": deny
    "*git reflog expire*": deny
    "*git.exe reflog expire*": deny
    "git reflog delete*": deny
    "git.exe reflog delete*": deny
    "*git reflog delete*": deny
    "*git.exe reflog delete*": deny
    "git gc*": deny
    "git.exe gc*": deny
    "*git gc*": deny
    "*git.exe gc*": deny
    "git prune*": deny
    "git.exe prune*": deny
    "*git prune*": deny
    "*git.exe prune*": deny
    "git replace*": deny
    "git.exe replace*": deny
    "*git replace*": deny
    "*git.exe replace*": deny
    "git notes add*": deny
    "git.exe notes add*": deny
    "*git notes add*": deny
    "*git.exe notes add*": deny
    "git notes remove*": deny
    "git.exe notes remove*": deny
    "*git notes remove*": deny
    "*git.exe notes remove*": deny
    "git submodule update*": deny
    "git.exe submodule update*": deny
    "*git submodule update*": deny
    "*git.exe submodule update*": deny
    "git submodule add*": deny
    "git.exe submodule add*": deny
    "*git submodule add*": deny
    "*git.exe submodule add*": deny
    "git sparse-checkout*": deny
    "git.exe sparse-checkout*": deny
    "*git sparse-checkout*": deny
    "*git.exe sparse-checkout*": deny
    "git bisect*": deny
    "git.exe bisect*": deny
    "*git bisect*": deny
    "*git.exe bisect*": deny
    "git maintenance*": deny
    "git.exe maintenance*": deny
    "*git maintenance*": deny
    "*git.exe maintenance*": deny
    "git\t*": deny
    "*git\t*": deny
    "git.exe\t*": deny
    "*git.exe\t*": deny
    "git  *": deny
    "*git  *": deny
    "git.exe  *": deny
    "*git.exe  *": deny
    "*--no-verify*": deny
    "rm -rf /": deny
    "rm -rf *": deny
    "rm -fr /": deny
    "rm -fr *": deny
    "rm -r -f *": deny
    "rm -f -r *": deny
    "rm -rf .*": deny
    "rm -r /": deny
    "rm -R /": deny
    "rm -r .": deny
    "rm -rf .": deny
    "rm --recursive --force*": deny
    "Remove-Item*-Recurse*-Force*": deny
    "Remove-Item*-r*-fo*": deny
    "rmdir /s*": deny
    "del /q /s*": deny
    "del /s /q*": deny
    "find . -delete*": deny
    "find * -delete*": deny
    "python -c *": deny
    "python.exe -c *": deny
    "python3 -c *": deny
    "py -c *": deny
    "py.exe -c *": deny
    "powershell* -c *": deny
    "powershell* -Command *": deny
    "powershell* -command *": deny
    "pwsh* -c *": deny
    "pwsh* -Command *": deny
    "pwsh* -command *": deny
    "bash -c *": deny
    "bash.exe -c *": deny
    "sh -c *": deny
    "sh.exe -c *": deny
    "zsh -c *": deny
    "zsh.exe -c *": deny
    "node -e *": deny
    "node.exe -e *": deny
    "node --eval *": deny
    "node.exe --eval *": deny
    "ruby -e *": deny
    "ruby.exe -e *": deny
    "perl -e *": deny
    "perl.exe -e *": deny
    "cmd /c git *": deny
    "cmd.exe /c git *": deny
    "*&&*rm *": deny
    "*;*rm *": deny
    "*|*rm *": deny
    "*&&*Remove-Item*": deny
    "*;*Remove-Item*": deny
    "*&&*del *": deny
    "*;*del *": deny
    "*search_grant*": deny
    "*Start-Process*git*": deny
    "*saps *git*": deny
    "*Invoke-Command*git*": deny
    "start git*": deny
    "start /b git*": deny
    "start /min git*": deny
    "cmd /c \"git*": deny
    "cmd.exe /c \"git*": deny
    "cmd /c *git*": deny
    "cmd.exe /c *git*": deny
    "cmd /k *git*": deny
    "g`it*": deny
    "gi`t*": deny
    "g`i`t*": deny
    "*g`it *": deny
    "*gi`t *": deny
    "*g`i`t *": deny
    "gh pr merge*": deny
    "*gh pr merge*": deny
    "gh.exe pr merge*": deny
    "*gh.exe pr merge*": deny
    "gh pr close*": deny
    "*gh pr close*": deny
    "gh.exe pr close*": deny
    "*gh.exe pr close*": deny
    "gh pr reopen*": deny
    "*gh pr reopen*": deny
    "gh.exe pr reopen*": deny
    "*gh.exe pr reopen*": deny
    "gh pr review*": deny
    "*gh pr review*": deny
    "gh.exe pr review*": deny
    "*gh.exe pr review*": deny
    "gh pr edit*": deny
    "*gh pr edit*": deny
    "gh.exe pr edit*": deny
    "*gh.exe pr edit*": deny
    "gh pr ready*": deny
    "*gh pr ready*": deny
    "gh.exe pr ready*": deny
    "*gh.exe pr ready*": deny
    "gh pr comment*": deny
    "*gh pr comment*": deny
    "gh.exe pr comment*": deny
    "*gh.exe pr comment*": deny
    "gh pr create*": deny
    "*gh pr create*": deny
    "gh.exe pr create*": deny
    "*gh.exe pr create*": deny
    "gh issue create*": deny
    "*gh issue create*": deny
    "gh.exe issue create*": deny
    "*gh.exe issue create*": deny
    "gh issue close*": deny
    "*gh issue close*": deny
    "gh.exe issue close*": deny
    "*gh.exe issue close*": deny
    "gh issue reopen*": deny
    "*gh issue reopen*": deny
    "gh.exe issue reopen*": deny
    "*gh.exe issue reopen*": deny
    "gh issue delete*": deny
    "*gh issue delete*": deny
    "gh.exe issue delete*": deny
    "*gh.exe issue delete*": deny
    "gh issue edit*": deny
    "*gh issue edit*": deny
    "gh.exe issue edit*": deny
    "*gh.exe issue edit*": deny
    "gh issue comment*": deny
    "*gh issue comment*": deny
    "gh.exe issue comment*": deny
    "*gh.exe issue comment*": deny
    "gh issue transfer*": deny
    "*gh issue transfer*": deny
    "gh.exe issue transfer*": deny
    "*gh.exe issue transfer*": deny
    "gh issue lock*": deny
    "*gh issue lock*": deny
    "gh.exe issue lock*": deny
    "*gh.exe issue lock*": deny
    "gh repo create*": deny
    "*gh repo create*": deny
    "gh.exe repo create*": deny
    "*gh.exe repo create*": deny
    "gh repo delete*": deny
    "*gh repo delete*": deny
    "gh.exe repo delete*": deny
    "*gh.exe repo delete*": deny
    "gh repo edit*": deny
    "*gh repo edit*": deny
    "gh.exe repo edit*": deny
    "*gh.exe repo edit*": deny
    "gh repo archive*": deny
    "*gh repo archive*": deny
    "gh.exe repo archive*": deny
    "*gh.exe repo archive*": deny
    "gh repo rename*": deny
    "*gh repo rename*": deny
    "gh.exe repo rename*": deny
    "*gh.exe repo rename*": deny
    "gh repo transfer*": deny
    "*gh repo transfer*": deny
    "gh.exe repo transfer*": deny
    "*gh.exe repo transfer*": deny
    "gh repo fork*": deny
    "*gh repo fork*": deny
    "gh.exe repo fork*": deny
    "*gh.exe repo fork*": deny
    "gh repo sync*": deny
    "*gh repo sync*": deny
    "gh.exe repo sync*": deny
    "*gh.exe repo sync*": deny
    "gh release create*": deny
    "*gh release create*": deny
    "gh.exe release create*": deny
    "*gh.exe release create*": deny
    "gh release delete*": deny
    "*gh release delete*": deny
    "gh.exe release delete*": deny
    "*gh.exe release delete*": deny
    "gh release edit*": deny
    "*gh release edit*": deny
    "gh.exe release edit*": deny
    "*gh.exe release edit*": deny
    "gh release upload*": deny
    "*gh release upload*": deny
    "gh.exe release upload*": deny
    "*gh.exe release upload*": deny
    "gh secret*": deny
    "*gh secret*": deny
    "gh.exe secret*": deny
    "*gh.exe secret*": deny
    "gh variable set*": deny
    "*gh variable set*": deny
    "gh.exe variable set*": deny
    "*gh.exe variable set*": deny
    "gh variable delete*": deny
    "*gh variable delete*": deny
    "gh.exe variable delete*": deny
    "*gh.exe variable delete*": deny
    "gh workflow run*": deny
    "*gh workflow run*": deny
    "gh.exe workflow run*": deny
    "*gh.exe workflow run*": deny
    "gh workflow enable*": deny
    "*gh workflow enable*": deny
    "gh.exe workflow enable*": deny
    "*gh.exe workflow enable*": deny
    "gh workflow disable*": deny
    "*gh workflow disable*": deny
    "gh.exe workflow disable*": deny
    "*gh.exe workflow disable*": deny
    "gh run rerun*": deny
    "*gh run rerun*": deny
    "gh.exe run rerun*": deny
    "*gh.exe run rerun*": deny
    "gh run cancel*": deny
    "*gh run cancel*": deny
    "gh.exe run cancel*": deny
    "*gh.exe run cancel*": deny
    "gh run delete*": deny
    "*gh run delete*": deny
    "gh.exe run delete*": deny
    "*gh.exe run delete*": deny
    "gh label create*": deny
    "*gh label create*": deny
    "gh.exe label create*": deny
    "*gh.exe label create*": deny
    "gh label delete*": deny
    "*gh label delete*": deny
    "gh.exe label delete*": deny
    "*gh.exe label delete*": deny
    "gh label edit*": deny
    "*gh label edit*": deny
    "gh.exe label edit*": deny
    "*gh.exe label edit*": deny
    "gh auth*": deny
    "*gh auth*": deny
    "gh.exe auth*": deny
    "*gh.exe auth*": deny
    "gh ssh-key*": deny
    "*gh ssh-key*": deny
    "gh.exe ssh-key*": deny
    "*gh.exe ssh-key*": deny
    "gh gpg-key*": deny
    "*gh gpg-key*": deny
    "gh.exe gpg-key*": deny
    "*gh.exe gpg-key*": deny
    "gh api*-X *": deny
    "*gh api*-X *": deny
    "gh.exe api*-X *": deny
    "*gh.exe api*-X *": deny
    "gh api*--method*": deny
    "*gh api*--method*": deny
    "gh.exe api*--method*": deny
    "*gh.exe api*--method*": deny
    "gh api*-f *": deny
    "*gh api*-f *": deny
    "gh.exe api*-f *": deny
    "*gh.exe api*-f *": deny
    "gh api*-F *": deny
    "*gh api*-F *": deny
    "gh.exe api*-F *": deny
    "*gh.exe api*-F *": deny
    "gh api*--field*": deny
    "*gh api*--field*": deny
    "gh.exe api*--field*": deny
    "*gh.exe api*--field*": deny
    "gh api*--raw-field*": deny
    "*gh api*--raw-field*": deny
    "gh.exe api*--raw-field*": deny
    "*gh.exe api*--raw-field*": deny
    "gh api*--input*": deny
    "*gh api*--input*": deny
    "gh.exe api*--input*": deny
    "*gh.exe api*--input*": deny
    "*| sh": deny
    "*| sh *": deny
    "*|sh": deny
    "*|sh *": deny
    "*| bash": deny
    "*| bash *": deny
    "*|bash": deny
    "*|bash *": deny
    "*| zsh": deny
    "*| zsh *": deny
    "*|zsh": deny
    "*|zsh *": deny
    "*| iex*": deny
    "*|iex*": deny
    "*| Invoke-Expression*": deny
    "*|Invoke-Expression*": deny
    "iex *": deny
    "iex(*": deny
    "*; iex *": deny
    "*(iex *": deny
    "*Invoke-Expression*": deny
    "*DownloadString(*": deny
    "*<(curl*": deny
    "*<(wget*": deny
    "*<(iwr*": deny
    "*scripts/gemini-research*": deny
    "git branch --list*": allow
    "git branch -a*": allow
    "git branch -v*": allow
    "git branch --show-current*": allow
    "git worktree list*": allow
    "git tag -l*": allow
    "git tag --list*": allow
    "git stash list*": allow
    "git config --get*": allow
    "git config --list*": allow
  webfetch: deny
  websearch: deny
  codesearch: deny
---
<!-- GENERATED by scripts/sync-adapters.ps1 from agents/roles/devops.md. Do not edit. -->

# DevOps

## Mục tiêu
Để mọi thay đổi được kiểm tra tự động và phát hành lặp lại được, có đường quay lui rõ ràng.

## Kỹ năng & Cẩm nang áp dụng (Skills Applied)
- **`ship`** (`.agents/skills/ship/SKILL.md`): Quy trình release sản xuất: pre-flight checks, bump version, changelog, PR gate.
- **`careful`** (`.agents/skills/careful/SKILL.md`): Rào chắn an toàn, cảnh báo và dừng lại trước các thao tác shell hủy hoại dữ liệu.
- **`cloud-recipes`** (`agents/knowledge/cloud-recipes.md`): Cẩm nang kiến trúc điện toán đám mây: Least Privilege IAM, Exponential Backoff kèm Full Jitter, Graceful Shutdown cho stateless containers.
- **`cso-security-framework`** (`agents/knowledge/cso-security-framework.md`): Áp dụng chuẩn kiểm toán an ninh CI/CD, cô lập bí mật môi trường (Secrets Scanning), và thiết lập các cổng kiểm tra an toàn tự động.
- **`zero-downtime-migrations`** (`agents/knowledge/zero-downtime-migrations.md`): Tách rời pha chạy database migration khỏi pha rollout container để bảo đảm tính tương thích ngược hai chiều.

## Đầu vào
- Task card, `PROJECT.md` (lệnh build, test, môi trường), file stack.
- Spec và ADR về hạ tầng, nếu có.

## Đầu ra
- Pipeline CI trong `.github/**` (hoặc thư mục tương đương của nền tảng CI): chạy build, test, lint, `scripts/sync-adapters.ps1 -Check` và `scripts/merge-gate.ps1` khi phù hợp.
- Cấu hình đóng gói và môi trường (`Dockerfile`, `docker-compose`, `infra/`, `deploy/`).
- Runbook trong `docs/runbooks/`: cách triển khai, cách quay lại, cách xử lý sự cố thường gặp.
- Trong card: **kịch bản hoàn tác tự động < 60 giây** của mọi thay đổi triển khai.

## Quyền hạn
- Được sửa: `.github/**`, `infra/**`, `deploy/**`, `Dockerfile*`, `docker-compose*`, `docs/runbooks/**`, `tasks/**`, `docs/notes/inbox/**`.
- Được chạy build và lệnh đóng gói cục bộ.

## Điều cấm
- Không deploy hay thay đổi môi trường thật khi chưa có người dùng duyệt rõ ràng cho từng lần.
- Không đặt khóa bí mật, mật khẩu, token vào file cấu hình hay pipeline. Dùng kho bí mật của nền tảng và chỉ ghi tên biến.
- Không sửa `src/`, `agent_core/`, `tests/` và không sửa `.env*`.
- Không tắt kiểm tra (test, lint, merge gate) trong pipeline để cho qua.
- Không dùng `push --force` hay đổi cấu hình bảo vệ nhánh.
- Không tự commit hoặc push khi chưa được người dùng yêu cầu và duyệt từng lệnh (`AGENTS.md` quy tắc 4); vẫn cấm mọi cách né (subshell escapes: `python -c`, `powershell -c`, `bash -c`, `git -c alias.*`). Việc deploy do người dùng chạy lệnh.

## Định nghĩa hoàn thành
- Pipeline chạy xanh trên nhánh thử, thất bại thì báo rõ bước nào.
- Có runbook và kịch bản hoàn tác tự động được chứng minh khả năng revert trong < 60 giây.
- Không có bí mật nào trong file đã sửa; tuân thủ chuẩn Least Privilege.
- Đã ghi ghi chú cho agent sau vào `docs/notes/inbox/` theo `agents/protocols/handoff-note.md` (khi có điều agent sau cần biết; không có thì bỏ qua).
