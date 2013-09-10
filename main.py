from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from pyobjus import autoclass


class Ball(Widget):
    
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PyobjusGame(Widget):

    ball = ObjectProperty(None)
    Bridge = ObjectProperty(None)
    screen = ObjectProperty(autoclass('UIScreen').mainScreen())
    bridge = ObjectProperty(None)
    sensitivity = ObjectProperty(50)

    def __init__(self, *args, **kwargs):
        super(PyobjusGame, self).__init__()
        self.Bridge = autoclass('bridge')
        UIScreen = autoclass('UIScreen')
        self.bridge = self.Bridge.alloc().init()
        self.bridge.startAccelerometer()
        self.width = self.screen.bounds.size.width
        self.height = self.screen.bounds.size.height

    def update(self, dt):
        self.ball.move()
        self.ball.velocity_x = self.bridge.ac_x * self.sensitivity
        self.ball.velocity_y = self.bridge.ac_y * self.sensitivity

        if (self.ball.y < 0) or (self.ball.top >= self.height):
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.right >= self.width):
            self.ball.velocity_x *= -1


class PyobjusBallApp(App):
    
    def build(self):
        game = PyobjusGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PyobjusBallApp().run()
