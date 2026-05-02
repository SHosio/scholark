"""Flesch readability diagnostic for prose-tighten skill.

Strips LaTeX commands and never-touch zones (citations, math, code, comments,
captions), then computes Flesch Reading Ease and Flesch-Kincaid Grade Level
using textstat. Outputs JSON.

Usage: python3 flesch.py <path-to-tex>
Exit codes: 0 success, 1 usage/IO error, 2 textstat not installed.
"""

import json
import re
import sys


def strip_latex(text):
    """Strip LaTeX commands and never-touch zones, return plain prose."""
    # Remove line comments (% to end of line) but not escaped \%
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    # Remove display math
    text = re.sub(r'\$\$[\s\S]*?\$\$', '', text)
    text = re.sub(r'\\\[[\s\S]*?\\\]', '', text)
    # Remove inline math
    text = re.sub(r'\$[^$\n]*\$', '', text)
    text = re.sub(r'\\\([\s\S]*?\\\)', '', text)
    # Remove math/code/verbatim environments
    for env in ('equation', 'align', 'eqnarray', 'gather',
                'verbatim', 'lstlisting', 'minted'):
        text = re.sub(
            rf'\\begin\{{{env}\*?\}}[\s\S]*?\\end\{{{env}\*?\}}',
            '', text
        )
    # Remove \verb||
    text = re.sub(r'\\verb\|[^|]*\|', '', text)
    # Remove \caption{...} contents
    text = re.sub(r'\\caption\*?\{[^}]*\}', '', text)
    # Remove citations and refs entirely
    text = re.sub(
        r'\\(cite|citep|citet|autocite|textcite|parencite|ref|autoref|label|cref|Cref)\*?\{[^}]*\}',
        '', text
    )
    # Keep content of formatting wrappers
    text = re.sub(
        r'\\(emph|textbf|textit|underline|textsc|textsf|texttt)\{([^}]*)\}',
        r'\2', text
    )
    # Remove section headers (we want body prose)
    text = re.sub(
        r'\\(section|subsection|subsubsection|paragraph|subparagraph|chapter|part)\*?\{[^}]*\}',
        '', text
    )
    # Remove other \cmd{arg}
    text = re.sub(r'\\\w+\*?\{[^}]*\}', '', text)
    # Replace escaped percent with literal
    text = text.replace(r'\%', '%')
    # Remove standalone commands
    text = re.sub(r'\\\w+\*?', '', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compute(latex_path):
    """Read a .tex file, strip it, compute Flesch metrics."""
    with open(latex_path, 'r', encoding='utf-8') as f:
        latex = f.read()
    plain = strip_latex(latex)
    if not plain:
        return {
            'fre': None,
            'fkgl': None,
            'words': 0,
            'sentences': 0,
            'error': 'No prose found after LaTeX stripping',
        }
    import textstat
    return {
        'fre': round(textstat.flesch_reading_ease(plain), 2),
        'fkgl': round(textstat.flesch_kincaid_grade(plain), 2),
        'words': textstat.lexicon_count(plain),
        'sentences': textstat.sentence_count(plain),
    }


def main(argv):
    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
