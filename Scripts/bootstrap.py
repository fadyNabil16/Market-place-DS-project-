import pip

def install(package:str) -> None:
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

packaes = ['PyQt5']
if __name__ == '__main__':
    for pack in packaes:
        install(pack)