import os
import httpx
import yaml
import sys

def main():
    checks = []
    
    # 1. openenv.yaml exists + required fields
    has_yaml = os.path.exists("openenv.yaml")
    if has_yaml:
        with open("openenv.yaml") as f:
            data = yaml.safe_load(f)
            checks.append(("openenv.yaml valid", "name" in data and "tasks" in data))
    else:
        checks.append(("openenv.yaml exists", False))
        
    # Check server
    try:
        r = httpx.get("http://localhost:7860/health")
        checks.append(("GET /health returns 200", r.status_code == 200))
        
        r2 = httpx.get("http://localhost:7860/tasks")
        checks.append(("GET /tasks returns 3 Configs", r2.status_code == 200 and len(r2.json()) == 3))
    except:
        checks.append(("Server running", False))
        
    # File checks
    checks.append(("Dockerfile exists", os.path.exists("Dockerfile")))
    checks.append(("inference.py exists", os.path.exists("inference.py")))
    checks.append((".env.example exists", os.path.exists(".env.example")))
    checks.append(("README.md exists", os.path.exists("README.md")))
    
    passed = sum(1 for c in checks if c[1])
    print(f"--- ContractEnv Pre-submission Checklist ---")
    for name, status in checks:
        color = "\033[92mPASS\033[0m" if status else "\033[91mFAIL\033[0m"
        print(f"[{color}] {name}")
        
    print(f"\n{passed}/{len(checks)} checks passed.")
    if passed == len(checks):
        print("Ready to submit!")
    else:
        print("Please fix the failures before submitting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
