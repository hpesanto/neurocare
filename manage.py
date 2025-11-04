#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neurocare_project.settings")
    # Optional: attach VS Code debugger when NEUROCARE_DEBUGPY env var is set.
    # Start the server with --noreload when using this to avoid the autoreloader
    # spawning child processes that won't wait_for_client.
    if os.environ.get("NEUROCARE_DEBUGPY"):
        try:
            import debugpy

            port = int(os.environ.get("NEUROCARE_DEBUGPY_PORT", 5678))
            debugpy.listen(("0.0.0.0", port))
            print(f"debugpy listening on 0.0.0.0:{port} — not waiting for client")
        except Exception as exc:
            print("Could not start debugpy:", exc)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
