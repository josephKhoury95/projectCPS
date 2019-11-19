"""
toy utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

sqlite uses float keyword and cpppo use REAL keyword.

if ACTUATORX is 1 then is ON otherwise is OFF.
"""

from minicps.utils import build_debug_logger

toy_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

# IP = {
#     'plc1': '10.0.0.1',
#     'plc2': '10.0.0.2',
#     'scada': '10.0.0.3',
# }

# CO_0_2a = ('CO', 1, '2a')
# HR_0_2a = ('HR', 1, '2a')

CO_0_2a = ('CO', 1)
HR_0_2a = ('HR', 1)

DI_0_2a = ('DI', 1)
IR_0_2a = ('IR', 1)

# IP = {
#     'plc1': '192.168.1.1',
#     'scada_ser': '192.168.1.4',
# }

IP = {
    'eml_server':       '192.168.1.1',
    'web_server':       '192.168.1.2',
    'db_server':        '192.168.1.3',

    'computer1':        '192.168.1.4',
    'computer2':        '192.168.1.5',
    'computer3':        '192.168.1.6',

    'scada_ser':        '192.168.1.7',
    'scada_hmi':        '192.168.1.8',
    'scada_his':        '192.168.1.9',

    'plc1':             '192.168.1.10',
}

# IP = {
#     'eml_server':       '135.1.0.1',
#     'web_server':       '135.1.0.10',
#     'db_server':        '135.1.0.11',
#
#     'computer1':        '135.1.1.1',
#     'computer2':        '135.1.1.10',
#     'computer3':        '135.1.1.11',
#
#     'scada_ser':        '135.1.10.1',
#     'scada_hmi':        '135.1.10.10',
#     'scada_his':        '135.1.10.11',
#
#     'plc1':             '135.1.11.1',
# }

# MAC = {
#     'plc1': '00:00:00:00:00:01',
#     'plc2': '00:00:00:00:00:02',
#     'rtu1': '00:00:00:00:00:03',
#     'scada': '00:00:00:00:00:04',
# }

MAC = {
    'eml_server':       '77:72:04:c2:09:1e',
    'web_server':       '42:05:a7:c8:fc:a0',
    'db_server':        'cf:95:c3:04:b0:c5',

    'computer1':        'ff:40:ad:e0:4d:54',
    'computer2':        'a9:bc:0e:6b:d3:b1',
    'computer3':        '0f:38:a6:64:83:9d',

    'scada_ser':        'ba:65:29:71:fd:9d',
    'scada_hmi':        'ad:36:a5:19:3b:ed',
    'scada_his':        '4e:52:c4:12:77:f9',

    'plc1':             'f5:8e:ca:8c:ac:f0',
}



# others
PLC1_DATA = {
    'SENSOR1': '0',
    'SENSOR2': '0.0',
    'SENSOR3': '0',
    'ACTUATOR1': '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2': '0',
}

# PLC2_DATA = {
#     'SENSOR3': '0'  # interlock with PLC1
# }


# protocol
# PLC1_MAC = '00:00:00:00:00:01'
PLC1_TAGS = (
    ('SENSOR1', 1, 'INT'),
    ('SENSOR2', 1, 'REAL'),
    ('SENSOR3', 1, 'INT'),  # interlock with PLC2
    ('ACTUATOR1', 1, 'INT'),  # 0 means OFF and 1 means ON
    ('ACTUATOR2', 1, 'INT'))
# PLC1_TAGS = (
#     ('flag1', 'INT'),
#     ('README', 1, 'STRING'),
# )
# PLC1_ADDR = '10.0.0.1'
PLC1_SERVER = {
    'address': IP['plc1'],
    'tags': PLC1_TAGS
}
PLC1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC1_SERVER
}

# PLC2_MAC = '00:00:00:00:00:02'
# PLC2_ADDR = '10.0.0.2'

# PLC2_TAGS = (
#     ('SENSOR3', 2, 'INT'), )  # interlock with PLC1
# # PLC2_TAGS = (
# #     ('flag1', 'INT'),
# #     ('README', 1, 'STRING'),
#
# PLC2_SERVER = {
#     'address': IP['plc2'],
#     'tags': PLC2_TAGS
# }
# PLC2_PROTOCOL = {
#     'name': 'enip',
#     'mode': 1,
#     'server': PLC2_SERVER
# }

# SCADA_MAC = '00:00:00:00:00:03'
# SCADA_ADDR = '10.0.0.3'
SCADA_TAGS = ()
SCADA_SERVER = {
    'address': IP['scada_ser'],
    'tags': SCADA_TAGS
}
SCADA_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': SCADA_SERVER
}


# RTU1_TAGS = (10, 10, 10, 10)
# RTU1_SERVER = {
#     'address': IP['rtu1'],
#     'tags': RTU1_TAGS
# }
# RTU1_PROTOCOL = {
#     'name': 'modbus',
#     'mode': 1,
#     'server': RTU1_SERVER
# }



NETMASK = '/24'

# state
PATH = 'toy_db.sqlite'
NAME = 'toy_table'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE toy_table (
    name              TEXT NOT NULL,
    datatype          TEXT NOT NULL,
    value             TEXT,
    pid               INTEGER NOT NULL,
    PRIMARY KEY (name, pid)
);
"""
SCHEMA_INIT = """
    INSERT INTO toy_table VALUES ('SENSOR1',   'int', '0', 1);
    INSERT INTO toy_table VALUES ('SENSOR2',   'float', '0.0', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '1', 1);
    INSERT INTO toy_table VALUES ('ACTUATOR1', 'int', '1', 1);
    INSERT INTO toy_table VALUES ('ACTUATOR2', 'int', '0', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '2', 2);
"""
