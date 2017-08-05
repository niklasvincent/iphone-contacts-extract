# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import string
import sqlite3
import sys
from collections import namedtuple


Contact = namedtuple("Contact", ["full_name", "phone_numbers"])


def printable(s):
    characters = set(string.printable)
    return filter(lambda x: x in characters, s)


def to_vcard(contact):
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:{}".format(contact.full_name)
    ]

    for phone_number in contact.phone_numbers:
        lines.append("TEL;TYPE=HOME,VOICE:{}".format(phone_number))

    lines.append("END:VCARD")

    return "\n".join(lines)


def contacts_to_vcard(contacts):
    vcards = [to_vcard(c) for c in contacts if c.phone_numbers]
    return "\n".join(vcards)


def extract_contacts(db):
    c = db.cursor()

    contacts = []
    contact_rows = c.execute('SELECT Z_PK, ZFULLNAME FROM ZWACONTACT')

    for contact_row in contact_rows.fetchall():
        numbers = c.execute(
            'SELECT ZPHONE FROM ZWAPHONE WHERE ZCONTACT = ?',
            (contact_row[0], )
        ).fetchall()
        numbers = [printable(n[0]) for n in numbers]
        contacts.append(
            Contact(full_name=contact_row[1], phone_numbers=numbers)
        )

    return contacts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=str,
                        help="input SQLite filename")
    parser.add_argument("--output", required=True, type=str,
                        help="output vCARD 3.0 filename")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("No such database file: {}".format(args.input))
        sys.exit(1)

    db = sqlite3.connect(args.input)

    contacts = extract_contacts(db)
    vcards = contacts_to_vcard(contacts)

    with open(args.output, "w") as f:
        f.write(vcards)

    print("Wrote {} contacts to {}".format(len(contacts), args.output))


if __name__ == "__main__":
    main()
