from collections import Counter
import sys

from funkcni_test import test_zakladni_pruchod_hrou

if __name__ == '__main__':
    passed_vs_failed = Counter()
    fail_types = Counter()

    try:
        number_of_tests = int(sys.argv[1])
    except (ValueError, IndexError):
        number_of_tests = 100

    for __ in range(number_of_tests):
        try:
            test_zakladni_pruchod_hrou()
        except AssertionError as err:
            passed_vs_failed.update(failed=1)
            fail_types.update({str(err): 1})
        else:
            passed_vs_failed.update(passed=1)
    print(f'{passed_vs_failed}')
    for message, n in sorted(fail_types.items(), key=lambda e: e[1],
                             reverse=True):
        print(message.ljust(40), f'{n:3}', n * '#')
