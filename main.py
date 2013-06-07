import pygame, sys, os
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

platformListing = []
projectileListing = []
TERMINALVELOCITY = 2
TERMINALHORIZONTALVELOCITY = 5

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #master_image, master_rect = load_image('megamanSpriteSheet.png')

        self.image, self.rect = load_image('spike.bmp')
        self.grounded = False
        self.velocity = [0,0]
        self.cameraOffset = 0

    def update(self):

        if pygame.key.get_pressed()[K_RIGHT] and self.velocity[0] < TERMINALHORIZONTALVELOCITY:
            self.velocity[0] += 1
        elif pygame.key.get_pressed()[K_LEFT] and self.velocity[0] > -TERMINALHORIZONTALVELOCITY:
            self.velocity[0] += -1
        elif pygame.key.get_pressed()[K_UP] and self.grounded:
            self.velocity[1] += -20
            self.grounded = False
            
        if not self.grounded:
            if self.checkGrounded():
                self.velocity[1] = 0
            else:
                if self.velocity[1] <= TERMINALVELOCITY:
                    self.velocity[1] += 1
        else:
            self.checkGrounded()
            if self.velocity[0] > 0:
                self.velocity[0] -= 0.3
            else:
                self.velocity[0] += 0.3
                
        self.rect = self.rect.move((self.velocity[0],self.velocity[1]))
        self.cameraOffset += self.velocity[0]

    def checkGrounded(self):
        for i in platformListing:
            if i.hitBox.colliderect(self.rect.move(0,self.velocity[1])):
                self.grounded = True
                return True
        self.grounded = False
        return False

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image, (screen.get_width() / 2, self.rect.y))

    def shootProjectile(self):
        Projectile(self.rect.center)

class Platform:
    """ Platforms for getting higher. Container for a Surface and rect"""
    def __init__(self, topLeft, width, height, color=(0,0,0)):
        self.visualPlatform = pygame.Surface((width,height))
        self.visualPlatform.convert()
        self.visualPlatform.fill(color)
        self.hitBox = pygame.Rect(topLeft,(width,height))
        platformListing.append(self)

class Projectile:
    """ Projectiles that fly through the air!"""
    def __init__(self, topLeft):
        self.visualHitBox = pygame.Surface((10,10))
        self.visualHitBox.convert()
        self.visualHitBox.fill((150,250,50))
        self.hitBox = pygame.Rect(topLeft, (10,10))
        projectileListing.append(self)

    def update(self):
        self.hitBox.x += 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("monkey.bmp")
        self.rect.center = center
        self.dead = False

    def update(self):
        for i in projectileListing:
            if self.rect.collidepoint(i.hitBox.center):
                self.dead = True

    def draw(self, offset):
        if not self.dead:
            screen = pygame.display.get_surface()
            screen.blit(self.image, (self.rect.x - offset, self.rect.y))

def main():
    
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000, 400))
    pygame.display.set_caption('BegaMan')
    pygame.mouse.set_visible(0)

    #Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #Create the background
    background = pygame.Surface(screen.get_size())
    backgtround = background.convert()
    background.fill((250, 250, 250))

    #Display The Background
    screen.blit(background, (0,0))
    pygame.display.flip()

    #Prepare Game Objects
    clock = pygame.time.Clock()
    camera = pygame.rect.Rect(0,0,700,400)

    ground = Platform((0, 370), 700, 30)
    platform1 = Platform((600, 200), 700, 30)

    player = Player()
    player.rect = player.rect.move(350,0)
    enemy = Enemy((1000, 200))
    allsprites = pygame.sprite.Group(player, enemy)

    going = True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                player.shootProjectile()

        screen.blit(background, (0,0))
        for i in platformListing:
            location = [i.hitBox.left, i.hitBox.top]
            #location[0] += 350 - player.rect.center[0]
            location = (location[0] - player.cameraOffset, location[1])
            screen.blit(i.visualPlatform, location)

        for i in projectileListing:
            i.update()
            location = [i.hitBox.left, i.hitBox.top]
            location = (location[0] - player.cameraOffset, location[1])
            screen.blit(i.visualHitBox, location)
            
        allsprites.update()
        player.draw()
        enemy.draw(player.cameraOffset)
        pygame.display.flip()

if __name__ == '__main__':
    main()
