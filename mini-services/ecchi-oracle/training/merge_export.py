#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECCHI-ORACLE — merge LoRA adapter into the base model and export full weights.

Usage:
  python merge_export.py --base Qwen/Qwen2.5-1.5B-Instruct \
      --adapter ../checkpoints/oracle-1.5b/adapter --out ../models/ecchi-oracle-1
"""
import argparse, os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dtype", default="bfloat16")
    args = ap.parse_args()

    dtype = torch.bfloat16 if args.dtype == "bfloat16" else torch.float16
    model = AutoModelForCausalLM.from_pretrained(
        args.base, torch_dtype=dtype, device_map="cpu", trust_remote_code=True)
    model = PeftModel.from_pretrained(model, args.adapter)
    model = model.merge_and_unload()
    tokenizer = AutoTokenizer.from_pretrained(args.base, trust_remote_code=True)

    os.makedirs(args.out, exist_ok=True)
    model.save_pretrained(args.out, safe_serialization=True)
    tokenizer.save_pretrained(args.out)
    print("MERGED ->", args.out)
    print("Next: convert to GGUF (see export_gguf.md) or serve with vLLM/Ollama.")


if __name__ == "__main__":
    main()
