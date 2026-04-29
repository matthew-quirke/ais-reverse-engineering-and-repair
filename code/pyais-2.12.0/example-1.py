from pyais.encode import encode_dict
from pyais.messages import MessageType1

# This statement tells us which fields can be set for messages of type 1
print(MessageType1.fields())

# A dictionary of fields that we want to encode
# Note that you can pass many more fields for type 1 messages, but we let pyais
# use default values for those keys
data = {
    'course': 219.3,
    'lat': 17.771015,
    'lon': 177.1859367,
    'mmsi': '366053209',
    'type': 1
}

# This creates an encoded AIS message
# Note, that `encode_dict` returns always a list of fragments.
# This is done, because you may never know if a message fits into the 82 character
# size limit of payloads
encoded = encode_dict(data)
print(encoded)

# You can also change the NMEA fields like the radio channel:
print(encode_dict(data, radio_channel="B"))
