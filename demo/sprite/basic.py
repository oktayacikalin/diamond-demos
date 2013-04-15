#!/usr/bin/env python
'''
Demonstrates how to display a sprite out of a vault. For easier future updates
we are using a sprite sheet which has been built using the tilesheet_maker.py.

Note:
A sprite sheet is nothing more than a normal sprite vault but split into two
parts (.py and .json file). You could always put everything into the .py file
but you will have to manually update the sprite data and cannot use the
tilesheet_maker.py anymore.
You could also modify the .py file in a way that it will include and merge other
sprite data so that you can combine both worlds. The tilesheet_maker.py will
never modify an existing .py file, but it will always overwrite the .json file.
'''

import sys
import os

# Make sure that our diamond engine can be found.
sys.path.insert(0, os.path.abspath('../../'))

from diamond.scene import SceneManager, Scene
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps
from diamond.sprite import Sprite

import basic_spritesheet


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'framerate': 60,
    # 'scaling': 1.5,  # 1.0 is normal; 2.0 would be double window size.
}


class SpriteScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.add_to(fps_node)
        fps.set_align_box(DISPLAY_LAYOUT['screen_size'][0], 0, 'right')

    def setup(self):
        super(SpriteScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.bind(self.ticker)
        self.__setup_fps()

        sprite = Sprite.make(basic_spritesheet)
        sprite.set_align_box(*DISPLAY_LAYOUT['screen_size'])
        sprite.add_to(self.root_node)


def main():
    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Basic Sprite Example')
    manager.add_scene(SpriteScene, scene_id='main')
    manager.run('main')


if __name__ == '__main__':
    main()
