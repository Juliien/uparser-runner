echo "[SERV] building python.. image"
./packager/python_image/build.sh

echo "[SERV] starting agent..."
ls
cd urunner
python3.8 ./app.py