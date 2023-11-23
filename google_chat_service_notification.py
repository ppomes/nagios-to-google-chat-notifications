#!/usr/bin/env python3

import argparse
import requests
import json

def get_emoji_for_state(state):
    # Returns the emoji corresponding to the specified state
    if state == 'OK':
        return '✅'  # Green check emoji for OK
    elif state == 'WARNING':
        return '⚠️'  # Yellow emoji for WARNING
    elif state == 'CRITICAL':
        return '❗'  # Red emoji for CRITICAL
    else:
        return '❓'  # Default information emoji for other states

def format_google_chat_message(notification_type, host_name, service_desc, service_state, service_output):
    # Gets the emoji corresponding to the state
    emoji = get_emoji_for_state(service_state)

    # Formats the message with Nagios variables
    formatted_message = f"{emoji} <b>{notification_type}</b> <U>{service_desc}</U> on <a href='http://{host_name}'>{host_name}</a> is <b>{service_state}</b>\n<I>{service_output}</I>"

    return formatted_message

def send_google_chat_message(webhook_url, notification_type, host_name, service_desc, service_state, service_output, proxy=None):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    # Formats the message
    message_text = format_google_chat_message(notification_type, host_name, service_desc, service_state, service_output)

    message = {'text': message_text}
    payload = {'cards': [{'sections': [{'widgets': [{'textParagraph': {'text': message_text}}]}]}]}

    # Configures the proxy if provided
    proxies = {'http': proxy, 'https': proxy} if proxy else {}

    try:
        response = requests.post(
            webhook_url,
            headers=headers,
            data=json.dumps(payload),
            proxies=proxies,  # Use the proxy
        )

        response.raise_for_status()  # Raise an exception for HTTP error codes

        print("Message sent successfully to Google Chat.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Google Chat: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a message to Google Chat.')
    parser.add_argument('webhook_url', help='URL of the Google Chat webhook')
    parser.add_argument('notification_type', help='Type of the notification (PROBLEM, RECOVERY, WARNING, etc.)')
    parser.add_argument('host_name', help='Host name')
    parser.add_argument('service_desc', help='Service description')
    parser.add_argument('service_state', help='Service state')
    parser.add_argument('service_output', help='Service output')
    parser.add_argument('--proxy', help='URL of the proxy (optional)')

    args = parser.parse_args()

    send_google_chat_message(args.webhook_url, args.notification_type, args.host_name, args.service_desc, args.service_state, args.service_output, args.proxy)
