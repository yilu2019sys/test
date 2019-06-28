import json


def save_json(file_name: str, result_ab: dict):
        with open(file_name, "w") as fp:
                json.dump(result_ab, fp, ensure_ascii=True, indent=2)


if __name__ == "__main__":
        print ('fin')
