This will take a few steps and a computer. First, you will need to install Python. There are many tutorials for this.


Once Python is installed and you’re in a code editor, type these commands in terminal:

* Pip install beautifulsoup4
* pip install requests



Go to your TikTok profile and hit “Following”.

On the following tab, scroll down until you reach the limit of users. You may have to scroll up and down to get TikTok to load more users.

Go to your browser Console. This is commonly done by any of the following:

* Right click > inspect element
* Right click > view source
* F12


Now you should have a bunch of HTML code on the screen. If you want to verify that it worked, you can search in the inspector for the name of an account you follow. It should appear in a block of code labeled by <li> account name </li>


Copy paste all of that HTML into a file called “following.html”. Use Notepad or your favorite text editor to create this. 


Once this is done, you can run extract_following.py.


Depending on the speed of your computer and the number of accounts, this might be instant or take over 10 minutes. Be patient. You will know it’s done when you have a file called following_tables.html in the same folder. 


You can now open following_Tables.html using your web browser to get a list of the followers. 