import time
import container


def main():
    print("IOL Trader")
    last_check = 0
    times = 0
    while True:
        if time.time() - last_check > 600:
            data = container.Apis.iol_api().get_portfolio("argentina")
            print(data)
            times = times + 1
            last_check = time.time()
        if times == 3:
            exit(0)
        time.sleep(30)
        print("Checking data")


if __name__ == '__main__':
    main()
