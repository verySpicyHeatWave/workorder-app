class TaskItem:
    def __init__(this, taskNo: int, summary: str, ref: str, index: int) -> None:
        if not taskNo:
            taskNo = 0
        this.number: int = taskNo
        this.summary: str = summary
        this.reference: str = ref
        this.planned_row: int = index
        this.actuals_row: int = index + 17