import pygame

NOT_STARTED = -1
STARTED = 0
HIT_DELAY = 200


class Battle:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
        self.turn = 1
        self.state = NOT_STARTED

    def draw(self, surface):
        if self.state == NOT_STARTED:
            return
        self.team1.draw(surface)
        self.team2.draw(surface)
        if len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
            pygame.draw.line(surface, (255, 0, 0), self.team1.sprites()[0].rect.midright,
                             self.team2.sprites()[0].rect.midleft, 3)

            hit_circle = pygame.Surface((self.team1.sprites()[0].rect.width, self.team1.sprites()[0].rect.height),
                                        pygame.SRCALPHA)
            pygame.draw.circle(hit_circle, (255, 0, 0, 100), hit_circle.get_rect().center,
                               hit_circle.get_rect().width // 2 - 5, 0)

            if self.turn == 1:
                surface.blit(hit_circle, self.team2.sprites()[0].rect.topleft)
            else:
                surface.blit(hit_circle, self.team1.sprites()[0].rect.topleft)

    def start(self, trainer1, trainer2):
        if self.state == NOT_STARTED:
            self.trainer1 = trainer1
            self.trainer2 = trainer2
            self.team1 = pygame.sprite.Group()
            self.team1.add(trainer1.best_team(self.n))
            self.team2 = pygame.sprite.Group()
            self.team2.add(trainer2.best_team(self.n))
            if len(self.team1) < self.n or len(self.team2) < self.n:
                return

            y = self.y
            for pokemon in self.team1:
                pokemon.rect.topleft = (self.x, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            y = self.y
            for pokemon in self.team2:
                pokemon.rect.topleft = (self.x + 280, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            self.state = STARTED
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.state == STARTED:
            nowTime = pygame.time.get_ticks()
            if nowTime - self.last_update > HIT_DELAY:
                self.last_update = nowTime
            else:
                return
            if self.turn == 1 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team1.sprites()[0].attack(self.team2.sprites()[0])
                if self.team2.sprites()[0].hp <= 0:
                    self.team2.remove(self.team2.sprites()[0])
                if len(self.team2.sprites()) == 0:
                    return self.finish(1)
            elif self.turn == 2 and len(self.team1.sprites()) > 0 and len(self.team2.sprites()) > 0:
                self.team2.sprites()[0].attack(self.team1.sprites()[0])
                if self.team1.sprites()[0].hp <= 0:
                    self.team1.remove(self.team1.sprites()[0])
                if len(self.team1.sprites()) == 0:
                    return self.finish(2)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.team1.update()
            self.team2.update()

    def finish(self, result):
        self.state = NOT_STARTED
        for p in self.team1:
            self.trainer1.add(p)
        for p in self.team2:
            self.trainer2.add(p)
        if result == 1:
            self.trainer1.wins += 1
        else:
            self.trainer2.wins += 1

    def started(self):
        return True if self.state == STARTED else False
