import logging.config
import pprint
from logging import INFO, getLogger
from pathlib import Path

import orjson
from misskey import Misskey as Mk

logger = getLogger(__name__)
logger.setLevel(INFO)


class MisskeyManager:
    instance_name: str
    token: str
    misskey: Mk

    def __init__(self, instance_name: str, token: str) -> None:
        self.instance_name = instance_name
        self.token = token
        self.misskey = Mk(instance_name, i=token)
        self.misskey.timeout = 120

    @property
    def user_dict(self) -> dict:
        if hasattr(self, "_user_dict"):
            return self._user_dict
        self._user_dict = self.misskey.i()
        return self._user_dict

    def _run(self, path: str, params: dict = {}) -> list[dict] | dict | bool:
        response = self.misskey._Misskey__request_api(path, **params)
        return response

    def notes_with_reactions(self, limit: int = 100, last_since_id: str = "") -> list[dict]:
        user_dict = self.user_dict
        user_id = user_dict["id"]
        # https://misskey-hub.net/docs/api/endpoints/users/reactions.html
        params = {
            "userId": str(user_id),
            "limit": int(limit),
        }
        if last_since_id != "":
            params["sinceId"] = str(last_since_id)

        reaction_dict = self._run("users/reactions", params)
        return reaction_dict


if __name__ == "__main__":
    logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)
    config_path: Path = Path("./config/config.json")
    config_dict = orjson.loads(config_path.read_bytes())
    instance_name = config_dict["misskey"]["instance"]
    token = config_dict["misskey"]["token"]
    misskey = MisskeyManager(instance_name, token)
    response = misskey.notes_with_reactions()
    pprint.pprint(response)
