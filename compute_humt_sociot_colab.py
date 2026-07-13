"""
compute_humt_sociot_colab.py
================================
Google Colab TPU-compatible version of the Textual Displacement (TD) pipeline.

HOW TO USE IN COLAB
-------------------
1. Upload this file to your Colab session.
2. Install dependencies (run once):
       !pip install transformers torch scipy

3. Set your arguments in the COLAB CONFIGURATION block below
   (mirrors the original CLI call):
       python compute_humt_sociot.py examples.csv --input_column text --metric humt

4. Run all cells. When prompted, upload your CSV file via the file picker.

WHAT HAS CHANGED vs. the original script
-----------------------------------------
- TPU device detection  : prefers XLA TPU when available, falls back to CUDA/CPU
- File upload           : google.colab.files.upload() replaces the filename CLI arg
- Argument parsing      : hard-coded COLAB CONFIGURATION block replaces argparse
                          (the same variables are set, so all downstream logic is
                           identical to the original)
- model.train() kept    : dropout must stay active so n_samples produces variance
                          and std is non-zero. torch.no_grad() is still used inside
                          compute_set_log_sum_exp to skip gradient computation.
- Everything else       : unchanged — same phrase sets, category_index, compute_ci,
                          calculate_td, and results-saving logic
"""

# ─────────────────────────────────────────────────────────────────────────────
# COLAB CONFIGURATION  ←  Edit these three lines to match your CLI command
# Equivalent to:
#   python compute_humt_sociot.py examples.csv --input_column text --metric humt
# ─────────────────────────────────────────────────────────────────────────────
INPUT_COLUMN = "text"                 # --input_column
METRICS      = ["humt"]              # --metric  (list: e.g. ["humt", "sociot_gender"])
SAVE_PATH    = None                  # --save_path (None → auto-generated under results/)
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import numpy as np
import pandas as pd
import scipy.stats
import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── 1. TPU / device setup ────────────────────────────────────────────────────
def get_device():
    """
    Return the best available device.
    Priority: XLA TPU  →  CUDA GPU  →  CPU
    """
    try:
        import torch_xla.core.xla_model as xm          # available on Colab TPU
        device = xm.xla_device()
        print(f"[device] Using TPU: {device}")
        return device, "xla"
    except ImportError:
        pass

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"[device] Using GPU: {torch.cuda.get_device_name(0)}")
        return device, "cuda"

    device = torch.device("cpu")
    print("[device] Using CPU")
    return device, "cpu"

device, device_type = get_device()

# ── 2. File upload (Colab) ───────────────────────────────────────────────────
def upload_file_colab():
    """
    Use Colab's built-in file picker to upload a CSV.
    Returns the local path of the uploaded file.
    """
    try:
        from google.colab import files
        print("\nPlease upload your CSV file using the file picker below.")
        uploaded = files.upload()                       # opens the file picker
        if not uploaded:
            raise RuntimeError("No file was uploaded.")
        filename = list(uploaded.keys())[0]
        print(f"[upload] Received: {filename}")
        return filename
    except ImportError:
        # Running outside Colab (e.g., local testing) — fall back to a prompt
        filename = input("Enter the path to your CSV file: ").strip()
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        return filename

# ── 3. Phrase sets & index  (UNCHANGED) ──────────────────────────────────────
category_terms = {
    "humt":                   ["He", "She", "It"],
    "sociot_status":          ["commanded", "proclaimed", "demanded",
                               "pleaded", "mentioned", "asked"],
    "sociot_social_distance": ["friend", "partner", "girlfriend",
                               "boyfriend", "husband", "wife", "stranger"],
    "sociot_gender":          ["She", "He"],
    "sociot_warmth":          ["friend", "lover", "mentor", "idol",
                               "stranger", "enemy", "examiner", "dictator"],
}

category_index = {
    "sociot_warmth":          4,
    "sociot_status":          3,
    "humt":                   2,
    "sociot_gender":          1,
    "sociot_social_distance": 6,
}

# ── 4. Model loading ─────────────────────────────────────────────────────────
print("[model] Loading GPT-2 tokenizer and model …")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model     = AutoModelForCausalLM.from_pretrained("gpt2")

# Send model to the target device
model.to(device)

# IMPORTANT: model.train() is intentional — it keeps dropout active so that
# each of the n_samples forward passes returns a slightly different log-prob.
# This variance is what produces a non-zero std/SEM. torch.no_grad() inside
# compute_set_log_sum_exp still suppresses gradients, so there is no extra
# memory or speed cost from being in train mode.
model.train()
print("[model] Ready (train mode — dropout active for sampling variance).\n")

# ── 5. Core computation  (logic UNCHANGED, wrapped in torch.no_grad) ─────────
def compute_set_log_sum_exp(inputs_batch):
    """Compute log-sum-exp over a batch of padded inputs. UNCHANGED."""
    with torch.no_grad():
        outputs  = model(**inputs_batch, labels=inputs_batch["input_ids"])
        log_probs = -outputs.loss
    return torch.logsumexp(log_probs, dim=0).item()


def compute_ci(prompt, candidates, n_samples=100):
    """
    Compute contextual inference score for a prompt against a candidate set.
    UNCHANGED except device tensors are moved via .to(device).
    """
    prompt = f'"{prompt}"' if prompt else ""
    input_batches = []

    for word in candidates:
        if word in ["He", "She", "It"]:
            input_prompt = f"{word} said, {prompt}"
        elif word.endswith("ed"):
            input_prompt = f"He {word}, {prompt}"
        elif word in ["friend", "partner", "girlfriend",
                      "boyfriend", "husband", "wife"]:
            input_prompt = f"My {word} said, {prompt}"
        else:
            input_prompt = f"The {word} said, {prompt}"

        inputs = tokenizer(
            input_prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
        ).to(device)
        input_batches.append(inputs)

    # Pad to a uniform length across candidates
    input_ids      = pad_sequence(
        [inp["input_ids"].squeeze(0)      for inp in input_batches],
        batch_first=True,
    )
    attention_mask = pad_sequence(
        [inp["attention_mask"].squeeze(0) for inp in input_batches],
        batch_first=True,
    )
    inputs_batch = {"input_ids": input_ids, "attention_mask": attention_mask}

    # For XLA/TPU: mark_step() after each forward pass to keep graph bounded
    results = []
    for _ in range(n_samples):
        results.append(compute_set_log_sum_exp(inputs_batch))
        if device_type == "xla":
            import torch_xla.core.xla_model as xm
            xm.mark_step()

    mean_result = np.mean(results)
    sem_result  = scipy.stats.sem(results)
    return mean_result, sem_result


def calculate_td(df, input_col, metric):
    """
    Calculate log-ratios for each row and metric. UNCHANGED.
    """
    df = df.dropna(subset=[input_col]).copy()
    df[f"{input_col}_trunc"] = df[input_col].str[:300]

    word_list   = category_terms[metric]
    split_index = category_index[metric]
    first_lex   = word_list[:split_index]
    second_lex  = word_list[split_index:]

    def compute_row(row):
        response  = row[f"{input_col}_trunc"]
        a_score, a_std = compute_ci(response, first_lex)
        b_score, b_std = compute_ci(response, second_lex)
        log_ratio = a_score - b_score
        return log_ratio, np.sqrt(a_std**2 + b_std**2)

    df[[f"{metric}_{input_col}",
        f"std_{metric}_{input_col}"]] = df.apply(
            compute_row, axis=1, result_type="expand"
        )
    return df

# ── 6. Metric validation  (UNCHANGED logic) ──────────────────────────────────
def validate_metrics(values):
    invalid = [m for m in values if m not in category_terms]
    if invalid:
        print(f"Error: Invalid metrics: {', '.join(invalid)}")
        print("Valid choices:", ", ".join(category_terms.keys()))
        sys.exit(1)
    return values

# ── 7. Main ───────────────────────────────────────────────────────────────────
def main():
    # -- (a) Validate configuration block ------------------------------------
    input_column = INPUT_COLUMN
    metrics      = validate_metrics(METRICS)

    print("=" * 60)
    print(f"Input column : {input_column}")
    print(f"Metrics      : {metrics}")
    print("=" * 60)

    # -- (b) Upload / locate the CSV -----------------------------------------
    filename = upload_file_colab()

    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"\n[data] Loaded {len(df):,} rows from '{filename}'")

    # -- (c) Compute TD for each metric  (UNCHANGED loop) --------------------
    for metric in metrics:
        print(f"\n[compute] metric={metric}  column={input_column}")
        df = calculate_td(df, input_column, metric)

    # -- (d) Save results  (UNCHANGED path logic) ----------------------------
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    if SAVE_PATH:
        save_path = SAVE_PATH
    else:
        base = os.path.splitext(os.path.basename(filename))[0]
        save_path = os.path.join(
            results_dir,
            f"{base}_{input_column}_{'_'.join(metrics)}.csv",
        )

    df.to_csv(save_path, index=False)
    print(f"\n[done] Saved output → {save_path}")

    # -- (e) Download result in Colab ----------------------------------------
    try:
        from google.colab import files
        files.download(save_path)
        print("[download] File sent to browser download.")
    except ImportError:
        print(f"[info] Running outside Colab — find your file at: {save_path}")


if __name__ == "__main__":
    main()
