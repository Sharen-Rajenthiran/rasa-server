# Rasa Server

A Rasa Pro chatbot server for handling course registration inquiries for UTM students.

## Description

This Rasa chatbot assists students with:
- Course registration information
- Course availability and prerequisites
- Timetable information for MECS0033 and MECS1033
- Email notifications for course registration confirmation

## Prerequisites

- Python 3.8 or higher
- Rasa Pro license key (for Rasa Pro 3.15.3)
- Gmail account with App Password (for email notifications)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Rename `.env.example` to `.env`
   - Update the following variables in `.env`:
     ```
     RASA_LICENSE=your-rasa-license-code
     ```
   - Request your RASA Licence key from [Rasa Developer Edition](https://rasa.com/rasa-pro-developer-edition-license-key-request)

3. **Update Email Configuration (Sender):**
   - Navigate to `\rasa-server\actions\actions.py`
   - Update the lines from 97 - 98 in `actions.py`:
     ```
     sender_email = "your-gmail-address"
     password = "your_app_password"
     ```
   - Note: The `Password` is not your Login Password, it is APP Password from your Google Account. See below links:
      - [Google Support: Create & use app passwords](https://support.google.com/accounts/answer/185833?hl=en)
      - [App passwords](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4MWoBbK0B8oBiyokd0-ZQhNc5UseMYjKq9BXW7g2WOSkeMAnWkskhryOzV2MIqDsSUTxosxv44pWPO4CcgnR7HFTycpEre9jZm3Y0KXdzxzeBIYSt8)

4. **Train the model:**
   ```bash
   rasa train
   ```

## Running the Server

### Start Rasa Server
```bash
rasa run --enable-api --cors "*" --debug
```

The server will start on `http://localhost:5005`

### Start Actions Server
In a separate terminal, run:
```bash
rasa run actions
```

The actions server will start on `http://localhost:5055`

## Project Structure

```
rasa-server/
├── actions/               # Custom actions
│   └── actions.py        # Course inquiry and email notification actions
├── data/                 # Training data
│   ├── flows.yml        # Conversation flows
│   └── patterns.yml     # NLU patterns
├── models/              # Trained models
├── config.yml           # Rasa configuration
├── domain.yml           # Domain configuration (slots, responses, actions)
├── endpoints.yml        # External endpoints configuration
├── credentials.yml      # Channel credentials
├── courses.json         # Course information database
└── requirements.txt     # Python dependencies
```

## Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings → Security
   - Under "Signing in to Google", select "App Passwords"
   - Generate a new app password for "Mail"
3. Add credentials to `.env` file

### Course Data

Course information is stored in `courses.json`. You can modify this file to add or update course details.

## Available Flows

- **course_registration_flow**: Handles complete course registration process
- **course_information_flow**: Provides course information and selection
- **email_notification_flow**: Sends email notifications to students

## Troubleshooting

### Common Issues

**Issue: "Action server not reachable"**
- Ensure the actions server is running on port 5055
- Check `endpoints.yml` configuration

**Issue: "Email not sending"**
- Verify Gmail App Password is correct in `.env`
- Check internet connection
- Ensure sender email has 2FA enabled

**Issue: "Model not loading"**
- Run `rasa train` to create a new model
- Check for errors in training data files

**Issue: "CORS errors"**
- Ensure Rasa server is started with `--cors "*"` flag
- Check client configuration matches server port

## Development

### Testing the Bot

Use Rasa's interactive shell:
```bash
rasa shell --debug
```

### Viewing Logs

Run with debug mode enabled:
```bash
rasa run --enable-api --cors "*" --debug
```

## License

This project uses Rasa Pro 3.15.3 which requires a valid license.