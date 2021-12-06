import base64
import datetime
import json
import time


class GameState:
    def __init__(self):
        self.flags = {}
        self.room_id = '0000_start'
        self.last_changed = ''

    def is_set(self, flag_key):
        if flag_key.startswith('~'):
            return not self.flags.get(flag_key[1:], False)
        return self.flags.get(flag_key, False)

    def _change(self):
        self.last_changed = str(datetime.datetime.now())

    def set_flag(self, flag_key):
        if flag_key.startswith('~'):
            self.flags[flag_key[1:]] = False
            self._change()
        else:
            self.flags[flag_key] = True
            self._change()

    def set_room(self, room_id):
        self.room_id = room_id
        self._change()

    def serialize(self):
        return json.dumps(dict(
            last_changed=self.last_changed,
            flags=self.flags,
            room_id=self.room_id
        ))

    @classmethod
    def deserialize(cls, serialized):
        gamestate = cls()
        record = base64.b64decode(serialized).decode('utf-8')
        j = json.loads(record)
        gamestate.last_changed = j.last_changed
        gamestate.flags = j.flags
        gamestate.room_id = j.room_id
        return gamestate
