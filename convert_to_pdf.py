#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts the Team Task Delegation Framework markdown to PDF format.
"""

import os
import sys
from pathlib import Path
import markdown2
import weasyprint
from weasyprint import HTML, CSS
import re


def create_custom_css():
    """Create custom CSS for PDF styling"""
    css_content = """
    @page {
        margin: 1in;
        size: letter;
        @top-center {
            content: "Smart India Hackathon: Autonomous Lunar Habitat Robot";
            font-family: Arial, sans-serif;
            font-size: 10pt;
            color: #333;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-family: Arial, sans-serif;
            font-size: 10pt;
            color: #666;
        }
    }

    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        font-size: 11pt;
        margin: 0;
        padding: 0;
    }

    /* Title and Headers */
    h1 {
        color: #003366;
        font-size: 22pt;
        font-weight: bold;
        text-align: center;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #003366;
        page-break-after: avoid;
    }

    h2 {
        color: #0066cc;
        font-size: 18pt;
        font-weight: bold;
        margin: 25px 0 12px 0;
        page-break-after: avoid;
    }

    h3 {
        color: #336699;
        font-size: 16pt;
        font-weight: bold;
        margin: 20px 0 10px 0;
        page-break-after: avoid;
    }

    h4 {
        color: #4d79a4;
        font-size: 14pt;
        font-weight: bold;
        margin: 15px 0 8px 0;
        page-break-after: avoid;
    }

    h5 {
        color: #666699;
        font-size: 13pt;
        font-weight: bold;
        margin: 12px 0 6px 0;
        page-break-after: avoid;
    }

    h6 {
        color: #808080;
        font-size: 12pt;
        font-weight: bold;
        margin: 10px 0 5px 0;
        page-break-after: avoid;
    }

    /* Paragraphs */
    p {
        margin: 8px 0;
        text-align: justify;
        orphans: 2;
        widows: 2;
    }

    /* Lists */
    ul, ol {
        margin: 10px 0;
        padding-left: 25px;
    }

    li {
        margin: 4px 0;
        page-break-inside: avoid;
    }

    ul li {
        list-style-type: disc;
    }

    ul ul li {
        list-style-type: circle;
    }

    ul ul ul li {
        list-style-type: square;
    }

    /* Emphasis */
    strong, b {
        font-weight: bold;
        color: #003366;
    }

    em, i {
        font-style: italic;
        color: #336699;
    }

    /* Code formatting */
    code {
        font-family: 'Courier New', monospace;
        background-color: #f5f5f5;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 10pt;
        border: 1px solid #ddd;
    }

    pre {
        font-family: 'Courier New', monospace;
        background-color: #f8f8f8;
        padding: 12px;
        border-radius: 5px;
        border: 1px solid #ddd;
        overflow-x: auto;
        font-size: 10pt;
        margin: 12px 0;
        page-break-inside: avoid;
    }

    /* Tables */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    th {
        background-color: #f2f2f2;
        font-weight: bold;
        color: #003366;
    }

    /* Special sections */
    .team-member {
        background-color: #f0f8ff;
        border-left: 4px solid #0066cc;
        padding: 12px;
        margin: 10px 0;
        page-break-inside: avoid;
    }

    .phase-header {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0 15px 0;
        border: 1px solid #b3d9ff;
        page-break-inside: avoid;
    }

    .week-section {
        margin: 15px 0;
        padding: 10px;
        border-left: 3px solid #ccc;
        page-break-inside: avoid;
    }

    /* Page breaks */
    .page-break {
        page-break-before: always;
    }

    .no-break {
        page-break-inside: avoid;
    }

    /* Links */
    a {
        color: #0066cc;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    /* Blockquotes */
    blockquote {
        border-left: 4px solid #0066cc;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #f9f9f9;
        font-style: italic;
    }

    /* Horizontal rules */
    hr {
        border: none;
        height: 2px;
        background-color: #ddd;
        margin: 25px 0;
    }

    /* Footer styling */
    .footer {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 2px solid #003366;
        text-align: center;
        font-style: italic;
        color: #666;
    }
    """
    return css_content


def preprocess_markdown(content):
    """Preprocess markdown content for better PDF conversion"""

    # Add CSS classes to team member sections
    content = re.sub(r'#### \*\*(.*?)\*\*\n', r'<div class="team-member"><h4><strong>\1</strong></h4>', content)

    # Add CSS classes to phase headers
    content = re.sub(r'## (Phase \d+:.*?)\n', r'<div class="phase-header"><h2>\1</h2></div>', content)

    # Add CSS classes to week sections
    content = re.sub(r'### (Week.*?)\n', r'<div class="week-section"><h3>\1</h3>', content)

    # Close team member divs (simple heuristic)
    lines = content.split('\n')
    result_lines = []
    in_team_member = False

    for i, line in enumerate(lines):
        if '<div class="team-member">' in line:
            if in_team_member:
                result_lines.append('</div>')
            result_lines.append(line)
            in_team_member = True
        elif line.startswith('#### **') and in_team_member:
            result_lines.append('</div>')
            result_lines.append(line)
        elif line.startswith('###') or line.startswith('##') or line.startswith('#'):
            if in_team_member:
                result_lines.append('</div>')
                in_team_member = False
            result_lines.append(line)
        else:
            result_lines.append(line)

    if in_team_member:
        result_lines.append('</div>')

    return '\n'.join(result_lines)


def convert_markdown_to_pdf(input_file, output_file):
    """Convert markdown file to PDF format"""
    try:
        # Read markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Preprocess markdown
        content = preprocess_markdown(content)

        # Convert markdown to HTML
        html_content = markdown2.markdown(
            content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'cuddled-lists',
                'metadata',
                'toc'
            ]
        )

        # Wrap in full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Smart India Hackathon: Autonomous Lunar Habitat Robot - Team Task Delegation Framework</title>
        </head>
        <body>
            {html_content}
            <div class="footer">
                <p>Generated on {Path(input_file).stat().st_mtime} | Team Task Delegation Framework</p>
            </div>
        </body>
        </html>
        """

        # Create CSS
        css_content = create_custom_css()

        # Convert to PDF
        html_doc = HTML(string=full_html)
        css_doc = CSS(string=css_content)

        html_doc.write_pdf(output_file, stylesheets=[css_doc])

        print(f"✅ Successfully converted {input_file} to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error converting to PDF: {str(e)}")
        return False


def main():
    """Main function"""
    # Set file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / "Team_Task_Delegation_Framework.md"
    output_file = script_dir / "Team_Task_Delegation_Framework.pdf"

    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        print("Available files:")
        for file in script_dir.glob("*.md"):
            print(f"  - {file.name}")
        return False

    print(f"🚀 Converting {input_file.name} to PDF format...")
    print(f"📁 Input: {input_file}")
    print(f"📄 Output: {output_file}")

    success = convert_markdown_to_pdf(input_file, output_file)

    if success:
        print(f"\n🎉 Conversion completed successfully!")
        print(f"📋 PDF file created: {output_file}")
        try:
            print(f"📊 File size: {output_file.stat().st_size / 1024:.1f} KB")
        except:
            print("📊 File size: Unable to determine")
    else:
        print(f"\n💥 Conversion failed!")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
