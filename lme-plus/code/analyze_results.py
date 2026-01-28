#!/usr/bin/env python3
"""
Statistical Analysis for LME+ Results

Implements NLP-standard statistical tests per ACL/EMNLP best practices:
- McNemar's test: Pairwise classifier comparison on single test set
- Paired bootstrap confidence intervals: 10,000 samples
- Error categorization and per-question analysis

References:
- Dror et al. (2018): "The Hitchhiker's Guide to Testing Statistical Significance in NLP"
- Dietterich (1998): "Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms"
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any
import numpy as np
from scipy import stats


def load_results(results_dir: Path) -> Tuple[Dict[str, bool], Dict[str, Dict], str]:
    """
    Load results from a directory.
    Returns: (question_id -> correct mapping, question_id -> full result, method_name)
    """
    # Find the results file (not summary)
    results_files = list(results_dir.glob("results_*.json"))
    if not results_files:
        raise FileNotFoundError(f"No results file found in {results_dir}")

    results_file = results_files[0]  # Take the first/only one

    with open(results_file) as f:
        data = json.load(f)

    correct_map = {r["question_id"]: r["correct"] for r in data}
    full_map = {r["question_id"]: r for r in data}

    # Extract method name from directory name
    method_name = results_dir.name

    return correct_map, full_map, method_name


def mcnemar_test(correct_a: Dict[str, bool], correct_b: Dict[str, bool]) -> Dict[str, Any]:
    """
    McNemar's test for comparing two classifiers on the same test set.

    Based on the 2x2 contingency table:
    - n00: both wrong
    - n01: A wrong, B correct (B better)
    - n10: A correct, B wrong (A better)
    - n11: both correct

    Only discordant pairs (n01 + n10) matter for McNemar's test.

    Returns test statistic, p-value, and contingency counts.
    """
    # Get common questions
    common_ids = set(correct_a.keys()) & set(correct_b.keys())

    n00 = n01 = n10 = n11 = 0

    for qid in common_ids:
        a_correct = correct_a[qid]
        b_correct = correct_b[qid]

        if not a_correct and not b_correct:
            n00 += 1
        elif not a_correct and b_correct:
            n01 += 1
        elif a_correct and not b_correct:
            n10 += 1
        else:
            n11 += 1

    # McNemar's test statistic (with continuity correction)
    discordant = n01 + n10

    if discordant == 0:
        # No discordant pairs - can't compute meaningful statistic
        return {
            "n00": n00, "n01": n01, "n10": n10, "n11": n11,
            "discordant": discordant,
            "chi2": None,
            "p_value": 1.0,
            "significant": False,
            "note": "No discordant pairs"
        }

    # Chi-squared statistic with continuity correction
    chi2 = (abs(n01 - n10) - 1) ** 2 / (n01 + n10)
    p_value = 1 - stats.chi2.cdf(chi2, df=1)

    return {
        "n00": n00,
        "n01": n01,  # B wins
        "n10": n10,  # A wins
        "n11": n11,
        "discordant": discordant,
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6),
        "significant": p_value < 0.05
    }


def bootstrap_ci(correct: Dict[str, bool], n_bootstrap: int = 10000,
                 confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Compute bootstrap confidence interval for accuracy.

    Returns: (lower, point_estimate, upper)
    """
    results = list(correct.values())
    n = len(results)

    if n == 0:
        return (0.0, 0.0, 0.0)

    # Point estimate
    point_estimate = sum(results) / n

    # Bootstrap resampling
    rng = np.random.default_rng(42)  # For reproducibility
    bootstrap_accs = []

    for _ in range(n_bootstrap):
        sample = rng.choice(results, size=n, replace=True)
        bootstrap_accs.append(np.mean(sample))

    # Percentile confidence interval
    alpha = 1 - confidence
    lower = np.percentile(bootstrap_accs, 100 * alpha / 2)
    upper = np.percentile(bootstrap_accs, 100 * (1 - alpha / 2))

    return (round(lower, 4), round(point_estimate, 4), round(upper, 4))


def paired_bootstrap_diff(correct_a: Dict[str, bool], correct_b: Dict[str, bool],
                          n_bootstrap: int = 10000, confidence: float = 0.95) -> Dict[str, Any]:
    """
    Paired bootstrap test for the difference between two systems.
    More appropriate than independent bootstrap when systems are evaluated on the same test set.

    Returns CI for (accuracy_a - accuracy_b), and whether it excludes 0.
    """
    common_ids = sorted(set(correct_a.keys()) & set(correct_b.keys()))
    n = len(common_ids)

    if n == 0:
        return {"diff": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "significant": False}

    # Arrays for efficient resampling
    results_a = np.array([correct_a[qid] for qid in common_ids], dtype=float)
    results_b = np.array([correct_b[qid] for qid in common_ids], dtype=float)

    # Point estimate of difference
    diff = np.mean(results_a) - np.mean(results_b)

    # Paired bootstrap
    rng = np.random.default_rng(42)
    bootstrap_diffs = []

    for _ in range(n_bootstrap):
        indices = rng.choice(n, size=n, replace=True)
        sample_a = results_a[indices]
        sample_b = results_b[indices]
        bootstrap_diffs.append(np.mean(sample_a) - np.mean(sample_b))

    # Percentile CI
    alpha = 1 - confidence
    ci_lower = np.percentile(bootstrap_diffs, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_diffs, 100 * (1 - alpha / 2))

    # Significant if CI excludes 0
    significant = (ci_lower > 0) or (ci_upper < 0)

    return {
        "diff": round(diff, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "significant": significant,
        "n_samples": n
    }


def categorize_error(result: Dict) -> str:
    """
    Categorize an error into types for analysis.
    """
    if result["correct"]:
        return "correct"

    agent_answer = result.get("agent_answer", "").lower()

    # No answer / refusal patterns
    no_answer_patterns = [
        "don't have enough information",
        "i don't know",
        "cannot find",
        "no information",
        "unable to find",
        "not found",
        "no relevant"
    ]

    if any(p in agent_answer for p in no_answer_patterns):
        return "no_answer"

    # Very short answer might indicate failure
    if len(agent_answer.strip()) < 10:
        return "empty_or_short"

    # Otherwise it's a wrong answer
    return "wrong_answer"


def error_analysis(full_results: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Analyze error patterns.
    """
    categories = defaultdict(list)

    for qid, result in full_results.items():
        cat = categorize_error(result)
        categories[cat].append(qid)

    total = len(full_results)

    return {
        "total": total,
        "categories": {
            cat: {
                "count": len(qids),
                "percentage": round(len(qids) / total * 100, 1),
                "question_ids": qids
            }
            for cat, qids in categories.items()
        }
    }


def per_question_comparison(all_correct: Dict[str, Dict[str, bool]]) -> Dict[str, Dict]:
    """
    Create per-question comparison matrix showing which methods got each question right.
    Useful for identifying questions that are particularly hard/easy or method-specific.
    """
    # Get all unique questions
    all_qids = set()
    for correct in all_correct.values():
        all_qids.update(correct.keys())

    methods = list(all_correct.keys())

    comparison = {}
    for qid in sorted(all_qids):
        comparison[qid] = {
            method: all_correct[method].get(qid, None)
            for method in methods
        }

    # Find interesting questions
    interesting = {
        "all_correct": [],      # All methods got it right
        "all_wrong": [],        # All methods got it wrong
        "discriminative": []    # Some methods right, some wrong
    }

    for qid, results in comparison.items():
        valid_results = [v for v in results.values() if v is not None]
        if not valid_results:
            continue

        if all(valid_results):
            interesting["all_correct"].append(qid)
        elif not any(valid_results):
            interesting["all_wrong"].append(qid)
        else:
            interesting["discriminative"].append(qid)

    return {
        "matrix": comparison,
        "summary": interesting,
        "n_discriminative": len(interesting["discriminative"]),
        "n_all_correct": len(interesting["all_correct"]),
        "n_all_wrong": len(interesting["all_wrong"])
    }


def analyze_results(results_dirs: List[Path], output_file: Path = None) -> Dict[str, Any]:
    """
    Main analysis function.
    """
    # Load all results
    all_correct = {}
    all_full = {}
    method_names = []

    for results_dir in results_dirs:
        correct, full, name = load_results(results_dir)
        all_correct[name] = correct
        all_full[name] = full
        method_names.append(name)

    print(f"Loaded {len(method_names)} methods: {method_names}")

    analysis = {
        "methods": method_names,
        "accuracy": {},
        "bootstrap_ci": {},
        "mcnemar_tests": {},
        "paired_bootstrap": {},
        "error_analysis": {},
        "per_question": None
    }

    # Compute accuracy and bootstrap CI for each method
    print("\n=== Accuracy with 95% Bootstrap CI ===")
    for name in method_names:
        correct = all_correct[name]
        acc = sum(correct.values()) / len(correct)
        ci_lower, _, ci_upper = bootstrap_ci(correct)

        analysis["accuracy"][name] = round(acc, 4)
        analysis["bootstrap_ci"][name] = {
            "lower": ci_lower,
            "upper": ci_upper,
            "n": len(correct)
        }

        print(f"{name}: {acc:.1%} [{ci_lower:.1%}, {ci_upper:.1%}] (n={len(correct)})")

    # Pairwise McNemar tests
    print("\n=== Pairwise McNemar Tests ===")
    for i, name_a in enumerate(method_names):
        for name_b in method_names[i+1:]:
            key = f"{name_a}_vs_{name_b}"
            result = mcnemar_test(all_correct[name_a], all_correct[name_b])
            analysis["mcnemar_tests"][key] = result

            sig = "*" if result["significant"] else ""
            print(f"{key}: p={result['p_value']:.4f}{sig} (discordant={result['discordant']}, A_wins={result['n10']}, B_wins={result['n01']})")

    # Paired bootstrap differences
    print("\n=== Paired Bootstrap 95% CI for Differences ===")
    for i, name_a in enumerate(method_names):
        for name_b in method_names[i+1:]:
            key = f"{name_a}_minus_{name_b}"
            result = paired_bootstrap_diff(all_correct[name_a], all_correct[name_b])
            analysis["paired_bootstrap"][key] = result

            sig = "*" if result["significant"] else ""
            print(f"{key}: diff={result['diff']:+.1%} [{result['ci_lower']:+.1%}, {result['ci_upper']:+.1%}]{sig}")

    # Error analysis for each method
    print("\n=== Error Analysis ===")
    for name in method_names:
        err = error_analysis(all_full[name])
        analysis["error_analysis"][name] = err

        print(f"\n{name}:")
        for cat, info in err["categories"].items():
            print(f"  {cat}: {info['count']} ({info['percentage']:.1f}%)")

    # Per-question comparison
    comparison = per_question_comparison(all_correct)
    analysis["per_question"] = comparison

    print(f"\n=== Per-Question Summary ===")
    print(f"All methods correct: {comparison['n_all_correct']}")
    print(f"All methods wrong: {comparison['n_all_wrong']}")
    print(f"Discriminative (some right, some wrong): {comparison['n_discriminative']}")

    # Save if output specified
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\nAnalysis saved to {output_file}")

    return analysis


def print_latex_table(analysis: Dict[str, Any]):
    """Print results as a LaTeX table."""
    print("\n=== LaTeX Table ===")
    print(r"\begin{tabular}{lcccc}")
    print(r"\toprule")
    print(r"Method & Accuracy & 95\% CI & $n$ \\")
    print(r"\midrule")

    for method in analysis["methods"]:
        acc = analysis["accuracy"][method]
        ci = analysis["bootstrap_ci"][method]
        n = ci["n"]
        print(f"{method} & {acc:.1%} & [{ci['lower']:.1%}, {ci['upper']:.1%}] & {n} \\\\")

    print(r"\bottomrule")
    print(r"\end{tabular}")


def main():
    parser = argparse.ArgumentParser(description="Statistical analysis of LME+ results")
    parser.add_argument("--results", "-r", nargs="+", required=True,
                        help="Result directories to analyze")
    parser.add_argument("--output", "-o", type=str,
                        help="Output JSON file for analysis")
    parser.add_argument("--latex", action="store_true",
                        help="Print LaTeX table")

    args = parser.parse_args()

    results_dirs = [Path(r) for r in args.results]
    output_file = Path(args.output) if args.output else None

    analysis = analyze_results(results_dirs, output_file)

    if args.latex:
        print_latex_table(analysis)


if __name__ == "__main__":
    main()
