#!/usr/bin/env python3
"""
Eval runner for NewsLeopard API skill.

Usage:
    python evals/run_evals.py              # run all evals
    python evals/run_evals.py --trigger    # trigger eval only
    python evals/run_evals.py --functional # functional eval only
    python evals/run_evals.py --model claude-haiku-4-5-20251001
"""

import argparse
import json
import sys
from pathlib import Path

import anthropic
import yaml

EVALS_DIR = Path(__file__).parent
SKILL_DIR = EVALS_DIR.parent / "newsleopard-api"
DEFAULT_MODEL = "claude-sonnet-4-6"


def load_skill_description() -> str:
    """Extract the description field from SKILL.md YAML frontmatter."""
    skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    # Parse YAML frontmatter between --- markers
    if not skill_md.startswith("---"):
        sys.exit("Error: SKILL.md does not start with YAML frontmatter")
    end = skill_md.index("---", 3)
    frontmatter = yaml.safe_load(skill_md[3:end])
    if not frontmatter or "description" not in frontmatter:
        sys.exit("Error: Could not find description in SKILL.md frontmatter")
    return frontmatter["description"]


def load_full_skill_content() -> str:
    """Load SKILL.md and all reference files as combined content."""
    parts = [(SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")]
    refs_dir = SKILL_DIR / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            parts.append(f"\n\n--- {ref_file.name} ---\n\n")
            parts.append(ref_file.read_text(encoding="utf-8"))
    return "".join(parts)


def run_trigger_eval(client: anthropic.Anthropic, model: str) -> tuple[int, int]:
    """Run trigger evaluation: does the query match this skill?"""
    print("=== Trigger Eval ===")

    cases = json.loads((EVALS_DIR / "trigger_eval.json").read_text(encoding="utf-8"))
    description = load_skill_description()

    passed = 0
    total = len(cases)

    for i, case in enumerate(cases, 1):
        query = case["query"]
        expected = case["should_trigger"]

        try:
            response = client.messages.create(
                model=model,
                max_tokens=16,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"You are evaluating whether a user query should trigger a skill.\n\n"
                            f"Skill description:\n{description}\n\n"
                            f"User query:\n{query}\n\n"
                            f"Should this query trigger the skill above? "
                            f"Answer with exactly one word: true or false"
                        ),
                    }
                ],
            )
        except anthropic.APIError as e:
            query_short = query[:60] + ("..." if len(query) > 60 else "")
            print(f'{i:2d}. \u2717 ERROR  "{query_short}"  — API error: {e}')
            continue

        answer_text = response.content[0].text.strip().lower()
        got = "true" in answer_text

        ok = got == expected
        if ok:
            passed += 1

        mark = "\u2713" if ok else "\u2717"
        status = "PASS" if ok else "FAIL"
        query_short = query[:60] + ("..." if len(query) > 60 else "")
        print(f'{i:2d}. {mark} {status}  "{query_short}"  (expected={str(expected).lower()}, got={str(got).lower()})')

    pct = passed / total * 100 if total else 0
    print(f"\nTrigger: {passed}/{total} passed ({pct:.1f}%)\n")
    return passed, total


def run_functional_eval(client: anthropic.Anthropic, model: str) -> tuple[int, int]:
    """Run functional evaluation: does the generated code meet expectations?"""
    print("=== Functional Eval ===")

    cases = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    skill_content = load_full_skill_content()

    total_expectations = 0
    passed_expectations = 0

    for case in cases:
        case_id = case["id"]
        prompt = case["prompt"]
        expectations = case["expectations"]

        print(f"[{case_id}] {prompt[:60]}...")

        # Step 1: Generate output from the skill + prompt
        try:
            gen_response = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"You are a coding assistant with access to the following API documentation:\n\n"
                            f"{skill_content}\n\n"
                            f"---\n\n"
                            f"User request:\n{prompt}\n\n"
                            f"Provide the complete implementation."
                        ),
                    }
                ],
            )
        except anthropic.APIError as e:
            print(f"  \u2717 Generation failed — API error: {e}")
            total_expectations += len(expectations)
            print()
            continue
        generated = gen_response.content[0].text

        # Step 2: Judge each expectation
        for exp in expectations:
            total_expectations += 1

            try:
                judge_response = client.messages.create(
                    model=model,
                    max_tokens=256,
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                f"You are a strict code reviewer judging whether generated code meets a specific expectation.\n\n"
                                f"Generated code:\n```\n{generated}\n```\n\n"
                                f"Expectation: {exp}\n\n"
                                f"Does the generated code meet this expectation? "
                                f"Answer on the first line with exactly PASS or FAIL, "
                                f"then on the next line provide a brief reason."
                            ),
                        }
                    ],
                )
            except anthropic.APIError as e:
                print(f"  \u2717 {exp} — API error: {e}")
                continue

            judge_text = judge_response.content[0].text.strip()
            first_line = judge_text.split("\n")[0].strip().upper()
            ok = first_line.startswith("PASS")
            if ok:
                passed_expectations += 1

            mark = "\u2713" if ok else "\u2717"
            reason = ""
            if not ok:
                lines = judge_text.split("\n")
                reason_lines = [l.strip() for l in lines[1:] if l.strip()]
                if reason_lines:
                    reason = f' — "{reason_lines[0]}"'
            print(f"  {mark} {exp}{reason}")

        print()

    pct = passed_expectations / total_expectations * 100 if total_expectations else 0
    print(f"Functional: {passed_expectations}/{total_expectations} expectations passed ({pct:.1f}%)\n")
    return passed_expectations, total_expectations


def main():
    parser = argparse.ArgumentParser(description="Run evals for NewsLeopard API skill")
    parser.add_argument("--trigger", action="store_true", help="Run trigger eval only")
    parser.add_argument("--functional", action="store_true", help="Run functional eval only")
    parser.add_argument("--all", action="store_true", help="Run all evals (default)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    run_all = not args.trigger and not args.functional

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

    results = []

    if args.trigger or run_all:
        results.append(("Trigger", *run_trigger_eval(client, args.model)))

    if args.functional or run_all:
        results.append(("Functional", *run_functional_eval(client, args.model)))

    # Summary
    if len(results) > 1:
        print("=== Summary ===")
        total_passed = sum(r[1] for r in results)
        total_all = sum(r[2] for r in results)
        for name, p, t in results:
            pct = p / t * 100 if t else 0
            print(f"  {name}: {p}/{t} ({pct:.1f}%)")
        overall_pct = total_passed / total_all * 100 if total_all else 0
        print(f"  Overall: {total_passed}/{total_all} ({overall_pct:.1f}%)")


if __name__ == "__main__":
    main()
