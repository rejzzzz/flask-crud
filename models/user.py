from datetime import datetime
import re
from werkzeug.security import generate_password_hash
from db import get_db


def validate_user_data(data, is_create=False):
    if not isinstance(data, dict):
        return {'is_valid': False, 'message': 'No data provided'}

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip() if is_create else None

    if not name:
        return {'is_valid': False, 'message': 'Name is required'}
    if not email:
        return {'is_valid': False, 'message': 'Email is required'}
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return {'is_valid': False, 'message': 'Invalid email format'}
    if is_create and not password:
        return {'is_valid': False, 'message': 'Password is required'}
    if is_create and len(password) < 6:
        return {'is_valid': False, 'message': 'Password must be at least 6 characters'}

    return {'is_valid': True, 'message': 'Valid data'}


def hash_password(plain_password):
    return generate_password_hash(plain_password)


def get_next_user_id():

    now = datetime.now()
    date_str = now.strftime("%y%m%d")  # e.g., "240405"
    collection = get_db()

    # Daily counter: resets every day
    counter_doc = collection.database.counters.find_one_and_update(
        {'_id': f"user_id_seq_{date_str}"},
        {'$inc': {'sequence': 1}},
        upsert=True,
        return_document=True
    )

    seq = counter_doc['sequence']

    if seq > 999999:
        raise RuntimeError(f"Daily user limit (999,999) exceeded for {now.strftime('%Y-%m-%d')}")

    return f"U{date_str}{seq:06d}"