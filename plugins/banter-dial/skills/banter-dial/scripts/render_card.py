#!/usr/bin/env python3
"""Render a validated Banter Card as a branded SVG share image."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import sys
import textwrap
import tomllib
from typing import Any

from validate_card import CardValidationError, load_and_validate


ACCENTS = {
    "grounded": "#F7F8FA",
    "weird": "#4DD7FF",
    "unhinged": "#C7FF4A",
}
DIALS = (
    ("WARMTH", "warmth"),
    ("WIT", "wit"),
    ("BLUNTNESS", "bluntness"),
    ("ENERGY", "energy"),
    ("BREVITY", "brevity"),
)


def _description_lines(description: str) -> list[str]:
    lines = textwrap.wrap(description, width=58, break_long_words=False)
    return lines[:3] or [""]


def render_card_svg(card: dict[str, Any]) -> str:
    accent = ACCENTS[card["weirdness"]]
    name = escape(card["name"])
    weirdness = escape(card["weirdness"].upper())
    description = [escape(line) for line in _description_lines(card["description"])]

    description_svg = "\n".join(
        f'    <text x="82" y="{258 + index * 34}" class="description">{line}</text>'
        for index, line in enumerate(description)
    )

    dial_rows: list[str] = []
    for index, (label, field) in enumerate(DIALS):
        y = 398 + index * 44
        value = card[field]
        active_width = value * 48
        dial_rows.append(
            f'''    <text x="82" y="{y + 8}" class="dial-label">{label}</text>
    <rect x="258" y="{y - 10}" width="240" height="12" rx="6" fill="#303641"/>
    <rect x="258" y="{y - 10}" width="{active_width}" height="12" rx="6" fill="{accent}"/>
    <text x="522" y="{y + 8}" class="dial-value">{value}/5</text>'''
        )

    dials_svg = "\n".join(dial_rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-label="Banter Card: {name}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B0D11"/>
      <stop offset="1" stop-color="#171B22"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .ui {{ font-family: "Segoe UI", Arial, sans-serif; }}
      .description {{ font: 24px "Segoe UI", Arial, sans-serif; fill: #A8AFBB; }}
      .dial-label {{ font: 700 17px "Segoe UI", Arial, sans-serif; fill: #858E9C; letter-spacing: 2px; }}
      .dial-value {{ font: 700 17px "Segoe UI", Arial, sans-serif; fill: #D9DDE4; }}
    </style>
  </defs>
  <rect width="1200" height="675" fill="url(#bg)"/>
  <circle cx="1120" cy="70" r="260" fill="{accent}" opacity="0.035"/>
  <rect x="38" y="34" width="1124" height="607" rx="36" fill="#151920" stroke="#343A45" stroke-width="2"/>
  <rect x="82" y="72" width="178" height="42" rx="21" fill="#252B34"/>
  <text x="171" y="100" text-anchor="middle" class="ui" fill="#C4CAD3" font-size="18" font-weight="700" letter-spacing="2">BANTER CARD</text>
  <rect x="916" y="72" width="188" height="42" rx="21" fill="{accent}" opacity="0.16"/>
  <text x="1010" y="100" text-anchor="middle" class="ui" fill="{accent}" font-size="18" font-weight="750" letter-spacing="2">{weirdness}</text>
  <text x="82" y="199" class="ui" fill="#F7F8FA" font-size="58" font-weight="750" letter-spacing="-2">{name}</text>
{description_svg}
  <line x1="620" y1="170" x2="620" y2="562" stroke="#2B313B" stroke-width="2"/>
{dials_svg}
  <g transform="translate(840 330)">
    <circle cx="0" cy="0" r="126" fill="#191D24" stroke="#343A45" stroke-width="25"/>
    <path d="M-106 50 A126 126 0 0 1 103 -81" fill="none" stroke="{accent}" stroke-width="25" stroke-linecap="round"/>
    <path d="M0 0 L96 -83" stroke="#4DD7FF" stroke-width="27" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="38" fill="#F7F8FA"/>
    <circle cx="0" cy="0" r="17" fill="#111318"/>
    <circle cx="-113" cy="54" r="13" fill="#6F7785"/>
    <circle cx="0" cy="-139" r="13" fill="#6F7785"/>
    <circle cx="111" cy="-95" r="15" fill="{accent}" filter="url(#glow)"/>
  </g>
  <text x="840" y="530" text-anchor="middle" class="ui" fill="#F7F8FA" font-size="32" font-weight="750">BanterDial</text>
  <text x="840" y="566" text-anchor="middle" class="ui" fill="#858E9C" font-size="18" font-weight="600" letter-spacing="2">SAME AGENT. DIFFERENT VIBE.</text>
  <text x="82" y="604" class="ui" fill="{accent}" font-size="19" font-weight="700">Turn down the corporate. Turn up the weird.</text>
</svg>
'''


def default_output_path(card_path: Path) -> Path:
    return card_path.with_suffix(".svg")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path, help="validated .banter.toml file")
    parser.add_argument("--output", "-o", type=Path, help="output SVG path")
    parser.add_argument("--force", action="store_true", help="overwrite output if it exists")
    args = parser.parse_args()

    output = args.output or default_output_path(args.card)
    if output.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {output}", file=sys.stderr)
        return 2

    try:
        card = load_and_validate(args.card)
    except (OSError, tomllib.TOMLDecodeError, CardValidationError) as error:
        print(f"Cannot render card: {error}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_card_svg(card), encoding="utf-8")
    print(f"Rendered: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
