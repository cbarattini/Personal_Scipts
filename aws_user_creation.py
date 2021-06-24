import boto3

iam = boto3.resource('iam')
client = boto3.client('iam')
domain = "@sureco.com"

username = input("Please enter a new Username: ")
passw = input("Please Enter a password: ")

# Create IAM User account
response = iam.create_user(
    UserName=username,
    Tags=[
        {
            'Key': 'Email',
            'Value': username + domain,
        },
        {
            'Key': 'Department',
            'Value': "IT",
        }
    ]
)

# Set a profile for password assignment
profile = client.create_login_profile(
    UserName=username,
    Password=passw,
    PasswordResetRequired=True
)

# Option to add programmatic access
accessKeys = input("Do you require programmatic access?(y/n): ")
if accessKeys == "y":
    iam_keys = client.create_access_key(UserName=username)
    print("Programmatic Access has been enabled")
    print(iam_keys)
elif accessKeys == "n":
    print("Console access only has been granted")

# Option to list groups and select
responseGroups = client.list_groups()
groups = responseGroups['Groups']
index = 1

for group in groups:
    print(f'{index}: {group["GroupName"]}')
    index += 1

# creating an empty list
options = []

# number of elemetns as input
n = int(input("Enter number of groups : "))

# iterating till the range
for i in range(0, n):
    ele = int(input())
    options.append(ele) # adding the element

print(options)
for option in options:
    arn = groups[option - 1]["Arn"]
    group = arn.split("/")
    print(f'You selected group {option}: {arn}')
    responseAddGroup = client.add_user_to_group(UserName=username, GroupName=group[1])
    print(responseAddGroup)