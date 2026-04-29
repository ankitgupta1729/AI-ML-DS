### Source: Tech with Tim

1. Before starting see the official documents from `https://code.claude.com/docs/en/quickstart`. 

2. In Desktop version of claude code, there are 3 mode: chat, code and cowork.

3. First you have to install git on your system and so you have to go into claude code chat and ask `can u install git for me`.

4. You can ask claude to `How do I connect my github account to the terminal here?` and follow the steps to connect claude with your github account 
   
5. Now, open Cursor IDE (it is a VSCode fork) and open a new folder `ClaudeCodeTest` and then open the terminal and type `claude`.

Now write the prompt as `Make tic tac toe that I can play on the web`. 

You can run claude in multiple terminals also.

6. For any help, we can use `/help` in claude terminal.

7. In claude, there are various modes like plan mode (creates a detailed plan that claude will follow), ask mode (default mode where we ask something before the claude does something) and code mode (it's just going to code by default. It's not going to ask you for permission). 

In Claude Terminal,

`accepts edits on` --> coding mode
`plan mode on` --> plan mode
`? for shortcuts` --> ask mode

Using `Shift+Tab`, you can toggle with different modes.

8. Using `ESC+ESC` means if you press escape key 2 times then you clear all the text/commands from the claude terminal. If you have to go previous text then you have to press Up Arrow key. Simliarly, if you have to go next text then you have to press Down Arrow key. And you cycle it in this way.

9. If you have to line break or go to new line then you have to press `Alt/Option + Enter/Return`.

10. While asking, you should have to clear what you want and be specific. 

11. You can install `Wisper Flow` so that you don't have to type in claude terminal. You can tell and it will convert into text.

12. After getting the response from planning mode, you can use `Ctrl+O` to expand it. 

13. For larger projects, you can instruct claude to create a git repo after connecting with your account in github and you can see in github also. 

14. When you put `/exit` and starts the claude again then you lost all the previous history because a new session starts. So, you have to use claude.md file and memory. So, to have a persistant memory, you have to use `/init` command first and then `claude.md` will be created automatically and it is having all the information based on your codebase and the analysis.

Now, again when you put `/exit` and ask like `What do you know about this project?` then you will get the information from the claude.md file.  

15. Using `/tasks` command, you can get to know about background task or any other task. 