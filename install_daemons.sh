git clone https://github.com/postgres/postgres.git
cd postgres
./configure --prefix=$1
make 
make install

git clone https://github.com/jemin6/CIS322.git
tar -xvzf httpd-2.4.25.tar.gz
cd httpd-2.4.25
./configure --prefix=$1
make
make install
