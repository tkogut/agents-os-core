import os
import sys
import subprocess
import shutil
import getpass
import json
import glob

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bootstrap_zed.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    try:
        user = getpass.getuser()
    except KeyError:
        user = os.environ.get('USER', os.environ.get('USERNAME', 'user'))

    # Path to the projects directory in the user's home
    projects_dir = os.path.expanduser("~/projects")
    project_path = os.path.join(projects_dir, project_name)

    # SEC-01: Path Sanitization (Directory Traversal Prevention & Builder isolation)
    real_projects_dir = os.path.realpath(projects_dir)
    real_project_path = os.path.realpath(project_path)
    try:
        common = os.path.commonpath([real_projects_dir, real_project_path])
        if common != real_projects_dir or real_project_path == real_projects_dir:
            raise ValueError()
    except ValueError:
        print(f"❌ ERROR: Project path '{real_project_path}' is outside the allowed workspace: '{real_projects_dir}'", file=sys.stderr)
        sys.exit(1)

    print(f"--- Bootstrapping Zed project: {project_name} ---")

    try:
        # a) Create project structure
        print(f"Creating directory structure at: {real_project_path}")
        os.makedirs(os.path.join(real_project_path, ".agents"), exist_ok=True)
        os.makedirs(os.path.join(real_project_path, "src"), exist_ok=True)
        print(" -> Structure created successfully.")

        # b) Initialize git repository
        print("Initializing Git repository...")
        _ = subprocess.run(["git", "init"], cwd=real_project_path, check=True, capture_output=True)
        print(" -> Git repository initialized.")

        # Ensure local git identity is configured to prevent commit failures in sandboxes
        has_user_name = False
        has_user_email = False
        try:
            res_name = subprocess.run(["git", "config", "user.name"], cwd=real_project_path, capture_output=True, text=True)
            if res_name.returncode == 0 and res_name.stdout.strip():
                has_user_name = True
        except Exception:
            pass

        try:
            res_email = subprocess.run(["git", "config", "user.email"], cwd=real_project_path, capture_output=True, text=True)
            if res_email.returncode == 0 and res_email.stdout.strip():
                has_user_email = True
        except Exception:
            pass

        if not has_user_name or not has_user_email:
            print("   ⚙️ Unconfigured Git user identity detected. Configuring locally for this repository...")
            if not has_user_name:
                subprocess.run(["git", "config", "--local", "user.name", user], cwd=real_project_path, check=True)
            if not has_user_email:
                subprocess.run(["git", "config", "--local", "user.email", f"{user}@users.noreply.github.com"], cwd=real_project_path, check=True)
            print("   -> Git identity set successfully.")

        # c) Create hidden root commit
        print("Creating initial root commit...")
        _ = subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "chore: initial commit", "--no-verify"],
            cwd=real_project_path,
            check=True,
            capture_output=True
        )
        print(" -> Root commit created.")

        # d) Create .zed/ and copy settings
        zed_dir = os.path.join(real_project_path, ".zed")
        os.makedirs(zed_dir, exist_ok=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_root = os.path.dirname(script_dir) # execution -> agents-os-core worktree root

        # Load and validate settings template to prevent exfiltration (Zero-Leak Policy)
        settings_template = os.path.join(core_root, "templates", "zed_project_settings.json")
        destination_settings = os.path.join(zed_dir, "settings.json")

        print(f"Copying and validating Zed settings template from {settings_template}...")

        settings = {}
        if os.path.exists(settings_template):
            try:
                with open(settings_template, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except Exception as e:
                print(f"⚠️ Template load failed: {e}. Generating compliant defaults...")
        else:
            print(f"⚠️ Template not found at {settings_template}. Generating compliant defaults...")

        # Strict exfiltration blocking: Nested Telemetry structure & AI Privacy
        if "telemetry" not in settings or not isinstance(settings["telemetry"], dict):
            settings["telemetry"] = {}
        settings["telemetry"]["diagnostics"] = False
        settings["telemetry"]["metrics"] = False
        settings["ai_privacy"] = "high"

        # Write compliant settings
        with open(destination_settings, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f" -> Compliant settings successfully written to {destination_settings}")

        # e) Open project in Zed
        # Format for Windows UNC path to access WSL filesystem dynamically
        distro = os.environ.get("WSL_DISTRO_NAME", "Ubuntu")
        # Split project_path into individual components and join using backslashes for Windows UNC
        path_parts = [p for p in real_project_path.split("/") if p]
        windows_path = f"\\\\wsl.localhost\\{distro}\\" + "\\".join(path_parts)

        print(f"Opening project in Zed: {windows_path}")

        # Robust, cross-platform launcher detection for Zed
        zed_cmd = None
        if shutil.which("zed"):
            zed_cmd = "zed"
        elif shutil.which("zed.exe"):
            zed_cmd = "zed.exe"
        else:
            # Check standard Windows AppData programs locations
            for path in glob.glob("/mnt/c/Users/*/AppData/Local/Programs/Zed/bin/zed.exe"):
                if os.path.exists(path):
                    zed_cmd = path
                    break

            if not zed_cmd:
                # Check standard Program Files locations
                for path in ["/mnt/c/Program Files/Zed/bin/zed.exe", "/mnt/c/Program Files/Zed/Zed.exe"]:
                    if os.path.exists(path):
                        zed_cmd = path
                        break

        if not zed_cmd:
            print("⚠️ WARNING: Zed executable was not found in the PATH or standard Windows directories.", file=sys.stderr)
            print(f"Please open the project manually in Zed at: {windows_path}", file=sys.stderr)
        else:
            print(f" -> Launching Zed using executable: {zed_cmd}")
            _ = subprocess.run([zed_cmd, windows_path], check=True)
            print(" -> Zed launched successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during a subprocess call: {e}", file=sys.stderr)
        if e.stdout is not None:
            print(f"STDOUT: {e.stdout.decode()}", file=sys.stderr)
        if e.stderr is not None:
            print(f"STDERR: {e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- Project '{project_name}' successfully initialized for Zed. ---")

if __name__ == "__main__":
    main()
