from app.modules.can.dbc_parser import DBCParser

parser = DBCParser()

database = parser.parse_file(
    "app/modules/can/sample_data/vehicle.dbc"
)

for message in database.messages.values():

    print(f"\nMessage: {message.name}")
    print(f"Signal Count: {len(message.signals)}")

    for signal in message.signals:
        print(signal.name)