import time
import sys
import os
from datetime import date, datetime
from colorama import Fore, Back, Style, just_fix_windows_console
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

def program_quit():
    
  console.print("\nExiting program.\n", style="bold")
  console.print("Goodbye", style="bold")
  #console.print(Markdown("★─▄█▀▀║░▄█▀▄║▄█▀▄║██▀▄║─★\n★─██║▀█║██║█║██║█║██║█║─★\n★─▀███▀║▀██▀║▀██▀║███▀║─★\n★───────────────────────★\n★───▐█▀▄─ ▀▄─▄▀ █▀▀──█───★\n★───▐█▀▀▄ ──█── █▀▀──▀───★\n★───▐█▄▄▀ ──▀── ▀▀▀──▄───★"))
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
  
  # Create absolute path and find directory. Find parent directory of that and create history/ directory if there isn't one already 
  # Feed into path.join for use with the .py file. 
  # The exec file will use sys.executable to find the path of the exec file and write to a file there
  # Exec file was created using py-installer.
  
  absolutePath = os.path.realpath(sys.argv[0])
  directoryName = os.path.dirname(absolutePath)
  parentDirectory = os.path.dirname(directoryName)

  historyDir = parentDirectory + "/history/"

  if os.path.exists(historyDir) == False:
    os.mkdir(historyDir)
  
  # open a .txt file in append/read mode as a "file_object"
  with open(os.path.join(historyDir, "laps-history.txt"), "a+") as file_object:

    file_object.seek(0)

    checkedFileForText = file_object.read(100)
    
    # If file is not empty then add line breaks before first line
    if len(checkedFileForText) > 0:
      file_object.write("\n\n")

    file_object.write("Date: ")
    file_object.write(f"{str(PROGRAM_START_DATE)}.")
    
    file_object.write(f"\nStarted on {PROGRAM_START_DAY_OF_WEEK} at {PROGRAM_START_TIME_FOR_WRITE}.")

    programEndDayOfWeek = datetime.now().strftime('%A')
    file_object.write(f'\nEnded on {programEndDayOfWeek} at {datetime.now().strftime("%I:%M %p")}.\n\n')

    file_object.write("Tasks and times:\n\n")

    write_task_and_times(file_object, taskNameList, taskTimeList)
    
    file_object.write(f"\n\nComments:\n\n{commentInput}\n")
    
    file_object.write("-" * 20)

    console.print(f"\nWriting to {historyDir}")

def calculate_repeated_task_times():
    
  for task in repeatedTasks:
  
    if repeatedTasks[task] > SECONDS_IN_HOUR:
      repeatedTasks[task] /= SECONDS_IN_HOUR
      repeatedTasks[task] = round(repeatedTasks[task], 2)
      repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Hours."

    elif repeatedTasks[task] > SECONDS_IN_MINUTE:
      repeatedTasks[task] /= SECONDS_IN_MINUTE
      repeatedTasks[task] = round(repeatedTasks[task], 2)
      repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Minutes."

    else:
      repeatedTasks[task] = "for " + str(repeatedTasks[task]) +  " Seconds."

# Print summary of tasks and times before writing data to file

def final_print():
  
  console.print("\nExiting Laps. First, [bold]here's a breakdown of your day:[/bold]\n")

  console.print(f"{str(PROGRAM_START_DATE)}\n")

  if date.today() != PROGRAM_START_DATE:
    console.print(f"Ended on {str(date.today())}\n")

  taskNamesAndTimes = "\n".join("{} {}".format(x.upper(), y) for x, y in zip(taskNameList, taskTimeList))
  console.print(taskNamesAndTimes, "\n",)
  
  calculate_repeated_task_times()
  
  for task in repeatedTasks:
    console.print("A total of", task.upper(), repeatedTasks[task], sep=" ")

  # Print totalTimeString
  console.print(totalTimeString)

  console.print("\n" + "-" * 20)
  
  commentInput = console.input("[green]Add any comments you have below:[/green]\n\n")

  return commentInput

def are_you_sure_you_want_to_exit():
    
  console.print("You haven't completed your current task yet. Are you sure you want to exit? Type \"Yes\" or \"No\".")

  checkExitResponse = input()

  if checkExitResponse.casefold() == "yes".casefold():
    return True
  
  elif checkExitResponse.casefold() == "no".casefold():
    print("Okay.")
    return False
  
  askThemAgainResponse = are_you_sure_you_want_to_exit()

  return askThemAgainResponse

def ask_again():

  console.print("Type \"done\" to finish timing a task, \"rename\" to rename your task, or \"exit\" to abandon your current task and exit.")

  userInput = input()
  print()
  
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
      return hours * SECONDS_IN_HOUR + minutes * SECONDS_IN_MINUTE + seconds
    
    except ValueError:
      return None  # Invalid format

  # Check if the input string is in the format "X hour(s)", "X minute(s)", or "X second(s)"
  if ' ' in userInput:
    
    parts = userInput.split(' ')
    
    if len(parts) != 2:
      return None  # Invalid format
    
    try:
      value = float(parts[0])
      unit = parts[1].lower()
      if unit.endswith('s'):
        unit = unit[:-1]  # Remove 's' from the unit if present
      if unit == 'hour' or unit == 'hours':
        return value * SECONDS_IN_HOUR
      elif unit == 'minute' or unit == 'minutes':
        return value * SECONDS_IN_MINUTE
      elif unit == 'second' or unit == 'seconds':
        return value
      else:
        return None  # Invalid unit
    
    except ValueError:
      return None  # Invalid format

  return None

def keep_checking_for_rename(userInput):
  
  taskLengthInput = userInput

  while rename_task(taskLengthInput) != False:

    console.print(f"How long did you work on [indian_red1]{taskName.upper()}?\n")
    taskLengthInput = input()
  
  return taskLengthInput

def create_task_manually(userInput):

  if userInput.casefold() != "manual".casefold():

    return False
  
  console.print("\nYou'd like to [bold]manually[/bold] enter a task and time. What task would you like to enter?\n")
  taskName = input()

  console.print(f"\nGot it. How long did you work on [indian_red1]{taskName.upper()}[/indian_red1]?\nYou can type this in HH:MM:SS format or in regular English (e.g. 20 minutes).")
  console.print(f"Type \"rename\" to rename your task.\n")

  taskLengthInput = input()

  taskLengthInput = keep_checking_for_rename(taskLengthInput)

  timeInSeconds = convert_to_seconds(taskLengthInput)
  
  while timeInSeconds is None:

    taskLengthInput = console.input("\nLooks like you typed your time in an invalid format (or maybe you tried typing in \"rename\"). Try typing it in [bold]either HH:MM:SS format or in regular English (e.g. 1 hour, 2 minutes, or 3 seconds).[/bold]\n\n")

    taskLengthInput = keep_checking_for_rename(taskLengthInput)
    
    timeInSeconds = convert_to_seconds(taskLengthInput)

  global totalTime, totalTimeString
  totalTime += timeInSeconds

  timeStringsReturned = calculate_task_times(timeInSeconds, totalTime)

  totalTimeString = timeStringsReturned[1]
  
  addTasksToLists(taskName, timeInSeconds, timeStringsReturned)

  print_task_recap(taskName, timeStringsReturned[2], timeStringsReturned[1], timeStringsReturned[4])
  
  # ASCII divider
  print("-" * 20)

  global hasNotEnteredFirstTask
  # global taskWasEnteredAndCompleted 
  hasNotEnteredFirstTask = False
  # taskWasEnteredAndCompleted = True

  userDone = True

  return userDone

def cancel_task(userInput):

  if userInput.casefold() != "cancel".casefold():

      return None

  console.print("Are you sure you want to cancel your current task? You'll lose the data. Type [green]\"yes\"[/green] or [green]\"no\"[/green]\n")

  answer = input()

  if answer.casefold() == "yes".casefold():
    return True
  
  elif answer.casefold() == "no".casefold():
    return None

  return cancel_task(userInput)

def rename_task(userInput):

  if userInput.casefold() != "rename".casefold():
    return False

  print("What would you like to change or rename your task to?\n")

  newTaskName = input()
  print("\n")
  console.print(f"Task name changed to [indian_red1]{newTaskName.upper()}.[/indian_red1]\n")
  
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

  rename_task(userInput)
  
  if cancel_task(userInput) == True:

    return 3

  doneOrExitResponse = ask_again()
  
  checkAgainResponse = check_input(doneOrExitResponse)

  return checkAgainResponse

def print_task_recap(taskName, taskTimeUnits, totalTimeString, taskTime):

  global taskNumber

  console.print(f"[bold]{taskName.upper()}[/bold] (Task No. {str(taskNumber)})")
  console.print(f"{str(taskTime)} {str(taskTimeUnits)} of {taskName.upper()}.", style="bold")
  console.print(totalTimeString, style="bold")
  
  taskNumber += 1

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

def calculate_task_times(taskTime, totalTime):

  if taskTime > SECONDS_IN_HOUR:
    taskTime /= SECONDS_IN_HOUR
    taskTime = round(taskTime, 2)
    taskTimeUnits = "Hours"
    taskTimeString = "for " + str(taskTime) +  " Hours."

  elif taskTime > SECONDS_IN_MINUTE:
    taskTime /= SECONDS_IN_MINUTE
    taskTime = round(taskTime, 2)
    taskTimeUnits = "Minutes"
    taskTimeString = "for " + str(taskTime) +  " Minutes."

  else:
    taskTimeUnits = "Seconds"
    taskTimeString = "for " + str(taskTime) +  " Seconds."

  if totalTime > SECONDS_IN_HOUR:
    totalTime /= SECONDS_IN_HOUR
    totalTime = round(totalTime, 2)
    totalTimeUnits = "Hours"
    totalTimeString = str(totalTime) + " Hours in total."

  elif totalTime > SECONDS_IN_MINUTE:
    totalTime /= SECONDS_IN_MINUTE
    totalTime = round(totalTime, 2)
    totalTimeUnits = "Minutes"
    totalTimeString = str(totalTime) + " Minutes in total."
      
  else:
    totalTime = round(totalTime, 2)
    totalTimeUnits = "Seconds"
    totalTimeString = str(totalTime) + " Seconds in total."

  return taskTimeString, totalTimeString, taskTimeUnits, totalTimeUnits, taskTime

def check_premature_done(taskName):
    
  if taskName.casefold() != "done".casefold():
    return taskName

  console.print("You can't be done yet! Type a [green]task name[/green] first or \"exit\" if you'd like to quit.\n")
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

PROGRAM_START_TIME = time.time() # not currently using this. should delete?
PROGRAM_START_TIME_FOR_WRITE = datetime.now().strftime("%I:%M %p")
PROGRAM_START_DATE = date.today()
PROGRAM_START_DAY_OF_WEEK = datetime.now().strftime('%A')

SECONDS_IN_HOUR = 3600
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

taskNameList = []
taskTimeList = []
taskTimesInSecondsList = []
repeatedTasks = {}

HAS_NOT_COMPLETED_A_TASK_MESSAGE = "Nothing was done before program exit."
totalTimeString = HAS_NOT_COMPLETED_A_TASK_MESSAGE
totalTime = 0
taskTime = 0
taskNumber = 1

hasNotEnteredFirstTask = True
taskWasEnteredAndCompleted = False
prompt = "So, what are you working on?\n"

console = Console()
just_fix_windows_console()

programOn = True
 
console.print(" ", justify="center")
console.print("Welcome to Laps!", style="bold", justify="center")

while programOn:

  console.print("\nType in your task's name. \nType \"done\" to time your task, \"rename\" to edit your task, \"manual\" to enter a task manually, or \"exit\" to stop and save.\n")
  console.print(f"{prompt}", style="green")
  taskName = input()

  prompt = "What are you working on now?\n"

  taskName = check_premature_done(taskName)
  checkResultForQuit = check_quit(taskName)
  
  if checkResultForQuit == True:

    userCommentReturned = final_print()
    create_file_and_write(userCommentReturned)
    break

  elif create_task_manually(taskName) == True:

    taskWasEnteredAndCompleted = True
    continue

  hasNotEnteredFirstTask = False
  
  taskWasEnteredAndCompleted = False

  taskStartTime = time.time()
  taskStartTimeHourFormat = datetime.now().strftime("%I:%M:%S %p")

  console.print(f"\nStarting [indian_red1]{taskName.upper()}[/indian_red1] at {str(taskStartTimeHourFormat)}\n")
  console.print(f"Type \"done\" when you're done with \"{taskName}\".\n")
  secondInput = input()
  print()

  CheckInputForManual = create_task_manually(secondInput)

  checkInputResult = check_input(secondInput)

  checkInputForQuit = checkInputResult
  if checkInputForQuit == 2:

    userCommentReturned = final_print()
    create_file_and_write(userCommentReturned)

    break
  
  elif checkInputForQuit == 3:
    continue

  taskWasEnteredAndCompleted = True

  currentTime = time.time()

  taskTime = round((currentTime - taskStartTime), 2)

  totalTime += taskTime 

  timeStringsReturned = calculate_task_times(taskTime, totalTime)

  totalTimeString = timeStringsReturned[1]

  addTasksToLists(taskName, taskTime, timeStringsReturned)

  print_task_recap(taskName, timeStringsReturned[2], timeStringsReturned[1], timeStringsReturned[4])

  # ASCII divider
  console.print("-" * 20)

program_quit()
