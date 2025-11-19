'''
This script converts a subset of LaTeX commands to Markdown.
'''
import re

def convert_latex_to_markdown(latex_content):
    # Sections and subsections
    content = re.sub(r'\\section{(.*?)}', r'## \1', latex_content)
    content = re.sub(r'\\subsection{(.*?)}', r'### \1', content)
    content = re.sub(r'\\subsubsection{(.*?)}', r'#### \1', content)

    # Bold and italic
    content = re.sub(r'\\textbf{(.*?)}', r'**\1**', content)
    content = re.sub(r'\\emph{(.*?)}', r'*\1*', content)

    # Lists
    content = re.sub(r'\\begin{enumerate}', '', content)
    content = re.sub(r'\\end{enumerate}', '', content)
    content = re.sub(r'\\begin{itemize}', '', content)
    content = re.sub(r'\\end{itemize}', '', content)
    content = re.sub(r'\\item', r'* ', content)

    # Equations
    content = re.sub(r'\\begin{equation}', r'```', content)
    content = re.sub(r'\\end{equation}', r'```', content)
    content = re.sub(r'\\begin{align}', r'```', content)
    content = re.sub(r'\\end{align}', r'```', content)

    # Code listings
    content = re.sub(r'\\begin{verbatim}', r'```', content)
    content = re.sub(r'\\end{verbatim}', r'```', content)
    content = re.sub(r'\\begin{lstlisting}\\[language=Python,.*?\\]', r'```python', content)
    content = re.sub(r'\\end{lstlisting}', r'```', content)

    # Tables
    content = re.sub(r'\\begin{table\\[h\\]}', '', content)
    content = re.sub(r'\\centering', '', content)
    content = re.sub(r'\\small', '', content)
    content = re.sub(r'\\begin{tabular}{.*?}', '', content)
    content = re.sub(r'\\end{tabular}', '', content)
    content = re.sub(r'\\toprule', '', content)
    content = re.sub(r'\\midrule', '', content)
    content = re.sub(r'\\bottomrule', '', content)
    content = re.sub(r'& ', r' | ', content)
    content = re.sub(r' \\\\', r'', content)

    # Citations
    content = re.sub(r'\\cite{(.*?)}', r'[\1]', content)

    # Remove labels
    content = re.sub(r'\\label{.*?}', '', content)
    
    # Remove boxed
    content = re.sub(r'\\boxed{(.*?)}', r'\1', content)

    # Remove other LaTeX commands
    content = re.sub(r'\\begin{thebibliography}{\d+}', r'### References', content)
    content = re.sub(r'\\end{thebibliography}', '', content)
    content = re.sub(r'\\bibitem{(.*?)}', r'[\1] ', content)

    return content

if __name__ == "__main__":
    with open("/home/ubuntu/UBP_Repo/computational_grammar/01/ubp_3.5_symbol_operators_manual_section.tex", "r") as f:
        latex_text = f.read()

    markdown_text = convert_latex_to_markdown(latex_text)

    with open("/home/ubuntu/UBP_3.6_Instruction_Manual.md_temp", "w") as f:
        f.write(markdown_text)
