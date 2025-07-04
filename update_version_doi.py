python update_version_doi.py --old-version v3.0 --new-version v3.1 --old-doi 10.5281/zenodo.15739561 --new-doi 10.5281/zenodo.99999999
#!/usr/bin/env python3
import os
import argparse
import fnmatch

# --- Utilities to parse .gitignore ---
def load_gitignore(path='.gitignore'):
    ignores = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignores.append(line)
    return ignores

def is_ignored(filepath, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(filepath, pat) or fnmatch.fnmatch(os.path.basename(filepath), pat):
            return True
    return False

# --- Script main ---
def main():
    parser = argparse.ArgumentParser(description="Omega Framework version/DOI updater")
    parser.add_argument('--old-version', required=True)
    parser.add_argument('--new-version', required=True)
    parser.add_argument('--old-doi', required=True)
    parser.add_argument('--new-doi', required=True)
    args = parser.parse_args()

    exts = ['.md', '.tex', '.json', '.yml', '.yaml', '.rst', '.bib']
    gitignore = load_gitignore()
    updated = []

    for root, dirs, files in os.walk('.'):
        for fname in files:
            fpath = os.path.join(root, fname)
            relpath = os.path.relpath(fpath, '.')
            if not any(fname.endswith(ext) for ext in exts):
                continue
            if is_ignored(relpath, gitignore):
                continue
            # Read and update file if needed
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            new_content = content.replace(args.old_version, args.new_version).replace(args.old_doi, args.new_doi)
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated.append(relpath)
    # Print update log
    if updated:
        print("✅ Updated version/DOI in:")
        for u in updated:
            print("  -", u)
    else:
        print("No files updated. Check if version/DOI appears in supported file types.")

if __name__ == '__main__':
    main()
