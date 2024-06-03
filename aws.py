import boto3
import tkinter as tk
from tkinter import messagebox, ttk
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json

# Load AWS accounts from JSON file
def load_aws_accounts():
    with open('aws_accounts.json', 'r') as file:
        return json.load(file)['accounts']

# Connect to EC2
def connect_to_ec2(access_key, secret_key, region):
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        return ec2
    except (NoCredentialsError, PartialCredentialsError) as e:
        messagebox.showerror("Error", "Invalid AWS Credentials")
        return None

def refresh_instances():
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    response = ec2.describe_instances()
    for widget in instance_frame.winfo_children():
        widget.destroy()
    
    row = 1  # Start from row 1 to leave space for headers
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            ip_address = instance.get('PublicIpAddress', 'N/A')
            launch_time = instance['LaunchTime']
            name = 'N/A'
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']

            tk.Label(instance_frame, text=name).grid(row=row, column=0, padx=5, pady=2, sticky='w')
            tk.Label(instance_frame, text=instance_id).grid(row=row, column=1, padx=5, pady=2, sticky='w')
            tk.Label(instance_frame, text=state).grid(row=row, column=2, padx=5, pady=2, sticky='w')
            tk.Label(instance_frame, text=ip_address).grid(row=row, column=3, padx=5, pady=2, sticky='w')
            tk.Label(instance_frame, text=launch_time).grid(row=row, column=4, padx=5, pady=2, sticky='w')
            
            tk.Button(instance_frame, text="Start", command=lambda iid=instance_id: start_instance(iid)).grid(row=row, column=5, padx=5, pady=2)
            tk.Button(instance_frame, text="Stop", command=lambda iid=instance_id: stop_instance(iid)).grid(row=row, column=6, padx=5, pady=2)
            tk.Button(instance_frame, text="Reboot", command=lambda iid=instance_id: reboot_instance(iid)).grid(row=row, column=7, padx=5, pady=2)
            tk.Button(instance_frame, text="Copy IP", command=lambda ip=ip_address: copy_ip(ip)).grid(row=row, column=8, padx=5, pady=2)
            
            row += 1

def start_instance(instance_id):
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    ec2.start_instances(InstanceIds=[instance_id])
    refresh_instances()

def stop_instance(instance_id):
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    ec2.stop_instances(InstanceIds=[instance_id])
    refresh_instances()

def reboot_instance(instance_id):
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    ec2.reboot_instances(InstanceIds=[instance_id])
    refresh_instances()

def copy_ip(ip_address):
    root.clipboard_clear()
    root.clipboard_append(ip_address)
    root.update()  # Now it stays on the clipboard after the window is closed

def start_all_instances():
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    instances = [item.cget("text") for item in instance_frame.grid_slaves(column=1) if item.winfo_class() == 'Label']
    ec2.start_instances(InstanceIds=instances)
    refresh_instances()

def stop_all_instances():
    selected_account_name = selected_account.get()
    account = next(acc for acc in aws_accounts if acc['name'] == selected_account_name)
    
    ec2 = connect_to_ec2(
        account['access_key'],
        account['secret_key'],
        account['region']
    )
    if ec2 is None:
        return
    instances = [item.cget("text") for item in instance_frame.grid_slaves(column=1) if item.winfo_class() == 'Label']
    ec2.stop_instances(InstanceIds=instances)
    refresh_instances()

def refresh_all_instances():
    refresh_instances()

# Load AWS accounts
aws_accounts = load_aws_accounts()

# Tkinter GUI
root = tk.Tk()
root.title("AWS EC2 Manager")

# AWS Account Selection
tk.Label(root, text="Select AWS Account:").grid(row=0, column=0, padx=10, pady=10)
selected_account = tk.StringVar()
account_dropdown = ttk.Combobox(root, textvariable=selected_account)
account_dropdown['values'] = [account['name'] for account in aws_accounts]
account_dropdown.grid(row=0, column=1, padx=10, pady=10)
account_dropdown.current(0)

# Create a Frame for the scrollable area
scroll_frame = tk.Frame(root)
scroll_frame.grid(row=1, column=0, columnspan=9, padx=10, pady=10, sticky='nsew')

# Canvas and Frame for instances and buttons
canvas = tk.Canvas(scroll_frame, width=700, height=500)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

instance_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=instance_frame, anchor='nw')

instance_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Add headers
headers = ['Name', 'Instance ID', 'State', 'IP Address', 'Launch Time', 'Start', 'Stop', 'Reboot', 'Copy IP']
for col_num, header in enumerate(headers):
    tk.Label(instance_frame, text=header, font=('Arial', 13, 'bold')).grid(row=0, column=col_num, padx=5, pady=5, sticky='w')

# Buttons
refresh_button = tk.Button(root, text="Refresh", command=refresh_instances)
refresh_button.grid(row=2, column=0, padx=10, pady=10)

# Global action buttons
start_all_button = tk.Button(root, text="Start All", command=start_all_instances)
start_all_button.grid(row=3, column=1, padx=10, pady=10)

stop_all_button = tk.Button(root, text="Stop All", command=stop_all_instances)
stop_all_button.grid(row=3, column=2, padx=10, pady=10)

refresh_all_button = tk.Button(root, text="Refresh All", command=refresh_all_instances)
refresh_all_button.grid(row=3, column=3, padx=10, pady=10)

# Make the main window resizable
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Main loop
root.mainloop()
