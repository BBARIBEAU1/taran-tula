#!/usr/bin/env python3
"""Shared shelob-spider signature banner for taran-tula, ara-gog, arac-hne, shelob."""
import os
import sys

SPIDER = r"""
                       .::::..
                        .-11131.
                   ..    ..        ..    ..
         ..     .-3::. ..:-:.....:-:     .:::
         .. ..:.184..:--443333-:..:.       581
        ..   ...::..:::-14511145111-::::...:53:.
               :57:     .:-33377751----1:   .:.
               :993   .14578758778757531:. :781
               .-43:.:5988878988888988873:.-881
              .:.1771399999990975799999907--31.
             --..-344475444579098998877774131-:
    ....  .::::::.:1454443334779897434455341.::
       ...31 .371:----:38998888989888887795:.-4-.-.
          :. .:.-3-:---1574345434787888754-:-111.        ...
             .:154---11-151:11-1334179851.:---:::
             :144-13-:11-31::148971:4731--::-3--:
            .-11:-33- .:---1-17771::11--::::-541:
            -1: .14-.    :374:13--53-:. .-31-34-
           :5-  .11.       34: .-54.    :11-..1-.
           34   :1: .-:    .-. .3-      :11.  .-:
          .4.   -5:                     .--.  .4-
          ::    :3.                     .-:    51
          :      1.                     33     1:
                 .                     -4.     -
                                      .1
                                      :.
"""

# Orange for the dense digits (the spider glow), purple for the faint edges.
_COLORS = {
    "0": (255, 170, 60), "9": (255, 170, 60), "8": (255, 150, 50),
    "7": (250, 130, 50), "5": (240, 110, 60), "4": (225, 95, 70),
    "3": (205, 85, 95), "1": (175, 80, 130), "-": (140, 75, 150),
    ":": (115, 65, 140), ".": (90, 55, 120),
}


def _use_color(stream):
    return stream.isatty() and os.environ.get("NO_COLOR") is None


def print_banner(tool="", tagline="", stream=sys.stderr):
    color = _use_color(stream)
    out = []
    for line in SPIDER.strip("\n").split("\n"):
        if color:
            parts = []
            for c in line:
                rgb = _COLORS.get(c)
                parts.append(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{c}" if rgb else c)
            line = "".join(parts) + "\033[0m"
        out.append(line)
    if tool:
        name = f"  {tool}" + (f"  ·  {tagline}" if tagline else "")
        out.append(f"\033[1;38;2;255;150;50m{name}\033[0m" if color else name)
    print("\n".join(out) + "\n", file=stream)


if __name__ == "__main__":
    print_banner(*(sys.argv[1:3]), stream=sys.stdout)
