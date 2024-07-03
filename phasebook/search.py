from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def match_id(user_value, search_value):
    return str(user_value) == str(search_value)

def match_name(user_value, search_value):
    return search_value.lower() in user_value.lower()

def match_age(user_value, search_value):
    if user_value is None:
        return False
    return int(search_value) - 1 <= int(user_value) <= int(search_value) + 1

def match_occupation(user_value, search_value):
    return search_value.lower() in user_value.lower()


def search_users(args):
    if not args:  # If args is empty, return all users
        return USERS

    match_functions = {
        "id": match_id,
        "name": match_name,
        "age": match_age,
        "occupation": match_occupation,
    }

    # Dictionary to hold matched users for each criterion
    matched_users = {key: [] for key in args.keys()}

    for key, value in args.items():
        if key in match_functions:
            match_function = match_functions[key]
            matched_users[key].extend(user for user in USERS if match_function(user.get(key), value))

    # Combine matched users while preserving the order of criteria
    ordered_results = []
    seen_users = set()

    for key in args.keys():
        for user in matched_users[key]:
            user_tuple = tuple(user.items())
            if user_tuple not in seen_users:
                ordered_results.append(user)
                seen_users.add(user_tuple)

    return ordered_results