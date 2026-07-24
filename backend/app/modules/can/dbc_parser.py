from pathlib import Path

from app.modules.can.dbc_models import (
    DBCDatabase,
    DBCMessage,
    DBCSignal,
)

class DBCParser:

    def __init__(self):
        pass
    def parse_file(self, file_path: str) -> DBCDatabase:
        """
        Parse an entire DBC file.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        database = DBCDatabase()

        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        current_message = None

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line.startswith("BO_"):

                current_message = self._parse_message(line)

                database.messages[current_message.can_id] = current_message
            
            if line.startswith("SG_") and current_message is not None:

                signal = self._parse_signal(line)

                current_message.signals.append(signal)
            if line.startswith("VAL_"):
                self._parse_value_table(line,database,)

        return database
    
    def _parse_message(self, line: str) -> DBCMessage:
        """
        Parse a BO_ message definition.
        """

        tokens = line.split()

        can_id = int(tokens[1])

        name = tokens[2].rstrip(":")

        dlc = int(tokens[3])

        transmitter = tokens[4]

        return DBCMessage(
            can_id=can_id,
            name=name,
            dlc=dlc,
            transmitter=transmitter,
        )
    
    def _parse_signal(self, line: str) -> DBCSignal:
        """
        Parse an SG_ signal definition.
        """

        tokens = line.split()

        name = tokens[1]

        bit_info = tokens[3]

        start_bit = int(bit_info.split("|")[0])

        length = int(bit_info.split("|")[1].split("@")[0])

        byte_order = bit_info.split("@")[1][0]

        value_type = bit_info.split("@")[1][1]

        factor_offset = tokens[4].strip("()")

        factor = float(factor_offset.split(",")[0])

        offset = float(factor_offset.split(",")[1])

        minimum_maximum = tokens[5].strip("[]")

        minimum = float(minimum_maximum.split("|")[0])

        maximum = float(minimum_maximum.split("|")[1])

        unit = tokens[6].strip('"')

        return DBCSignal(
            name=name,
            start_bit=start_bit,
            length=length,
            byte_order=byte_order,
            value_type=value_type,
            factor=factor,
            offset=offset,
            minimum=minimum,
            maximum=maximum,
            unit=unit,
        )
    def _parse_value_table(self,line: str,database: DBCDatabase,) -> None:
        """
        Parse VAL_ definitions.
        """

        tokens = line.split()

        can_id = int(tokens[1])

        signal_name = tokens[2]

        message = database.messages.get(can_id)

        if message is None:
            return

        signal = None

        for s in message.signals:

            if s.name == signal_name:
                signal = s
                break

        if signal is None:
            return

        i = 3

        while i < len(tokens) - 1:

            if tokens[i] == ";":
                break

            value = int(tokens[i])

            text = tokens[i + 1].replace('"', "").replace(";", "")

            signal.value_table[value] = text

            i += 2