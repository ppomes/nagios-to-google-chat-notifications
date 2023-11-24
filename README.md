# Nagios to Google Chat Integration

This repository contains Python scripts to enable integration between Nagios notifications and Google Chat.

## Scripts

- `google_chat_host_notification.py`: Sends host notifications to Google Chat.
- `google_chat_service_notification.py`: Sends service notifications to Google Chat.

## Prerequisites

- Python 3
- [Requests](https://docs.python-requests.org/en/latest/) library
- Access to a Google Chat room and knowledge of its webhook URL

## Usage

### Manual run

Execute the scripts manually to test:
```bash
git clone https://github.com/ppomes/nagios-to-google-chat-notifications.git
cd nagios-to-google-chat-notifications
pip install -r requirements.txt
./google_chat_host_notification.py your-host UP 'Host is up' --proxy 'http://your-proxy-url'
./google_chat_service_notification.py PROBLEM your-host 'Your Service' CRITICAL 'Service is in a critical state' --proxy 'http://your-proxy-url'
```
**Note:** The `--proxy` argument is optional and can be used if your environment requires a proxy for internet access

### Nagios Configuration

#### For Host Notifications

```cfg
define command {
    command_name    notify-host-by-google-chat
    command_line    /usr/bin/python3 /path/to/google_chat_host_notification.py '$CONTACTPAGER$' '$HOSTNAME$' '$HOSTSTATE$' '$HOSTOUTPUT$' --proxy 'http://your-proxy-url'
}
```

#### For Service Notification

```cfg
define command {
    command_name    notify-service-by-google-chat
    command_line    /usr/bin/python3 /path/to/google_chat_service_notification.py '$CONTACTPAGER$' '$NOTIFICATIONTYPE$' '$HOSTNAME$' '$SERVICEDESC$' '$SERVICESTATE$' '$SERVICEOUTPUT$' --proxy 'http://your-proxy-url'
}
```

#### Nagios Contact Configuration

```cfg
define contact {
    contact_name                    your-contact
    use                             generic-contact
    alias                           Your Contact
    email                           your-email@example.com
    pager                           your-google-chat-webhook-url
}
```

Replace your-google-chat-webhook-url with your actual Google Chat webhook URL.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

