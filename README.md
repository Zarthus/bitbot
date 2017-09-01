# BitBot
Python3 event-driven modular IRC bot!

## Dependencies
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [twitter](https://pypi.python.org/pypi/twitter)
* [scrypt](https://pypi.python.org/pypi/scrypt)
* [suds](https://pypi.python.org/pypi/suds-jurko)

## Configurating
To get BitBot off the ground, there's some API-keys and the like in bot.json.example. move it to bot.json, fill in the API keys you want (and remove the ones you don't want - this will automatically disable the modules that rely on them.)

## Eagle
BitBot's National Rail module can optionally include output from Network Rail's SCHEDULE via [Eagle](https://github.com/EvelynSubarrow/Eagle)

## Running
Just run `./start.py`

On first boot, he'll ask for a first server to connect to then exit. do `./start.py` again and he'll connect to that server and join #bitbot (to get him to join other channels, simply invite him to them.)

## Data storage
The main data storage for Bitbot is done in his sqlite3 database, bot.db.
