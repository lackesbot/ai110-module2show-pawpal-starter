# PawPal+ Project Reflection

## 1. System Design

- a user should eneter their information and pets information
- a user should edit the tasks.
- a user should see the daily tasks.
**a. Initial design**

- Briefly describe your initial UML design.
Owner owns pet
Schedule belongs to Owner
Schedule is for Pet 
Schedule contains schedulkedTask
Scheduledtask wraps task
Scheduler creates Schedule 

- What classes did you include, and what responsibilities did you assign to each?
For my UML Digram classes I have Owner, Pet, Task, ScheduledTask, Schedule, Scheduler.
Owner class holds all the basic pet oners information such as their first and last name
Pet class holds all the pets information inluding name, gender, age, species, breed and allergies
ScheduledTask holds task and its start time and reason. The reason is included so to aid with the final schedule summary.
Schedule holds owner, pet, scheduledtask, summary and the total duration to finally display everything.
Scheduler holds a function to generate the schedule and prompt builder for the summary. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I added end_time to scheduledTask class because I had the start_time but not the end_time
Also I added available_minutes to sceheduler for the user to note how much time they have for the tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? The scheduler considers readability and overlapping.
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes. Oner tradedoff it makes is the used of index loops
- Why is that tradeoff reasonable for this scenario? Tradeoff is reasonable because it shifts the best case back to O(n^2)

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)? I used AI tools for brainsdtormioimg, writting a7 noting thongs that IO may have forgotten in my readme file and updating my functions with comments of their work. 
- What kinds of prompts or questions were most helpful? I found prompts that were specific when taking a specific section for example I hand one methiod that I just found it to be redundant and thus, I attached those lines of code for my AI and asked it, how best I can summarize that function ionto something smaller. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is. When implementing some pof the test cases it was adding irrelevant test
- How did you evaluate or verify what the AI suggested? I checked with the project desc but also with my UML diagram to ensure everything looked good. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? I tested core behavior, correctness, logic and conflict
- Why were these tests important? These test are importnat because they help evaluate and pinpoint that all reas are good and working well.

**b. Confidence**

- How confident are you that your scheduler works correctly? 4 stars
- What edge cases would you test next if you had more time? I'll test correctness, when adding multiple pets and having their schedule overlapp.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with? I'm ovrall satisfied with how well I was able to go through each section of the project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign? In terms of improving, one thoing IO want to focus more on is dedicating more time to each section, ensuring that I also tackle the problems 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project? Having specific prompst for the AI really goes along way in fulfilling the vision that you have fopr the program.
