#!/usr/bin/env python3

import sys
import os #USE OS.WALK, CANT USE OS.SYSTEM#
import re

USAGE = "Usage: myfind [--regex=pattern | --name=filename] directory [command]"

# You can change this function signature if desired
def find(directory, regex=None, name=None, command=None):
    """A simplified find command."""

    command_clone = command #for error printing purposes later

    #ERROR HANDLING: NAME AND REGEX
    if(name != None and regex != None):
        sys.exit(USAGE)

    adds = [];#paths/addresses of each file and directory
    if(directory is None):
        sys.exit(USAGE)

    if(regex is None):
        regex = ".*" #MATCHES EVERYTHING
    counter = 0
    walk = list(os.walk(directory)) #FORMAT: [DIRECTORY],[DIRECORIES],[FILES]

    if(walk == []):
        sys.exit(USAGE)

    #SETS UP LIST OF ADDRESSES TO PRINT START
    while(counter < len(walk)):
        start, dirs, files = walk[counter]

        if(name is None):
            temp = start.split("/")
            if(re.search(regex, temp[len(temp) - 1])):
                adds.append(start)

        else:
            temp_dir = start.split("/")
            if(name == temp_dir[len(temp_dir) - 1]):
                adds.append(start)



        #PREPARE "TOPRINT" LIST
        i = 0
        while(i < len(files)):

            if(name is None):
                toPrint=start + "/" + files[i]
                temp = toPrint.split("/")
                if(re.search(regex, temp[len(temp)-1])):
                    adds.append(toPrint)

            else:

                if(files[i] == name):
                    toPrint = start + "/" + files[i]
                    adds.append(toPrint)


            i += 1

        counter += 1
    #SET UP LIST OF ADDRESSES TO PRINT END
        #NO COMMAND ()
    if(command is None):
        i = 0
        while(i < len(adds)):
            print(adds[i])
            i += 1
        #COMMAND
    else:

        command = command.split()
        comm = command[0]
        flags = []


        #SET UP FLAGS (SKIP 0, COMMAND)
        i = 1
        while(i < len(command)):
            flags.append(command[i])
            i += 1
        #SET UP FLAGS DONE

        #EXEC LOOP START
        retCodes = []
        i = 0

        try:
            while(i < len(adds)):
                pid = os.fork()

                if(pid == 0): #CHILD
                    j = 0
                    while(j < len(flags)):
                        flags[j] = flags[j].replace("{}", adds[i])
                        j += 1

                    comm = comm.replace("{}",adds[i])
                    fName = comm.split("/")
                    fName = fName[len(fName)-1]
                    flags.insert(0, fName)
                    os.execvp(comm, flags)

                if(pid == -1): #FAILED FORK
                    j = 0
                    while(j < len(flags)):
                        flags[j] = flags[j].replace("{}", adds[i])
                        j += 1

                    err = adds[i]
                    j =0
                    while(j < len(flags)):
                        err += " " + flags[j]
                        j += 1
                    sys.stderr.write("Error: Unable to start process '" + err + "'\n")

                else: #PARENT
                    os.wait()

                i += 1

        except PermissionError: #FILE NOT EXECUTABLE
            command_clone=command_clone.replace("{}", adds[i])
            sys.stderr.write("Error: Unable to start process '"+command_clone+"'\n")

        except FileNotFoundError: #COMMAND DOESN'T EXIST
            command_clone=command_clone.replace("{}", adds[i])
            sys.stderr.write("Error: Unable to start process '"+command_clone+"'\n")

    #EXEC LOOP DONE

    #DETERMINE RETURN CODE
    if(command != None and not os.path.exists("/usr/bin/"+comm) and not os.path.exists("/bin/"+comm)):
        if(comm == "{}"):
            return 0 #VALID COMMAND
        return 1 #INVALID COMMAND
    else:
        return 0 #VALID COMMAND

    #END OF FIND()


if __name__ == "__main__":
    # TODO parse arguments here

    #EXIT WITH ERROR IF EXTRA ARGUMENTS/FLAGS GIVEN
    if(len(sys.argv) > 4):
        sys.exit(USAGE)

    #DEFAULT VARIABLE PARAMETERS TO NONE
    directory = None
    regex = None
    name = None
    command = None

    #SET UP PARAMETER VARIABLES
    i = 1
    dirDone = False
    while(i < len(sys.argv)):
        temp = sys.argv[i].split("=")
        if(len(temp) > 1):
            if(temp[0] == "--regex"):
                regex=temp[1]
            elif(temp[0] == "--name"):
                name = temp[1]
        else:
            if(not dirDone):
                directory = sys.argv[i]
                dirDone = True

            elif(dirDone):
                command = sys.argv[i]

        i += 1
    #SET UP PARAMETER VARIABLES DONE


    code = find(directory, regex = regex, name = name, command = command)
    sys.exit(code)
