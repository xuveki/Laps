import time
import sys
from datetime import date, datetime
import os

def program_quit():
    
    print("\nExited")

    sys.exit(0)  

# Iterate through the task list and write the names and times to the file

def write_task_and_times(file_object, taskNameList, taskTimeList):

    manualIndex = 0
    
    for taskName in taskNameList:

        file_object.write(f"{taskName.upper()} {taskTimeList[manualIndex]}")
        
        # uses current index integer that iterates with for loop. Using the index variable will call the first instance of the index value which could be an earlier task with the same name.

        manualIndex += 1

        file_object.write("\n")
    
    #file_object.write("\n")
    
    for task in repeatedTasks:
        
        file_object.write(f"\nA total of {task.upper()} {repeatedTasks[task]}")

    file_object.write("\n")
    file_object.write(totalTimeString)

def create_file_and_write(commentInput):
    
    # open a .txt file to append
    
    # Create absolute path and find directory to feed into path.join for use with the .py file. 
    # The exec file will use sys.executable to find the path of the exec file and write to a file there
    # Exec file was created using py-installer.
    
    absolutePath = os.path.realpath(sys.argv[0])
    directoryName = os.path.dirname(absolutePath)
    
    # open a .txt file in append/read mode as a "file_object"
    with open(os.path.join(directoryName, "Laps-History.txt"), "a+") as file_object:

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
    print(taskNamesAndTimes, "\n",)
    
    calculate_repeated_task_times()
    
    for task in repeatedTasks:
        
        print("A total of", task.upper(), repeatedTasks[task], sep=" ")

    # Print totalTimeString
    print(totalTimeString)

    # ASCII divider
    print("\n" + "-" * 20)
    print("Comments:\n" + commentInput)

    return commentInput

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

def ask_again():

    print("Type \"done\" to finish timing a task, \"change\" to edit your task, or \"exit\" to abandon your current task and exit.")

    userInput = input()
    print("\n")
    
    return userInput

def convert_to_seconds(userInput):
            
    # Check if the input string is in the format HH:MM:SS
    if ':' in userInput:
        
        parts = userInput.split(':')

        if len(parts) != 3:
            return None  # Invalid format
        
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        
        except ValueError:
            return None  # Invalid format

    # Check if the input string is in the format "X hour(s)", "X minute(s)", or "X second(s)"
    if ' ' in userInput:
        
        parts = userInput.split(' ')
        
        if len(parts) != 2:
            return None  # Invalid format
        
        try:
            value = int(parts[0])
            unit = parts[1].lower()
            if unit.endswith('s'):
                unit = unit[:-1]  # Remove 's' from the unit if present
            if unit == 'hour' or unit == 'hours':
                return value * 3600
            elif unit == 'minute' or unit == 'minutes':
                return value * 60
            elif unit == 'second' or unit == 'seconds':
                return value
            else:
                return None  # Invalid unit
        
        except ValueError:
            return None  # Invalid format

    return None

def manual_task_input(userInput):

    if userInput.casefold() != "manual".casefold():

        return False
    
    print("\nYou'd like to manually enter a task and time. What task would you like to enter?\n")
    taskName = input()
    
    print(f"\nGot it. How long did you work on {taskName}?\nYou can type this in HH:MM:SS format or as in regular English (e.g. 20 minutes)\n")

    taskLengthInput = input()

    timeInSeconds = convert_to_seconds(taskLengthInput)
    
    while timeInSeconds is None:

        taskLengthInput = input("\nLooks like you typed your time in an invalid format. Try typing it in either HH:MM:SS format or in regular English (e.g. 1 hour, 2 minutes, or 3 seconds).")

    global totalTime, totalTimeString
    totalTime += timeInSeconds

    timeStringsReturned = calculate_task_times(timeInSeconds, totalTime)

    totalTimeString = timeStringsReturned[1]
    
    addTasksToLists(taskName, timeInSeconds, timeStringsReturned)

    print_task_recap(taskName, timeStringsReturned[2], timeStringsReturned[1], timeStringsReturned[4])

    global hasNotEnteredFirstTask
    # global taskWasEnteredAndCompleted 
    hasNotEnteredFirstTask = False
    # taskWasEnteredAndCompleted = True

    userDone = True

    return userDone

def change_task_name(userInput):

    if userInput.casefold() != "change".casefold():

        return False

    print("What would you like to change your task to?\n")

    newTaskName = input()
    print("\n")
    print(f"Task name changed to {newTaskName}.\n")
    
    global taskName
    taskName = newTaskName

    return

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

# Check if they're done, checks if they want to exit. Checks if they want to change the task name. If not, keeps asking them. May call check_quit() and ask_again()

def check_input(userInput):
    
    if userInput.casefold() == "done".casefold():
        
        return 1

    checkQuitResult = check_quit(userInput)

    if checkQuitResult == True:

        endProgram = 2
        return endProgram

    change_task_name(userInput)

    doneOrExitResponse = ask_again()
    
    checkAgainResponse = check_input(doneOrExitResponse)

    return checkAgainResponse

def print_task_recap(taskName, taskTimeUnits, totalTimeString, taskTime):

    print(f"{str(taskTime)} {str(taskTimeUnits)} of {taskName.upper()}.")
    print(totalTimeString)

def add_total_time_repeated_tasks(taskNameList, taskName, taskTime, taskTimesInSecondsList):
    
    repeatedTasksTotalTimeSum = taskTime

    # Check for repeated tasks not counting the last entry: range(len -1)

    for task in range(len(taskNameList) - 1):

        hasTheTaskBeenDoneBefore = taskName.upper() == taskNameList[task].upper()
        
        if hasTheTaskBeenDoneBefore == False:

            continue

        repeatedTasksTotalTimeSum += taskTimesInSecondsList[task]
        repeatedTasksTotalTimeSum = round(repeatedTasksTotalTimeSum, 2)
        repeatedTasks[taskName] = repeatedTasksTotalTimeSum

    return repeatedTasks

def addTasksToLists(taskName, taskTime, timeStringsReturned):

    taskNameList.append(taskName)
    taskTimeList.append(timeStringsReturned[0])
    taskTimesInSecondsList.append(taskTime)

    add_total_time_repeated_tasks(taskNameList, taskName, taskTime, taskTimesInSecondsList)

    return

# taskNameList = repeatedTasks[0]
# taskTimeList = repeatedTasks[1]
# taskTimesInSecondsList = repeatedTasks[2]

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

def check_premature_done(taskName):
    
    if taskName.casefold() != "done".casefold():

        return taskName

    print("You can't be done yet! Type a task name first or \"exit\" if you'd like to quit.\n")
    newInput = input()

    taskName = check_premature_done(newInput)
    
    return taskName

# START

# The stack:
# check_input -> check_quit -> back to check_input -> ask_again -> back and check_input(recurse)
# check_quit might call are_you_sure... and if they are -> return into check_quit -> final_print
# create_file_and_write
# create_file_and_write calls write_task_and_times and returns through the stack into main
# check_input 's return is stored into checkInputResult

programStartTime = time.time()

programStartTimeForFileWrite = datetime.now().strftime("%I:%M %p")

todaysDate = date.today()
todayDayOfWeekFormat = datetime.now().strftime('%A')
programEndDayOfWeekFormat = datetime.now().strftime('%A')

taskNameList = []
taskTimeList = []
taskTimesInSecondsList = []
repeatedTasks = {}

hasNotCompletedATaskMessage = "Nothing was done before program exit."
totalTimeString = hasNotCompletedATaskMessage
totalTime = 0
taskTime = 0

taskNumber = 1

hasNotEnteredFirstTask = True
taskWasEnteredAndCompleted = False

programOn = True

print("Welcome to Laps!")

while programOn:

    print("\nType your task's name. \nType \"done\" to time your task, \"change\" to edit your task, or \"exit\" to stop and save.\n")
    print("So what are you working on?\n")
    taskName = input()

    taskName = check_premature_done(taskName)
    checkResult = check_quit(taskName)
    
    if checkResult == True:

        userCommentReturned = final_print()
        create_file_and_write(userCommentReturned)
        break

    elif manual_task_input(taskName) == True:

        taskWasEnteredAndCompleted = True
        continue

    hasNotEnteredFirstTask = False
    
    taskWasEnteredAndCompleted = False

    taskStartTime = time.time()
    taskStartTimeHourFormat = datetime.now().strftime("%I:%M:%S %p")

    print(f"\nStarting {taskName.upper()} at {str(taskStartTimeHourFormat)}\n")
    print(f"Type \"done\" when you're done with \"{taskName}\".\n")
    secondInput = input()
    print("\n")

    CheckInputForManual = manual_task_input(secondInput)

    checkInputResult = check_input(secondInput)

    checkInputForQuit = checkInputResult
    if checkInputForQuit == 2:

        userCommentReturned = final_print()
        create_file_and_write(userCommentReturned)

        break

    taskWasEnteredAndCompleted = True

    currentTime = time.time()

    taskTime = round((currentTime - taskStartTime), 2)

    totalTime += taskTime 

    timeStringsReturned = calculate_task_times(taskTime, totalTime)

    totalTimeString = timeStringsReturned[1]

    addTasksToLists(taskName, taskTime, timeStringsReturned)

    print(f"{taskName.upper()} (Task No. {str(taskNumber)})")

    print_task_recap(taskName, timeStringsReturned[2], timeStringsReturned[1], timeStringsReturned[4])

    # ASCII divider
    print("-" * 20)

    taskNumber += 1
    programEndDayOfWeekFormat = datetime.now().strftime('%A')

program_quit()