import os
import sys
import subprocess
import shutil
import getpass

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

    print(f"--- Bootstrapping Zed project: {project_name} ---")

    try:
        # a) Create project structure
        print(f"Creating directory structure at: {project_path}")
        os.makedirs(os.path.join(project_path, ".agents"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "src"), exist_ok=True)
        print(" -> Structure created successfully.")

        # b) Initialize git repository
        print("Initializing Git repository...")
        subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
        print(" -> Git repository initialized.")

        # c) Create hidden root commit
        print("Creating initial root commit...")
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "chore: initial commit", "--no-verify"],
            cwd=project_path,
            check=True,
            capture_output=True
        )
        print(" -> Root commit created.")

        # d) Create .zed/ and copy settings
        zed_dir = os.path.join(project_path, ".zed")
        os.makedirs(zed_dir, exist_ok=True)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_root = os.path.dirname(os.path.dirname(script_dir)) #execution -> agents-os-core -> worktree root
        
        # This assumes the script is run from within the worktree structure
        settings_template = os.path.join(core_root, "templates", "zed_project_settings.json")
        destination_settings = os.path.join(zed_dir, "settings.json")
        
        print(f"Copying Zed settings template from {settings_template}...")
        shutil.copyfile(settings_template, destination_settings)
        print(f" -> Settings copied to {destination_settings}")

        # e) Open project in Zed
        # Format for Windows UNC path to access WSL filesystem
        windows_path = f"\\\\wsl.localhost\\Ubuntu\\home\\{user}\\projects\\{project_name}"
        print(f"Opening project in Zed: {windows_path}")
        subprocess.run(["zed", windows_path], check=True)
        print(" -> Zed launched successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during a subprocess call: {e}", file=sys.stderr)
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode()}", file=sys.stderr)
        if e.stderr:
            print(f"STDERR: {e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- Project '{project_name}' successfully initialized for Zed. ---")

if __name__ == "__main__":
    main()
