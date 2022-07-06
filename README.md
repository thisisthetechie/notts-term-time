# Notts Term Time

This is just a little scraper to read the Nottingham Term Times from the Nottingham City website and create Calendar Events for the term starts, ends and half-terms.

## Credentials

This requires credentials to run - it needs a file called `credentials.json` creating with the following content:

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