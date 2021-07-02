# No cron job

import requests, logging, json, sys, datetime, time, random, os
from bs4 import BeautifulSoup
from github import Github
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


g = Github(ACCESS_TOKEN)

number  = random.randrange(1000000, 9999999)

file_name = "storage/analyze_"+str(number)+".txt"

# First value is requests remaining, second value is request limit.
rl1 = g.rate_limiting
print("RL1 | Limit: {}, Remaining: {}, Reset: {}.".format(
    rl1[1], rl1[0], g.rate_limiting_resettime))


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def sendIt(text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def atLeastNumberOfStars(repo, number):
    stars = int(repo.stargazers_count)
    if stars >= int(number):
        return True
    return False

def hasThisTopic(repo, *arg):
    topics = repo.get_topics()
    while topics:
        topic = topics.pop(0)
        for topicToFind in arg:
            if topicToFind in topic:
                return True
    return False

def hasThisFileInRoot(repo, *arg):
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        for filename in arg:
            if file_content.type == "dir":
                pass
            else:
                if str(filename) in (str(file_content)):
                    return True
    return False

def analyze(repo):
    degree = 0

    # > 50 stars
    if atLeastNumberOfStars(repo, 50):
        degree += 1

    # has php
    # if hasThisTopic(repo, "c++"):
    #     degree += 1
    # if hasThisTopic(repo, "management"):
    #     degree += 1
    # if hasThisTopic(repo, "startups"):
    #     degree += 1
    # if hasThisTopic(repo, "Cross-platform"):
    #     degree += 1
    # if hasThisTopic(repo, "game"):
    #     degree += 1
    # if hasThisTopic(repo, "sound"):
    #     degree += 1
    # has docker or docker compose
    # if hasThisFileInRoot(repo, "Docker", "docker-compose"):
    #     degree += 1
    if degree > 0:
        output = f'{repo.clone_url}, {repo.stargazers_count} stars, {degree} degrees'
        print(output)
        sendIt(output)

def search_github(keywords):
    """
    Parameters:
    query – string
    sort – string (‘stars’, ‘forks’, ‘updated’)
    order – string (‘asc’, ‘desc’)
    qualifiers – keyword dict query qualifiers

    :param keywords:
    :return:
    """
    query = '+'.join(keywords) + '+in:readme+in:description+language:c++'
    result = g.search_repositories(query, 'updated', 'desc')

    print(f'Found {result.totalCount} repo(s)')

    for repo in result:
        analyze(repo)



def main():
    #keywords = input('Enter keyword(s)[e.g python, flask, postgres]: ')
    #keywords = [keyword.strip() for keyword in keywords.split(',')]
    #keywords = ["desktop","windows","sound","manager","Recorder","Keyboard","Gaming","Monitor","Auto","Screen","Clock","System","Lockscreen","AutoHotkey","Editor"]
    #keywords = ["desktop"]
    #keywords = ["manager"]
    keywords = ["screen"]

    delta_hour = 0

    while True:
        now_hour = datetime.datetime.now().hour
        if delta_hour != now_hour:
            try:
                print("Searching")
                while True:
                    search_github(keywords)
            except:
                print("Error waiting for an hour")
        delta_hour = now_hour

        time.sleep(60)


if __name__ == '__main__':
    main()