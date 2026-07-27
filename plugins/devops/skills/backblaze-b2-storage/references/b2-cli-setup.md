# B2 CLI Installation & Authentication

## Installation

```bash
# macOS
brew install b2-tools

# Linux (Debian/Ubuntu)
sudo apt install backblaze-b2

# Linux (via pip)
pip install b2

# Verify
b2 version
```

## CLI Authentication

```bash
# Authorize interactively without exposing credentials in process arguments
b2 account authorize

# Or load credentials from 1Password through documented environment variables
export B2_APPLICATION_KEY_ID="$(op read 'op://Infrastructure/Backblaze/key_id')"
export B2_APPLICATION_KEY="$(op read 'op://Infrastructure/Backblaze/application_key')"
b2 account authorize
unset B2_APPLICATION_KEY_ID B2_APPLICATION_KEY

# Credentials stored in ~/.b2_account_info (SQLite)
# Override with B2_ACCOUNT_INFO env var
```

## Terraform Authentication

```bash
export B2_APPLICATION_KEY_ID="your-key-id"
export B2_APPLICATION_KEY="your-application-key"

# Or load values from 1Password into the provider environment
export B2_APPLICATION_KEY_ID="$(op read 'op://Infrastructure/Backblaze/key_id')"
export B2_APPLICATION_KEY="$(op read 'op://Infrastructure/Backblaze/application_key')"
```
