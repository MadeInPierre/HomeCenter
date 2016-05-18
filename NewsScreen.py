import pygame
from NewsCollector import *
from Helpers import *
from PushbulletManager import PushbulletManager as PM
from AnimationManager import *

class NewsScreen():
    '''
    Application d'actualites. Cette appli recupere les derniers articles de LeMonde.fr, les affiche avec un design epure, et offre
    un cote interactif a l'utilisateur.
    L'application affiche une liste d'articles avec les titres. Si un titre interesse l'utilisateur, celui-ci peut
    '''
    def __init__(self, WindowRes):
        '''
        Demarrage et initialisation de l'application.
        Chargement d'images, recuperation des articles, demarrage de pushbullet.
        '''
        self.WindowRes = WindowRes
        self.ScreenStatus = "FADING_IN"
        self.bg = pygame.image.load("Images/news1.png")
        self.hamburger_img = pygame.image.load("Images/hamburger.png")
        self.home = pygame.image.load("Images/homenews.png")

        self.LMm_img    = pygame.image.load("Images/NewsScreen/LeMondeM.png")
        self.LMfull_img = pygame.image.load("Images/NewsScreen/LeMondeFull.png")
        self.FB_img = pygame.image.load("Images/NewsScreen/fb.png")

        self.ancrage = 0.0
        self.banner_chrono = AnimationManager()
        self.banner_extended = False
        self.banner_pos = 38.0




        '''
        Initialisation et connection au service qui permettra d'envoyer le lien de l'article clique au
        telephone portable associe au systeme : le service Pushbullet.
        '''
        self.connexion = True
        print "Starting pushbullet service..."
        try:
            self.pushbullet = PM()
            print "Connected."
        except:
            self.pushbullet = None
            self.connexion = False
            print "No Internet connection."

        '''
        Recuperation et classement des actualites chez LeMonde.fr
        '''
        itemTitleFont       = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 14)
        itemDescriptionFont = pygame.font.Font("Fonts/HelveticaNeue-Light.ttf", 11)
        self.lemonde_items = []
        print "Getting LeMonde news..."
        for item in NewsCollector().get_lemonde_posts():
            '''
            On cree des objets poru chaque article de la classe mineure (voir en fin de fichier).
            '''
            self.lemonde_items.append(NewsItem(itemTitleFont, item[0], item[1], item[2], item[3], itemDescriptionFont, item[4], item[5]))





    def Update(self, InputEvents):
        '''
        On gere les entrees utilisateur.
        '''
        for event in InputEvents:
            if "TOUCH" in event:
                mousepos = pygame.mouse.get_pos()
                '''
                On ouvre ou ferme la banniere laterale si l'utilisateur le demande.
                '''
                if Helpers.is_in_rect(mousepos, [0, 38, 38, 38]):
                    self.banner_extended = not self.banner_extended

            if "SCROLL" in event and "ENDSCROLL" not in event:
                '''
                On fait monter ou descendre la liste des articles quand l'utilisateur le demande.
                '''
                scroll = Helpers.get_message_x_y(event)
                self.ancrage -= scroll[1]
                if self.ancrage > 0:
                    self.ancrage = 0
                elif self.ancrage < 480 - 220 * (int(len(self.lemonde_items) / 2) + len(self.lemonde_items) % 2) - 20: # CORRIGER LES VALEURS
                    self.ancrage  = 480 - 220 * (int(len(self.lemonde_items) / 2) + len(self.lemonde_items) % 2) - 20
                print int(len(self.lemonde_items) / 2) + len(self.lemonde_items) % 2
        '''
        On laisse chaque objet de la liste des articles se gérer (animations, entrees tactiles..)
        '''
        for item in self.lemonde_items:
            #if item.ActiveDraw is True:
            item.Update(InputEvents, self.pushbullet)

        '''
        Animation de l'apparition et disparition de la baniere.
        '''
        if self.banner_extended is False:
            if self.banner_pos > 39:
                self.banner_pos = Helpers.mathlerp(self.banner_pos, 38, 0.5)
            else:
                self.banner_pos = 38
        if self.banner_extended is True:
            if self.banner_pos < 189:
                self.banner_pos = Helpers.mathlerp(self.banner_pos, 190, 0.5)
            else:
                self.banner_pos = 190


    def Draw(self, gameDisplay):
        '''
        Affichage et rendering de toute l'application.
        '''
        Helpers.blit_alpha(gameDisplay, self.bg, (0, 0 + self.ancrage * 0.1), 100)

        '''
        On dessine tous les articles a la bonne position
        '''
        offset = 200 + 20 # taille de chaque card et espace entre chaque
        count = 0
        for item in self.lemonde_items:
            drawpos = (80 + 349 * (count % 2 == 1), 20 + offset * int(count / 2) + self.ancrage)

            if drawpos[1] > -200 and drawpos[1] < self.WindowRes[1]:
                gameDisplay.blit(item.Render(drawpos), drawpos)
            else:
                item.drawpos = drawpos
                item.ActiveDraw = False
            count += 1

        '''
        On dessine la banniere
        '''
        # Draw the banner's bg
        bannersurface = pygame.Surface((self.banner_pos, self.WindowRes[1])).convert_alpha()
        bannersurface.fill((20, 20, 30, 225))


        Helpers.draw_line(bannersurface, 0, 38, 38, 1, (200, 200, 200)) #haut
        Helpers.draw_line(bannersurface, 0, 76, 38, 1, (200, 200, 200)) #bas
        Helpers.draw_line(bannersurface, 38 * int(self.banner_pos != 38) - 1, 38, 1, 39, (200, 200, 200)) #gauche
        bannersurface.blit(self.hamburger_img, (0, 38))

        if self.banner_pos != 38:
            bannersurface.blit(self.LMm_img, (0, 38*3 + 5))
            bannersurface.blit(self.LMfull_img, (52, 38*3 + 8))

        gameDisplay.blit(bannersurface, (0, 0))

        gameDisplay.blit(self.home, (0, 0))

    def Quit(self):
        pass
    def __str__(self):
        return "NEWSSCREEN"









class NewsItem():
    '''
    Cette classe est un des rectangles qui correspondent a chaque article dans l'interface : je l'appelle la "Card".
    La classe principale cree une liste d'objets de cette classe, chacun ayant les donnees d'un article.
    '''


    def __init__(self, titlefont, title, date, hour, link, descriptionfont, description, image):
        '''
        Initialisation des elements dont la Card a besoin.
        '''
        self.CardSize = (329, 200)
        self.ActiveDraw = False

        self.Title = title
        self.Date = date
        self.Hour = hour
        self.Link = link
        self.Description = description

        self.Image = image
        print image.get_rect()
        self.Image = pygame.transform.scale(self.Image, (400, 200))
        print self.Image.get_width() * (self.Image.get_height() / 200)

        self.openonphone_img = pygame.image.load("Images/NewsScreen/openInBrowser.png")
        self.more_img = pygame.image.load("Images/NewsScreen/more.png")
        self.sent_img = pygame.image.load("Images/NewsScreen/sent.png")

        self.TitleFont = titlefont
        self.DescriptionFont = descriptionfont

        self.drawpos = (2000, 2000)
        self.banner_extended = False
        self.banner_pos = 140

        self.requestpush = False
        self.sentpush = False
        self.pushchrono = AnimationManager()

        self.CardSurface = pygame.Surface((329, 200))
        self.reRender = True








    def Update(self, InputEvents, pushbullet):
        '''
        Partie qui s'occupe de gerer les etats de Pushbullet (le service qui permet d'envoyer l'article sur son portable).
        Trois etats :
            - Inactif, ou self.requestpush et self.sentpush sont a False. On attend que l'utilisateur active le service.
            - Actif, notification pas encore envoyee. On envoie la notification. self.requestpush est a True et self.sentpush est a False
            - Envoye, self.requestpush est a True et self.setnpush est a True. Cet etat resqte actif pendant quelques secondes
                pour l'animation, et tout repasse a False plus tard.
        '''
        if self.requestpush is True:
            try:
                pushbullet.send_link(self.Title, self.Link)
                self.sentpush = True
                self.pushchrono.reset()
            except:
                pass
            self.requestpush = False

        '''
        Partie qui gere les entrees tactiles
        '''
        for event in InputEvents:
            if "TOUCH" in event:
                '''
                On prend la position du clic relative a la position de la Card, puisque cette classe ne s'occupe que de la Card.
                '''
                if Helpers.is_in_rect(pygame.mouse.get_pos(), [self.drawpos[0], self.drawpos[1], self.CardSize[0], self.CardSize[1]]):
                    mousepos = (pygame.mouse.get_pos()[0] - self.drawpos[0], pygame.mouse.get_pos()[1] - self.drawpos[1])

                    '''
                    Si on clique sur l'icone d'envoi Pushbullet, activer l'envoi et les animations.
                    '''
                    if Helpers.is_in_rect(mousepos, [self.CardSize[0] - 40, self.CardSize[1] - 40, 40, 40]) and self.banner_pos == 0:
                        self.requestpush = True
                        self.reRender = True
                    '''
                    Si on clique sur la baniere, la faire apparaitre ou disparaitre.
                    '''
                    if Helpers.is_in_rect(mousepos, [0, self.CardSize[1] - 60, self.CardSize[0], 60]) and self.banner_extended is False:
                        self.banner_extended = True
                    if Helpers.is_in_rect(mousepos, [0, 0, self.CardSize[0], 60]) and self.banner_extended is True:
                        self.banner_extended = False
                else:
                    '''
                    Si on a capte un clic mais qu'il est en dehors de la Card, on rabaisse la banniere.
                    '''
                    self.banner_extended = False

        '''
        Animations de la banniere
        '''
        if self.banner_extended is True:
            if self.banner_pos > 1:
                self.banner_pos = Helpers.mathlerp(self.banner_pos, 0, 0.5)
                self.reRender = True
            else:
                self.banner_pos = 0
        if self.banner_extended is False:
            if self.banner_pos < 139:
                self.banner_pos = Helpers.mathlerp(self.banner_pos, 140, 0.5)
                self.reRender = True
            else:
                self.banner_pos = 140








    def Render(self, drawpos):
        '''
        Ici, on dessine l'integralite des elements qui composent la Card.
        '''
        self.ActiveDraw = True
        self.drawpos = drawpos

        if self.reRender == True:
            self.reRenderAll(drawpos)

        '''
        On renvoie a la classe principale le rendu final de la Card. La classe principale la dessinera au bon endroit.
        '''
        return self.CardSurface



    def reRenderAll(self, drawpos):
        self.reRender = False
        '''
        On cree la surface on l'on dessine la Card
        '''
        self.drawpos = drawpos
        s = pygame.Surface(self.CardSize).convert_alpha()

        '''
        On affiche le fond d'ecran, qui est l'image de l'article
        '''
        s.blit(self.Image, (0, 0))

        '''
        Baniere blanche en bas qui contient le titre de l'article. Il s'agrandit si l'on a clique dessus
        pour afficher la description de l'article.
        '''
        white_titlebanner = pygame.Surface((self.CardSize[0], 200 - self.banner_pos + 1)).convert_alpha()
        white_titlebanner.fill((220, 220, 220, 240))
        s.blit(white_titlebanner, (0, self.banner_pos))

        '''
        Titre de l'article
        '''
        self.render_text_in_zone(s, self.Title, self.TitleFont, (0, 0, 0), (5, self.banner_pos + 8), 320, 22)

        '''
        Elements a l'interieur de la banniere, qui apparait quand on clique dessus.
        '''
        if self.banner_pos is not 140:
            '''
            Description courte de l'article, dessinee avec la focntion permettant d'ecrire automatiquement sur
            plusieurs lignes
            '''
            self.render_text_in_zone(s, self.Description, self.DescriptionFont, (0, 0, 0), (10, self.banner_pos + 60), 320, 18)

            '''
            Partie qui s'occupe de l'icone en bas a gauche, anime pour illustrer chaque etat de la fonctionnalite Pushbullet (celle qui
            permet d'ouvrir l'article sur le telephone)
            '''
            '''
            Dessin d'un carre plus fonce derriere l'icone, question design
            '''
            blur = pygame.Surface((40, 40)).convert_alpha()
            blur.fill((0, 0, 0, 20))
            s.blit(blur, (self.CardSize[0] - 40, self.CardSize[1] - 40 + self.banner_pos))

            '''
            Changement et animation des icones en fonction de l'etat du service Pushbullet
            '''
            if self.requestpush == True:
                '''
                Si requestpush est a True, cela veut dire que Pushbullet est en train d'envoyer l'article. On dessine l'icone correspondant,
                sans animation.
                '''
                s.blit(self.more_img, (self.CardSize[0] - 32.5, self.CardSize[1] - 32.5 + self.banner_pos))
                self.reRender = True
            elif self.sentpush == True:
                '''
                Cette zone s'active quand la notification a ete envoyee. L'icone est animee en disparaissant progressivement, et reactive
                la troisieme partie lorsque l'icone de confirmation d'envoi a disparu.
                '''
                Helpers.blit_alpha(s, self.sent_img, (self.CardSize[0] - 30, self.CardSize[1] - 30 + self.banner_pos),
                                   - 128 * self.pushchrono.elapsed_time() + 255)

                self.reRender = True

                if - 128 * self.pushchrono.elapsed_time() + 255 < 0:
                    self.sentpush = False


            else:
                '''
                Lorsque Pushbullet ne fait rien, on affiche l'icone standart qui invite l'uyilisateur a envoyer l'article sur son
                portable.
                '''
                s.blit(self.openonphone_img, (self.CardSize[0] - 35, self.CardSize[1] - 35 + self.banner_pos))

        self.CardSurface.blit(s, (0, 0))



    def render_text_in_zone(self, gameDisplay, text, font, color, startpos, horizontal_size_limit, interligne):
        '''
        Fonction qui permet d'ecrire du texte sur plusieurs lignes. Voir la fonction dans CalendarScreen pour plus de details.
        '''
        s = font.render(text, True, color) # on dessine le texte une première fois pour avoir sa longueur
        h_size = horizontal_size_limit - startpos[0] # la limite en longueur que le texte ne doit pas depasser
        vertical_size = 0 # voir return en derniere ligne

        '''
        Si le texte est trop long, on le coupe jusqu'a ce qu'il reste dans l'espace delimite
        '''
        if s.get_rect().width > h_size:
            splitted_text = text.split() # On separe la phrase entre chaque mot
            final_lines = []

            cropped_size = 0
            done = False
            for i in range(len(splitted_text) - 1, -1, -1): # on scanne toues les mots en partant du dernier
                if not done:
                    word_image = font.render(splitted_text[i], True, color) # on dessine le mot pour avoir

                    cropped_size += word_image.get_rect().width + 4 # on compte ce mot en plus dans la largeur du texte
                    if s.get_rect().width - cropped_size < h_size: # on teste si le bout coupe est suffisant pour que le titre ne depasse pas la
                                                                   # limite
                        '''
                        On prepare le dessin en dessinant la premier ligne...
                        '''
                        first_line_text = ""
                        for word in splitted_text[0:i]:
                            first_line_text += " " + word
                        first_line = font.render(first_line_text, True, color)
                        final_lines.append(first_line)

                        '''
                        ... separement a la deuxieme (le bout de la premiere coupee)
                        '''
                        line_text = ""
                        for word in range(i, len(splitted_text)):
                            line_text += " " + splitted_text[word]

                        final_line = font.render(line_text, True, color)
                        final_lines.append(final_line)

                        done = True

            '''
            On dessine les lignes sur l'ecran, avec la bonne position
            '''
            for linenumber in range(0, len(final_lines)):
                gameDisplay.blit(final_lines[linenumber], (startpos[0], startpos[1] + interligne * linenumber))
            vertical_size = interligne * len(final_lines) # on enregistre l'espace vertical qui a ete utilise pour afficher le texte
                                                  # (voir return en derniere ligne)

        else:
            gameDisplay.blit(s, startpos) # si le titre n'est pas trop long, on le dessine simplement.
            vertical_size = s.get_rect().height
        return vertical_size # redonne la taille verticale qui a ete utilisee pour afficher ce texte (utile pour afficher les prochains titres en dessous).



'''
TODO LIST !
     - Correct the end of lines in multiline rendering
     - Correct limit at 2 lines on multiline rendering
     - Performance optimisations
     - Banner design and finalisation
'''
