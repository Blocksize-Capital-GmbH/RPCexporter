from exporter.jsonRPCRequest import JsonRPCRequest


def test_to_json_empty_params():
    request = JsonRPCRequest(method="getSlot", params=[])
    serialized = request.to_json()
    assert serialized == {"jsonrpc": "2.0", "id": 1, "method": "getSlot", "params": []}


def test_to_json_no_params():
    request = JsonRPCRequest(method="getSlot", params=None)
    serialized = request.to_json()
    assert serialized == {"jsonrpc": "2.0", "id": 1, "method": "getSlot", "params": []}
