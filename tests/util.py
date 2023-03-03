import contextlib
import os
import shlex
import shutil
import subprocess
from typing import Any, Iterator, Mapping


@contextlib.contextmanager
def generate_temporary_project(
    cookies: Any, **kwargs: Mapping[Any, Any]
) -> Iterator[Any]:
    try:
        result = cookies.bake(**kwargs)
        yield result
    finally:
        shutil.rmtree(str(result.project))


@contextlib.contextmanager
def inside_directory_of(result: Any) -> Iterator[None]:
    old_dir = result.project.chdir()
    yield
    os.chdir(old_dir)


def check_output_in_result_dir(command: str, result: Any) -> str:
    """Run the given command in the directory of `result`.

    The `command` parameter should be a string, while `result` is the
    object generated by the `cookies` PyTest fixture, an object of type
    `pytest_cookies.Result`. The type annotation is `Any`, because
    `pytest_cookies` is missing type annotations and `mypy` cannot deal with
    that.
    If the command returns with a non-zero code, this function raises an
    exception.
    Returns the combined stdout and stderr outputs.
    """
    with inside_directory_of(result):
        output = subprocess.check_output(
            shlex.split(command), stderr=subprocess.STDOUT
        )
    return str(output)
