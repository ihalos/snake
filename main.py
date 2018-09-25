import pygame
from random import randint

class Snake(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([80,80])
        self.image.fill([255,255,255])
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.direction = "right"
        self.eat_count = 0
        self.tail = []
        
    def update(self):
        self.update_tail()
        self.update_head()

    def update_head(self):        
        #Update snake head
        if self.direction == "right":
            self.rect = self.rect.move(80, 0)
        elif self.direction == "left":
            self.rect = self.rect.move(-80, 0)
        elif self.direction == "up":
            self.rect = self.rect.move(0, -80)
        elif self.direction == "down":
            self.rect = self.rect.move(0, 80)

    def update_tail(self):
        #Update tail
        if len(self.tail) == 1:
            self.tail[0].update_position(self.rect)           
        elif len(self.tail) > 1:
            for i in range(0, len(self.tail)-1):
                self.tail[len(self.tail)-i-1].update_position(self.tail[len(self.tail)-i-2].get_rect())
            self.tail[0].update_position(self.rect)

    def change_direction(self, dir):
        if self.direction == "right" and dir == "left" or\
           self.direction == "left" and dir == "right" or\
           self.direction == "up" and dir == "down" or\
           self.direction == "down" and dir == "up":
            return
        self.direction = dir

    def increase_speed(self):
        self.speed = self.speed_flat + self.eat_count * 0.1

    def self_collision(self):
        for t in self.tail:
            if(self.rect.colliderect(t.rect)):
                return True
        return False

    def border_collision(self):
        return not self.area.contains(self.rect)

    def get_tail_rect_list(self):
        if len(self.tail) < 1:
            return None
        rect_list = []
        for t in self.tail:
            rect_list.append(t.rect)
        return rect_list

    def eat_collision(self, apple):
        if self.rect.colliderect(apple.rect):
            self.tail.insert(0, Tail(self.rect))
            self.eat_count += 1
            apple.random_position(self.rect, self.get_tail_rect_list())
            return True
        return False

    

class Tail(pygame.sprite.Sprite):

    def __init__(self, rect_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([80,80])
        self.image.fill([0,255,0])
        self.rect = rect_pos
        
    def update_position(self, new_rect_pos):
        if new_rect_pos:
            self.rect = new_rect_pos

    def get_rect(self):
        return self.rect

    def get_direction(self):
        return self.direction


class Apple(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([80,80])
        self.image.fill([255,0,0])
        self.rect = self.image.get_rect()

        #self.random_position()

    def update(self):
        pass

    def random_position(self, snake_head, snake_tail):
        collision_head = self.rect.colliderect(snake_head)
        #if snake_tail is not None:
        collision_tail = self.rect.collidelist(snake_tail)
        while collision_head or collision_tail != -1:
            rand_x = randint(0,9)*80
            rand_y = randint(0,9)*80
            self.rect.x = rand_x
            self.rect.y = rand_y
            collision_head = self.rect.colliderect(snake_head)
            collision_tail = self.rect.collidelist(snake_tail)

def main():
    #Init pygame
    pygame.init()

    #Init screen
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0 #Background colour

    #Init clock and framerate
    clock = pygame.time.Clock()
    frame_rate = 4

    #Init snake
    snake = Snake()

    #Init apple
    apple = Apple()

    #Init sprites
    snakesprite = pygame.sprite.RenderPlain(snake)
    tailsprites = pygame.sprite.RenderPlain(snake.tail)
    applesprite = pygame.sprite.RenderPlain(apple)
    

    while 1:
        clock.tick(frame_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.change_direction("up")
                    break
                elif event.key == pygame.K_s:
                    snake.change_direction("down")
                    break
                elif event.key == pygame.K_a:
                    snake.change_direction("left")
                    break
                elif event.key == pygame.K_d:
                    snake.change_direction("right")
                    break
                elif event.key == pygame.K_q:
                    return

    
        #Draw background colour
        screen.fill(black)

        #Update tail sprites
        tailsprites = pygame.sprite.RenderPlain(snake.tail)

        #Update
        snakesprite.update()
        tailsprites.update()
        applesprite.update()

        #Snake collision
        if(snake.self_collision() or snake.border_collision()):
            return
        if snake.eat_collision(apple) and snake.eat_count % 5 == 0:
            frame_rate += 1

        #Draw
        applesprite.draw(screen)
        tailsprites.draw(screen)
        snakesprite.draw(screen)

        #Flip the image
        pygame.display.flip()


if __name__ == '__main__':
    main()
