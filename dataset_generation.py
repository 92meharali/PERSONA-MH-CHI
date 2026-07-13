from datasets import load_dataset
import pandas as pd
import re
from pathlib import Path


OUTPUT_DIR = Path("counselbench_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def clean_text(x):
    """Basic text cleaning for CSV output."""
    if pd.isna(x):
        return ""

    x = str(x)
    x = re.sub(r"<br\s*/?>", "\n", x)
    x = re.sub(r"\s+", " ", x)
    return x.strip()


def load_hf_dataset(name):
    """Load first split of a Hugging Face dataset as pandas DataFrame."""
    ds = load_dataset(name)
    print(f"\nLoaded: {name}")
    print(ds)

    split = list(ds.keys())[0]
    return ds[split].to_pandas()


# ---------------------------------------------------------
# 1. Load datasets
# ---------------------------------------------------------

eval_df = load_hf_dataset("izi-ano/CounselBench-Eval")
adv_df = load_hf_dataset("izi-ano/CounselBench-Adv")

print("\nEval columns:", eval_df.columns.tolist())
print("Adv columns:", adv_df.columns.tolist())

print("\nEval rows:", len(eval_df))
print("Adv rows:", len(adv_df))


# ---------------------------------------------------------
# 2. Create CounselBench-Eval prompt file
#    2,000 evaluations -> 100 unique real patient questions
# ---------------------------------------------------------

eval_questions = (
    eval_df[["questionID", "questionTitle", "questionText", "topic"]]
    .drop_duplicates(subset=["questionID"])
    .copy()
)

eval_questions["questionTitle"] = eval_questions["questionTitle"].apply(clean_text)
eval_questions["questionText"] = eval_questions["questionText"].apply(clean_text)
eval_questions["topic"] = eval_questions["topic"].apply(clean_text)

# Use questionText if available, otherwise fall back to questionTitle
eval_questions["prompt"] = eval_questions["questionText"]
eval_questions.loc[
    eval_questions["prompt"].str.strip() == "", "prompt"
] = eval_questions["questionTitle"]

eval_questions["source_set"] = "CounselBench-Eval"
eval_questions["prompt_type"] = "normal_real_patient"

eval_questions = eval_questions[
    [
        "source_set",
        "prompt_type",
        "questionID",
        "topic",
        "questionTitle",
        "questionText",
        "prompt",
    ]
].sort_values(["topic", "questionID"])

eval_output_path = OUTPUT_DIR / "counselbench_eval_100_prompts.csv"
eval_questions.to_csv(eval_output_path, index=False, encoding="utf-8-sig")


# ---------------------------------------------------------
# 3. Create CounselBench-Adv prompt file
#    20 rows × 6 failure-mode columns -> 120 prompts
# ---------------------------------------------------------

adv_failure_cols = [
    "apathetic",
    "assumptions",
    "symptoms",
    "judgmental",
    "medication",
    "therapy",
]

missing_cols = [col for col in adv_failure_cols if col not in adv_df.columns]
if missing_cols:
    raise ValueError(f"Missing expected adversarial columns: {missing_cols}")

adv_questions = adv_df[adv_failure_cols].copy()

# Convert wide format into long format:
# columns become failure_mode, cell values become prompts
adv_questions = adv_questions.melt(
    var_name="failure_mode",
    value_name="prompt"
)

adv_questions["prompt"] = adv_questions["prompt"].apply(clean_text)
adv_questions = adv_questions[adv_questions["prompt"].str.strip() != ""]

adv_questions = adv_questions.drop_duplicates(
    subset=["failure_mode", "prompt"]
).reset_index(drop=True)

adv_questions["questionID"] = [
    f"adv_{i + 1:03d}" for i in range(len(adv_questions))
]

adv_questions["source_set"] = "CounselBench-Adv"
adv_questions["prompt_type"] = "adversarial_expert_authored"
adv_questions["topic"] = "adversarial"

adv_questions = adv_questions[
    [
        "source_set",
        "prompt_type",
        "questionID",
        "topic",
        "failure_mode",
        "prompt",
    ]
]

adv_output_path = OUTPUT_DIR / "counselbench_adv_120_prompts.csv"
adv_questions.to_csv(adv_output_path, index=False, encoding="utf-8-sig")


# ---------------------------------------------------------
# 4. Print verification summary
# ---------------------------------------------------------

print("\nSaved files:")
print(f"1. {eval_output_path}")
print(f"2. {adv_output_path}")

print("\nCounselBench-Eval unique prompts:", len(eval_questions))
print("CounselBench-Adv prompts:", len(adv_questions))

print("\nCounselBench-Eval topic counts:")
print(eval_questions["topic"].value_counts().sort_index())

print("\nCounselBench-Adv failure-mode counts:")
print(adv_questions["failure_mode"].value_counts().sort_index())

print("\nDone.")