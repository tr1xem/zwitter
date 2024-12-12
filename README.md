# Zwitter
<centre>[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=zwitter&repository=tr1xem%2Fzwitter&branch=main&run_command=python+main.py&privileged=true&instance_type=free&ports=8080%3Bhttp%3B%2F&hc_protocol%5B8080%5D=http&hc_grace_period%5B8080%5D=5&hc_interval%5B8080%5D=30&hc_restart_limit%5B8080%5D=3&hc_timeout%5B8080%5D=20&hc_path%5B8080%5D=%2Fcheck&hc_method%5B8080%5D=get)<br></centre>
Zwitter is a real time chat app based on a python module [NiceGui](https://nicegui.io/) supporting auto avatar genration and dark and light theme.

## Requirements

- NiceGui
- MiddleWare
- FastApi

Note: Python 3.10+ Recommended

## How to run?

1.)  Set env variables see example env (the last 2 are for compatibility with linux mysql)

2.) ``` pip install -r requirements.txt ```

3.) ``` python main.py ```


## TODO

- [X] Login System
- [x] Sql Integration
- [x] Remote Sql  support
- [X] Online user list
- [X] Account Page
- [ ] Multi Threading
- [X] User List
- [X] Reply System
- [X] Avatar Options
- [ ] Custom Status
- [ ] Custom Indicators
- [ ] Chat rooms

## Screenshots

Main Page:

![image](https://github.com/user-attachments/assets/0ae35e2d-b3cf-4737-8a9e-bba5586d7e13)

Registration Page:

![image](https://github.com/user-attachments/assets/7e109b52-5ab9-4b31-af2b-9e68185c4838)

Account Page:

![image](https://github.com/user-attachments/assets/f22836a3-1037-4e06-aabd-92a4e318433e)

Chat Ui:

![image](https://github.com/user-attachments/assets/d2e30182-a97c-47a6-b362-e6d192145118)

## License

**GNU General Public License v3.0**

Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.




_“Bad programmers worry about the code. Good programmers worry about data structures and their relationships.”
― Linus Torvalds_
