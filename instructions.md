# goodhare
What is goodhare? An python app that helps you migrate out of Spotify by listing your liked songs and playlists so you can later download/acquire them from other sources.

## Structure
1. tokens, credentials and secrets saved on .env file
2. Flask insterface
3. app divided in scripts for authentication, data gathering and data outputting (so these can be expanded later)
4. Basic procedure: user authenticates on spotify, token is gathered, list the playlists (including liked songs), user chooses which lists to export, all songs in the selected playlists (name, author, album, year) is saved in a csv file