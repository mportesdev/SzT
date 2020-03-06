from funkcni_test import test_zakladni_pruchod_hrou

if __name__ == '__main__':
    wins = 0
    losses = 0

    while wins + losses < 100:
        try:
            test_zakladni_pruchod_hrou()
        except AssertionError:
            losses += 1
        else:
            wins += 1
    print(f'{losses=}')
    print(f'{wins=}')
