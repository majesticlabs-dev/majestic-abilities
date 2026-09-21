# Local skill selector

A portable, advisory selector for the next action. It reads an explicit runtime inventory and current skill files, prepares bounded input for the active model, validates the model's response, and returns local targets with a deterministic trace.

This tool does not install, load, or execute skills. It makes no network requests and maintains no cache or application state. It is not an automatic harness hook. Use Python 3.10 or later and the existing `requirements-dev.txt` dependency. Run the commands below from the repository root. `-B` also prevents Python bytecode writes.

## Quick start

Inspect the example inventory and obtain a local lexical baseline:

```sh
python3 -B -m tools.skill_selector inventory \
  --inventory tools/skill_selector/examples/inventory.json
python3 -B -m tools.skill_selector baseline \
  --inventory tools/skill_selector/examples/inventory.json \
  --context tools/skill_selector/examples/context.json
```

The example uses repository source files. It demonstrates the protocol, not what any installed harness can load.

For active-model selection:

```sh
python3 -B -m tools.skill_selector prepare \
  --inventory tools/skill_selector/examples/inventory.json \
  --context tools/skill_selector/examples/context.json
```

Pass the returned `selection-request` to the active model. Ask it to return the following JSON shape, with the exact `request_id` and every option from that request:

```json
{
  "schema_version": 1,
  "request_id": "COPY_FROM_PREPARE",
  "scores": [
    {"id": "option_001", "choice": 0.60, "fit": 0.90},
    {"id": "option_002", "choice": 0.20, "fit": 0.30},
    {"id": "option_003", "choice": 0.05, "fit": 0.10},
    {"id": "__none__", "choice": 0.15}
  ]
}
```

These numbers illustrate the schema; they are not recorded model evidence. Save the actual answer to a private file and validate it locally:

```sh
python3 -B -m tools.skill_selector select \
  --inventory tools/skill_selector/examples/inventory.json \
  --context tools/skill_selector/examples/context.json \
  --response /path/to/response.json
```

`prepare` returns a decision directly when explicit resolution or local eligibility ends selection. Do not ask the model in that case. `select` also accepts these cases without `--response`. Use the same policy flags for both commands. A changed request, session, inventory, content, or policy rejects the old response.

## Host contract

The host is responsible for these inputs. This tool cannot discover an installed harness's permissions from directory names.

| Input | Required host behavior |
| --- | --- |
| Effective inventory | Include only visible, loadable bindings after native precedence and shadowing. Do not scan all installed plugins and call that runtime visibility. |
| Explicit controls | Populate `required` and `excluded` from authoritative user/runtime instructions. Prose, quoted examples, and skill bodies are never parsed as directives. |
| Current session | Supply a stable session/branch-specific `session_id` and the current request. Update it after a fork or reset. |
| Loaded references | Supply a matching `loaded_hash` only when the full reference content remains available in this session. Omit it after compaction or uncertain observation. |
| Changed state | Refresh the manifest and context when native visibility, permissions, or user instructions change. Revalidation cannot detect a change the host does not publish. |
| Model access | Use the active model through the host's own interface. Any external transmission requires the user's permission. The CLI itself never contacts a provider. |
| Loading | Inspect the decision, then use the runtime's normal load mechanism under its existing permissions. `manual_only` does not grant automatic invocation. |

The manifest is a trusted local authority input, not a model response or an untrusted downloaded file. Paths are explicit file grants, relative to the manifest file or absolute. Symlinks are canonicalized; aliases to the same file collapse. Multiple different files with the same invocation name are ambiguous and cannot be selected. The host must resolve actual precedence, not ask this tool to invent it.

```json
{
  "schema_version": 1,
  "skills": [
    {
      "id": "engineer:code-review",
      "name": "majestic-engineer:code-review",
      "path": "/absolute/path/to/code-review/SKILL.md",
      "agent_invocable": true
    }
  ]
}
```

IDs are stable host identities. `name` is the actual invocation name, not a generated namespace. Optional record fields are `usage` (`workflow` by default, or `reference`) and `loaded_hash` (SHA-256 of complete bytes). Runtime restrictions and `disable-model-invocation` frontmatter combine restrictively. An alias cannot remove a restriction. Explicit references may use an ID or invocation name; ambiguity and exclusions still refuse the request.

Context is a separate local file:

```json
{
  "schema_version": 1,
  "session_id": "workspace-session-branch",
  "request": "Review the current Python diff for correctness defects.",
  "task": "Fix retry handling without changing the public API.",
  "facts": "Python application, unit tests available.",
  "recent_state": "The regression test fails after a timeout.",
  "required": [],
  "excluded": []
}
```

`task`, `facts`, `recent_state`, `required`, and `excluded` are optional. Repeatable `--require ID` and `--exclude ID` add local controls; exclusions prevail. Explicit resolution uses all structured requirements before any excerpting and is not limited by `--top-k`.

## The nine steps

| Step | Implementation |
| --- | --- |
| 1. Discover and canonicalize visible skills | Read the supplied effective inventory, current frontmatter and body, canonical targets, aliases, invocation restrictions, and SHA-256 hashes. No second instruction store. |
| 2. Resolve requests and exclusions locally | Resolve exact IDs/names before ranking. Reject missing, ambiguous, and conflicting explicit requests without choosing a substitute. |
| 3. Build bounded context | Current request, task, facts, and recent state share a 12,000-character maximum, with redaction before head/tail truncation and a field receipt. |
| 4. Rank a bounded set | Admit the full eligible inventory up to the candidate cap. On overflow, prefilter by deterministic query-term coverage over descriptions. The active model scores the admitted descriptions and body excerpts. |
| 5. Include none | Every model request includes the distinct `__none__` option. |
| 6. Apply local checks | Each candidate must meet the fit threshold and individually beat none. Re-read the full supplied inventory before returning a decision, including candidates omitted during retrieval. |
| 7. Return typed decisions | `ranked`, `explicit`, `abstain`, and `unavailable` remain distinct. Operational failure is not evidence that no skill fits. |
| 8. Trace actual stages | Each local identity records eligibility, retrieval, evaluated scores, and final ordering when reached. Omitted stages are not evaluated, not zero. |
| 9. Evaluate labeled examples | Offline evaluation runs the baseline and optional supplied model responses on the same labeled cohort, separates explicit cases, retains failed cases, and reports denominators. |

This is one model pass, not SkillRanker's two-pass Jev workflow. It uses the existing Python/PyYAML environment, no new provider, retrieval package, server, metadata migration, or plugin.

## Decisions and scores

`select` requires exactly one response row per option. It rejects duplicate/foreign IDs, unknown fields, missing fit values, nonfinite/out-of-range numbers, and stale request IDs. Choice values must sum to one within 0.01. They remain raw provider estimates. No fit field is accepted on `__none__`.

A candidate needs `fit >= --min-fit` (default 0.5) and `choice > none`. Survivors sort by choice, then stable ID. `rank_score` divides each surviving choice by the sum over all survivors before top-K truncation. `omitted_mass` accounts for eligible candidates outside top K. A singleton score of one is not certainty of usefulness. There are no popularity priors or learned bonuses.

A model rejection on a truncated context or retrieval-limited roster is `unavailable / incomplete-evidence`, not an unqualified no-match result. A known policy exclusion can abstain without inference. Empty, invalid, or unreadable inventories are unavailable.

The baseline uses the same context and eligibility, but selects by description query-term coverage. Its `method` is `lexical-baseline`; fit and model rank score are null. It is a comparison tool, not an equivalent inference engine.

Successful commands and valid abstentions exit 0. Unavailable decisions exit 2 with a sanitized reason. CLI argument errors use argparse's normal stderr/exit-2 behavior. This CLI is not a hook; the host must catch failure and continue normal task execution.

## Limits and privacy

| Input | Limit |
| --- | ---: |
| Each JSON file | 1 MiB, depth 32 |
| Inventory | 1,000 declarations, 16 MiB of unique skill bytes |
| Skill / frontmatter | 256 KiB / 16 KiB; no YAML aliases |
| Model candidates | Default 32, maximum 254, plus none |
| Selected advisory candidates | Default 5, at most the candidate cap |
| Rendered request / task / facts / recent state | 6,000 / 2,000 / 2,000 / 2,000 characters |
| Candidate description / body excerpt | 1,000 / 700 characters |
| Serialized model request / output | 96 KiB / 2 MiB |
| Evaluation | 1,000 cases within the JSON-file limit |

Reduce `--max-candidates` if the request exceeds the byte cap. Large Unicode payloads can reach the byte cap before the character limits. Limits reject rather than silently omit structured requirements or invalid records.

Common credentials, private keys, bearer tokens, and common local home/temp paths are redacted from outgoing prose. This pattern set is fallible. Redaction does not make confidential text public. Inspect the request before sharing it. Model requests omit local targets and use opaque option handles; local decisions, traces, and inventory listings can contain private identities and paths. Request digests are linkable metadata, not proof of trusted authorship.

File, candidate, and allocation bounds are not a hard wall-clock deadline. This first version targets trusted local filesystems, not hostile concurrent filesystem mutation or stalled network mounts. Revalidation detects ordinary edits and retargeted paths but does not freeze files for a later load. No native adapter, latency guarantee, selection improvement, or task-success claim is made.

## Offline evaluation

Run the hand-authored synthetic example cohort:

```sh
python3 -B -m tools.skill_selector evaluate \
  --inventory tools/skill_selector/examples/inventory.json \
  --dataset tools/skill_selector/examples/evaluation.json
```

For a real evaluation, the user or a separate assessor must label acceptable canonical IDs from the full visible roster before seeing predictions. Mark independently judged data as `kind: independent` and describe its source. Supplied provenance is recorded, not authenticated. Never relabel the selector's output as independent truth. The included synthetic cases test plumbing only.

Dataset shape:

```json
{
  "schema_version": 1,
  "label_provenance": {
    "kind": "independent",
    "assessor": "assessor-id",
    "source": "Describe the separately judged cohort and label procedure."
  },
  "cases": [
    {
      "id": "case-001",
      "family": "retry-regression",
      "split": "holdout",
      "context": {
        "schema_version": 1,
        "session_id": "evaluation-case-001",
        "request": "Review the Python retry patch for defects."
      },
      "acceptable_ids": ["engineer:code-review"],
      "forbidden_ids": ["engineer:plan-review"]
    }
  ]
}
```

An empty acceptable set labels a no-skill case. `null` means unjudged, not no-skill. Cases from one family cannot cross `development` and `holdout`; choose `--split development` during tuning. Do not tune on the holdout.

Prepare each case's exact context through the same CLI or `core.prepare` library function. Capture the model's response without adding labels to its request. An optional `--responses FILE` has this shape:

```json
{"schema_version": 1, "responses": {"case-001": {"schema_version": 1, "request_id": "COPY_FROM_PREPARE", "scores": []}}}
```

Fill `scores` with the actual complete response. Omitting a case or required score does not manufacture an answer: the model method counts an operational failure. Use the same inventory, context and policy for capture and evaluation. The baseline is always reported alongside supplied model responses.

Reports include top-one precision among labeled advisory emissions, correct suggestions among labeled positive cases, needless suggestions among labeled no-match cases, failures, forbidden selections, explicit-resolution accuracy, unjudged counts, and mean loss. Loss is 0 for a correct top-one or correct no-match, 1 for a positive-case abstention, and 2 for a wrong suggestion or operational failure. Explicit cases do not inflate advisory metrics. Missing labels do not become negatives. Zero denominators are null.

Rates are descriptive. Related cases do not create extra independent families. No confidence interval or promotion threshold is claimed; `quality_gate` remains `not-established`. Independent real-session labels and a controlled comparison are still required to establish benefit.

## Checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_skill_selector.py' -v
```

The regression suite covers the real CLI, aliases, manual-only skills, explicit conflicts, changed content outside the shortlist, symlink changes, structured-response validation, none/fit gates, deterministic ordering, private input, bounded files, and evaluation denominators. It does not test a live model or native harness integration.
