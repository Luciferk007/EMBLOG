from pathlib import Path

from app.modules.can.parser import CANParser


def test_parse_file():
    parser = CANParser()

    sample_file = (
        Path(__file__).parent.parent / "sample_data" / "candump.log"
    )

    frames = parser.parse_file(str(sample_file))

    assert len(frames) == 3
    assert frames[0].interface == "can0"
    assert frames[0].can_id == "123"
    assert frames[0].dlc == 8
    assert frames[0].data == [17, 34, 51, 68, 85, 102, 119, 136]


def test_invalid_file():
    parser = CANParser()

    try:
        parser.parse_file("invalid.log")
        assert False
    except FileNotFoundError:
        assert True