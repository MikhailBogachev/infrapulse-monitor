"""Submit isolated foundation tasks and print their correlation IDs."""

from uuid import uuid4

from infrapulse.worker import QUEUES, app


def main() -> None:
    for lane in QUEUES:
        task_id = str(uuid4())
        app.send_task(f"infrapulse.smoke.{lane}", task_id=task_id, mandatory=True, retry=False)
        print(task_id)


if __name__ == "__main__":
    main()
