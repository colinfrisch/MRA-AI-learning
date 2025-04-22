import requests

ACCESS_TOKEN = 'EAAJ7vGqYZB5ABO42p4mZCJTg3rL14QSVJuoyIkZAqd7aG0gNJyA15S4Avv8sy3gpu0PSZBY42TWh74gFfeHXLQZAt0ZACTlhZAEJLd7svZBIUaPws4vUwH0m9ZBrcsfmicDwSI6gu7ZBYPjg26dTZAj7mi1gfL2JxVCIzAxTPpHNxlboeZCc9BNzZBKZCc3Y7IuAxvaQLfvgo85oRaXaRfZBGcchImoQIJd780ZD'  # Replace this with your actual token
PHONE_NUMBER_ID = '661285417059859'
RECIPIENT_PHONE_NUMBER = '33770210937'  # No + or spaces

url = f'https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}


payload = {
    'messaging_product': 'whatsapp',
    'to': RECIPIENT_PHONE_NUMBER,
    'type': 'text',
    'text': {
        'body': 'coucou www.google.com'
    }
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print('✅ Message sent successfully.')
else:
    print(f'❌ Failed to send message. Status code: {response.status_code}')
    print(f'Response: {response.text}')