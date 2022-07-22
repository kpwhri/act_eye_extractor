import re


DH_PAT = re.compile(
    fr'\b(?:'
    fr'dh|dis[ck]\W*hemo\w*'
    fr')\b',
    re.I
)

