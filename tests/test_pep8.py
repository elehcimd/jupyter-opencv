from os.path import dirname, abspath
from pycodestyle import StyleGuide


def test_pep8():
    report = StyleGuide(ignore=['E501', 'E402']).check_files([dirname(abspath(__file__)) + '/../'])
    report.print_statistics()

    if report.messages:
        raise Exception("pep8")
