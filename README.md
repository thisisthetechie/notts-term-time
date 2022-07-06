# Notts Term Time

This is just a little scraper to read the Nottingham Term Times from the Nottingham City website and create Calendar Events for the term starts, ends and half-terms.

## Choose your poison

There are 3 different scrapers, each with the same basic functionality - but they each have a key use:

### scraper-csv

This scraper will output a CSV File containing the term dates

### scraper-ics

This scraper will output an ICS Calendar file containing the term dates

### scraper-365

This is the main scraper and will, once authenticated with your Office Account, post calendar events on your behalf. It _will_ check to see if the entry already exists - there's nothing worse than duplicate entries.

## Using scraper-365

The scraper is easy to use, but it does require authentication (as mentioned). This means it also requires some information from your Office Account. I have used the O365 library to achieve this. It's not ideal, but it works - and you will not need to run the scraper very often as it picks up a good 3 years worth of term dates at a time.

## Credentials

Credentials (and all other personal data) is stored in a file called `credentials.json` with the following content:

```js
{
    "user_email"      : "you@yourdomain.com",
    "tenant_id"       : "[Your Microsoft Tenant ID]",
    "application_key" : "[An Application Key]",
    "secret_key"      : "[A Secret Key associated with the Application Key]",
    "calendar_name"   : "My Calendar Name"
}
```

## Running the code

To start, you will need to authenticate. This is an OAuth authentication that will last around 60-90 mins:

```sh
python authenticate.py
```

You will be prompted to click a link (or copy it to your browser), this will take you to a Microsoft Login for you to authenticate. Once completed, you will be left with a blank page. Copy the contents of the Address Bar and paste it into your terminal window.

If all is successful, you should receive a message like this:

```
Authentication Flow Completed. Oauth Access Token Stored. You can now use the API.
```

You can now move on to the next part, running the main script:

```sh
python scraper-365.py
```

There is an error message about Pytz being deprecated, ignore that. You are looking for the outputs from the script itself telling you it's found an entry, and if it does not already exist in your calendar it will create the entry for you.