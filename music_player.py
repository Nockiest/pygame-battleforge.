from pygame import mixer
mixer.init()

# pygame.display.set_caption("Wargame Batelfield simulator")
 

# sound_boom = pygame.mixer.Sound("media/artillery-blast.ogg")
# marching_sound = pygame.mixer.Sound("media/infantry-march.wav")

  
# # hudba v pozadí
# pygame.mixer.music.load("media/bg-music.wav")
# pygame.mixer.music.set_volume(0.2)
# # Přehrajeme hudbu v pozadí
# pygame.mixer.music.play(-1, 0.0) # -1 = repeat endlessly, start
# # pygame.time.delay(3000)
# # pygame.mixer.music.stop(

    
# marching_sound.set_volume(0.1)
# # Přehrání zvuku
# sound_boom.play()
# pygame.time.delay(2000)
# marching_sound.play()
def play_sound_file(url):
  
    mixer.music.load(url)
    mixer.music.play()