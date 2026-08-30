# GitHub User Attachments

Use this adapter only when the target is a GitHub pull request or issue and the project supplies `GITHUB_ATTACHMENTS_TOKEN`. Do not substitute another credential or upload to another host when it is absent.

GitHub documents browser-based attachments at [Attaching files](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files). The upload endpoint below is not a documented public API and can change without notice. A failed upload is a blocked evidence step, not permission to improvise another upload path.

## Preconditions

1. Read the current PR or issue body before editing it.
2. Confirm the target repository and authenticated identity.
3. Inspect the media for secrets, personal data, customer data, internal URLs, and unrelated applications.
4. Keep the media outside the repository.
5. Use one of these MIME types:
   - `image/png`
   - `image/jpeg`
   - `image/gif`
   - `image/webp`
   - `video/mp4`

If a recording is WebM, convert it to H.264 MP4 for broad playback compatibility:

```sh
ffmpeg -i in.webm -c:v libx264 -pix_fmt yuv420p out.mp4
```

## Upload

Set the target values and stop cleanly when the credential is absent:

```sh
repo=owner/repo
file=/absolute/path/to/before.png
mime=image/png

if [[ -z "${GITHUB_ATTACHMENTS_TOKEN:-}" ]]; then
  printf '%s\n' 'GITHUB_ATTACHMENTS_TOKEN is unset; attachment upload skipped.' >&2
  exit 0
fi

login=$(GH_TOKEN="$GITHUB_ATTACHMENTS_TOKEN" gh api user --jq .login)
repository_id=$(GH_TOKEN="$GITHUB_ATTACHMENTS_TOKEN" gh api "repos/$repo" --jq .id)
printf 'Uploading as %s to %s\n' "$login" "$repo" >&2

curl -fsS -X POST \
  "https://uploads.github.com/user-attachments/assets" \
  --url-query "name=$(basename "$file")" \
  --url-query "content_type=$mime" \
  --url-query "repository_id=$repository_id" \
  -H "Authorization: Bearer $GITHUB_ATTACHMENTS_TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: $mime" \
  --data-binary "@$file"
```

A successful response contains a `https://github.com/user-attachments/` URL. Stop and report the failure if the request fails or the response does not contain that URL. Do not claim that the evidence is attached until the URL is present in the saved PR or issue body.

## Embed

Use descriptive alternative text for images:

```markdown
![Before: checkout validation error](https://github.com/user-attachments/assets/...)
```

Put a video URL on its own line:

```markdown
https://github.com/user-attachments/assets/...
```

Before saving an edited body:

1. Preserve every unrelated existing URL that contains `github.com/user-attachments/`.
2. Replace only embeds whose evidence became stale because of the current change.
3. Use a body file instead of shell-interpolated inline Markdown.
4. Re-read the saved body and confirm that the new embeds are present and resolve.

If a later implementation change alters the shown state or interaction, recapture the media and replace the stale embeds before reporting visual verification as complete.
