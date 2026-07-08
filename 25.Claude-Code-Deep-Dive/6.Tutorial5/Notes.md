1. To resume the conversation, you can use `/resume`. Supoose, you ask in the claude terminal as `hi, how are you` and then you kill the terminal and again you open the claude terminal and put the command as `/resume` to see previous conversation.

2. You can see the release notes using `/release-notes`.

3. First we create a simple project. So, first clear the context using `/clear`. Now, write in `paln mode` using `shift+tab`cas:

`I want to create a vite project with ts support and I also want to create express backend that support typescript. I want to use tanstack query for api calls. So, create a basic todo app.` click enter and kill the terminal.

Now, open another vscode terminal and install the context7 mcp server from `https://github.com/upstash/context7` and run the command as `npx --claude ctx7 setup` and then follow instructions like select MCP server and claude and login through browser. Now, in this another terminal, open claude terminal and check using `/mcp` command that mcp server is installed or not.

Now, type `claude --resume`  and ask `Hey can you check latest vite docs using context7 mcp server, check how we install vite project, also check latest docs how we install tanstack query` and execute in plan mode.

When the app build is completing, you can run as:

To run it:
  # terminal 1
  cd 6.Tutorial5/server && npm run dev      # http://localhost:3001

  # terminal 2
  cd 6.Tutorial5/client && npm run dev      # http://localhost:5173

  I haven't opened the browser to verify the UI renders — the backend API is verified, and both projects compile, but you'll want to load
  http://localhost:5173 to confirm add/toggle/delete behave correctly visually.

open http://localhost:5173 in a browser to confirm the UI works. 

4. Using `npx ccusage@latest` in vscode terminal, we can check the claude usage and cost with date.

5. Claude Code Hooks:

First copy the page info from `https://code.claude.com/docs/en/hooks` and then open a new instance of claude code terminal and then paste the page info which you copied then put `\` for new line and then ask `can you explain this hooks concept using docs` and then execute in plan mode.

Using pre-hooks, you can apply the restriction like claude will not see the `.env` file. 

Now, ask `can you create a hook that prints a console log after any task is done or pending or needs for approval. Create it for local files, not global and it should be shell commands file for these hooks that you have created. Also let me know where you have created these hooks and how you can use them. Also test these hooks for me. Also create the logs as well. I am new to this so explain in depth.`

6. Claude Subagents:

Open new claude terminal instance and paste the docs from `https://code.claude.com/docs/en/sub-agents` and ask `can you explain this multi agents concept using docs. Can you create a doc for multiagent so that I can feed into next prompt. Also create a memory file    claude.md in the current folder by using /init command in claude code` and then execute it.

Now, use `/exit` and then use `claude --resume` and select `sullstack-todo-app` chat and give multiagent guide file by dragging the file in claude terminal and ask ` how will you use this multiagent support to do task fast. Do all the things in current folder and execute them to make app faster and improved using multiagent support.`. 

Now, again use `claude --resume` after exit and reload and see agents using `/agents` command.

7. You can create slash commands like `/explain-this-file` using claude and use it in vscode terminal.

