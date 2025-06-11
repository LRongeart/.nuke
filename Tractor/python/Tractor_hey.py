#############################################################
###################HEY TRACTOR v1.0##########################
#################by Andrea Geremia###########################
###############www.andreageremia.it##########################
#############################################################

import sys
import nuke
import nukescripts
import Tractor
import getpass
import time

#  !!!! TO BE ENABLED ONCE READY  !!!!
#from tractor.api import query
#from tractor import api
#import tractor.api.query as tq


def talk_with_tractor():
    global username
    username = getpass.getuser()


#################### INSTRUCTIONS ########################
# Modify the user name and the password of your profile  #
##########################################################
    
#    SIMTRACKER = {"user": "root", #  !!!! TO ENABLE ONCE READY !!!!
#                  "password": ""}
    
#    tq.setEngineClientParam(user=SIMTRACKER["user"], password=SIMTRACKER["password"])
    
    global my_jobs_done
    my_jobs_done = "" # !!!! TO SWITCH ONCE READY !!!!
    #my_jobs_done = tq.jobs("done and stoptime > -1h and owner=" + username + "", sortby=["-stoptime"], limit=40)

    global my_jobs_active
    my_jobs_active = "" # !!!! TO SWITCH ONCE READY !!!!
#    my_jobs_active = tq.jobs("active and not error and owner=" + username + "", columns=["jid", "title", "numdone", "maxtid"], sortby=["-priority"], limit=20)

    global my_jobs_ready
    my_jobs_ready = "" # !!!! TO SWITCH ONCE READY !!!!
#    my_jobs_ready = tq.jobs("ready and not active and owner=" + username + "", columns=["jid", "title", "numdone", "maxtid"], sortby=["-priority"], limit=40)

    global my_jobs_error
    my_jobs_error = "" # !!!! TO SWITCH ONCE READY !!!!
#    my_jobs_error = tq.jobs("error and owner=" + username + "", columns=["jid", "title", "numdone", "maxtid"], sortby=["-priority"], limit=10)

    global my_jobs_paused
    my_jobs_paused = ""
#    my_jobs_paused = tq.jobs("not done and Job.pausetime > '1000-01-01 00:00:00.000000+00' and owner=" + username + "", columns=["jid", "title", "numdone", "maxtid", "pausetime"], sortby=["-priority"], limit=20)
    
    
    n_jobs_active = len(my_jobs_active) + len(my_jobs_ready) + len(my_jobs_error)
    
    array= []



def update():
    global p
    p.finishModalDialog(True)

    p = ShapePanel()
    
    p.show_modal_dialog()

#-----------------------------------------------------

def retry_job(id, title):
    if nuke.ask('Are you sure you want to retry this job: ' + title + ' ?'):
        # tq.retry("jid=" + id + " and error") # !!!! TO ENABLE ONCE READY !!!!
        time.sleep(2)
        update()



#-------------------------------------------------------

def unpause_job(id, title):
    if nuke.ask('Are you sure you want to unpause this job: ' + title + ' ?'):
        # tq.unpause("jid=" + id + " and Job.pausetime > '1000-01-01 00:00:00.000000+00'") # !!!! TO ENABLE ONCE READY !!!!
        time.sleep(2)
        update()

#-------------------------------------------------------

#----------------------------------------
def get_elementPercentage(elem):
        if elem['numdone'] > 0:
            percentage = int(elem['numdone']/float(elem['maxtid'])*100)
        else:
            percentage = 0
        return str(elem['jid']) + '    ' + elem['title'] + '    ' + str(percentage) + "%"

#-------------------------------------------

def get_element(elem):
        return str(elem['jid']) + '    ' + elem['title']

#-------------------------------------------

def get_id(elem):
        return elem['jid']
#------------------------------------------

def get_title(elem):
        return elem['title']

#--------------------------------------------


class ShapePanel(nukescripts.PythonPanel):
    def __init__(self):
        talk_with_tractor()
        #create window
        nukescripts.PythonPanel.__init__(self, 'Tractor elements from ' + username )
        self.setMinimumSize(800, 300)
        
      
        def add_knob():
            #add KNOBS
            
            #ACTIVE JOBS
            if(len(my_jobs_active)>0):
                self.addKnob(nuke.Text_Knob("ACTIVE JOBS (" + str(len(my_jobs_active)) + "): "))
                for elem in my_jobs_active:
                    knob = nuke.Text_Knob(str(get_id(elem)), get_elementPercentage(elem))
                    knob.setValue(" ")
                    knob.clearFlag(nuke.ENDLINE)
                    self.addKnob(knob)
    
    
            #READY JOBS
            if(len(my_jobs_ready)>0):
                self.addKnob(nuke.Text_Knob("READY JOBS (" + str(len(my_jobs_ready)) + "): "))
                for elem in my_jobs_ready:
                    knob = nuke.Text_Knob(str(get_id(elem)), get_elementPercentage(elem))
                    knob.setValue(" ")
                    knob.clearFlag(nuke.ENDLINE)
                    self.addKnob(knob)
            
            #PAUSED JOBS
            #get_paused_job(my_jobs_paused)
            if(len(my_jobs_paused)>0):
                self.addKnob(nuke.Text_Knob("PAUSED JOBS (" + str(len(my_jobs_paused)) + "): "))
                for elem in my_jobs_paused:
                    knob = nuke.Text_Knob(str(get_id(elem)), get_elementPercentage(elem))
                    knob.setValue(" ")
                    knob.clearFlag(nuke.ENDLINE)
                    self.addKnob(knob)                    

                    self.button = nuke.PyScript_Knob("unpause_" + str(get_id(elem)), "Unpause", "Tractor_hey.unpause_job('" + str(get_id(elem)) + "','" + str(get_title(elem)) + "')")
                    self.button.setTooltip(str(get_id(elem)))
                    self.addKnob(self.button)
            
    
            #ERROR JOBS
            if(len(my_jobs_error)>0):
                self.addKnob(nuke.Text_Knob("JOBS with ERROR (" + str(len(my_jobs_error)) + "): "))
                for elem in my_jobs_error:
                    knob = nuke.Text_Knob(str(get_id(elem)), get_elementPercentage(elem))
                    knob.setValue(" ")
                    knob.clearFlag(nuke.ENDLINE)
                    self.addKnob(knob)

                    self.button = nuke.PyScript_Knob("retry_" + str(get_id(elem)), "Retry", "Tractor_hey.retry_job('" + str(get_id(elem)) + "','" + str(get_title(elem)) + "')")
                    self.button.setTooltip(str(get_id(elem)))
                    self.addKnob(self.button)
                    #print self.button.tooltip()
    
    
            #JOBS DONE
            if(len(my_jobs_done)>0):
                self.addKnob(nuke.Text_Knob("JOBS DONE in the last hour (" + str(len(my_jobs_done)) + "): "))
                for elem in my_jobs_done:
                    knob = nuke.Text_Knob(get_element(elem))
                    knob.setValue(" ")
                    knob.clearFlag(nuke.ENDLINE)
                    self.addKnob(knob)

    
            #ALL OK!
            if(len(my_jobs_paused)==0 and len(my_jobs_error)==0 and len(my_jobs_ready)==0 and len(my_jobs_active)==0 and len(my_jobs_done)==0):
                knob = nuke.Text_Knob("all your jobs are DONE!!")
                self.addKnob(knob)
            

            #divider
            self.divider = nuke.Text_Knob("divider","")
            self.addKnob(self.divider)
    
            self.button = nuke.PyScript_Knob("update", "Update", "Tractor_hey.update()")
            self.button.setFlag(nuke.STARTLINE)
            self.addKnob(self.button)
#------------------------------------------------------------------------


        add_knob()
        
 
   
    def show_modal_dialog(self):
        nukescripts.PythonPanel.showModal(self)


def main():
    global p
    p = ShapePanel()
    talk_with_tractor()
    p.show_modal_dialog()

#main()
