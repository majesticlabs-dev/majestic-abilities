# Makefile Automation for OpenTofu

## Why Makefile?

Makefiles provide:
- Consistent CLI interface across teams
- Variable injection and defaults
- Secret loading integration (1Password, Vault)
- Guard rails against misuse
- Self-documenting targets

## Basic Structure

```makefile
# Define known targets
TARGETS := apply plan destroy output help
CATCH_ALL := $(filter-out $(TARGETS),$(MAKECMDGOALS))

# Parse workspace/stack from command line
STACK_PATH := $(firstword $(CATCH_ALL))
WORKSPACE := $(firstword $(subst /, ,$(STACK_PATH)))
STACK := $(word 2,$(subst /, ,$(STACK_PATH)))

# Defaults
AWS_REGION ?= us-east-1
TOFU ?= tofu

# Variable arguments passed to all commands
VAR_ARGS = -var="workspace=$(WORKSPACE)" -var="stack=$(STACK)" -var="aws_region=$(AWS_REGION)"

.PHONY: apply plan destroy output help guard

plan: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) plan $(VAR_ARGS)

apply: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) apply $(VAR_ARGS)

destroy: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) destroy $(VAR_ARGS)

output: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) output $(VAR_ARGS)

help:
	@echo "Usage: make <target> <workspace>/<stack>"
	@echo "Targets: apply plan destroy output"
	@echo "Example: make plan production/core"

guard:
	@if [ -z "$(WORKSPACE)" ] || [ -z "$(STACK)" ]; then \
		echo "Usage: make <target> <workspace>/<stack>"; \
		exit 1; \
	fi

# Catch-all to ignore workspace/stack as targets
%:
	@:
```

## Usage Pattern

```bash
# Preview changes
make plan shared/backend
make plan production/core

# Apply changes
make apply production/core

# Destroy (with confirmation)
make destroy staging/app

# View outputs
make output production/core
```

## Secret Loading with 1Password

```makefile
OP ?= op
OP_ENV_FILE ?= .op.env

# Prefix commands with secret loading
CMD_PREFIX = $(OP) run --env-file=$(OP_ENV_FILE) --

plan: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) plan $(VAR_ARGS)

apply: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) apply $(VAR_ARGS)
```

## Dynamic Variable Injection

```makefile
# Require an explicit reviewed IPv4 /32 or IPv6 /128 CIDR.
ADMIN_CIDR ?=
ifeq ($(strip $(ADMIN_CIDR)),)
$(error Set ADMIN_CIDR to the reviewed administrative CIDR)
endif
VAR_ARGS = -var="workspace=$(WORKSPACE)" \
           -var="stack=$(STACK)" \
           -var='db_allowed_ips=["$(ADMIN_CIDR)"]'

# Environment-specific overrides
ifeq ($(WORKSPACE),production)
  VAR_ARGS += -var="instance_size=large"
endif
```

## Output Inspection

Do not add generic `-json` or `-raw` Make targets because those modes reveal sensitive outputs in plaintext. Keep the default masked display for human inspection:

```makefile
output: guard
	@$(TOFU) -chdir=$(WORKSPACE)/$(STACK) output
```

When automation needs one documented non-sensitive output, read it in the consuming protected process rather than printing all outputs through a general-purpose target.

## Init with Backend Config

```makefile
init: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) init \
		-backend-config="bucket=$(STATE_BUCKET)" \
		-backend-config="key=$(WORKSPACE)/$(STACK)/terraform.tfstate" \
		-backend-config="region=$(AWS_REGION)"

# Reconfigure backend
reinit: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) init -reconfigure
```

## Validation and Formatting

```makefile
validate: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) validate

fmt:
	$(TOFU) fmt -recursive

fmt-check:
	$(TOFU) fmt -recursive -check

# Pre-commit hook integration
check: fmt-check
	@for dir in */*/; do \
		echo "Validating $$dir..."; \
		$(TOFU) -chdir=$$dir validate || exit 1; \
	done
```

## State Operations

```makefile
state-list: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) state list

state-show: guard
	@if [ -z "$(RESOURCE)" ]; then \
		echo "Usage: make state-show RESOURCE=aws_instance.web production/core"; \
		exit 1; \
	fi
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) state show $(RESOURCE)

# Backup state before dangerous operations into a mode-0600 temporary file.
state-backup: guard
	@umask 077; backup=$$(mktemp "$${TMPDIR:-/tmp}/tofu-state.XXXXXX"); \
		$(TOFU) -chdir=$(WORKSPACE)/$(STACK) state pull > "$$backup"; \
		printf 'Protected state backup: %s\n' "$$backup"
```

## Lock Management

```makefile
# Force unlock (dangerous - use with caution)
unlock: guard
	@if [ -z "$(LOCK_ID)" ]; then \
		echo "Usage: make unlock LOCK_ID=xxx production/core"; \
		exit 1; \
	fi
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) force-unlock $(LOCK_ID)
```

## Multi-Stack Operations

```makefile
STACKS := shared/backend production/core staging/core

plan-all:
	@for stack in $(STACKS); do \
		echo "=== Planning $$stack ==="; \
		$(MAKE) plan $$stack || exit 1; \
	done

# Parallel planning (independent stacks only)
plan-parallel:
	@echo "shared/backend production/core" | xargs -P2 -n1 $(MAKE) plan
```

## Directory Structure Convention

```
project/
├── Makefile              # Root automation
├── .op.env               # 1Password references
├── providers.tf          # Shared provider config (symlinked)
├── shared_variables.tf   # Shared variable validation (symlinked)
├── shared/
│   └── backend/          # State infrastructure
│       ├── main.tf
│       ├── backend.tf
│       ├── providers.tf  → ../../providers.tf
│       └── shared_variables.tf → ../../shared_variables.tf
├── production/
│   └── core/
│       ├── main.tf
│       ├── backend.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── providers.tf  → ../../providers.tf
│       └── shared_variables.tf → ../../shared_variables.tf
└── staging/
    └── core/
        └── ...
```

## Complete Production Makefile

```makefile
TARGETS := apply plan destroy output init validate fmt help
CATCH_ALL := $(filter-out $(TARGETS),$(MAKECMDGOALS))
STACK_PATH := $(firstword $(CATCH_ALL))
WORKSPACE := $(firstword $(subst /, ,$(STACK_PATH)))
STACK := $(word 2,$(subst /, ,$(STACK_PATH)))

AWS_REGION ?= us-east-1
OP ?= op
OP_ENV_FILE ?= .op.env
TOFU ?= tofu

CMD_PREFIX = AWS_REGION=$(AWS_REGION) $(OP) run --env-file=$(OP_ENV_FILE) --
VAR_ARGS = -var="workspace=$(WORKSPACE)" -var="stack=$(STACK)" -var="aws_region=$(AWS_REGION)"

.PHONY: $(TARGETS) guard

plan: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) plan $(VAR_ARGS)

apply: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) apply $(VAR_ARGS)

destroy: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) destroy $(VAR_ARGS)

output: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) output $(VAR_ARGS)

init: guard
	$(CMD_PREFIX) $(TOFU) -chdir=$(WORKSPACE)/$(STACK) init

validate: guard
	$(TOFU) -chdir=$(WORKSPACE)/$(STACK) validate

fmt:
	$(TOFU) fmt -recursive

help:
	@echo "Usage: make <target> <workspace>/<stack>"
	@echo ""
	@echo "Targets:"
	@echo "  plan      Preview infrastructure changes"
	@echo "  apply     Apply infrastructure changes"
	@echo "  destroy   Destroy infrastructure"
	@echo "  output    Show stack outputs"
	@echo "  init      Initialize stack backend"
	@echo "  validate  Validate configuration"
	@echo "  fmt       Format all .tf files"
	@echo ""
	@echo "Examples:"
	@echo "  make plan shared/backend"
	@echo "  make apply production/core"

guard:
	@if [ -z "$(WORKSPACE)" ] || [ -z "$(STACK)" ]; then \
		echo "Error: Missing workspace/stack argument"; \
		echo "Usage: make <target> <workspace>/<stack>"; \
		exit 1; \
	fi

%:
	@:
```
