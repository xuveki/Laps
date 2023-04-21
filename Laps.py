import time
import sys
from datetime import date
from datetime import datetime
import os

def program_quit():
    
    print("\nExited")

    sys.exit(0)  

# Iterate through the task list and write the names and times to the file

def write_task_and_times(file_object, taskNameList, taskTimeList):

    manualIndex = 0
    
    for taskNameInList in taskNameList:

        file_object.write(f"{taskNameInList.upper()} {taskTimeList[manualIndex]}")
        
        # uses current index integer that iterates with for loop. Using the index variable will call the first instance of the index value which could be an earlier task with the same name.

        manualIndex += 1

        file_object.write("\n")
    
    file_object.write("\n")

    file_object.write("\nIn total:\n")
    
    for task in repeatedTasks:
        
        file_object.write(f"\n{task.upper()} {repeatedTasks[task]}")

    file_object.write("\n")
    file_object.write(totalTimeString)

def create_file_and_write(commentInput):
    
    # open a .txt file to append
    
    # Create absolute path and find directory to feed into path.join for use with the .py file. 
    # The exec file will use sys.executable to find the path of the exec file and write to a file there
    # Exec file was created using py-installer.
    
    lapsWriteToPath = os.path.dirname(sys.executable)

    with open(os.path.join(lapsWriteToPath, "Laps-History.txt"), "a+") as file_object:

        file_object.seek(0)

        checkedFileForText = file_object.read(100)
        
        # If file is not empty then add line breaks before first line
        if len(checkedFileForText) > 0:
            file_object.write("\n\n")

        file_object.write("Date: ")
        file_object.write(f"{str(todaysDate)}.")
        
        file_object.write(f"\nStarted on {todayDayOfWeekFormat} at {programStartTimeForFileWrite}.")

        file_object.write(f'\nEnded on {programEndDayOfWeekFormat} at {datetime.now().strftime("%I:%M %p")}.\n\n')

        file_object.write("Tasks and times:\n\n")

        write_task_and_times(file_object, taskNameList, taskTimeList)
        
        file_object.write(f"\n\nComments:\n\n{commentInput}\n")
        
        file_object.write("-" * 20)

def calculate_repeated_task_times():
    
    for task in repeatedTasks:
    
        if repeatedTasks[task] > 3600:
            repeatedTasks[task] /= 3600
            repeatedTasks[task] = round(repeatedTasks[task], 2)
            repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Hours."

        elif repeatedTasks[task] > 60.00:
            repeatedTasks[task] /= 60.00
            repeatedTasks[task] = round(repeatedTasks[task], 2)
            repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Minutes."

        else:
            repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Seconds."

# Print summary of tasks and times before writing data to file

def final_print():
    
    print("\nOkay. You want to exit. Add any comments below:\n")
    commentInput = input()
    print("\n")

    print(f"{str(todaysDate)}\n")

    taskNamesAndTimes = "\n".join("{} {}".format(x.upper(), y) for x, y in zip(taskNameList, taskTimeList))
    print(taskNamesAndTimes)
    
    calculate_repeated_task_times()

    print("\nIn total:\n")
    
    for task in repeatedTasks:
        
        print(task.upper(), repeatedTasks[task], sep=" ")

    # Print totalTimeString
    print(totalTimeString)

    # ASCII divider
    print("\n" + "-" * 20)
    print("Comments:\n" + commentInput)

    create_file_and_write(commentInput)

def are_you_sure_you_want_to_exit():
    
    print("You haven't completed your current task yet. Are you sure you want to exit? Type \"Yes\" or \"No\".")

    checkExitResponse = input()

    if checkExitResponse.casefold() == "yes".casefold():
        
        return True
    
    elif checkExitResponse.casefold() == "no".casefold():
        
        print("Okay.")
        return False
    
    askThemAgainResponse = are_you_sure_you_want_to_exit()

    return askThemAgainResponse

# Take input from user. If they want to exit, where in the program are they and react accordingly

def check_quit(userInput):
    
    if userInput.casefold() != 'exit'.casefold():

        return False

    if hasNotEnteredFirstTask == True:

        program_quit()
        return

    if taskWasEnteredAndCompleted == False:

        areTheySure = are_you_sure_you_want_to_exit()

        if areTheySure == False:
            
            return False

    return True

def ask_again():

    print("Type \"done\" to finish timing a task. Type \"exit\" to abandon your current task and exit.")
    print("\n")

    userInput = input()
    
    return userInput

# Check if they're done, checks if they want to exit. If not, keeps asking them. May call check_quit() and ask_again()

def check_input(userInput):
    
    if userInput.casefold() == "done".casefold():
        
        return

    checkQuitResult = check_quit(userInput)

    if checkQuitResult == True:

        endProgram = True
        return endProgram

    doneOrExitResponse = ask_again()
    
    checkAgainResponse = check_input(doneOrExitResponse)

    return checkAgainResponse

def print_task_recap(taskName, taskTimeUnits, totalTimeString, taskTime):

    print(f"{str(taskTime)} {str(taskTimeUnits)} of {taskName.upper()}.")
    print(totalTimeString)

def add_total_time_repeated_tasks(taskNameList, taskName, taskTime, taskTimesInSeconds):
    
    repeatedTasksTotalTimeSum = taskTime

    for task in range(len(taskNameList)):

        hasTheTaskBeenDoneBefore = taskName.upper() == taskNameList[task].upper()
        
        if hasTheTaskBeenDoneBefore == False:

            continue

        repeatedTasksTotalTimeSum += round(taskTimesInSeconds[task], 2)
        repeatedTasks[taskName] = repeatedTasksTotalTimeSum

    return repeatedTasks

# Calculate task time units and save time strings for later use

def calculate_task_times(taskTime, totalTime):

    if taskTime > 3600:
        taskTime /= 3600
        taskTime = round(taskTime, 2)
        taskTimeUnits = "Hours"
        taskTimeString = "for " + str(taskTime) +  " Hours."

    elif taskTime > 60.00:
        taskTime /= 60.00
        taskTime = round(taskTime, 2)
        taskTimeUnits = "Minutes"
        taskTimeString = "for " + str(taskTime) +  " Minutes."

    else:
        taskTimeUnits = "Seconds"
        taskTimeString = "for " + str(taskTime) +  " Seconds."

    if totalTime > 3600:
        totalTime /= 3600
        totalTime = round(totalTime, 2)
        totalTimeUnits = "Hours"
        totalTimeString = str(totalTime) + " Hours in total."

    elif totalTime > 60.00:
        totalTime /= 60.00
        totalTime = round(totalTime, 2)
        totalTimeUnits = "Minutes"
        totalTimeString = str(totalTime) + " Minutes in total."
        
    else:
        totalTimeUnits = "Seconds"
        totalTimeString = str(totalTime) + " Seconds in total."

    return taskTimeString, totalTimeString, taskTimeUnits, totalTimeUnits, taskTime

# START

# The stack:
# check_input -> check_quit -> back to check_input -> ask_again -> back and check_input(recurse)
# check_quit might call are_you_sure... and if they are -> return into check_quit -> final_print
# That calls create_file_and_write
# create_file_and_write calls write_task_and_times and returns through the stack into main
# check_input 's return is stored into checkInputResult

programStartTime = time.time()

programStartTimeForFileWrite = datetime.now().strftime("%I:%M %p")

todaysDate = date.today()
todayDayOfWeekFormat = datetime.now().strftime('%A')

taskNameList = []
taskTimeList = []
taskTimesInSeconds = []
repeatedTasks = {}

hasNotCompletedATaskMessage = "Nothing was done before program exit."
totalTimeString = hasNotCompletedATaskMessage

taskNumber = 1

hasNotEnteredFirstTask = True

programOn = True

while programOn:

    print("\nType your task's name. \nType \"done\" to time your task or type \"exit\" to stop and save.\n")
    print("So what are you working on?\n")
    taskName = input()
    
    if check_quit(taskName) == True:

        final_print()
        
        break

    hasNotEnteredFirstTask = False
    
    taskWasEnteredAndCompleted = False

    taskStartTime = time.time()
    taskStartTimeHourFormat = datetime.now().strftime("%I:%M:%S %p")

    print(f"\nStarting {taskName.upper()} at {str(taskStartTimeHourFormat)}\n")
    print(f"Type \"done\" when you're done with \"{taskName}\".\n")
    secondInputExpectedToBeDone = input()

    checkInputResult = check_input(secondInputExpectedToBeDone)

    print(" ")

    checkInputForQuit = checkInputResult
    if checkInputForQuit == True:

        final_print()

        break

    taskWasEnteredAndCompleted = True

    currentTime = time.time()

    taskTime = round((currentTime - taskStartTime), 2)

    totalTime = round((currentTime - programStartTime), 2)

    print(f"{taskName.upper()} (Task No. {str(taskNumber)})")

    timeStringsReturned = calculate_task_times(taskTime, totalTime)

    totalTimeString = timeStringsReturned[1]

    repeatedTasksForPrint = add_total_time_repeated_tasks(taskNameList, taskName, taskTime, taskTimesInSeconds)

    taskNameList.append(taskName)
    taskTimeList.append(timeStringsReturned[0])
    taskTimesInSeconds.append(taskTime)

    print_task_recap(taskName, timeStringsReturned[2], timeStringsReturned[1], timeStringsReturned[4])

    # ASCII divider
    print("-" * 20)

    taskNumber += 1
    programEndDayOfWeekFormat = datetime.now().strftime('%A')

program_quit()