# CampusFlow - IT Helpdesk Ticketing System
Team: Felix Gangese Terkula (Engineer A) + Oyilo (Engineer B)

Engineer A (Felix): ticket creation, validation, priority engine, persistence
- campusflow/tickets.py, storage.py
- 19 tests

How to run:
python3 -m unittest discover -s tests -v

Priority (IN ORDER):
1. high AND >=10 -> critical
2. high OR >=10 -> high
3. medium OR >=3 -> medium
4. rest -> low
