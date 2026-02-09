import pygame
from pygame.locals import *
import re

class tEDE_Face:
    def __init__(self):
        pygame.init()
        # Configuracion de pantalla segun tu ejemplo
        self.window = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption("tED-E Face System")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_emotion = "IDLE"
        self.frame_index = 0
        
        # Diccionario de Sprites por emocion
        # Cargamos las secuencias de 3 imagenes para cada estado
        base_path = "/home/tede/tEDEOS/Faces/"
        try:
            self.sprites = {
                "HAPPY": [
                    pygame.image.load(f"{base_path}happy_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}happy_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}happy_3.png").convert_alpha()
                ],
                "SAD": [
                    pygame.image.load(f"{base_path}sad_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}sad_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}sad_3.png").convert_alpha()
                ],
                "MEH": [
                    pygame.image.load(f"{base_path}meh_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}meh_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}meh_3.png").convert_alpha()
                ],
                "ANGRY": [
                    pygame.image.load(f"{base_path}angry_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}angry_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}angry_3.png").convert_alpha()
                ],
                "IDLE": [
                    pygame.image.load(f"{base_path}idle_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}idle_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}idle_3.png").convert_alpha()
                ],
                "THINKING": [
                    pygame.image.load(f"{base_path}thinking_1.png").convert_alpha(),
                    pygame.image.load(f"{base_path}thinking_2.png").convert_alpha(),
                    pygame.image.load(f"{base_path}thinking_3.png").convert_alpha()
                ]
                
            }
        except pygame.error as e:
            print(f"Error cargando imagenes: {e}")
            # Fallback: crear una superficie vacia si fallan las imagenes
            self.sprites = {"MEH": [pygame.Surface((800, 600))]}

    def update_emotion(self, emotion):
        """Cambia la emocion actual y reinicia el indice de animacion."""
        emotion = re.sub(r'[\W\s]+', '', emotion)
        if emotion in self.sprites:
            if self.current_emotion != emotion:
                self.current_emotion = emotion
                self.frame_index = 0
        else:
            self.current_emotion = "IDLE"

    def draw(self):
        """Maneja la animacion y el dibujado."""
        # Limpiar pantalla (importante para que no se solapen los frames)
        self.window.fill((0, 0, 0))

        # Obtener la lista de imagenes de la emocion actual
        current_sprites = self.sprites.get(self.current_emotion, self.sprites["MEH"])

        # Control de ciclo de animacion 
        if self.frame_index >= len(current_sprites):
            self.frame_index = 0

        # Seleccionar imagen y dibujar
        image = current_sprites[self.frame_index]
        self.window.blit(image, (0, 0))

        # Actualizar display
        pygame.display.update()

        # Incrementar frame para la siguiente llamada
        self.frame_index += 1
        
        # Control de velocidad de la animacion (FPS)
        # 3-5 FPS es ideal para ese estilo de animacion "robotica"
        self.clock.tick(5) 

    def quit(self):
        pygame.quit()
