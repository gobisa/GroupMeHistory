echo "rm chat.db"
rm chat.db
echo "sqlite3 chat.db < create.sql"
sqlite3 chat.db < create.sql
echo "python3 history.py"
python3 history.py