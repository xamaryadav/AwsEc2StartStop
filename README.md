# AWS EC2 Manager

AWS EC2 Manager is a Python-based GUI tool for managing AWS EC2 instances. With a user-friendly interface, it allows users to efficiently manage their EC2 instances by providing functionalities to start, stop, reboot instances, and copy their IP addresses. The tool supports multiple AWS accounts, making it ideal for users managing resources across different environments or clients.

## Features

- **List EC2 Instances:** Display details such as Name, Instance ID, State, IP Address, and Launch Time.
- **Manage Instances:** Start, Stop, and Reboot individual instances with easy-to-use buttons.
- **Copy IP Address:** Quickly copy the IP address of an instance to the clipboard.
- **Bulk Actions:** Start, Stop, and Refresh all instances with a single click.
- **Multiple AWS Accounts:** Seamlessly switch between different AWS accounts.

## Requirements

- Python 3.6+
- Boto3
- Tkinter

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/aws-ec2-manager.git
    cd aws-ec2-manager
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create the AWS accounts configuration file:**
    Create a file named `aws_accounts.json` in the root directory with the following structure:
    ```json
    {
        "accounts": [
            {
                "name": "Account 1",
                "access_key": "YOUR_ACCESS_KEY",
                "secret_key": "YOUR_SECRET_KEY",
                "region": "YOUR_REGION"
            },
            {
                "name": "Account 2",
                "access_key": "YOUR_ACCESS_KEY",
                "secret_key": "YOUR_SECRET_KEY",
                "region": "YOUR_REGION"
            }
        ]
    }
    ```

## Usage

1. **Run the application:**
    ```sh
    python aws.py
    ```

2. **Select an AWS account from the dropdown menu.**
3. **Click "Refresh" to load the list of EC2 instances.**
4. **Use the provided buttons to Start, Stop, Reboot, or Copy IP of individual instances.**
5. **Use the "Start All", "Stop All", and "Refresh All" buttons to perform actions on all instances.**

## Screenshots

![AWS EC2 Manager Screenshot]

## Contributing

Contributions are welcome! Please create an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE] file for details.

