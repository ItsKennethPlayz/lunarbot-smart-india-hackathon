#!/usr/bin/env python3
"""
Universal Markdown Converter
Converts the Team Task Delegation Framework markdown to multiple formats (DOC, PDF).
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def print_banner():
    """Print a cool banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                   🚀 LUNARBOT CONVERTER 🚀                     ║
    ║              Smart India Hackathon Document Converter         ║
    ║                                                                ║
    ║    Converting Markdown → DOC & PDF like a space-age wizard!   ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def scan_markdown_files(directory):
    """Scan directory for markdown files"""
    markdown_files = []
    directory = Path(directory)

    # Common markdown extensions
    extensions = ['*.md', '*.markdown', '*.mdown', '*.mkd']

    for ext in extensions:
        markdown_files.extend(directory.glob(ext))

    # Sort by name and remove duplicates
    markdown_files = sorted(list(set(markdown_files)), key=lambda x: x.name.lower())

    return markdown_files


def select_file_interactive(script_dir):
    """Interactive file selection"""
    print("\n📁 Scanning for markdown files...")
    markdown_files = scan_markdown_files(script_dir)

    if not markdown_files:
        print("❌ No markdown files found in the current directory!")
        return None

    print(f"\n🔍 Found {len(markdown_files)} markdown file(s):")
    print("═" * 50)

    for i, file in enumerate(markdown_files, 1):
        # Get file size
        try:
            size = file.stat().st_size / 1024
            size_str = f"({size:.1f} KB)"
        except:
            size_str = "(size unknown)"

        # Get modification time
        try:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            time_str = mtime.strftime("%Y-%m-%d %H:%M")
        except:
            time_str = "unknown"

        print(f"  {i:2d}. 📄 {file.name}")
        print(f"      🕒 Modified: {time_str} | 📊 Size: {size_str}")
        if i < len(markdown_files):
            print()

    print("═" * 50)

    while True:
        try:
            print(f"\n🎯 Please select a file to convert (1-{len(markdown_files)}):")
            print("   💡 Tip: Just press Enter to select the first file")
            print("   ❌ Type 'q' or 'quit' to exit")

            choice = input("👉 Your choice: ").strip()

            # Handle quit
            if choice.lower() in ['q', 'quit', 'exit']:
                print("👋 Goodbye! Space missions can wait...")
                return None

            # Handle default (empty input)
            if not choice:
                choice = "1"

            # Convert to number
            file_index = int(choice) - 1

            if 0 <= file_index < len(markdown_files):
                selected_file = markdown_files[file_index]
                print(f"\n✅ Selected: {selected_file.name}")
                return selected_file
            else:
                print(f"❌ Invalid choice! Please enter a number between 1 and {len(markdown_files)}")

        except ValueError:
            print("❌ Invalid input! Please enter a number or 'q' to quit")
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Exiting...")
            return None


def get_format_interactive():
    """Interactive format selection"""
    print("\n📋 Choose output format:")
    print("═" * 30)
    print("  1. 📝 DOC only (Microsoft Word)")
    print("  2. 📄 PDF only (Portable Document)")
    print("  3. 🚀 Both DOC and PDF (recommended!)")
    print("═" * 30)

    while True:
        try:
            choice = input("👉 Your choice (1-3) [default: 3]: ").strip()

            if not choice:
                choice = "3"

            if choice == "1":
                return "doc"
            elif choice == "2":
                return "pdf"
            elif choice == "3":
                return "both"
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Using default format 'both'...")
            return "both"


def convert_to_doc(input_file, output_file):
    """Import and run DOC conversion"""
    try:
        # Import the convert_to_doc module
        import importlib.util

        doc_converter_path = Path(__file__).parent / "convert_to_doc.py"
        spec = importlib.util.spec_from_file_location("convert_to_doc", doc_converter_path)
        if spec is None or spec.loader is None:
            raise ImportError("Could not load convert_to_doc module")

        doc_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doc_module)

        return doc_module.convert_markdown_to_doc(input_file, output_file)
    except Exception as e:
        print(f"❌ Error in DOC conversion: {str(e)}")
        return False


def convert_to_pdf(input_file, output_file):
    """Import and run PDF conversion using reportlab"""
    try:
        # Import the convert_to_pdf_reportlab module
        import importlib.util

        pdf_converter_path = Path(__file__).parent / "convert_to_pdf_reportlab.py"
        spec = importlib.util.spec_from_file_location("convert_to_pdf_reportlab", pdf_converter_path)
        if spec is None or spec.loader is None:
            raise ImportError("Could not load convert_to_pdf_reportlab module")

        pdf_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pdf_module)

        return pdf_module.convert_markdown_to_pdf_reportlab(input_file, output_file)
    except Exception as e:
        print(f"❌ Error in PDF conversion: {str(e)}")
        return False


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Convert markdown files to various formats (DOC, PDF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_all.py                    # Interactive mode - choose file and format
  python convert_all.py --interactive      # Force interactive mode
  python convert_all.py --format doc       # Convert to DOC only (interactive file selection)
  python convert_all.py --input custom.md  # Use specific input file
  python convert_all.py --batch            # Batch mode - convert all markdown files
        """
    )

    parser.add_argument(
        '--input', '-i',
        default=None,
        help='Input markdown file (if not specified, interactive selection will be used)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['doc', 'pdf', 'both'],
        default=None,
        help='Output format (if not specified, interactive selection will be used)'
    )

    parser.add_argument(
        '--output-dir', '-o',
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--interactive', '-int',
        action='store_true',
        help='Force interactive mode (default behavior when no input specified)'
    )

    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Batch mode - convert all markdown files found'
    )

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Set paths
    script_dir = Path(__file__).parent
    output_dir = Path(args.output_dir)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine input file(s)
    input_files = []

    if args.batch:
        # Batch mode - get all markdown files
        print("\n🔄 Batch mode activated - scanning for all markdown files...")
        markdown_files = scan_markdown_files(script_dir)
        if not markdown_files:
            print("❌ No markdown files found in the current directory!")
            return False
        input_files = markdown_files
        selected_format = args.format if args.format else 'both'
        print(f"📋 Found {len(input_files)} files to convert")

    elif args.input:
        # Specific input file provided
        input_file = script_dir / args.input
        if not input_file.exists():
            print(f"❌ Input file not found: {input_file}")
            print("Available markdown files:")
            for file in scan_markdown_files(script_dir):
                print(f"  - {file.name}")
            return False
        input_files = [input_file]
        selected_format = args.format if args.format else get_format_interactive()

    else:
        # Interactive mode (default)
        print("\n🎮 Interactive mode activated!")
        selected_file = select_file_interactive(script_dir)
        if not selected_file:
            return False
        input_files = [selected_file]
        selected_format = args.format if args.format else get_format_interactive()

    print(f"\n📂 Output directory: {output_dir}")
    print(f"🎯 Format(s): {selected_format}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 60)

    # Process each file
    total_success = 0
    total_files = len(input_files)
    all_results = {}

    for file_num, input_file in enumerate(input_files, 1):
        if len(input_files) > 1:
            print(f"\n📄 Processing file {file_num}/{total_files}: {input_file.name}")
            print("-" * 40)

        print(f"📁 Input file: {input_file}")

        # Track results for this file
        results = {}

        # Convert to DOC
        if selected_format in ['doc', 'both']:
            output_file = output_dir / f"{input_file.stem}.docx"
            print(f"\n📝 Converting to DOC format...")
            print(f"   Output: {output_file}")

            success = convert_to_doc(input_file, output_file)
            results['doc'] = {'success': success, 'file': output_file}

            if success and args.verbose:
                try:
                    size = output_file.stat().st_size / 1024
                    print(f"   📊 File size: {size:.1f} KB")
                except:
                    pass

        # Convert to PDF
        if selected_format in ['pdf', 'both']:
            output_file = output_dir / f"{input_file.stem}.pdf"
            print(f"\n📋 Converting to PDF format...")
            print(f"   Output: {output_file}")

            success = convert_to_pdf(input_file, output_file)
            results['pdf'] = {'success': success, 'file': output_file}

            if success and args.verbose:
                try:
                    size = output_file.stat().st_size / 1024
                    print(f"   📊 File size: {size:.1f} KB")
                except:
                    pass

        # Count successes for this file
        file_success_count = sum(1 for result in results.values() if result['success'])
        if file_success_count == len(results):
            total_success += 1

        all_results[input_file.name] = results

        if len(input_files) > 1:
            file_status = "✅ SUCCESS" if file_success_count == len(results) else "❌ PARTIAL/FAILED"
            print(f"   File result: {file_status}")

    # Print final summary
    print("\n" + "═" * 60)
    print("🎯 CONVERSION SUMMARY")
    print("═" * 60)

    for file_name, results in all_results.items():
        if len(input_files) > 1:
            print(f"\n📄 {file_name}:")

        for format_name, result in results.items():
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            print(f"  {format_name.upper()}: {status}")
            if result['success']:
                print(f"       📄 {result['file']}")

    print(f"\n🏆 {total_success}/{total_files} files converted successfully!")

    if total_success == total_files:
        print("🎉 All conversions completed successfully!")
        print("🌙 Ready for lunar mission documentation! 🚀")
    else:
        print("⚠️  Some conversions failed. Check error messages above.")

    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return total_success == total_files


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
