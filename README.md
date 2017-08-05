# iphone-contacts-extract

Extract all iOS contacts into a single vCard 3.0 file.

**Note**: Built and tested for iOS 9, might not work on more recent versions.

## How to use

1. Obtain your iOS Files using [this tool](http://supercrazyawesome.com/)
2. Find `Contacts.sqlite`
3. Run the script: `python extract.py --input Contacts.sqlite --output ~/Desktop/contacts.vcard`

The resulting vCard file can now be imported into OS X Contacts or other systems (e.g. Google Apps).