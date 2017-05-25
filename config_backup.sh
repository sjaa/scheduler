# backup config
# below 'exit' is to ensure this isn't run
exit
cp membership/config.py      config/membership_config.py
cp sched_announce/config     config/sched_announce_config.py
cp sched_announce/config.py  config/sched_announce_config.py
cp sched_announce/secrets.py config/sched_announce_secrets.py
cp sched_core/secrets.py     config/sched_core_secrets.py
cp scheduler/secrets.py      config/scheduler_secrets.py
cp scheduler/settings.py     config/scheduler_settings.py
cp sched_core/secrets.py     config/sched_core_secrets.py
cp sched_core/config.py      config/sched_core_config.py

#restore config
# below 'exit' is to ensure this isn't run
exit
cp config/membership_config.py      membership/config.py
cp config/sched_announce_config.py  sched_announce/config
cp config/sched_announce_config.py  sched_announce/config.py
cp config/sched_announce_secrets.py sched_announce/secrets.py
cp config/sched_core_secrets.py     sched_core/secrets.py
cp config/scheduler_secrets.py      scheduler/secrets.py
cp config/scheduler_settings.py     scheduler/settings.py
cp config/sched_core_secrets.py     sched_core/secrets.py
cp config/sched_core_config.py      sched_core/config.py

