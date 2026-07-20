from app.modules.can.parser import CANParser
from app.modules.can.dbc_parser import DBCParser
from app.modules.can.decoder import CANDecoder

frames = CANParser().parse_file(
    "app/modules/can/sample_data/candump.log"
)

database = DBCParser().parse_file(
    "app/modules/can/sample_data/vehicle.dbc"
)

decoder = CANDecoder(database)

for frame in frames:
    decoded = decoder.decode_frame(frame)

    print(decoded)