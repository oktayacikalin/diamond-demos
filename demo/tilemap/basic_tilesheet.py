from os.path import dirname, join


filename = join(dirname(__file__), 'basic_tiles.png')

sprites = {
    #                            rect        ,    hotspot,  delta, msecs
    'gw_001': {'none': [[(  0,   0,  64,  64), (  0,   0), (0, 0), 60]]},
    'gw_002': {'none': [[( 64,   0,  64,  64), ( 64,   0), (0, 0), 60]]},
    'gw_003': {'none': [[(128,   0,  64,  64), (128,   0), (0, 0), 60]]},
    'gw_004': {'none': [[(  0,  64,  64,  64), (  0,  64), (0, 0), 60]]},
    'gw_005': {'none': [[( 64,  64,  64,  64), ( 64,  64), (0, 0), 60]]},
    'gw_006': {'none': [[(128,  64,  64,  64), (128,  64), (0, 0), 60]]},
    'gw_007': {'none': [[(  0, 128,  64,  64), (  0, 128), (0, 0), 60]]},
    'gw_008': {'none': [[( 64, 128,  64,  64), ( 64, 128), (0, 0), 60]]},
    'gw_009': {'none': [[(128, 128,  64,  64), (128, 128), (0, 0), 60]]},

    'ge_001': {'none': [[(256,   0,  64,  64), (256,   0), (0, 0), 60]]},
    'ge_002': {'none': [[(320,   0,  64,  64), (320,   0), (0, 0), 60]]},
    'ge_003': {'none': [[(384,   0,  64,  64), (384,   0), (0, 0), 60]]},
    'ge_004': {'none': [[(256,  64,  64,  64), (256,  64), (0, 0), 60]]},
    'ge_005': {'none': [[(320,  64,  64,  64), (320,  64), (0, 0), 60]]},
    'ge_006': {'none': [[(384,  64,  64,  64), (384,  64), (0, 0), 60]]},
    'ge_007': {'none': [[(256, 128,  64,  64), (256, 128), (0, 0), 60]]},
    'ge_008': {'none': [[(320, 128,  64,  64), (320, 128), (0, 0), 60]]},
    'ge_009': {'none': [[(384, 128,  64,  64), (384, 128), (0, 0), 60]]},

    'green1': {'none': [[(512,   0,  64,  64), (512,   0), (0, 0), 60]]},
}

tile_size = (64, 64)
