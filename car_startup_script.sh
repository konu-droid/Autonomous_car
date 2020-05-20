sleep 0.01m;gnome-terminal --geometry=150x50 --tab --title="echo" -e "bash -c \"echo "hello";echo "there";exec bash\"" 
--tab --title="idea" -e "bash -c \"/opt/idea-IU-111.69/bin/idea.sh;exec bash\"" 
--tab --title="sql" -e "bash -c \"mysql -uroot -pigdefault;\"" 
--tab --title="firefox" -e "bash -c \"/usr/bin/firefox www.gmail.com;\""