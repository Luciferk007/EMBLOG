from app.modules.can.service import CANService

service = CANService()

decoded_messages = service.decode_log(
    "app/modules/can/sample_data/candump.log",
    "app/modules/can/sample_data/vehicle.dbc",
)

for message in decoded_messages:
    print(message)