from node2vec import *
import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')



class experiment:
    def __init__(self,bd,port,user,pss,label,param,trainset_p):
        self.bd = bd 
        self.port = port
        self.user = user
        self.pss = pss
        self.label = label
        self.trainset_p = trainset_p
        self.param = param
        self.p = figure(plot_width=1000, plot_height=600)    
        self.ratiosf = {}
        self.r_desv = {}
        self.n_desv = {}

    def run(self,a,b,jump):
        pal = pallete("links")
        for i in range(a,b):
            if self.param == "ns":
                n2v = node2vec(self.bd,self.port,self.user,self.pss,self.label,i*jump,200,6,"normal")
            if self.param == "l":
                n2v = node2vec(self.bd,self.port,self.user,self.pss,self.label,250000,200,i*jump,"normal")
            n2v.delete_rels(self.trainset_p)
            n2v.learn("normal")
            for r in n2v.r_types:
                con = neo4j.CypherQuery(n2v.graph_db, "MATCH (a)-[r:"+r+"]->(b) WHERE labels(a) <> [] AND labels(b) <> [] RETURN DISTINCT head(labels(a)) AS This, type(r) as To, head(labels(b)) AS That LIMIT 5").execute()
                if not r in self.ratiosf:
                    self.ratiosf[r] = []
                self.ratiosf[r].append(n2v.aciertos_rel(r,self.label,True,str(i*jump)+self.param+str(self.trainset_p)))
                if not r in self.r_desv:
                    self.r_desv[r] = []
                self.r_desv[r].append(n2v.r_desv[r])
                if not r in self.n_desv:
                    self.n_desv[r] = []
                self.n_desv[r].append(n2v.n_types_d[con[0]["That"]])
                ndesv = []

        for j,r in enumerate(self.ratiosf):
            x = []
            ratios = []
            rdesv = []
            ndesv = []
            for i,ratio in enumerate(self.ratiosf[r]):
                print "ja"
                x.append(i*jump)
                ratios.append(ratio)
                rdesv.append(self.r_desv[r][i]*10)
                ndesv.append(self.n_desv[r][i]*10)
            print ratios
            print x
            self.p.line(x, ratios, color=pal[j],legend=r+"(LPR)",line_width=1.5)
            self.p.line(x, rdesv, color=pal[j],legend=r+"(L-DESV)",line_dash='dashed')
            self.p.line(x, ndesv, color=pal[j],legend=r+"(N-DESV)",line_dash='dotted')

