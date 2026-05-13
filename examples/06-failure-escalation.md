# Example 06: Failure Escalation

## The Protocol

**Never retry blindly. Follow this ladder:**

### 1st failure: Read the error

```
$ python3 my_script.py
Traceback: ModuleNotFoundError: No module named 'requests'
```

Action: The error is clear. Install the missing module. Do NOT retry the same command.

### 2nd failure: Probe the environment

```
$ pip install requests
Permission denied
```

Action: Check who owns the environment, what Python version is active, and whether
there's a virtual environment. Run `which python3`, `ls -la .venv/`, `pip --version`.

### 3rd failure: Switch strategy or ask

```
$ source .venv/bin/activate
bash: .venv/bin/activate: No such file or directory
```

Action: The environment does not exist. Either create it, or switch to system Python.
If unsure, ask the user: "There is no .venv. Should I create one or use the system Python?"

## What NOT to do

- ❌ Run the same failing command 3+ times hoping it works
- ❌ Claim a tool is missing before verifying with `command -v`
- ❌ Kill processes unconditionally (`killall python` may kill the agent itself)
- ❌ Overwrite config files without reading them first

## Good escalation log

```
Attempt 1: pip install requests → Permission denied
Probe: Python is system-wide (3.12.13), no .venv exists
Attempt 2: pip install --user requests → Success
Verify: python3 -c 'import requests' → OK
```
