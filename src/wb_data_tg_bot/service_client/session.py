from requests import Session


class ServiceSession(Session):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers.update({
            "Accept": "application/json",
        })
