import json

from parsers.weblancer.service import WeblancerService


if __name__ == '__main__':
    service = WeblancerService()
    data = service.exec()
    
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    