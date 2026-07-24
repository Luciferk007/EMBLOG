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

print("\nValue Tables")

database = DBCParser().parse_file(
    "app/modules/can/sample_data/vehicle.dbc"
)

signal = database.messages[2015].signals[0]

print(signal.value_table)