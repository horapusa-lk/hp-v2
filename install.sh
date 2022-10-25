cd ~
apt update
apt install git
apt install python3
apt install python3-pip
git clone https://github.com/horapusa-lk/hp-v2
cd hp-v2
chmod +x *
pip3 install -r requirements.txt
bash v2ray.sh
