#!/usr/bin/env python3

import argparse
import requests
import json

def get_emoji_for_state(state):
    # Returns the emoji corresponding to the host state
    return '❗' if state == 'DOWN' else '✅' if state == 'UP' else '❓'  # Red emoji for DOWN, yellow for UP, and default for others

def format_google_chat_message(host_name, host_state, host_output):
    # Gets the emoji for the host state
    emoji = get_emoji_for_state(host_state)

    # Formats the message with Nagios variables
    formatted_message = f"{emoji} <a href='http://{host_name}'>{host_name}</a> is <b>{host_state}</b>\n<I>{host_output}"

    return formatted_message

def send_google_chat_message(webhook_url, host_name, host_state, host_output, proxy=None):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    # Formats the message
    message_text = format_google_chat_message(host_name, host_state, host_output)

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
    parser = argparse.ArgumentParser(description='Send a message to Google Chat for a host.')
    parser.add_argument('webhook_url', help='URL of the Google Chat webhook')
    parser.add_argument('host_name', help='Host name')
    parser.add_argument('host_state', help='Host state')
    parser.add_argument('host_output', help='Host output')
    parser.add_argument('--proxy', help='URL of the proxy (optional)')

    args = parser.parse_args()

    send_google_chat_message(args.webhook_url, args.host_name, args.host_state, args.host_output, args.proxy)
