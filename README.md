# Last.fm analysis

## Project Structure

```
dumps/          data of processed last.fm profiles
maps/           saved pictures of generated maps
shapes/         shapefiles for map drawing
src/            source code
tests/          unit tests
```

## Requirements

- Python 3.6 interpreter, pip 9.* and higher
- Other Python modules are listed in requirements.txt. 
- Basemap is not presented at PyPi so you need to download and install it manually.
Instructions can be found at https://matplotlib.org/basemap/users/installing.html

## Makefile

- `clear_results` removes `dumps/` and `maps/` directories with cached data
- `clear_cache` deletes Python's cache
- `sample` runs example with default parameters
- `install_reqs` installs Python modules listed in requirements.txt
- `start_bot` starts Telegram Bot in updating mode
- `build_image` build docker image in accordance to Dockerfile

## Installation

I've provided multiple solutions for installation:

- With `docker build` and further docker container operations.
- With `git clone`, navigating to cloned repository and installing requirements `make install_reqs`.

## Usage
`analyze -u <username> -l <limit>`

Where `<username>` is Last.fm username and strictly required 
and `<limit>` is amount of top artists to be extracted from library.
`<limit>` can be omitted, default value is 20 artists

## secrets.json

By default script tries to parse tokens from file named as `secrets.json`, you should create in on your own from `secrets.json.scrap`.
You can ask me via mail for API keys or use own ones.

## License

This software is distributed under GNU General Public License v3.0.
You are completely free to use, share and modify this code. 
And you are welcome, I'd be glad if someone uses code written by me :^)
