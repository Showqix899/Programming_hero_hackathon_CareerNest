
Project Overview:
This project is a Career Recommendation Platform named CareerNest. It helps users discover personalized job opportunities and learning resources based on their skills and career interests.


....................................................................................


Tech Stack Used:
1. Backend:
   Language: Python
2. Framework: 
   Django REST Framework
3. Other Tools:
   Git and GitHub (version control)
4. Database: SQLite
5. Redis and Celery for Background Task



......................................................................................



Project Setup:
1. For Windows, if you  don't have Docker on your Windows or Mac machine, download  -> https://docs.docker.com/desktop/
   for Linux (Ubuntu, etc) 
    sudo apt install docker.io docker-compose -y
    sudo systemctl enable docker
    sudo systemctl start docker
2. git clone https://github.com/Showqix899/Programming_hero_hackathon_CareerNest.git
3. cd PH_hackathon
4. python -m venv venv
5. venv\Scripts\activate   (for Windows)
   venv/bin/activate       (for macOS/Linux)
6. docker-compose up --build


****************************
(if you don't want to use Docker)

1. git clone https://github.com/Showqix899/Programming_hero_hackathon_CareerNest.git
2. cd PH_hackathon
3. python -m venv venv
4. chmod +x run.sh
5. ./run.sh

....................................................

Environment configuration:
1. After cloning, go to  cd PH_hackathon
2. Then create a .env file
3. Then paste in .env EMAIL_HOST_USER = youremail   EMAIL_PASS= your email's app password (this is for SMTP email service )


.............................................


Seed Data Usage Instruction:
*** It's included with docker-compose.yml and run.sh file. It's gonna execute automatically


****************************************************
Externals API >
1. Huggingface LLM ->https://router.huggingface.co/v1/moonshotai/Kimi-K2-Instruct-0905/
2. GenAI thinking model -> gemini-2.5-flash

 
