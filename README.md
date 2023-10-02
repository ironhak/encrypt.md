# encrypt.md
A minimal python utility to crypt all your markdown notes, with some extra utilities. 

### What does this do? 
Basically this program locate a folder choose by the user (for now you have to manualy edit `main.py`) and it will encrypt all .md files inside that folder, but with some extras: 
- YAML does not get encrypted
- the script is designed for .md files with a "modified: " property in the YAML, like this:
  ```
  ---
  created: 2023-02-07T23:20:32+01:00
  modified: 2023-02-07T23:20:32+01:00
  ---
  ```
- Every time an ecnryption/decryption happen, the script will restore the modification date of the file (as it appear on your OS file explorer) in order to maintain the previous one, basically the file will not result as modified even if it was indeed modifed. Thank's to this you can freely ecnrypt/decrypt your files keeping useful metadata.

### About this script
I'm not a professional coder, this was achieved thank's to massive help of GPT. I'm sharing because I needed this to crypt my daily notes entries, if I had that necessity I know someone will too, so if someone more experienced than me want to contribute to this project it would be amazing! Basically I'm just sharing an idea, the implementation works for now, but it can be surely better and with more features. 

#### A little more
As you may have noticed I shared directly a virtual environment, so that everyone (if there'll be any of you interested) can be on the same page and working with same version. Here's how the thing works: 
1. `cd`into this repo
2. `source bin/activate` to start the virtual environment
3. Go do `main.py`and on the file path locate a folder that contains `.md` files. I reccomend you to just make a copy of some daily notes and place it into the main directory, so that you can do your tests.
4. Run `python main.py`
5. You'll be asked for the creation of a password, a custom salt will be generated. Your password and your salt are stored on a hidden file called `.status`located on the main directory.
6. From now just follow the promots.

Hope this can help someone. Thank's for stopping by. 
