"""TakeMeter — classify a Goodreads review as analysis / impression / logbook.

Loads the fine-tuned DistilBERT checkpoint and prints the predicted label with
its confidence and the full probability distribution.

Usage:
    python predict.py "Your review text here"
    python predict.py                      # interactive: type reviews, Ctrl-D to quit
    echo "review text" | python predict.py
    python predict.py --model ./some-other-checkpoint "review text"
"""
import argparse
import sys
from pathlib import Path

DEFAULT_MODEL = "./takemeter-model"
LABELS = ["analysis", "impression", "logbook"]   # must match LABEL_MAP order in the notebook


def load(model_dir):
    model_path = Path(model_dir)
    if not model_path.is_dir():
        sys.exit(
            f"No model at {model_dir!r}.\n"
            "Run Section 3 of the notebook to fine-tune and save a checkpoint, "
            "then point --model at it."
        )

    # Trainer saves the actual model under checkpoint-* inside output_dir.
    if not (model_path / "config.json").is_file():
        checkpoints = sorted(
            (path for path in model_path.glob("checkpoint-*") if path.is_dir()),
            key=lambda path: int(path.name.rsplit("-", 1)[1])
            if path.name.rsplit("-", 1)[1].isdigit()
            else -1,
        )
        if not checkpoints:
            sys.exit(
                f"No Hugging Face checkpoint found in {model_dir!r}.\n"
                "Run Section 3 of the notebook to create a checkpoint."
            )
        model_path = checkpoints[-1]

    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tok = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return torch, tok, model


def classify(torch, tok, model, text):
    enc = tok(text, truncation=True, max_length=256, return_tensors="pt")
    with torch.no_grad():
        logits = model(**enc).logits
    probs = torch.softmax(logits, dim=-1)[0].tolist()
    # Prefer the model's own id2label if it carries real names, else our list.
    names = [model.config.id2label.get(i, LABELS[i]) for i in range(len(probs))]
    if any(n.startswith("LABEL_") for n in names):
        names = LABELS
    best = max(range(len(probs)), key=lambda i: probs[i])
    return names[best], probs[best], dict(zip(names, probs))


def show(label, conf, dist, text):
    print(f"\n  text       {text[:100]}{'...' if len(text) > 100 else ''}")
    print(f"  prediction {label}")
    print(f"  confidence {conf:.3f}")
    print("  distribution")
    for name, p in sorted(dist.items(), key=lambda kv: -kv[1]):
        bar = "#" * round(p * 40)
        
        print(f"    {name:11} {p:.3f}  {bar}")
    if conf < 0.50:
        print("  NOTE: confidence below 0.50 on a 3-class task is barely above the")
        print("        0.333 chance floor — treat this prediction as unreliable.")


def main():
    ap = argparse.ArgumentParser(description="Classify a Goodreads review.")
    ap.add_argument("text", nargs="*", help="review text (omit to read stdin / interactive)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"checkpoint dir (default {DEFAULT_MODEL})")
    args = ap.parse_args()

    torch, tok, model = load(args.model)

    if args.text:
        t = " ".join(args.text)
        show(*classify(torch, tok, model, t), t)
        return

    if not sys.stdin.isatty():
        t = sys.stdin.read().strip()
        if t:
            show(*classify(torch, tok, model, t), t)
        return

    print("TakeMeter — paste a review and press Enter (Ctrl-D to quit).")
    while True:
        try:
            t = input("\n> ").strip()
        except EOFError:
            print()
            return
        if t:
            show(*classify(torch, tok, model, t), t)


if __name__ == "__main__":
    main()
