from pushbullet import Pushbullet

class PushbulletManager():
    '''
    Classe qui s'occupe du service Pushbullet (voir dans NewsScreen).
    Elle initie la connexion avec le service, et permet l'envoi de liens et de textes au besoin,
    par defaut vers le telephone de Pierre (Nexus 6P).
    '''
    def __init__(self):
        API = 'o.NzPTn5UX6rCsuEB1gcYouTluy1GO2Wti'

        self.pb = Pushbullet(API)
        self.nexusDevice = self.pb.get_device("Huawei Nexus 6P")

    def send_test(self):
        push = self.nexusDevice.push_link("Cool site", "https://lemonde.com")

    def send_link(self, title, link):
        print "pushing link :" + link
        push = self.nexusDevice.push_link(title, link)

    def send_text(self, title, text):
        push = self.nexusDevice.send_text(title, text)
