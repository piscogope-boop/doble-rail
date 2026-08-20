"""Genera los iconos PNG de la app. Solo stdlib: zlib + struct."""
import zlib, struct

BG = (0x10, 0x13, 0x1A)
LEFT = (0x66, 0xAE, 0xC5)   # raíl del idioma nuevo
RIGHT = (0xCE, 0x8F, 0xA8)  # raíl del idioma intermedio


def rounded_rect(x, y, w, h, r):
    """Devuelve un test(px,py) -> bool para un rectángulo redondeado."""
    x0, y0, x1, y1 = x, y, x + w, y + h

    def inside(px, py):
        if not (x0 <= px < x1 and y0 <= py < y1):
            return False
        cx = min(max(px, x0 + r), x1 - r)
        cy = min(max(py, y0 + r), y1 - r)
        return (px - cx) ** 2 + (py - cy) ** 2 <= r * r

    return inside


def render(size):
    s = size / 512.0
    rail_w = int(96 * s)
    rail_h = int(340 * s)
    top = int(86 * s)
    gap = int(56 * s)
    total = rail_w * 2 + gap
    left_x = (size - total) // 2
    radius = rail_w // 2

    a = rounded_rect(left_x, top, rail_w, rail_h, radius)
    b = rounded_rect(left_x + rail_w + gap, top, rail_w, rail_h, radius)

    rows = []
    for py in range(size):
        row = bytearray([0])  # filtro None
        for px in range(size):
            if a(px, py):
                row += bytes(LEFT)
            elif b(px, py):
                row += bytes(RIGHT)
            else:
                row += bytes(BG)
        rows.append(bytes(row))
    return b"".join(rows)


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path, size):
    raw = render(size)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print(f"{path}  {size}x{size}  {len(png)} bytes")


if __name__ == "__main__":
    write_png("icon-192.png", 192)
    write_png("icon-512.png", 512)
