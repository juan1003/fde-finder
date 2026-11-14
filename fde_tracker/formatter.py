import sys
from datetime import datetime
from typing import List
from .models import FDERole

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def colorize(text: str, color_code: str, enable_color: bool = True) -> str:
    if not enable_color or not sys.stdout.isatty():
        return text
    return f"{color_code}{text}{Colors.RESET}"

def print_banner(enable_color: bool = True) -> None:
    now_str = datetime.now().strftime("%B %Y")
    title = "TOP FORWARD DEPLOYED ENGINEER (FDE) ROLES HIRING THIS MONTH"
    subtitle = f"Curated High-Impact Roles at Frontier AI Labs & Enterprise Tech ({now_str})"
    print()
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(colorize(f"  {title}", Colors.BOLD + Colors.GREEN, enable_color))
    print(colorize(f"  {subtitle}", Colors.DIM, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print()

def print_table(roles: List[FDERole], enable_color: bool = True) -> None:
    if not roles:
        print(colorize("  No roles matched your search criteria.", Colors.YELLOW, enable_color))
        print()
        return

    for r in roles:
        role_id = f"[{r.id}]"
        comp_tag = colorize(r.comp_range, Colors.YELLOW, enable_color)
        company_tag = colorize(r.company.upper(), Colors.BOLD + Colors.CYAN, enable_color)
        remote_tag = (
            colorize("[Remote OK]", Colors.GREEN, enable_color)
            if r.remote_friendly
            else colorize("[On-Site/Hybrid]", Colors.DIM, enable_color)
        )

        print(f" {colorize(role_id, Colors.BOLD, enable_color)} {company_tag} - {colorize(r.title, Colors.BOLD, enable_color)}")
        print(f"     Category : {colorize(r.category, Colors.BLUE, enable_color)} | {remote_tag}")
        print(f"     Location : {r.location}")
        print(f"     Est Comp : {comp_tag}")
        print(f"     Tech     : {', '.join(r.tech_stack)}")
        print(f"     Focus    : {r.summary}")
        print(f"     Apply    : {colorize(r.url, Colors.UNDERLINE + Colors.BLUE, enable_color)}")
        print(colorize("  " + "-" * 76, Colors.DIM, enable_color))
    print()
    print(colorize(f"  Total Roles Listed: {len(roles)} | Use '--detail <id>' to inspect full requirements.", Colors.DIM, enable_color))
    print()

def print_detail(role: FDERole, enable_color: bool = True) -> None:
    print()
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(colorize(f" ROLE DEEP DIVE: #{role.id} {role.company} - {role.title}", Colors.BOLD + Colors.GREEN, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(f" Company     : {colorize(role.company, Colors.BOLD + Colors.CYAN, enable_color)}")
    print(f" Title       : {role.title}")
    print(f" Department  : {role.department}")
    print(f" Category    : {role.category}")
    print(f" Location    : {role.location} ({'Remote-Friendly' if role.remote_friendly else 'Office/Hybrid Hub'})")
    print(f" Comp Range  : {colorize(role.comp_range, Colors.BOLD + Colors.YELLOW, enable_color)}")
    print(f" Hiring Status: {colorize(role.posted_period, Colors.GREEN, enable_color)}")
    print()
    print(colorize(" Mission & Scope:", Colors.BOLD, enable_color))
    print(f"   {role.summary}")
    print()
    print(colorize(" Core Technologies & Stack:", Colors.BOLD, enable_color))
    for t in role.tech_stack:
        print(f"   * {t}")
    print()
    print(colorize(" Why FDEs Excel Here:", Colors.BOLD, enable_color))
    print("   * High executive visibility and direct client architectural impact.")
    print("   * Hybrid role: ~70% hands-on software development, ~30% technical strategy.")
    print("   * Direct feedback loop to core platform and model research teams.")
    print()
    print(colorize(f" Apply Online: {role.url}", Colors.UNDERLINE + Colors.BLUE, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print()
