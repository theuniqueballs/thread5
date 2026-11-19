#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECCHI-ORACLE — QLoRA fine-tuning of a small chat LLM.

Base model (default): Qwen/Qwen2.5-1.5B-Instruct (1.5B, RU+EN, strong with tags).
Alternates: Qwen/Qwen2.5-3B-Instruct, meta-llama/Llama-3.2-3B-Instruct, HuggingFaceTB/SmolLM2-1.7B-Instruct.

Usage:
  python train_lora.py --data ../dataset/train.jsonl --val ../dataset/val.jsonl
  python train_lora.py --base Qwen/Qwen2.5-3B-Instruct --epochs 3 --out ../checkpoints/oracle-3b

Runs on a single 16GB GPU (or free-tier Colab T4 with seq len 1536).
"""
import argparse, os, json
import torch
from datasets import load_dataset
from transformers import (AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
                          TrainingArguments)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig


def build_format(example, tokenizer):
    """Apply the model's chat template to system/user/assistant messages."""
    msgs = example["messages"]
    if tokenizer.chat_template is None:
        # fallback: chatml
        tokenizer.chat_template = (
            "{% for message in messages %}"
            "{{ '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}"
            "{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"
        )
    text = tokenizer.apply_chat_template(msgs, tokenize=False)
    return {"text": text}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--data", default=os.path.join(os.path.dirname(__file__), "..", "dataset", "train.jsonl"))
    ap.add_argument("--val", default=os.path.join(os.path.dirname(__file__), "..", "dataset", "val.jsonl"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "checkpoints", "oracle-1.5b"))
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--max-len", type=int, default=2048)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--lora-alpha", type=int, default=32)
    args = ap.parse_args()

    # 2026-11-20: bitsandbytes требует CUDA — падать сразу и по-человечески
    if not torch.cuda.is_available():
        raise SystemExit("!! CUDA не найдена: QLoRA-тренировка требует GPU (bitsandbytes). "
                         "Для CPU-проверки датасета используй eval_oracle.py --fallback.")

    # 2026-11-20: compute-dtype по фактической поддержке GPU — жёсткий bf16
    # на T4 (Colab-цель README) ронял bitsandbytes в CUDA-ошибку
    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.base, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.base, quantization_config=bnb, device_map="auto",
        torch_dtype=torch.bfloat16, trust_remote_code=True,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    lora = LoraConfig(
        r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM",
        # qwen2/llama3-safe target list (unused subkeys simply don't match)
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    ds = load_dataset("json", data_files={"train": args.data, "validation": args.val})
    ds = ds.map(lambda ex: build_format(ex, tokenizer), remove_columns=[c for c in ds["train"].column_names if c != "text"])

    cfg = SFTConfig(
        output_dir=args.out,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch,
        gradient_accumulation_steps=args.accum,
        per_device_eval_batch_size=args.batch,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=5,
        eval_strategy="steps",
        eval_steps=25,
        save_strategy="steps",
        save_steps=50,
        save_total_limit=3,
        bf16=torch.cuda.is_bf16_supported(),
        max_seq_length=args.max_len,
        packing=False,
        dataset_text_field="text",
        report_to=[],
        seed=1337,
    )
    trainer = SFTTrainer(model=model, args=cfg, train_dataset=ds["train"],
                         eval_dataset=ds["validation"], processing_class=tokenizer)
    trainer.train()
    trainer.save_model(os.path.join(args.out, "adapter"))
    tokenizer.save_pretrained(os.path.join(args.out, "adapter"))
    with open(os.path.join(args.out, "train_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"base": args.base, "epochs": args.epochs, "lr": args.lr,
                   "lora_r": args.lora_r, "lora_alpha": args.lora_alpha,
                   "max_len": args.max_len, "dataset": "ecchi-oracle (dataset/train.jsonl — см. stats.json)"}, f, ensure_ascii=False, indent=2)
    print("DONE ->", os.path.join(args.out, "adapter"))


if __name__ == "__main__":
    main()
