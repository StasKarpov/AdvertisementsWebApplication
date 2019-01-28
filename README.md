# AdvertisementsWebApplication
This a backend for a simple advertizements board.
To run program open your cmd/terminal and type
```console
git clone https://github.com/StasKarpov/AdvertisementsWebApplication/
cd AdvertisementsWebApplication
pip install -r requirements.txt
cd advertizements
python manage.py migrate
python manage.py runserver
```
Now you have a backend running on 127.0.0.1:8000
which you ca access with the help of this fancy API map :)


![](https://github.com/StasKarpov/AdvertisementsWebApplication/blob/master/API_fancy_map.png)

Also, you can run tests with
'''console
python manage.py test
'''
