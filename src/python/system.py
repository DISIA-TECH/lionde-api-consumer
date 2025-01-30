import csv
import json
import os
import urllib

from src.python.api_consumer import APIConsumer
from src.python.init_configurations import ConfigLoader

rename_fields = {
        '26892': {
            "_id": "lead_id",
            "cid": "email",
            "ue1": "first_name",
            "ue2": "last_name",
            "ue3": "phone",
            "ref": "url",
            "uac": "location",
            "fi1": "zip_code",
            "fi2": "age",
            "uip": "user_ip",
            "org": "organization_code",
            "act": "activity_code",
            "pub": "publisher_code",
            "evt": "event_code",
            "gel": "management_code",
            "tid": "transaction_code",
            "tim": "timestamp",
            "fi6": "company",
            "fi5": "events",
        },
        '18484': {
            "_id": "lead_id",
            "fi1": "first_name",
            "fi2": "last_name",
            "fi6": "zip_code",
            "fi7": "phone",
            "cid": "email",
            "uip": "user_ip",
            "ref": "url",
            "org": "organization_code",
            "act": "activity_code",
            "pub": "publisher_code",
            "evt": "event_code",
            "gel": "management_code",
            "tid": "transaction_code",
            "tim": "timestamp",
            "uac": "location",
            "fi3": "age",
            "ue1": "events",
            "ue2": "company",
        }
    }


def downloader(config: ConfigLoader):
    activities = config.getattr('activities_ids').split(',')
    print(activities)
    for activity_id in activities:
        page = 0
        should_continue = True
        while should_continue:
            page += 1
            api = APIConsumer(config.getattr('base_url'))
            data = api.get(config.getattr('endpoint'), params_dict(config, activity_id, page))
            results = transform_data(data,activity_id)
            save_to_csv(results, config.getattr('csv_path'))
            if data['data']['pagination']['last_page'] == page:
                should_continue = False


def params_dict(config: ConfigLoader, activity_id: int, page: int):
    return {
        'activity_id':activity_id,
        'start_date': config.getattr('start_date'),
        'end_date': config.getattr('end_date'),
        'per_page': config.getattr('per_page'),
        'api_token': config.getattr('api_token'),
        'page': page
    }

def transform_data(json_data: dict, activity_id: str):
    transactions = json_data["data"]["transactions"]
    results = []
    for transaction in transactions:
        volatility_json = None
        new_transaction = {}
        for key, value in transaction.items():
            if key in rename_fields[activity_id]:
                decoded_value = urllib.parse.unquote(value) if isinstance(value, str) else value
                if value is not None and value.startswith('{') and value.endswith('}'):
                    try:
                        volatility_json = json.loads(decoded_value)
                    except json.JSONDecodeError:
                        pass
                new_transaction[rename_fields[activity_id][key]] = decoded_value
        if volatility_json is not None:
            for key, value in new_transaction.items():
                if key in volatility_json:
                    new_transaction[key] = volatility_json[key]
        results.append(dict(sorted(new_transaction.items())))
    return results


def save_to_csv(transactions: list, filename :str):
    if not transactions:
        print("No data to save.")
        return
    file_exists = os.path.exists(filename)
    headers = transactions[0].keys()
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerows(transactions)
    print(f"Data saved to {filename}")


