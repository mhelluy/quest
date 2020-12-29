from functions import *
import json
import var

@exp
class EndInfos:
    def GET(self):
        if this()["name"] == "DISPLAY":
            nreload = var.nreload
            if var.nreload == 1:
                var.nreload = 0
            return json.dumps({
                "show_answer": var.show_answer,
                "status": var.status,
                "nreload": nreload
            })
        else:
            dec = this()["answres"].get(var.currentquestion)
            return json.dumps({
                "decision": dec if dec is not None else -1,
                "status": var.status
            })


@exp
class PlayInfos:
    def GET(self,truemethod="GET",answ = None):
        if truemethod == "GET":
            if var.status == 2:
                return json.dumps({
                    "status": 2
                })
            else:
                if quest().time_isover():
                    var.status = 2
                return json.dumps({
                    "status": var.status
                })
        elif truemethod == "POST":
            this()["currentansw"] = answ
            this()["theorical_score"] = quest().score + var.bonuspoints
            var.bonuspoints -= 10
            if quest().qtype == "choices":
                answ = int(answ)
            correct = None
            correct = quest().isCorrect(answ)
            this()["answres"][var.currentquestion] = correct
            if correct:
                this()["score"] += this()["theorical_score"]
            if this() not in var.answcounter:
                var.answcounter.append(this())
            if len(var.answcounter) >= nb_players():
                var.status = 2
        

@exp
class PlayWait:
    def GET(self,raw=False):
        for s in var.sessions:
            if not s.get("isReady"):
                return json.dumps({
                    "isReady": False
                }) if not raw else False
        return json.dumps({
                    "isReady": True
                }) if not raw else True


@exp
class ModeratorActionsApp:
    def GET(self):
        relist = []
        for s in var.sessions:
            if s["name"] not in ["mod1207","DISPLAY"]:
                relist.append({
                    "name": s["name"],
                    "answer": s.get("currentansw"),
                    "decision": s["answres"][var.currentquestion]
                })
        return json.dumps(relist)
    def POST(self,setvar=None,setsessvar=None,changedecision=None,increm=None):
        if this()["name"] == "mod1207":
            if setvar is not None:
                setvar = json.loads(setvar)
                for v in setvar:
                    var.g()[v] = setvar[v]
            if setsessvar is not None:
                setsessvar = json.loads(setsessvar)
                for name in setsessvar:
                    s = getSessionByName(name)
                    for v in setsessvar[name]:
                        s[v] = setsessvar[name][v]
            if increm is not None:
                increm = json.loads(increm)
                for v in increm:
                    var.g()[v] += increm[v]    
            if changedecision is not None:
                var.nreload = 1
                changedecision = json.loads(changedecision)
                s = getSessionByName(changedecision["name"])
                if changedecision["new"] == 0:
                    s["score"] -= s["theorical_score"]
                else:
                    s["score"] += s["theorical_score"]
                s["answres"][var.currentquestion] = changedecision["new"]
                log(s["answres"][var.currentquestion])
        else:
            return "Operation not permitted"
@exp
class NameApp:
    def GET(self,raw=False):
        listNames = ""
        for s in var.sessions:
            name = s["name"]
            if name not in ["DISPLAY","mod1207"]:
                listNames += "<li>{}</li>".format(name)
        return json.dumps({
            "listNames": listNames,
            "start": var.status
        }) if not raw else listNames


@exp
class InfoWaitApp:
    def GET(self):
        return json.dumps({
            "nb_players": nb_players(),
            "start": var.status
        })

class Apps:
    def __init__(self):
        self.wnames = NameApp()
        self.winfos = InfoWaitApp()
        self.mactions = ModeratorActionsApp()
        self.pwait = PlayWait()
        self.pinfos = PlayInfos()
        self.einfos = EndInfos()
