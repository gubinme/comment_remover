import os
import re
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Programming languages configuration
LANGUAGE_CONFIG = {
    '.py': {
        'name': 'Python',
        'single_line': ['#'],
        'multi_line': [('"""', '"""'), ("'''", "'''")]
    },
    '.js': {
        'name': 'JavaScript',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.jsx': {
        'name': 'JavaScript JSX',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.ts': {
        'name': 'TypeScript',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.tsx': {
        'name': 'TypeScript TSX',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.java': {
        'name': 'Java',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.c': {
        'name': 'C',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.cpp': {
        'name': 'C++',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.cs': {
        'name': 'C#',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.css': {
        'name': 'CSS',
        'single_line': [],
        'multi_line': [('/*', '*/')]
    },
    '.html': {
        'name': 'HTML',
        'single_line': ['//'],
        'multi_line': [('<!--', '-->')]
    },
    '.xml': {
        'name': 'XML',
        'single_line': [],
        'multi_line': [('<!--', '-->')]
    },
    '.lua': {
        'name': 'Lua',
        'single_line': ['--'],
        'multi_line': [('--[[', ']]')]
    },
    '.rb': {
        'name': 'Ruby',
        'single_line': ['#'],
        'multi_line': [('=begin', '=end')]
    },
    '.php': {
        'name': 'PHP',
        'single_line': ['//', '#'],
        'multi_line': [('/*', '*/')]
    },
    '.go': {
        'name': 'Go',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.rs': {
        'name': 'Rust',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.swift': {
        'name': 'Swift',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.kt': {
        'name': 'Kotlin',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.sql': {
        'name': 'SQL',
        'single_line': ['--'],
        'multi_line': [('/*', '*/')]
    },
    '.sh': {
        'name': 'Shell',
        'single_line': ['#'],
        'multi_line': []
    },
    '.bat': {
        'name': 'Batch',
        'single_line': ['REM', 'rem', '::'],
        'multi_line': []
    },
    '.r': {
        'name': 'R',
        'single_line': ['#'],
        'multi_line': []
    },
    '.m': {
        'name': 'MATLAB',
        'single_line': ['%'],
        'multi_line': [('%{', '%}')]
    },
    '.scala': {
        'name': 'Scala',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
    '.dart': {
        'name': 'Dart',
        'single_line': ['//'],
        'multi_line': [('/*', '*/')]
    },
}


def detect_language(file_path):
    """Detects programming language by file extension"""
    ext = Path(file_path).suffix.lower()
    return LANGUAGE_CONFIG.get(ext, None)


def is_inside_string(line, pos, quote_char=None):
    """Checks if position is inside a string literal"""
    in_single = False
    in_double = False
    i = 0
    escape = False
    
    while i < pos:
        if escape:
            escape = False
            i += 1
            continue
            
        if line[i] == '\\':
            escape = True
        elif line[i] == '"' and not in_single:
            in_double = not in_double
        elif line[i] == "'" and not in_double:
            in_single = not in_single
        i += 1
    
    return in_single or in_double


def remove_single_line_comment(line, comment_markers, lang_config):
    """Removes single-line comment from a line"""
    original_line = line
    
    # For each comment marker
    for marker in comment_markers:
        pos = 0
        while True:
            pos = line.find(marker, pos)
            if pos == -1:
                break
            
            # Check if not inside a string
            if not is_inside_string(line, pos):
                # Found a comment
                before_comment = line[:pos]
                
                # Remove spaces before comment, but not line breaks
                before_comment = before_comment.rstrip(' \t')
                
                # If line before comment is empty - remove entire line
                if not before_comment.strip():
                    return ''
                else:
                    # Keep code before comment with newline
                    return before_comment + '\n'
            pos += 1
    
    return original_line


def remove_comments(content, lang_config):
    """Removes all comments from file content"""
    if not lang_config:
        return content
    
    lines = content.split('\n')
    result_lines = []
    in_multi_line_comment = False
    multi_line_end = None
    
    for line in lines:
        original_line = line
        
        # Check multi-line comments
        if lang_config['multi_line']:
            for start_marker, end_marker in lang_config['multi_line']:
                # If already in multi-line comment
                if in_multi_line_comment:
                    end_pos = line.find(multi_line_end)
                    if end_pos != -1:
                        # End of multi-line comment
                        after_comment = line[end_pos + len(multi_line_end):]
                        in_multi_line_comment = False
                        multi_line_end = None
                        
                        # If there is code after comment
                        if after_comment.strip():
                            line = after_comment
                            # Continue processing this line
                        else:
                            line = ''
                            break
                    else:
                        # Still in comment
                        line = ''
                        break
                
                # Check for start of multi-line comment
                if not in_multi_line_comment:
                    start_pos = 0
                    while True:
                        start_pos = line.find(start_marker, start_pos)
                        if start_pos == -1:
                            break
                        
                        if not is_inside_string(line, start_pos):
                            # Found start of multi-line comment
                            before_comment = line[:start_pos].rstrip(' \t')
                            
                            # Look for end on the same line
                            end_pos = line.find(end_marker, start_pos + len(start_marker))
                            if end_pos != -1:
                                # Comment starts and ends on same line
                                after_comment = line[end_pos + len(end_marker):]
                                
                                if before_comment.strip():
                                    # There is code before comment
                                    if after_comment.strip():
                                        # There is code after comment
                                        line = before_comment + ' ' + after_comment.lstrip()
                                    else:
                                        line = before_comment
                                else:
                                    # No code before comment
                                    if after_comment.strip():
                                        line = after_comment.lstrip()
                                    else:
                                        line = ''
                                start_pos = 0
                                continue
                            else:
                                # Multi-line comment continues
                                in_multi_line_comment = True
                                multi_line_end = end_marker
                                
                                if before_comment.strip():
                                    line = before_comment
                                else:
                                    line = ''
                                break
                        start_pos += 1
        
        # Remove single-line comments (if not in multi-line)
        if not in_multi_line_comment and lang_config['single_line'] and line:
            line = remove_single_line_comment(line, lang_config['single_line'], lang_config)
        
        # Add line based on logic:
        # If original line was empty - keep it empty
        # If line became empty after removing comment - skip it (don't add)
        # Otherwise - add the processed line
        if not original_line.strip():
            # Original line was empty - preserve it
            result_lines.append('')
        elif line:
            # Line has content after processing
            if line.endswith('\n'):
                result_lines.append(line[:-1])
            else:
                result_lines.append(line)
        # If line is empty but original_line had content - it was a comment-only line, skip it
    
    return '\n'.join(result_lines)


def get_all_files(input_dir):
    """Gets list of all files to process"""
    files = []
    for root, dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            lang_config = detect_language(file_path)
            if lang_config:
                files.append(file_path)
    return files


def process_file(input_path, output_path, lang_config):
    """Processes a single file"""
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    cleaned_content = remove_comments(content, lang_config)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)


def main():
    # Banner
    console.print()
    console.print(Panel.fit(
        "[bold cyan]COMMENT REMOVER[/bold cyan]\n"
        "[dim]Remove comments from source code[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()
    
    input_dir = 'input'
    output_dir = 'output'
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of files
    files = get_all_files(input_dir)
    
    if not files:
        console.print("[yellow]Warning:[/yellow] No files found in input folder for processing")
        console.print("[dim]Place code files in input folder and run the program again[/dim]")
        return
    
    console.print(f"[green]Files found for processing:[/green] [bold]{len(files)}[/bold]")
    console.print()
    
    # Table with list of languages
    languages = {}
    for file_path in files:
        lang_config = detect_language(file_path)
        lang_name = lang_config['name'] if lang_config else 'Unknown'
        languages[lang_name] = languages.get(lang_name, 0) + 1
    
    table = Table(title="Detected Languages", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Language", style="cyan")
    table.add_column("Files", justify="right", style="green")
    
    for lang, count in sorted(languages.items()):
        table.add_row(lang, str(count))
    
    console.print(table)
    console.print()
    
    # Processing files with progress
    processed = []
    failed = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.fields[current]}/{task.total}"),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=console,
        expand=True
    ) as progress:
        
        task = progress.add_task(
            "[cyan]Processing files...",
            total=len(files),
            current=0
        )
        
        for idx, file_path in enumerate(files):
            lang_config = detect_language(file_path)
            lang_name = lang_config['name'] if lang_config else 'Unknown'
            
            relative_path = os.path.relpath(file_path, input_dir)
            output_path = os.path.join(output_dir, relative_path)
            
            # Update current file description
            progress.update(
                task,
                description=f"[cyan]Processing:[/cyan] [yellow]{relative_path}[/yellow] [dim]({lang_name})[/dim]"
            )
            
            try:
                process_file(file_path, output_path, lang_config)
                processed.append((relative_path, lang_name))
            except Exception as e:
                failed.append((relative_path, str(e)))
            
            progress.update(task, advance=1, current=idx + 1)
    
    console.print()
    
    # Results
    if processed:
        console.print(Panel.fit(
            f"[bold green]Successfully processed:[/bold green] [bold]{len(processed)}[/bold] files\n"
            f"[dim]Results saved in output folder[/dim]",
            border_style="green",
            box=box.ROUNDED
        ))
    
    if failed:
        console.print()
        console.print(Panel.fit(
            f"[bold red]Processing errors:[/bold red] [bold]{len(failed)}[/bold] files",
            border_style="red",
            box=box.ROUNDED
        ))
        for file_path, error in failed:
            console.print(f"  [red]✗[/red] {file_path}: [dim]{error}[/dim]")
    
    console.print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Critical error:[/bold red] {e}")

