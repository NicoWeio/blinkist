import threading

from rich.console import Console
from rich.live import Live
from rich.progress import (BarColumn, MofNCompleteColumn, Progress,
                           SpinnerColumn, TimeRemainingColumn)

console = Console()

_job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    MofNCompleteColumn(),
    TimeRemainingColumn(),
)


def track(iterable, description="Working..."):
    """
    An alternative to rich.progress.track that allows multiple progress bars to be displayed at once.
    """
    my_job = _job_progress.add_task(description, total=len(iterable))
    for i in iterable:
        yield i
        _job_progress.update(my_job, advance=1)
    _job_progress.remove_task(my_job)


track_context = Live(_job_progress, refresh_per_second=10, console=console)


def status(message):
    """
    A context manager that displays a status message while the context is active.
    """
    class Status:
        def __enter__(self):
            self.job = _job_progress.add_task(description=message, total=0)

        def __exit__(self, exc_type, exc_val, exc_tb):
            _job_progress.remove_task(self.job)

    return Status()


def status_when_stalled(message, delay_seconds=5):
    """
    Displays a status message if the context is active for longer than a moment (as defined by delay_seconds).
    """
    class Status:
        def __enter__(self):
            self.job = None
            self.timer = threading.Timer(delay_seconds, self.show_status)
            self.timer.start()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.timer.cancel()
            if self.job is not None:
                _job_progress.remove_task(self.job)

        def show_status(self):
            self.job = _job_progress.add_task(description=message, total=0)

    return Status()
