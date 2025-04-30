#from __future__ import print_function
import nuke
import re


def print_pf_results(xml_path, node_name, cpu, wall):
    #SETTING UP VARIABLES
    node_to_search = "<Name>" + node_name + "</Name>"
    list_of_results = []
    frame_num_filter = "<Time>"
    list_of_time_lines = []
    line_offset_cpu = 18
    line_offset_wall = 19
    xml_line_num = 0

    print(node_name + "\n")

    #OPENING UP THE XML FILE AND GO OVER ALL THE LINES TO FIND SEARCH PATTERNS
    xml_file =  open(xml_path, 'r')
    for line in xml_file:
        xml_line_num += 1
        if frame_num_filter in line: #IF FRAME NUMBER FOUND, ADDING LINE NUMBER TO FRAME NUMBER LIST
            list_of_time_lines.append(xml_line_num)
        if node_to_search in line: #IF NODE NAME FOUND, ADDING LINE NUMBER TO NODE SEARCH PATTERN LIST
            list_of_results.append(xml_line_num)
    if len(list_of_results) == 0: #IF NODE NAME NOT FOUND IN XML
        print("There is no node with this name.")
    else:
        xml_file.seek(0,0) #RESETTING THE POINTER TO THE TOP OF THE XML FILE
        xml_lines = xml_file.readlines() #STORING INDIVIDUAL XML LINES IN LIST

        #GOING OVER THE LINE NUMBERS IN WHICH THE NODE NAME WAS FOUND
        for number in list_of_results:
            #DETERMINING THE FRAME NUMBER
            index = list_of_results.index(number)
            frame_num = xml_lines[int(list_of_time_lines[index]) - 1].rstrip()
            output_frame_num = str(re.sub('[^0-9]', '', frame_num))
            #ADDING THE LINE OFFSET TO GET TO THE ACTUAL PERFORMANCE INFORMATION AND EXTRACTING NUMERIC DATA ONLY
            line_cpu = xml_lines[number+line_offset_cpu].rstrip()
            output_line_cpu = re.sub('[^0-9]', '', line_cpu)
            line_wall = xml_lines[number+line_offset_wall].rstrip()
            output_line_wall = re.sub('[^0-9]', '', line_wall)
            #PRINTING THE RESULTS
            print("FRAME " + output_frame_num + ":")
            if cpu == True:
                print("cpu - " + output_line_cpu)
            if wall == True:
                print("wall - " + output_line_wall)
            print("")
    #CLOSING THE XML FILE
    xml_file.close()


def pf_panel():
    #CREATING THE PANEL FOR USER INTERACTION
    p = nuke.Panel('PF Check')
    #ADDING KNOBS TO THE PANEL
    p.addFilenameSearch('xml path', '/tmp')
    p.addSingleLineInput('node name', '')
    p.addBooleanCheckBox('cpu', False)
    p.addBooleanCheckBox('wall', True)
    #ASSIGNING THE PANEL TO A VARIABLE
    result = p.show()
    if result: #CHECKING IF THE USER CLICKED THE "OK" BUTTON
        if p.value('cpu') == False and p.value('wall') == False: #CHECKING IF NONE OF THE CHECKBOXES ARE TICKED
            print("No performance attribute selected.")
        else: #IF AT LEAST ONE OF THE CHECKBOXES IS TICKED CONTINUE WITH THE ACTUAL XML READ OUT SCRIPT
            print_pf_results(p.value('xml path'), p.value('node name'), p.value('cpu'), p.value('wall'))
