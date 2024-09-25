from managers import Game_Manager

class Base():
    def __init__(self, layer):
        self.layer = layer
        Game_Manager.draw[self.layer].append(self.draw)
        Game_Manager.event.append(self.event)
        Game_Manager.process.append(self.process)

    def event(self, event):
        pass
    
    def destroy(self):
        Game_Manager.draw[self.layer].remove(self.draw)
        Game_Manager.event.remove(self.event)
        Game_Manager.process.remove(self.process)

    def process(self):
        pass
    
    def draw(self, screen):
        pass

class Player(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Bomb(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Walls(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Bullet(Base):
    def __init__(self):
        super().__init__(layer = 1)


class Lives_Text(Base):
    def __init__(self):
        super().__init__(layer = 2)

