# Twitch Assistant

Hi this is my Virtual Assistant. I use it while I'm streaming to give some random stuff and entertaint my viewers.

It uses [ChatGPT](https://openai.com/blog/chatgpt), [Bing](https://bing.com/chat) and [NinjaAPI](https://api-ninjas.com/api) in order to generate diferent responses.

## Requirements

You will need you own api keys from [ChatGPT](https://openai.com/blog/chatgpt), [Bing](https://bing.com/chat) and [NinjaAPI](https://api-ninjas.com/api), if you want to use it.

Then create a ".env" file and add the keys there with the following names:

```bash
echo OPENAI_KEY="YOUR OPEN AI KEY" >> .env
echo NINJA_KEY="YOUR NINJA KEY" >> .env
```

Since the Bing API is not official, you better follow their instructions: [EdgeGPT](https://github.com/acheong08/EdgeGPT)

## Usage

If you want to use my assistant just share that I'm the creator of the code.

At the top of the main file are the key words in order to make the program answer:
```python
CHAT_PHRASE = "hey"
BING_PHRASE = "escúchame"
BUCKET_PHRASE = "deberíamos"
FACTS_PHRASE = "dime"
QUOTES_PHRASE = "cita"
JOKES_PHRASE = "chiste"
```

In addition, there is also a command to change between the two personalities that, at the moment, this project has, but you will have to look for it in the code since I might just play with those words a lot.

To run the program, just open your terminal and run main with:
```bash
python3 main.py
```

Then press "}" to start give the key work to your assistant

## Contributing

If you thing you can help me making the code better and adding new functionalities that may or not may be related with better twitch content, I will be grateful to receive your help. But please open a issue first to discuss what you would like to add or change.
