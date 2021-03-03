# Box Critters Name Checker

Want to check if a [Box Critters](https://boxcritters.com/) nickname is available but don't want to register an account to find out? If so, the Box Critters Name Checker is for you.

## Usage

*Requires Python 3.6 or newer*

1. Download the [latest Box Critters Name Checker](https://github.com/TimTree/box-critters-name-checker/releases/latest).
2. In the included `test.txt` file, type the nicknames you want to test sorted by line, like so:
```
Nickname1
Nickname2
Nickname3
```
3. In your Terminal, set your directory to the Box Critters Name Checker folder and execute
`python critterNames.py`.

Any untaken nicknames will appear at the end of your Terminal output after the script finishes.

## How it works

When you [register an account on the Box Critters website](https://boxcritters.com/join/index.html), you send a `RegisterPlayFabUser` POST request to the [PlayFab API](https://docs.microsoft.com/en-us/rest/api/playfab/client/authentication/registerplayfabuser?view=playfab-rest) with the following request body:

```
{
    TitleId: '5417', // Unique identifier for the game Box Critters
    DisplayName: nickname,
    Email: email,
    Password: password,
    RequireBothUsernameAndEmail: false
}
```

Before sending this POST request, the Box Critters website uses client-side JavaScript to ensure all relevant details (nickname, email, password) exist and are valid, otherwise registration prematurely errors out. This is a problem because entering a valid email risks actually registering an account when the POST request runs.

Thankfully, we can use Python to directly send the POST request, intentionally without the `Email` key. Not only does this ensure we never register an account, the API response returns one of two errors:

`NameNotAvailable` - The nickname is taken.

`InvalidParams` - The error we get since we excluded `Email`. It implies that the nickname is not taken.

## Exceptions

Nicknames with inappropriate words may be labeled as untaken, though you shouldn't try to register these names for obvious reasons.

## License

The Box Critters Name Checker is licensed under the MIT License.

<sup><sub>"Box Critters" is a trademark of Hyper Hippo Entertainment Ltd, which was not involved in the production of, and does not endorse, this product.</sub></sup>