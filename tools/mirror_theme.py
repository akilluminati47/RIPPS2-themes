"""Draft the other-side (Rx) layout of a theme: every element's x reflected about the screen's centre.

    python3 tools/mirror_theme.py "themes/thm_Adapt" "themes/thm_Adapt Rx" "Adapt Rx"

Copies the folder and rewrites conf_theme.cfg: aligned=1 elements (centred on x) move to 640 - x,
aligned=0 elements (x is the left edge) to 640 - x - width, tilt_x follows, POS_MID stays. Negative x
(counted from the right) is resolved first. It is a draft: text that should stay left-aligned inside a
panel, or art with a direction, may want a hand touch afterwards: run check_theme.py, then look at it in PCSX2 or on a PS2.
"""
import os, re, shutil, sys

W = 640


def mirror_cfg(text):
    out, block = [], []

    def flush():
        if not block:
            return
        kv = {}
        for line in block:
            m = re.match(r"^\s+(\w+)=(.*)$", line)
            if m:
                kv[m.group(1)] = m.group(2).strip()
        aligned = kv.get("aligned", "1") == "1"
        width = kv.get("width", "0")
        for line in block:
            m = re.match(r"^(\s+)(x|tilt_x)=(-?\d+)\s*$", line)
            if m:
                v = int(m.group(3))
                v = W + v if v < 0 else v
                if m.group(2) == "x" and not aligned and width.lstrip("-").isdigit():
                    v = W - v - int(width)
                else:
                    v = W - v
                line = "%s%s=%d" % (m.group(1), m.group(2), v)
            out.append(line)
        block.clear()

    for line in text.splitlines():
        if re.match(r"^[A-Za-z]+\d+:\s*$", line):
            flush()
            out.append(line)
        elif line.startswith(("\t", " ")):
            block.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    src, dst, name = sys.argv[1], sys.argv[2], sys.argv[3]
    if os.path.exists(dst):
        sys.exit("%s exists: pick a new folder" % dst)
    shutil.copytree(src, dst)
    p = os.path.join(dst, "conf_theme.cfg")
    text = mirror_cfg(open(p, encoding="utf-8").read())
    text = re.sub(r"^# Theme Name: .*$", "# Theme Name: " + name, text, count=1, flags=re.M)
    open(p, "w", newline="\n").write(text)
    print("drafted", dst)
