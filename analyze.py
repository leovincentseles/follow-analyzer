import requests
import sys
import time

def fetchFromAPI(link: str, token: str) -> dict[int, dict[str: str]]:    
    per_page, page = 100, 1
    resultDict = {}
    
    while True:
        payload = {"per_page": per_page, "page": page}
        responseArr = requests.get(url=link, params=payload, auth=('user', token)).json()
        if len(responseArr) == 0:
            break
    
        for element in responseArr:        
            try:
                resultDict[element["id"]] = element
            except:
                print(payload)
                print(element)
        page += 1
        print(len(resultDict), end=" ")
        sys.stdout.flush()
        time.sleep(5)

    print()
    return resultDict


def genResult(followingNotFollower: dict[str, str], followerNotFollowing: dict[str, str], fileName: str) -> None:
    with open(fileName, "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("\t<head>\n")
        f.write("\t\t<title>Analyzed results</title>\n")
        f.write("\t</head>\n")
        f.write("\t<body>\n")

        f.write(f"\t\t<h1>The people you follow but they don't follow back ({len(followingNotFollower)})</h1>\n")
        f.write("\t\t<ul>\n")
        for key, value in followingNotFollower.items():
            f.write(f'<li><a href="{value["html_url"]}">{value["login"]}</a></li>\n')
        f.write("</ul>\n")

        f.write(f"\t\t<h1>The people who follow you but you don't follow back ({len(followerNotFollowing)})</h1>\n")
        f.write("\t\t<ul>\n")
        for key, value in followerNotFollowing.items():
            f.write(f'<li><a href="{value["html_url"]}">{value["login"]}</a></li>\n')
        f.write("</ul>\n")

        f.write("\t</body>\n")
        f.write("</html>\n")

# User name and access token
username = input("username: ")
token = input("Token (press enter if don't have one):")

# Get the following information
link = f"https://api.github.com/users/{username}/following"
print(f"Collect the following of {username}: ", end="")
sys.stdout.flush()
following = fetchFromAPI(link, token)

# Get the followers information
link = f"https://api.github.com/users/{username}/followers"
print(f"Collect the follower of {username}: ", end="")
sys.stdout.flush()
follower = fetchFromAPI(link, token)

# Analyze the result for the following and follower
followingNotFollower = {key: value for key, value in following.items() if key not in follower}
followerNotFollowing = {key: value for key, value in follower.items() if key not in following}
del following
del follower

# Generate the result html which describes the following and follower
genResult(followingNotFollower, followerNotFollowing, "index.html")