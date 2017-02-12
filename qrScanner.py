import pygame
import pygame.camera
from pygame.locals import *
import qrtools

DEVICE = '/dev/video0'
SIZE = (640, 480)
QR_FILE = 'qrCode.png'
TEAM_NUMBER = input("What team number did you scout? ")
FILE = 'scoutingFile'

pygame.camera.init()

print "Press the right arrow to take a picture"

display = pygame.display.set_mode(SIZE, 0)
camera = pygame.camera.Camera(DEVICE, SIZE)
camera.start()
screen = pygame.surface.Surface(SIZE, 0, display)
capture = True

while capture:
    screen = camera.get_image(screen)
    display.blit(screen, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            capture = False
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            print "Picture Taken!"
            pygame.image.save(screen, QR_FILE)
            qr = qrtools.QR()
            qr.decode(QR_FILE)
            print "Here is the QR Code Data: "
            print qr.data
            print "Click the 'X' to exit"
            f = open(FILE, 'a')
            f.write('Team Number ' + str(TEAM_NUMBER) + ': ' + qr.data + '\n')

camera.stop()
pygame.quit()
