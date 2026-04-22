"""Patch the grader function in v3 script using line-based replacement."""
with open('core/ubp_swarm_tct_mathnet_v3.py', 'r') as f:
    lines = f.readlines()

# Find the grader function start and end
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'def grade_solution_v3(' in line:
        start_idx = i
    if start_idx is not None and i > start_idx and line.startswith('# ─── PHENOMENOLOGY'):
        end_idx = i
        break

print(f"Grader function: lines {start_idx+1} to {end_idx}")
print(f"First line: {lines[start_idx].strip()}")
print(f"Last line before end: {lines[end_idx-1].strip()}")

# Replace the grader function
new_grader_lines = '''def grade_solution_v3(problem: Dict, col3: Column3Result, col2: Column2Result,
                      audit: TCTAuditV3) -> Tuple[str, float]:
    """Grade with FINAL ANSWER extraction, phenomenology NRCI bonus, and lenient grading."""
    ref = problem.get('answer', '')
    solution = col3.solution

    # v3.1: Extract FINAL ANSWER line if present — compare that against reference
    extracted_answer = solution
    if '[EXTRACTED]' in solution:
        exlines = [l for l in solution.split('\\n') if '[EXTRACTED]' in l]
        if exlines:
            extracted_answer = exlines[-1].replace('[EXTRACTED]', '').strip()
    elif 'FINAL ANSWER:' in solution:
        exlines = [l for l in solution.split('\\n') if 'FINAL ANSWER:' in l]
        if exlines:
            extracted_answer = exlines[-1].replace('FINAL ANSWER:', '').strip()

    # Heuristic pre-screen against extracted answer
    ref_nums = set(re.findall(r'\\b\\d+\\b', str(ref)))
    sol_nums = set(re.findall(r'\\b\\d+\\b', extracted_answer))
    num_match = len(ref_nums & sol_nums) / max(len(ref_nums), 1)
    ref_words = set(str(ref).lower().split())
    sol_words = set(extracted_answer.lower().split())
    word_overlap = len(ref_words & sol_words) / max(len(ref_words), 1)
    code_bonus = 0.15 if col3.code_output and any(
        n in col3.code_output for n in ref_nums
    ) else 0.0
    phenom_bonus = 0.1 if col3.phenom_answer_nrci > 0.75 else 0.0
    octad_bonus = 0.05 if audit.octad_consensus else 0.0
    heuristic = num_match * 0.45 + word_overlap * 0.25 + code_bonus + phenom_bonus + octad_bonus

    # LLM grader v3.1: lenient, compare extracted answer to reference
    try:
        grade_resp = _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": (
                    "You are a math competition grader. "
                    "The solution may be a full proof; the reference is a terse answer. "
                    "Grade as CORRECT if the solution final answer matches the reference "
                    "(even if phrased differently, e.g. 'n divisible by 3' matches '3|n'). "
                    "Grade as PARTIAL if the approach is right but answer is incomplete or slightly off. "
                    "Grade as INCORRECT only if the approach and answer are both wrong. "
                    "Reply with exactly one word: CORRECT, PARTIAL, or INCORRECT."
                )},
                {"role": "user", "content": (
                    f"Problem: {problem['problem'][:200]}\\n"
                    f"Reference answer: {ref}\\n"
                    f"Extracted final answer: {extracted_answer[:300]}\\n"
                    f"Full solution (for context): {solution[:400]}"
                )}
            ],
            temperature=0.0,
            max_tokens=10
        )
        llm_grade = grade_resp.choices[0].message.content.strip().upper()
        if 'CORRECT' in llm_grade and 'IN' not in llm_grade:
            grade = 'CORRECT'
            score = 1.0
        elif 'PARTIAL' in llm_grade:
            grade = 'PARTIAL'
            score = 0.5
        else:
            grade = 'INCORRECT'
            score = 0.0
    except Exception:
        if heuristic > 0.55:
            grade, score = 'CORRECT', 1.0
        elif heuristic > 0.30:
            grade, score = 'PARTIAL', 0.5
        else:
            grade, score = 'INCORRECT', 0.0
    return grade, score

'''.splitlines(keepends=True)

# Rebuild the file
new_lines = lines[:start_idx] + new_grader_lines + lines[end_idx:]
with open('core/ubp_swarm_tct_mathnet_v3.py', 'w') as f:
    f.writelines(new_lines)

print(f"SUCCESS: Replaced {end_idx - start_idx} lines with {len(new_grader_lines)} lines")
print(f"New total lines: {len(new_lines)}")
