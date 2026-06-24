import tarfile, io, json, time

OUT = "df-hardlink-internal-1.0.0.tgz"
PKG = "df-hardlink-internal"

def add_dir(tar, name):
    info = tarfile.TarInfo(name.rstrip("/") + "/")
    info.type = tarfile.DIRTYPE
    info.mode = 0o755
    info.mtime = int(time.time())
    tar.addfile(info)

def add_file(tar, name, data, mode=0o644):
    b = data.encode()
    info = tarfile.TarInfo(name)
    info.type = tarfile.REGTYPE
    info.size = len(b)
    info.mode = mode
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(b))

def add_hardlink(tar, name, linkname):
    info = tarfile.TarInfo(name)
    info.type = tarfile.LNKTYPE
    info.linkname = linkname
    info.size = 0
    info.mode = 0o644
    info.mtime = int(time.time())
    tar.addfile(info)

pkg_json = {
    "name": PKG,
    "version": "1.0.0",
    "main": "index.js",
    "license": "MIT"
}

with tarfile.open(OUT, "w:gz") as tar:
    add_dir(tar, "package")
    add_file(tar, "package/package.json", json.dumps(pkg_json, indent=2) + "\n")
    add_file(tar, "package/index.js", "module.exports = 1;\n")
    add_file(tar, "package/normal.txt", "NORMAL_HARDLINK_SOURCE\n")

    # two variants because different extractors treat linkname differently
    add_hardlink(tar, "package/internal_pkgprefix", "package/normal.txt")
    add_hardlink(tar, "package/internal_noprefix", "normal.txt")

print(OUT)
