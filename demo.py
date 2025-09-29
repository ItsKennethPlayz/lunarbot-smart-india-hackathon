#!/usr/bin/env python3
"""
Demo script showing different ways to use the Lunarbot Document Converter
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and show results"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 40)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Main demo function"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                    🌙 LUNARBOT DEMO 🌙                         ║
    ║              Document Converter Usage Examples                 ║
    ║                                                                ║
    ║         Showing different ways to convert your markdown        ║
    ║            to professional DOC and PDF formats!               ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

    python_exe = "C:/Users/ayana/Projects/Lunarbot/.venv/Scripts/python.exe"

    # Example 1: Convert to both formats
    run_command(
        [python_exe, "convert_all.py"],
        "Convert to both DOC and PDF formats"
    )

    # Example 2: Convert to DOC only
    run_command(
        [python_exe, "convert_all.py", "--format", "doc"],
        "Convert to DOC format only"
    )

    # Example 3: Convert to PDF only
    run_command(
        [python_exe, "convert_all.py", "--format", "pdf"],
        "Convert to PDF format only"
    )

    # Example 4: Verbose mode
    run_command(
        [python_exe, "convert_all.py", "--verbose"],
        "Convert with verbose output"
    )

    # Example 5: Get help
    run_command(
        [python_exe, "convert_all.py", "--help"],
        "Show help information"
    )

    print(f"\n{'='*60}")
    print("🎉 Demo completed!")
    print("📋 Check the generated files:")

    script_dir = Path(__file__).parent
    for ext in ['.docx', '.pdf']:
        file_path = script_dir / f"Team_Task_Delegation_Framework{ext}"
        if file_path.exists():
            size = file_path.stat().st_size / 1024
            print(f"   ✅ {file_path.name} ({size:.1f} KB)")
        else:
            print(f"   ❌ {file_path.name} (not found)")

    print(f"\n🌙 Ready for lunar mission documentation! 🚀")


if __name__ == "__main__":
    main()
