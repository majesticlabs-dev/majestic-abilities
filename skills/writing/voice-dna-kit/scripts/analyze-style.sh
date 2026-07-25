#!/usr/bin/env sh
set -eu

if [ "$#" -eq 0 ]; then
  echo "Usage: analyze-style.sh FILE [FILE ...]" >&2
  exit 1
fi

python3 - "$@" <<'PY'
import collections
import pathlib
import re
import statistics
import sys

WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
ABBREVIATIONS = ("e.g.", "i.e.", "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "vs.")
SENTINEL = "∯"


def clean_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " CODE ", text)
    text = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("#", ">")):
            continue
        if not stripped:
            lines.append("")
            continue
        line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)
        line = re.sub(r"https?://\S+", "", line)
        line = re.sub(r"^\s*[-*+]\s+", "", line)
        lines.append(line.rstrip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def split_sentences(text):
    protected = re.sub(r"(?<=\d)\.(?=\d)", SENTINEL, text)
    for abbreviation in ABBREVIATIONS:
        protected = re.sub(
            re.escape(abbreviation),
            abbreviation.replace(".", SENTINEL),
            protected,
            flags=re.I,
        )
    parts = re.split(r"(?<=[.!?])[\"'”’\)\]]*\s+", protected)
    return [part.replace(SENTINEL, ".").strip() for part in parts if WORD_RE.search(part)]


def words(text):
    return WORD_RE.findall(text)


def pct(numerator, denominator):
    return 0 if denominator == 0 else round(numerator / denominator * 100, 1)


paths = [pathlib.Path(value) for value in sys.argv[1:]]
for path in paths:
    if not path.is_file():
        raise SystemExit(f"Not a readable file: {path}")

cleaned = [clean_markdown(path.read_text(encoding="utf-8", errors="ignore")) for path in paths]
prose = "\n\n".join(part for part in cleaned if part)
all_words = words(prose)
word_count = len(all_words)
paragraphs = [part.strip() for part in re.split(r"\n\s*\n", prose) if WORD_RE.search(part)]
sentences = split_sentences(prose)
sentence_lengths = [len(words(sentence)) for sentence in sentences]
paragraph_lengths = [len(words(paragraph)) for paragraph in paragraphs]
lower_words = [word.lower().replace("’", "'") for word in all_words]


def per_100(count):
    return 0 if word_count == 0 else round(count / word_count * 100, 2)


punctuation = {
    "commas": prose.count(","),
    "colons": prose.count(":"),
    "semicolons": prose.count(";"),
    "em_or_en_dashes": prose.count("—") + prose.count("–"),
    "exclamation_marks": prose.count("!"),
    "question_marks": prose.count("?"),
    "parenthetical_asides": len(re.findall(r"\([^\)]{3,}\)", prose)),
}
hedge_patterns = (
    r"\bprobably\b", r"\bperhaps\b", r"\bmaybe\b", r"\bmight\b",
    r"\bcould be\b", r"\blikely\b", r"\barguably\b", r"\broughly\b",
    r"\bnearly\b", r"\bfairly\b", r"\bbasically\b", r"\badmittedly\b",
    r"\bi think\b", r"\bi guess\b", r"\bsort of\b", r"\bkinda\b",
)
hedge_counts = collections.Counter()
for pattern in hedge_patterns:
    matches = re.findall(pattern, prose, flags=re.I)
    if matches:
        hedge_counts[pattern.replace(r"\b", "")] = len(matches)
contractions = [word for word in lower_words if "'" in word]
openers = []
for sentence in sentences:
    match = WORD_RE.search(sentence)
    if match:
        openers.append(match.group(0).lower())

print("# Style DNA Baseline")
print("\n## Sources")
for path in paths:
    print(f"- {path}")
print("\n## Core Metrics")
print(f"- Words: {word_count}")
print(f"- Unique words: {len(set(lower_words))}")
print(f"- Lexical diversity: {round(len(set(lower_words)) / word_count, 3) if word_count else 0}")
print(f"- Sentences: {len(sentences)}")
print(f"- Paragraphs: {len(paragraphs)}")
if sentence_lengths:
    print(f"- Average sentence length: {round(statistics.mean(sentence_lengths), 1)} words")
    print(f"- Median sentence length: {round(statistics.median(sentence_lengths), 1)} words")
    print(f"- Minimum / maximum sentence length: {min(sentence_lengths)} / {max(sentence_lengths)} words")
    for label, low, high in (("1-7", 1, 7), ("8-15", 8, 15), ("16-25", 16, 25)):
        count = sum(low <= length <= high for length in sentence_lengths)
        print(f"- Sentences {label} words: {count} ({pct(count, len(sentence_lengths))}%)")
    count = sum(length >= 26 for length in sentence_lengths)
    print(f"- Sentences 26+ words: {count} ({pct(count, len(sentence_lengths))}%)")
if paragraph_lengths:
    print(f"- Average paragraph length: {round(statistics.mean(paragraph_lengths), 1)} words")
    print(f"- Median paragraph length: {round(statistics.median(paragraph_lengths), 1)} words")

print("\n## Punctuation")
for name, count in punctuation.items():
    print(f"- {name.replace('_', ' ').title()}: {count} ({per_100(count)} per 100 words)")

print("\n## Tone Signals")
for label, pattern in {
    "First person singular": r"\b(i|me|my|mine)\b",
    "First person plural": r"\b(we|us|our|ours)\b",
    "Second person": r"\b(you|your|yours)\b",
}.items():
    count = len(re.findall(pattern, prose, flags=re.I))
    print(f"- {label}: {count} ({per_100(count)} per 100 words)")
print(f"- Contractions: {len(contractions)} ({per_100(len(contractions))} per 100 words)")
print(f"- Hedges: {sum(hedge_counts.values())} ({per_100(sum(hedge_counts.values()))} per 100 words)")
if hedge_counts:
    print("- Hedge examples: " + ", ".join(f"{key}={value}" for key, value in hedge_counts.most_common()))

print("\n## Signature Candidates")
for opener, count in collections.Counter(openers).most_common(15):
    print(f"- Opener `{opener}`: {count}")
fragments = [sentence for sentence, length in zip(sentences, sentence_lengths) if length <= 5]
if fragments:
    print("- Short sentence candidates:")
    for fragment in fragments[:10]:
        print(f"  - {fragment}")

print("\n## Review Warning")
print("Validate sentence boundaries and inspect examples before treating these baseline counts as conclusions.")
PY
