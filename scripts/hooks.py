import random

topics = [
"money","success","discipline","social media","rich people","mindset"
]

templates = [
"The truth they don't want you to know about {}",
"Nobody tells you this about {}",
"99% of people misunderstand {}",
"This will change how you see {} forever"
]

def generate_hook():
    topic = random.choice(topics)
    template = random.choice(templates)
    return template.format(topic)

if __name__ == "__main__":
    print(generate_hook())
