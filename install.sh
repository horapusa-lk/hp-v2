cd ~
# Update package
apt update
apt install git

#Install python
apt install python3
apt install python3-pip
#Install my script
git clone https://github.com/horapusa-lk/hp-v2
cd hp-v2
chmod +x *
pip3 install -r requirements.txt

python3 env_vars.py

cp /root/configs.py /usr/bin/
cp bot.py /usr/bin/
cp bot.service /lib/systemd/system/
sudo systemctl enable bot.service
bash v2ray.sh
reboot
