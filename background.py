import random
from assistant import Assistant

def main():
    Navi = Assistant()

    while True:
        num = random.randint(1,10000000000)
        if num == 1000:
            print(num)
            Navi.openai_response(10)


if __name__ == "__main__":
    main()
