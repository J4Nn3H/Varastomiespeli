import pygame

class Varastomiespeli:

    def __init__(self):
        pygame.init()

        self.lataa_kuvat()
        self.uusi_peli()

        self.korkeus = len(self.map)
        self.leveys = len(self.map[0])
        self.skaala = self.kuvat[0].get_width()

        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))

        self.fontti = pygame.font.SysFont("Arial", 25)

        pygame.display.set_caption("Työmiespeli")

        self.kello = pygame.time.Clock()

        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["lattia", "seina", "kohde", "laatikko", "robo", "kolikko"]:
            self.kuvat.append(pygame.image.load("src/" + nimi + ".png"))


    def uusi_peli(self):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 5, 1, 0, 0, 0, 0, 1, 1],
                    [1, 0, 3, 1, 1, 1, 1, 0, 0, 0, 0, 3, 1, 3, 0, 0, 0, 1, 1],
                    [1, 0, 5, 1, 5, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 1],
                    [1, 0, 3, 1, 0, 0, 3, 0, 3, 1, 0, 1, 1, 0, 0, 0, 0, 2, 1],
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 3, 0, 1, 0, 0, 0, 0, 2, 1],
                    [1, 0, 0, 3, 0, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 1, 1],
                    [1, 4, 0, 0, 0, 0, 5, 0, 0, 1, 1, 1, 1, 5, 0, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.aikalaskuri = 60
        self.aika_kay = False
        self.palkka = 0 
        self.laatikot = 4


    def silmukka(self):
        while True:
            self.tapahtuma()
            self.paivita_aika()
            self.piirra_naytto()
            self.kello.tick(60)


    def tapahtuma(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:

                if tapahtuma.key == pygame.K_LEFT:
                    if not self.aika_kay:  
                        self.aika_kay = True  
                    self.liikkeet(0, -1)

                if tapahtuma.key == pygame.K_RIGHT:
                    if not self.aika_kay:  
                        self.aika_kay = True 
                    self.liikkeet(0, 1)

                if tapahtuma.key == pygame.K_UP:
                    if not self.aika_kay:  
                        self.aika_kay = True  
                    self.liikkeet(-1, 0)

                if tapahtuma.key == pygame.K_DOWN:
                    if not self.aika_kay:  
                        self.aika_kay = True  
                    self.liikkeet(1, 0)

                if tapahtuma.key == pygame.K_F2: 
                    self.uusi_peli() 

                if tapahtuma.key == pygame.K_ESCAPE: 
                    exit() 

            if tapahtuma.type == pygame.QUIT: 
                exit() 


    def robon_sijainti(self):
        for y in range(self.korkeus):
            for x in range(self.leveys): 
                if self.map[y][x] in [4, 6]:
                    return (y, x) 


    def liikkeet(self, liike_y, liike_x):
        robo_vanha_y, robo_vanha_x = self.robon_sijainti()
        robo_uusi_y = robo_vanha_y + liike_y
        robo_uusi_x = robo_vanha_x + liike_x

        if self.map[robo_uusi_y][robo_uusi_x] in [1]:
            return

        if self.map[robo_uusi_y][robo_uusi_x] in [2, 3]:
            laatikko_uusi_y = robo_uusi_y + liike_y
            laatikko_uusi_x = robo_uusi_x + liike_x

            if self.map[laatikko_uusi_y][laatikko_uusi_x] in [1, 3, 5]:
                return

            self.map[robo_uusi_y][robo_uusi_x] = 4

            if self.map[laatikko_uusi_y][laatikko_uusi_x] == 2:
                self.map[laatikko_uusi_y][laatikko_uusi_x] = 0
                self.laatikko_perilla()
            else:
                self.map[laatikko_uusi_y][laatikko_uusi_x] = 3

        if self.map[robo_uusi_y][robo_uusi_x] == 5:
            self.loysit_kolikon()
            self.map[robo_uusi_y][robo_uusi_x] = 0

        self.map[robo_vanha_y][robo_vanha_x] = 0
        self.map[robo_uusi_y][robo_uusi_x] = 4    
                

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.map[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))

        teksti = self.fontti.render("Aika: " + str(int(self.aikalaskuri)), True, (255, 0, 0))
        self.naytto.blit(teksti, (30, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Laatikoita: " + str(int(self.laatikot)), True, (255, 0, 0))
        self.naytto.blit(teksti, (150, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Palkkasi: " + str(int(self.palkka)) + " €", True, (255, 0, 0))
        self.naytto.blit(teksti, (315, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (600, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (765, self.korkeus * self.skaala + 10))

        if self.aika_loppui():
            fontti = pygame.font.SysFont("Arial", 35)
            teksti = fontti.render("Et saanut kaikkia laatikoita ajoissa perille. Sait potkut!", True, (255, 255, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        if self.peli_lapi():
            fontti = pygame.font.SysFont("Arial", 50)
            teksti = fontti.render("Hienoa, selvisit työpäivästä!", True, (255, 255, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        if self.peli_lapi() and self.aika_kay: 
            self.aika_kay = False 

        pygame.display.flip()


    def peli_lapi(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.map[y][x] == 2:
                    return False
        return True
                

    def paivita_aika(self):
        if self.aika_kay:
            self.aikalaskuri -= 1 / 60
            if self.aikalaskuri < 0:
                self.aikalaskuri = 0


    def aika_loppui(self):
        return self.aikalaskuri <= 0


    def laatikko_perilla(self):
        self.palkka += 20
        self.laatikot -= 1


    def loysit_kolikon(self):
        self.palkka += 10

if __name__ == "__main__":
    Varastomiespeli()
