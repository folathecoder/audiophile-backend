def user_data_schema(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "address": user["address"],
        "phone_number": user["phone_number"],
        "user_role": user["user_role"],
        "email_verified": user["email_verified"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }


def all_user_data_schema(users):
    return [user_data_schema(user) for user in users]
