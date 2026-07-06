# Private → Public mirror setup

How to keep a **private** repo (everything) and a **public** repo (the same
history, minus one directory — here `_files/`). You work only in the private
repo; one command republishes a filtered mirror to the public repo.

This project is the reference implementation. Use the steps below to recreate it
for any other project.

## How it works

`sync-public.sh` makes a fresh throwaway clone of the private repo, uses
[`git-filter-repo`](https://github.com/newren/git-filter-repo) to delete the
excluded paths from **every commit**, then **force-pushes** the rewritten branch
to the public remote.

Consequences to be aware of:

- **History is preserved** but **rewritten** — public commit SHAs differ from
  private, so every sync is a force-push. Fine for a solo mirror; anyone with an
  old public clone must re-clone.
- Commits that *only* touched excluded paths become empty and are **pruned** from
  the public history.
- The excluded data **never reaches the public remote**, in any commit — verified
  by `git log -p --all | grep`.
- No persistent public clone is needed; the script pushes straight to the URL.

## Prerequisites

- `git`
- [`uv`](https://docs.astral.sh/uv/) — the script runs filter-repo via
  `uvx git-filter-repo`, so nothing needs to be permanently installed.

## One-time setup for a new project

Assume the working copy on disk is the **private** repo and you want to exclude
`_files/`. Replace the two URLs with your repos.

1. **Create both GitHub repos**: `PROJECT-private` (private) and `PROJECT`
   (public). Empty, no README.

2. **Point the working repo's `origin` at the private repo, and make sure there
   is *no* remote pointing at the public repo** (a stray `git push` to a public
   remote would leak the excluded files before they are filtered):

   ```bash
   git remote remove origin 2>/dev/null
   git remote add origin https://github.com/<you>/PROJECT-private.git
   git remote -v          # confirm: only the private URL, for fetch and push
   ```

3. **Copy `sync-public.sh` into the project root** and set its public URL — either
   edit the `PUBLIC_URL` default near the top, or always pass it via the
   environment (step 5). If excluding a directory other than `_files`, also change
   `EXCLUDE_REGEX` (see "Changing what gets excluded" below).

4. **Commit everything (including the excluded dir) and push to private:**

   ```bash
   git add -A
   git commit -m "Set up private repo with public-mirror sync"
   git push -u origin master
   ```

5. **Do the first public sync:**

   ```bash
   ./sync-public.sh
   # or, without editing the script:
   PUBLIC_URL=https://github.com/<you>/PROJECT.git ./sync-public.sh
   ```

That's it. There is no separate public working directory to maintain.

## Daily workflow

```bash
# ...make changes...
git add -A && git commit -m "..."
git push                 # -> private
./sync-public.sh         # -> public (filtered)
```

`sync-public.sh` syncs the committed `HEAD`, so **commit before running it**.

## Changing what gets excluded

The script deletes any path matching `EXCLUDE_REGEX` (a Python regex matched
against each file's full repo path). The default:

```
(?:^|/)_files/
```

matches a directory named exactly `_files` at any depth, and nothing else
(e.g. it will *not* touch `remove_redundant_files.py` or a `profile_files/` dir).

Notes if you customize it:

- Use a **non-capturing** group `(?:^|/)` for the boundary — `git-filter-repo`
  silently ignores a capturing `(^|/)`.
- Override per-run without editing the script:
  `EXCLUDE_REGEX='(?:^|/)(secrets|_files)/' ./sync-public.sh`

## Script configuration (env vars)

| Var             | Default                                   | Meaning                              |
| --------------- | ----------------------------------------- | ------------------------------------ |
| `BRANCH`        | `master`                                  | Branch to mirror.                    |
| `PUBLIC_URL`    | *(edit in script)*                        | Public remote to force-push to.      |
| `EXCLUDE_REGEX` | `(?:^|/)_files/`                          | Paths stripped from public history.  |
| `PUSH_TAGS`     | `0`                                       | Set to `1` to also force-push tags.  |

## Safety checklist

- The private working repo has **no remote** pointing at the public repo.
- After a sync, spot-check the public repo contains no excluded data:
  ```bash
  git clone --quiet <public-url> /tmp/check && \
    git -C /tmp/check log -p --all | grep -c '<something-from-the-excluded-files>'
  # expect: 0
  ```
