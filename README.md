# Before you Start
 A few things to change before Deploying
 1. file path, `msg_list.txt` and `scan.jpg` 's location
    Idealy the `scan.jpg` can be accessed through a web server
    or you can just use rsync/ftp to retrive it from server.
 2. `running_on_server` variable

# Constraints
 This script is tested only on
	Ubuntu 18.04.3 LTS 64bit
 With
	Python 3.6.8
 And the service is located either in **China** or **America**
 due to the lack of timezone compatibility cus I'm too lazy

# TODOs
 0.
  **Modularize & Clean up** the Codes
 1.
  Add `quiet` option, supresses stdout/stderr, and 
  redirect them into a logfile
 2.
  Add Options
   `-L  --msg_list <path>`
   `-Q  --save_qrcode_to <path>`
   `-D  --daemon`
   ... and many more
 3.
  Add auto timezone compatibility, so that the script
  can be deployed anywhere
 4.
  Create a Cron-like schedule parser which looks like
  `* * * 1 2 3 to_user msg`
 5.
  Send Image and File
