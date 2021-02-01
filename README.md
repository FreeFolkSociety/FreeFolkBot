# Free Folk Society Bot

This is the repository of the freefolk society bot
feel free to collaborate with this bot.


## Secrets
all secrets are provided trough a `.env` file example below
```
BOT_TOKEN=Bot_token
VOICE_ROLE_ID=Role_ID
```

## Voice mapping
One of the bot functions is to give acces to the lobby assinged to the same catogory as the voice channel
for this purpose there is a mapping which catogory Has which lobby ID

example of the yaml:
```yaml
Voice_Cat_to_channel:
  0000000000000000: 000000000000000 #Catogory-ID: Channel-ID
```
Where the fist ID is the ID of the catogory and the second of the lobby channel.
When Catogory Id can't find the bot won't add a lobby channel.  
