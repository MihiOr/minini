"""Package the saved MiNini v22_65 vehicle source as a BeamNG mod."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parent

def build():
    source = ROOT / "src"
    vehicle = source / "vehicles/Test_v22_449748833469"
    for name in ("main.jbeam", "engine.jbeam", "default.pc", "info.json",
                 "custom_motor_control.lua", "lua/controller/companion_custom_ecu.lua"):
        if not (vehicle / name).is_file():
            raise ValueError("Missing vehicle file: " + name)
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    target = destination / "Test_v22_65.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                relative = path.relative_to(source).as_posix()
                entry = zipfile.ZipInfo(relative, (2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (destination / "SHA256SUMS.txt").write_text(checksum + "  " + target.name + "\n", encoding="utf-8")
    print(target)
    return target

if __name__ == "__main__":
    build()
