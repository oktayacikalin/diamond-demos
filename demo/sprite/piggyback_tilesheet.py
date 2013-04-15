from json import load
from collections import OrderedDict
from os.path import splitext, dirname, join


locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
filename = join(dirname(__file__), filename)

autotiles = load(open('%s.autotiles.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict)
for at_group, at_sprites in autotiles.iteritems():
    autotiles[at_group] = OrderedDict([(':%s:%s' % (at_group, name), action) for name, action in at_sprites.iteritems()])
    sprites.update(autotiles[at_group])
