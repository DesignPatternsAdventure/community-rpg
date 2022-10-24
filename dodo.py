"""doit Script.

```py
# Ensure that packages are installed
poetry install
# List Tasks
poetry run doit list
# (Or use a poetry shell)
# > poetry shell
# (shell) doit list

# Run tasks individually (examples below)
(shell) doit run test
(shell) doit run test check
# Or all of the tasks in DOIT_CONFIG
(shell) doit
```

"""

from pattern_feedback_tool.doit_tasks import * # noqa: F401
