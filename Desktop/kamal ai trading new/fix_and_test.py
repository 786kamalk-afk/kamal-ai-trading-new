# fix_and_test.py
import os, re, sys, subprocess, json, zipfile, traceback, shutil
from pathlib import Path

ROOT = Path.cwd()
REPORT = {"renames": [], "import_updates": [], "import_failures": [], "pytest": None, "errors": []}

def find_py_files(root):
    return [p for p in root.rglob("*.py")]

def detect_duplicate_basenames(py_files):
    from collections import defaultdict
    d = defaultdict(list)
    for p in py_files:
        name = p.name
        if name == "__init__.py": continue
        d[name].append(p)
    return {name: paths for name, paths in d.items() if len(paths) > 1}

def safe_rename_duplicates(dupes):
    # rename each duplicate to folder__name.py and return mapping old_mod -> new_mod
    mapping = {}
    for base, paths in dupes.items():
        for p in paths:
            pkg = p.parent.name or "root"
            new_name = f"{pkg}__{base}"
            new_path = p.with_name(new_name)
            # ensure uniqueness
            i = 1
            while new_path.exists():
                new_path = p.with_name(f"{pkg}__{i}__{base}")
                i += 1
            p.rename(new_path)
            old_mod = str(p.relative_to(ROOT)).replace(os.sep, ".")[:-3]
            new_mod = str(new_path.relative_to(ROOT)).replace(os.sep, ".")[:-3]
            mapping[old_mod] = new_mod
            REPORT["renames"].append({"old": str(p), "new": str(new_path)})
    return mapping

def update_imports(mapping):
    # naive but practical replacements across all .py files
    count_updates = 0
    for py in find_py_files(ROOT):
        txt = py.read_text(encoding="utf-8")
        new_txt = txt
        for old_mod, new_mod in mapping.items():
            # 1) from old_mod import ...  -> from new_mod import ...
            new_txt = re.sub(rf'(^|\n)(\s*from\s+){re.escape(old_mod)}(\s+import\s+)', rf'\1\2{new_mod}\3', new_txt)
            # 2) import old_mod -> import new_mod
            new_txt = re.sub(rf'(^|\n)(\s*import\s+){re.escape(old_mod)}(\s|$|\n)', rf'\1\2{new_mod}\3', new_txt)
            # 3) from package import module  -> if module matches last part, replace it with renamed module basename
            if "." in old_mod:
                pkg, mod = old_mod.rsplit(".", 1)
                new_basename = new_mod.split(".")[-1]
                pattern = rf'(^|\n)(\s*from\s+){re.escape(pkg)}(\s+import\s+)([^\n]+)'
                def repl(m):
                    tail = m.group(4)
                    # replace bare module only where exact word matches
                    new_tail = re.sub(rf'(\b){re.escape(mod)}(\b)', rf'\1{new_basename}\2', tail)
                    return m.group(1) + m.group(2) + pkg + m.group(3) + new_tail
                new_txt = re.sub(pattern, repl, new_txt)
        if new_txt != txt:
            py.write_text(new_txt, encoding="utf-8")
            count_updates += 1
            REPORT["import_updates"].append(str(py))
    return count_updates

def sanity_import_all():
    import importlib.util, traceback
    failures = []
    for py in find_py_files(ROOT):
        if py.name == "__init__.py": continue
        rel = py.relative_to(ROOT)
        modname = ".".join(rel.with_suffix("").parts)
        try:
            spec = importlib.util.spec_from_file_location(modname, str(py))
            if spec and spec.loader:
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
        except Exception as e:
            failures.append({"module": modname, "file": str(py), "error": traceback.format_exc()})
    REPORT["import_failures"] = failures
    return failures

def run_pytest():
    try:
        r = subprocess.run(["pytest", "-q", "--disable-warnings"], cwd=str(ROOT), capture_output=True, text=True, timeout=600)
        REPORT["pytest"] = {"returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}
        return REPORT["pytest"]
    except Exception as e:
        REPORT["pytest"] = {"error": str(e)}
        return REPORT["pytest"]

def make_zip(out_name="kamal_ai_trading_pro_final_fixed.zip"):
    outp = ROOT.parent / out_name
    if outp.exists(): outp.unlink()
    with zipfile.ZipFile(outp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob("*"):
            z.write(p, p.relative_to(ROOT))
    return str(outp)

def main():
    try:
        py_files = find_py_files(ROOT)
        dupes = detect_duplicate_basenames(py_files)
        mapping = {}
        if dupes:
            mapping = safe_rename_duplicates(dupes)
        updates = update_imports(mapping) if mapping else 0
        failures = sanity_import_all()
        pytest_res = run_pytest()
        zip_path = make_zip()
        REPORT["zip"] = zip_path
        REPORT["summary"] = {
            "py_count": len(py_files),
            "dupe_count": len(dupes),
            "import_files_modified": updates,
            "import_failures_count": len(failures),
        }
    except Exception as e:
        REPORT["errors"].append(traceback.format_exc())
    finally:
        (ROOT / "fix_report.json").write_text(json.dumps(REPORT, indent=2), encoding="utf-8")
        print("DONE. Report written to fix_report.json")
        print("ZIP:", REPORT.get("zip"))

if __name__ == "__main__":
    main()
