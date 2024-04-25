# MyItmoGPT

![Static Badge](https://img.shields.io/badge/AUTHORS%3A-red) ![Static Badge](https://img.shields.io/badge/Alexey,%20Ksenia,%20Arkadiy-blue)


## How to start?
 Launching a bot involves several essential steps, each contributing to a seamless deployment process:

### 1. Cloning the Repository

This step is relatively straightforward:
```bash
    git clone https://github.com/AaLexUser/MyitmoGPT.git
```

### 2. Creating the Bot

As we highly prioritize the security of our clients, we cannot afford to host private information (such as logs and passwords) on our servers. Therefore, you need to create the bot yourself. To do this, use [BotFather](https://t.me/BotFather). We are interested in the HTTP API token - be sure to save it!

### 3. Setting up Environment Variables

Now, navigate to the recently cloned repository and create a file named ```.env``` in the ```src``` directory with the following content:

```
ISU_USERNAME={YOUR ISU USERNAME}
ISU_PASSWORD={YOUR ISO PASSWORD}
BOT_TOKEN={YOUR BOT TOKEN}
MY_TG_ID={YOUR TG ID}
YA_API_KEY= {...}
YA_DIR_ID= {...}
```

Let's break down what needs to be written here. The first three points are obvious, while the last two are well described 
in this article: [Integrating Yandex Disk API](https://habr.com/ru/articles/780008/).

```TG_ID``` is a bit more complicated - it's not your identifier with ```@```, but an immutable 
numerical value that identifies your account. To obtain it, execute the command /start in the bot [userinfobot](https://t.me/userinfobot).

### 4. Building Docker

In our repository, you can find a Dockerfile. We will use it to create a Docker image for the Python application using the Poetry tool to manage Python dependencies. To run this Dockerfile, you need to execute the docker build command in the directory containing the Dockerfile, specifying a tag for the image:



```bash
docker build -t {my-python-app}
```

### 5. Running Docker

Remember what you filled in the ```.env``` file? You now have a great opportunity to do it again!

```bash
docker run -e ISU_USERNAME=xxxxx \
-e ISU_PASSWORD=xxxxxxxx \
-e BOT_TOKEN=xxxxxxxxx \
-e MY_TG_ID=xxxxxxxxxx \
-e YA_API_KEY=xxxxxxxxxxxxx \
-e YA_DIR_ID=xxxxxxxxxxx \
itmogpt:latest
```

### 6. Enjoying the Experience

Once the bot is up and running, sit back and enjoy the experience! Interact with the bot, test its functionality, and observe its behavior in action. Whether it's automating tasks, providing assistance, or entertaining users, the bot's deployment marks the culmination of your efforts, offering a valuable addition to your platform or community.






