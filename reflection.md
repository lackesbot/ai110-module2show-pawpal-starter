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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
