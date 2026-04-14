1. Claude Code is an Agentic Coding tool which is created by Anthropic. Other coding tools include Co-Pilot, Cursor, Winsurf etc. 

2. First install the claude code on your system using `curl -fsSL https://claude.ai/install.sh | bash`. Now, Go to `Tutorial1` and type `claude` in vscode terminal. Before that take the subscription plan from `https://claude.com/pricing`

3. Now, start with chatting as `Can you provide me a summary of what this project is?`  

4. First type `/terminal-setup` command for key bindings for new line, so when you are chatting and you have to go to new line then press `shift+enter` for new line in claude terminal.

5. type `can you switch to a new branch called claude-edits`, so claude will switch to a new branch because claude has knowledge about the git branches. It can run bash commands also. It can do stage and commit as well and resolve conflicts as well in git after merging. You can check changed branches in VS Code.

6. Put some github code in current local folder. Now, it's a good idea to run `\init` command initially for `claude.md`, so calude code scans entire codebase of current folder and summarize and store into claude.md file. 

7. You can change the project structure in claude.md, for example, you can add a folder as `hooks` and then claude will understand it and then for your project, you can type, `can you create a hook to store user's theme preference in, when they toogle the theme on site? Store the value in local storage for next time. Don't use the hook anywhere yet.`

8. You can add memory for claude.md directly from the chat session. For example, type `# When making new page components, always add a link to that page in the header`. `#` is to memorize or you can use `/memory` command. Select `Project Memory` and check the claude.md file now. 

9. You can type `Can you add a new /about page with only an h2 title and a single line of lloren as content.`

10. To select a file in claude code terminal, use `@Notes.md` and then press `Tab` key. So, it will provide the context. For example, type `Convert @Notes.md to pdf` and press enter. You can add multiple files using @ symbol in the prompt. If you select few lines of a file then it will be displayed below the claude terminal.

We can also add images as context in the claude code terminal using drag and drop of images in the claude code terminal. 

11. You can use `/exit` command to exit the chat session completely. `/clear` command is used to clear the entire session context and chat history. 

`/compact` command is used to compacts the chat and context into a small summary.

If you press ESC twice then it rewind to a previous point in the session.

12. If you have used `/exit` command then you can put `/resume` again after opening the claude terminal to see previous chat sessions and context and resume from those sessions/contexts.

13. Reference Material: https://code.claude.com/docs/en/overview

14. 