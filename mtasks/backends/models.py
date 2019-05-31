from datetime import datetime
from typing import AnyStr


class ActorTask:
    createAt: datetime = None
    updateAt: datetime = None
    taskName: AnyStr
    taskID: AnyStr
    taskStatus: int
    taskInfo: Dict = None
    taskResult: Dict = None

    def to_dict(self):
        _dict = {
            'createAt': self.createAt,
            'updateAt': self.updateAt,
            'taskName': self.taskName,
            'taskID': self.taskID,
            'taskStatus': self.taskStatus,
            'taskInfo': self.taskInfo,
            'taskResult': self.taskResult,
        }
        return _dict



