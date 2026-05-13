#!/usr/bin/env python3
"""Trigger a Managed Agent session via POST /v1/sessions.

Environment variables:
- ANTHROPIC_API_KEY (required)
- MANAGED_AGENT_ID (required unless SESSION_PAYLOAD_JSON is provided)
- MANAGED_AGENTS_BASE_URL (optional, default: https://api.anthropic.com)
- SESSION_CREATE_PATH (optional, default: /v1/sessions)
- SESSION_ENVIRONMENT_ID (optional, added as environment_id when provided)
- VAULT_IDS (optional, comma-separated vault IDs for retrieval context)
- SESSION_INPUT (optional)
- SESSION_INPUT_FILE (optional, path to a UTF-8 text file)
- SESSION_PAYLOAD_JSON (optional, full JSON payload override)
- ANTHROPIC_VERSION (optional, default: 2023-06-01)
- ANTHROPIC_BETA (optional, default: managed-agents-2026-04-01)
- SESSION_MAX_RETRIES (optional, default: 3)
- SESSION_TIMEOUT_SECONDS (optional, default: 60)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, cast


def _get_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _load_input_text() -> str:
    file_path = os.environ.get("SESSION_INPUT_FILE", "").strip()
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()

    return os.environ.get(
        "SESSION_INPUT",
        "Run the twice-daily LinkedIn job search and resume/CV tailoring workflow.",
    ).strip()


def build_payload() -> dict[str, Any]:
    raw_payload = os.environ.get("SESSION_PAYLOAD_JSON", "").strip()
    if raw_payload:
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            raise ValueError(f"SESSION_PAYLOAD_JSON is not valid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("SESSION_PAYLOAD_JSON must decode to a JSON object")
        return cast(dict[str, Any], payload)

    agent_id = _get_required("MANAGED_AGENT_ID")
    input_text = _load_input_text()

    payload: dict[str, object] = {
        "agent": agent_id,
        "metadata": {
            "trigger": "github_actions",
            "session_input": input_text,
            "repository": os.environ.get("GITHUB_REPOSITORY", ""),
            "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
            "run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "ref": os.environ.get("GITHUB_REF", ""),
            "sha": os.environ.get("GITHUB_SHA", ""),
        },
    }

    environment_id = os.environ.get("SESSION_ENVIRONMENT_ID", "").strip()
    if environment_id:
        payload["environment_id"] = environment_id

    vault_ids_raw = os.environ.get("VAULT_IDS", "").strip()
    if vault_ids_raw:
        vault_ids = [v.strip() for v in vault_ids_raw.split(",") if v.strip()]
        if vault_ids:
            payload["vault_ids"] = vault_ids

    return payload


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        return int(response.status), body


def main() -> int:
    try:
        api_key = _get_required("ANTHROPIC_API_KEY")
        base_url = os.environ.get("MANAGED_AGENTS_BASE_URL", "https://api.anthropic.com").rstrip("/")
        path = os.environ.get("SESSION_CREATE_PATH", "/v1/sessions")
        if not path.startswith("/"):
            path = "/" + path

        timeout = int(os.environ.get("SESSION_TIMEOUT_SECONDS", "60"))
        max_retries = int(os.environ.get("SESSION_MAX_RETRIES", "3"))

        url = f"{base_url}{path}"
        payload = build_payload()

        anthropic_version = os.environ.get("ANTHROPIC_VERSION", "2023-06-01").strip() or "2023-06-01"
        anthropic_beta = os.environ.get("ANTHROPIC_BETA", "managed-agents-2026-04-01").strip() or "managed-agents-2026-04-01"

        headers = {
            "x-api-key": api_key,
            "anthropic-version": anthropic_version,
            "anthropic-beta": anthropic_beta,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        for attempt in range(1, max_retries + 1):
            try:
                status, body = _post_json(url=url, headers=headers, payload=payload, timeout=timeout)
                print(f"Session create request succeeded (status={status}).")
                print(body)
                return 0
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                retryable = exc.code >= 500 or exc.code == 429
                print(f"HTTP error on attempt {attempt}/{max_retries}: {exc.code}\n{body}", file=sys.stderr)
                if not retryable or attempt == max_retries:
                    return 1
            except urllib.error.URLError as exc:
                print(f"Network error on attempt {attempt}/{max_retries}: {exc}", file=sys.stderr)
                if attempt == max_retries:
                    return 1

            sleep_s = min(2 ** (attempt - 1), 8)
            time.sleep(sleep_s)

        return 1
    except Exception as exc:  # noqa: BLE001 - fail fast in automation
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

