#!/usr/bin/env python3

import sys
from apps import *
from classes import *
import var

if len(sys.argv) > 1:
    var.questions = getQuestions(sys.argv[1])
else:
    var.questions = getQuestions("questions.json")


# site principal
class Site:

    def __init__(self):
        self.apps = Apps()
        self.apps.exposed = True

    @exp
    def id(self):
        return str(cherrypy.session.get("id"))

    @exp
    def index(self):
        if cherrypy.session.get("id") is None:
            return content("site/index.html")
        else:
            return redirect("waiting")

    @exp
    def sessiondefine(self, name=None):
        if cherrypy.session.get("id") is None:
            id = len(var.sessions)
            cherrypy.session["id"] = id
            var.sessions.append({"name": name})
            if name == "DISPLAY" and var.s_display is None:
                var.s_display = this()
            elif name == "mod1207" and var.s_moderator is None:
                var.s_moderator = this()
            elif name not in ["DISPLAY", "mod1207"]:
                this()["answres"] = {}
                this()["score"] = 0
        return redirect("waiting")

    @exp
    def waiting(self):
        if cherrypy.session.get("id") is None:
            return redirect("index")
        if var.status:
            return redirect("play")
        if this()["name"] == "DISPLAY":
            # creation de la liste de noms
            return content("site/waiting_display.html").replace("<?listNames>", NameApp().GET(True))
        elif this()["name"] == "mod1207":
            return content("site/waiting.html").replace("<?nb_players>", str(nb_players())).\
                replace("<?moderator code>", "<button id='start'>Démarrer</button>").replace("<?moderator script>",
                                                                                             "<script src='static/js/wm_script.js'></script>")
        else:
            return content("site/waiting.html").replace("<?nb_players>", str(nb_players())).replace("<?moderator code>", "").replace("<?moderator script>", "")

    @exp
    def play(self):
        if var.currentquestion >= len(var.questions):
            var.status = 3
        if var.status == 1:
            this()["isReady"] = True
            this()["currentansw"] = None
            var.show_answer = 0
            if PlayWait().GET(True):  # si tous les joueurs sont prêts
                if this()["name"] == "DISPLAY":
                    var.answcounter = []
                    var.bonuspoints = nb_players() * 10
                    for s in var.sessions:
                        if s["name"] not in ["DISPLAY","mod1207"]:
                            s["theorical_score"] = quest().score
                    if quest().qtype == "choices":
                        answerdisp = ""
                        for choic in quest().choices:
                            answerdisp += "<div class='answer'><p>{}</p></div>".format(
                                choic)
                    else:
                        answerdisp = "<p id='pcash'>Écrivez la bonne réponse.</p>"
                    quest().time_reset()
                    return content("site/play_display.html").replace("<?question>", quest().question)\
                                                            .replace("<?compl>", quest().compl)\
                                                            .replace("<?choices>", answerdisp)\
                                                            .replace("<?time>", str(quest().time))
                elif this()["name"] == "mod1207":
                    return content("site/play_mod.html").replace("<?modact>",quest().modact)
                else:
                    answercli = ""
                    if this() not in var.answcounter:
                        if quest().qtype == "choices":
                            for choic in quest().choices:
                                answercli += "<div class='answer'></div>"
                        else:
                            answercli = "<div id='cashdiv'><input type='text' id='cashansw' placeholder='Écrivez la réponse'/><button id='bcash'>OK!</button></div>"
                        disp = "none"
                    else:
                        disp = "flex"
                    return content("site/play.html").replace("<?choices>", answercli)\
                        .replace("<?disp>",disp)
            else:
                return content("site/wplay.html")
        elif var.status == 2:
            return redirect("end")
        elif var.status == 3:
            return redirect("eog")
        else:
            return redirect("index")

    @exp
    def end(self):
        if var.status == 2:
            if this()["name"] == "DISPLAY":
                tblcont = ""
                sorsess = list(reversed(sorted([s for s in var.sessions if s["name"] not in [
                                 "mod1207", "DISPLAY"]], key=lambda s: s.get("score"))))
                for i, s in enumerate(sorsess):
                    tblcont += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        i + 1, s["name"], s["score"])

                frmansw = ""
                if var.show_answer:
                    frmansw = "<div><p>La réponse était <span id='answspan'>" + quest().getAnswer() + \
                    "</span></p></div><div id='expli'>{}</div>".format(quest().expli)

                return content("site/end_display.html").replace("<?tablecontent>", tblcont)\
                    .replace("<?answer>", frmansw)\
                    .replace("<?showansw>", str(var.show_answer))
            elif this()["name"] == "mod1207":
                tablecont = ""
                for s in var.sessions:
                    if s["name"] not in ["mod1207", "DISPLAY"]:
                        frmdecision = "<label for='" + s["name"] + "_true'>V</label><input type='radio' name='" + s["name"] + "_decision' id='" + s["name"] + "_true' value='V' {}/><hr/><label for='" + s["name"] + "_false'>F</label><input type='radio' name='" + s["name"] + "_decision' id='" + s["name"] + "_false' value='F' {}/>"
                        if s["answres"].get(var.currentquestion) in [None,-1,0]:
                            frmdecision = frmdecision.format("","checked")
                        elif s["answres"][var.currentquestion] in [1,2]:
                            frmdecision = frmdecision.format("checked","")
                        curansw = s.get("currentansw")
                        if curansw not in [None,-1] and quest().qtype != "cash":
                            curansw = quest().choices[int(curansw)]
                        tablecont += "<tr><td>{}</td><td>{}</td><td class='lastcol'>{}</td></tr>".format(s["name"],curansw,frmdecision)
                return content("site/end_mod.html").replace("<?tablecontent>",tablecont)
            else:
                this()["isReady"] = False
               # log(this()["answres"].get(var.currentquestion))
                if this()["answres"].get(var.currentquestion) in [None,-1]:
                    divreturn = "<div id='resp' class='ecoule'><p>Temps écoulé</p>"
                    this()["answres"][var.currentquestion] = -1
                elif this()["answres"][var.currentquestion] == 0:
                    divreturn = "<div id='resp' class='incorrect'><p>Réponse incorrecte</p>"
                elif this()["answres"][var.currentquestion] == 1:
                    divreturn = "<div id='resp' class='correct'><p>Réponse correcte</p>"
                elif this()["answres"][var.currentquestion] == 2:
                    divreturn = "<div id='resp' class='exact'><p>Réponse exacte</p>"
                return content("site/end.html").replace("<?answertype>", divreturn)\
                    .replace("<?score>", str(this()["score"]))
        elif var.status == 1:
            return redirect("play")
        else:
            return redirect("index")

    @exp
    def eog(self):
        if var.status == 3:
            sorsess = list(reversed(sorted([s for s in var.sessions if s["name"] not in [
                                    "mod1207", "DISPLAY"]], key=lambda s: s.get("score"))))
            if this()["name"] in ["DISPLAY","mod1207"]:
                tblcont = ""
                for i, s in enumerate(sorsess):
                        tblcont += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                            i + 1, s["name"], s["score"])
                return content("site/eog_display.html").replace("<?tablecontent>", tblcont)
            else:
                return content("site/eog.html").replace("<?place>",str(sorsess.index(this()) + 1))
        else:
            return redirect("index")


conf = {
    "/": {
        "tools.sessions.on": True,
        "tools.staticdir.root": sys.path[0],
        "tools.sessions.same_site": "lax"
        # "tools.sessions.secure": True
    },
    "/static": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "./site/public"
    },
    "/apps/wnames": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    },
    "/apps/winfos": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    },
    "/apps/mactions": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    },
    "/apps/pwait": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    },
    "/apps/pinfos": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    },
    "/apps/einfos": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    }
}

cherrypy.config.update({
    "server.socket_host": "0.0.0.0",
    "server.socket_port": 80
})

cherrypy.quickstart(Site(), "/", conf)
