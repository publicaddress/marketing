#!/bin/bash
cd assets
test -f message_logs.tsv && rm -rf message_logs.tsv
touch message_logs.tsv
echo "Importing new messages"

twilio api:core:messages:list --no-limit --properties="dateUpdated,from,body" \
| while read -r row ; do
  echo "$row" >> message_logs.tsv
done
printf "\n"
