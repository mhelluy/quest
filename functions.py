import cherrypy
import var
import json
import classes

exp = cherrypy.expose

def log(args):
    print("--------------------LOG------------------------\n\n{}\n\n-----------------------------------------------".format(args))


def content(fic):
    with open(fic,"r") as fichier:
        return fichier.read()

def redirect(url):
    return "<script>location.href=\"{}\"</script>".format(url)

def nb_players():
    return len(var.sessions) - int(var.s_display is not None) - int(var.s_moderator is not None)
    #return len(var.sessions) - 2

def this():
    return var.sessions[cherrypy.session["id"]]

def getSessionByName(name):
    for s in var.sessions:
        if s["name"] == name:
            return s

#obtenir questions depuis json
def getQuestions(file):
    with open(file,"r") as fichier:
        quests = json.loads(fichier.read())
    for i,quest in enumerate(quests):
        quests[i] = classes.Question(**quest)
    return quests

def quest():
    return var.questions[var.currentquestion]