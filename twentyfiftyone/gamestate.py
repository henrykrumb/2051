import base64
import json


class GameState:
    def __init__(self):
        self.flags = {}
        self.room_id = '0000_start'

    def is_set(self, flag_key):
        if flag_key.startswith('~'):
            return not self.flags.get(flag_key[1:], False)
        return self.flags.get(flag_key, False)

    def set_flag(self, flag_key):
        if flag_key.startswith('~'):
            self.flags[flag_key[1:]] = False
        else:
            self.flags[flag_key] = True

    def serialize(self):
        return json.dumps(dict(
            flags=self.flags,
            room_id=self.room_id
        ))

    @classmethod
    def deserialize(cls, serialized):
        gamestate = cls()
        record = base64.b64decode(serialized).decode('utf-8')
        j = json.loads(record)
        gamestate.flags = j.flags
        gamestate.room_id = j.room_id
        return gamestate
