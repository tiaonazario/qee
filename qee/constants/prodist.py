DRP_LIMIT = 3.0
DRC_LIMIT = 0.5

DTT_95 = 10.0
DTT_P_95 = 2.5
DTT_I_95 = 7.5
DTT_3_95 = 6.5

FD_LIMIT = 3.0

VOLTAGE_RANGE: dict[int, dict[str, int]] = {
    110: {
        'cr-sup': 117,
        'ad-sup': 116,
        'ad-inf': 101,
        'cr-inf': 96,
    },
    120: {
        'cr-sup': 127,
        'ad-sup': 126,
        'ad-inf': 110,
        'cr-inf': 104,
    },
    127: {
        'cr-sup': 135,
        'ad-sup': 133,
        'ad-inf': 117,
        'cr-inf': 110,
    },
    208: {
        'cr-sup': 220,
        'ad-sup': 218,
        'ad-inf': 191,
        'cr-inf': 181,
    },
    215: {
        'cr-sup': 122,
        'ad-sup': 121,
        'ad-inf': 106,
        'cr-inf': 100,
    },
    220: {
        'cr-sup': 233,
        'ad-sup': 231,
        'ad-inf': 202,
        'cr-inf': 191,
    },
    230: {
        'cr-sup': 244,
        'ad-sup': 242,
        'ad-inf': 212,
        'cr-inf': 200,
    },
    240: {
        'cr-sup': 254,
        'ad-sup': 252,
        'ad-inf': 221,
        'cr-inf': 209,
    },
    254: {
        'cr-sup': 269,
        'ad-sup': 267,
        'ad-inf': 234,
        'cr-inf': 221,
    },
    380: {
        'cr-sup': 403,
        'ad-sup': 399,
        'ad-inf': 350,
        'cr-inf': 331,
    },
    440: {
        'cr-sup': 466,
        'ad-sup': 462,
        'ad-inf': 405,
        'cr-inf': 383,
    },
}
