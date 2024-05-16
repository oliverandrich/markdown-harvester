# type: ignore

import nox
import tomlkit

with open("pyproject.toml", "rb") as f:
    project_data = tomlkit.parse(f.read())["project"]

    # Read supported Python versions from pyproject.toml
    python_versions = []
    for classifier in project_data["classifiers"]:
        if "Programming Language" in classifier and "Python" in classifier:
            split_classifier = classifier.split("::")
            if len(split_classifier) == 3:
                python_versions.append(split_classifier[2].strip())


@nox.session(python=python_versions)
def run_testsuite(session):
    if session.venv_backend == "uv":
        session.install("-r", "pyproject.toml", "--extra", "test", ".")
    else:
        session.install(".[test]")
    session.run("pytest", "--cov", "--cov-append", "--cov-report=")
