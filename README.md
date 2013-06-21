# myfitnesspal.py #

This is *myfitnesspal.py*. It's a Python script written by me - Brett Hutley <brett@hutley.net> in order to scrape my daily food data from the website MyFitnessPal.com.

In order to use it, first make your data publicly accessible (under Settings/Diary Settings/Diary Sharing on the website). The copy the `myfitnesspal.cfg.sample` file across to your home directory and call it `.myfitnesspal.cfg`. Edit it to suit your needs.

You will need to create the SQLite3 database. You can do this by running the following from the command line:

    sqlite3 myfitnesspal.db
    
    sqlite> .read myfitnesspal.sql
    sqlite> .exit

The script will load the `food` table in the database with the entries for either the date specified on the command line (in YYYY-MM-DD form), or the current date if no date is specified.
